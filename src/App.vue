<template>
  <v-app>
    <v-app-bar dense app>
      <v-row>
        <v-col md="11">
          <v-btn to="/" text v-if="this.$store.state.token !== ''">Home</v-btn>
          <v-btn to="/SelectProgram" text v-if="this.$store.state.token !== ''">Select programs</v-btn>
          <v-btn to="/Questionnaire" text v-if="this.$store.state.token !== ''">Questionnaire</v-btn>
          <v-menu offset-y v-if="this.$store.state.token !== ''">
            <template v-slot:activator="{ on, attrs }">
              <v-btn text v-bind="attrs" v-on="on">Report</v-btn>
            </template>
            <v-list>
              <v-list-item to="Answers" v-if="this.$store.state.advisor">
                <v-list-item-title>Answers</v-list-item-title>
              </v-list-item>
              <v-list-item to="LinkagesOverview">
                <v-list-item-title>Linkages</v-list-item-title>
              </v-list-item>
              <v-list-item  to="EvolutionOverview">
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
    logout: function () {
      this.$store.state.token = "";
      this.$router.push("/LoginPage");
    }
  }
};
</script>
