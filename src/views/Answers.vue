<template>
  <div>
    <h2 style="color:darkred">Answers report</h2>
    <h3>Click on the button to download the report with answers and questions</h3>
    <v-btn @click="getLink">download report</v-btn>
  </div>
</template>
<script>

export default {
  name: 'Answers',
  async mounted() {
  },
  data() {
    return {
      advisor: false,
      answers: [],
      new_short_answer: null,
      new_lang_answer: null,
    }
  },
  methods: {
    getLink: async function () {
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
      let input = server + '/api/epicorganization/report-pdf/';
      let res = await fetch(input, options);
      if (res.status !== 200) return;
      let blob = await res.blob();
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = "report.pdf";
      document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
      a.click();
      a.remove();  //afterwards we remove the element again
    },
  },
  components: {}
}
</script>

