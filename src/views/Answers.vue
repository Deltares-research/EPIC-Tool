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
    },
    async downloadDocx() {
      try {
        // Load the .docx template from the public directory
        const response = await axios.get("/template.docx", { responseType: "arraybuffer" });
        const content = response.data;

        // Create a new PizZip instance
        const zip = new PizZip(content);

        // Create a new Docxtemplater instance
        const doc = new Docxtemplater(zip, {
          paragraphLoop: true,
          linebreaks: true,
        });

        // Get the report content
        const reportContent = this.$refs.report.$el.innerText;

        // Set the data for the template
        doc.setData({
          report: reportContent,
        });

        try {
          // Render the document
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
        saveAs(out, "report.docx");
      } catch (error) {
        console.error("Error creating the document:", error);
      }
    },
  },
};
</script>
