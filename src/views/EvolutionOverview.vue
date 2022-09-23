<template>
  <div>
    <h2 style="color: darkred">Evolution report</h2>
    <v-row
        align="center"
        justify="space-around"
    >
      <v-btn class="primary" @click="generateGraph()">Generate evolution graph</v-btn>
    </v-row>
    <div v-if="true">
      <h3 style="color: darkred">Graph</h3>
      <v-img
          max-height="1000px"
          max-width="1000px"
          src="http://localhost:8000/eram_visuals.png"
      ></v-img>
      <a :href="pdfUrl" download>Download graph</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "EvolutionOverview",
  mounted() {
    this.dataLoaded = false;
    this.url = "";
  },
  methods: {
    generateGraph: async function () {
      this.loading = true;
      this.dataLoaded = false;
      const token = this.$store.state.token;
      const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'Token ' + token,
        },
      }
      let server = process.env.VUE_APP_BACKEND_URL;
      let programResponse = await fetch(server + '/api/summary/evolution-graph/', options);
      let res = await programResponse.json();
      this.dataLoaded = true;
      console.log(res)
      this.imageUrl = res.summary_graph;
      this.pdfUrl = res.summary_pdf.replace(server,"");
    }

  },
  data() {
    return {
      dataLoaded: false,
      imageUrl: "",
      pdfUrl: "",
    }
  }

}
</script>

<style scoped>

</style>