<template>
  <div>
    <h2 style="color:darkred">Answers report</h2>
    <h3 v-if="report === undefined">Click on the button to generate the report with answers and questions</h3>
    <div class="text-left">
      <v-btn v-if="report === undefined" @click="loadAnswers" color="primary" class="mx-2">create report</v-btn>
      <v-btn @click="printDownload" color="primary" v-if="report!==undefined">print</v-btn>
    </div>
    <br>
    <report ref="report" :report="report" :questions="questions" v-if="report!==undefined"/>
    <br>
  </div>
</template>
<script>
import Report from "@/components/Report";

export default {
  components: {
    Report,
  },
  name: 'Answers',
  async mounted() {
  },
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
    generateReport() {
      this.$refs.html2Pdf.generatePdf()
    },
    printDownload() {
      let w = window.open()
      w.document.write(this.$refs.report.$el.innerHTML)
      w.document.close()
      w.setTimeout(function () {
        w.print()
      }, 1000)
    },
    async beforeDownload({html2pdf, options, pdfContent}) {
      await html2pdf().set(options).from(pdfContent).toPdf().get('pdf').then((pdf) => {
        const totalPages = pdf.internal.getNumberOfPages()
        for (let i = 1; i <= totalPages; i++) {
          pdf.setPage(i)
          pdf.setFontSize(10)
          pdf.setTextColor(150)
          pdf.text('Page ' + i + ' of ' + totalPages, (pdf.internal.pageSize.getWidth() * 0.88), (pdf.internal.pageSize.getHeight() - 0.3))
        }
      }).save()
    },
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
  }
}
</script>

