<template>
  <div>
    <h2 style="color:darkred">Answers report</h2>
    <h3 v-if="report === undefined">Click on the button to generate the report with answers and questions</h3>
    <div class="text-left">
      <v-btn v-if="report === undefined" @click="loadAnswers" color="primary" class="mx-2">create report</v-btn>
      <v-btn @click="downloadDocx" color="primary" v-if="report!==undefined">download</v-btn>
    </div>
    <br>
    <report ref="report" :report="report" :questions="questions" v-if="report!==undefined"/>
    <br>
  </div>
</template>

<script>
import Report from "@/components/Report";
import PizZip from "pizzip";
import Docxtemplater from "docxtemplater";
import { saveAs } from "file-saver";
import axios from "axios";

export default {
  components: {
    Report,
  },
  name: 'Answers',
  data() {
    return {
      advisor: false,
      report: undefined,
      questions: undefined,
      structuredData: [],  // New property to store the organized data
      new_short_answer: null,
      new_lang_answer: null,
    }
  },
  methods: {
    async loadAnswers() {
      let server = process.env.VUE_APP_BACKEND_URL;
      const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'Token ' + this.$store.state.token,
        },
      }
      let input = server + '/api/epicorganization/report/';
      let res = await fetch(input, options);
      if (res.status !== 200) return;
      this.report = await res.json();

      input = server + '/api/question/';
      res = await fetch(input, options);
      if (res.status !== 200) return;
      this.questions = await res.json();

      this.organizeData();
    },

    organizeData() {
      // Create a set of question IDs for quick lookup and filter to include only those in the range 1 to 261
      const questionIds = new Set(this.questions
        .filter(q => q.id >= 1 && q.id <= 261)
        .map(q => q.id)
      );

      this.structuredData = this.report.map(program => {
        return {
          programName: program.name,
          questions: program.questions
            .filter(question => questionIds.has(question.id))  // Filter questions based on the question IDs
            .map(question => {
              return {
                questionTitle: question.title,
                answers: question.question_answers.answers.map(answer => {
                  return {
                    selectedChoice: this.getFormattedChoice(answer.selected_choice),
                    justifyAnswer: answer.justify_answer,
                  };
                }),
                summary: this.formatSummary(question.question_answers.summary)
              };
            })
        };
      });
    },
            // console.log('this.structuredData', this.structuredData)
    formatSummary(summary) {
      const formattedSummary = [];
      const fields = ["Strongly_disagree", "Disagree", "Neither_agree_nor_disagree", "Agree", "Strongly_agree"];

      fields.forEach(field => {
        if (summary[field] !== undefined) {
          formattedSummary.push(`${field.replace(/_/g, ' ')}: ${summary[field] || 0}`);
        }
      });

      return formattedSummary.join('\n');
    },

    getFormattedChoice(choice) {
      switch (choice) {
        case "STRONGLYDISAGREE":
          return "Strongly disagree";
        case "DISAGREE":
          return "Disagree";
        case "NEITHERAGREENORDISAGREE":
          return "Neither agree nor disagree";
        case "AGREE":
          return "Agree";
        case "STRONGLYAGREE":
          return "Strongly agree";
        default:
          return choice;
      }
    },

    async downloadDocx() {
      try {
        const response = await axios.get("/template.docx", { responseType: "arraybuffer" });
        const content = response.data;
        const zip = new PizZip(content);
        const doc = new Docxtemplater(zip, {
          paragraphLoop: true,
          linebreaks: true,
        });

        // Get current date, time and username
        const now = new Date();
        const dateString = now.toLocaleString();
        const yyyy = now.getFullYear();
        const mm = String(now.getMonth() + 1).padStart(2, '0');
        const dd = String(now.getDate()).padStart(2, '0');
        const dateStringTitle = `${yyyy}-${mm}-${dd}`;
        const username = this.$store.state.username;

        // Prepare the data for each program
        const data = {
          date: dateString,
          username: username,
        };
        //TODO: fix weird indentation of first item in the word
        this.structuredData.forEach((program, index) => {
          const programContent = program.questions.map(question => {
            const answers = question.answers.map(answer => `
              - Selected Choice: ${answer.selectedChoice}
                Justification: ${answer.justifyAnswer}
            `).join('');

            const summary = question.summary.split('\n').map(line => `    ${line}`).join('\n');

            return `
              
              Question:
                ${question.questionTitle}
              
              Answers:
                ${answers}
              
              Summary:
                ${summary}
            `;
          }).join('');

          data[`program${index + 1}`] = programContent.trim();
        });

        // Set the data for the template
        doc.setData(data);

        try {
          doc.render();
        } catch (error) {
          console.error(error);
          throw new Error("Error rendering the document");
        }

        // Generate the output file
        const out = doc.getZip().generate({
          type: "blob",
          mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        });

        // Save the file
        saveAs(out,  `ERAM_report_${dateStringTitle}.docx`);
      } catch (error) {
        console.error("Error creating the document:", error);
      }
    },
  },
};
</script>
