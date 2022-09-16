<template>
  <v-app>
    <v-app-bar dense app>
      <v-row>
        <v-col md="11">
          <v-btn to="/" text v-if="this.$store.state.token !== ''">Home</v-btn>
          <v-btn to="/SelectProgram" text v-if="this.$store.state.token !== ''">Select programs</v-btn>
          <v-btn to="/Questionnaire" text v-if="this.$store.state.token !== ''">Questionnaire</v-btn>
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn text v-bind="attrs" v-on="on">Report</v-btn>
            </template>
            <v-list>
              <v-list-item @click="getLink">
                <v-list-item-title>Answers</v-list-item-title>
              </v-list-item>
              <v-list-item to="LinkagesOverview">
                <v-list-item-title>Linkages</v-list-item-title>
              </v-list-item>
              <v-list-item @click="getLink">
                <v-list-item-title>Evolution</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <v-btn to="/EndPage" text v-if="this.$store.state.token !== ''">Finalize Questionnaire</v-btn>
        </v-col>
        <v-col md="1">
          <v-btn @click="logout" text v-if="this.$store.state.token !== ''">
            <v-icon>mdi-logout</v-icon>
            Logout
          </v-btn>
        </v-col>

      </v-row>
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
