<template>
  <v-app>
    <v-app-bar dense app>
      <v-btn to="/" text v-if="this.$store.state.token !== ''">Home</v-btn>
      <v-btn to="/SelectProgram" text v-if="this.$store.state.token !== ''">Select programs</v-btn>
      <v-btn to="/Questionnaire" text v-if="this.$store.state.token !== ''">Questionnaire</v-btn>
      <v-btn @click="getLink" v-if="this.$store.state.token !== ''" text >Report</v-btn>
      <v-btn to="/EndPage" text v-if="this.$store.state.token !== ''">Finalize Questionnaire</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="logout" text v-if="this.$store.state.token !== ''">
        <v-icon>mdi-logout</v-icon>
        Logout
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    answer: {}
  }),
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
    logout: function () {
      this.$store.state.token = "";
      this.$router.push("/LoginPage");
    }
  }
};
</script>
