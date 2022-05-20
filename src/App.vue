<template>
  <v-app>
    <v-app-bar dense app>
      <v-btn to="/" text>Home</v-btn>
      <v-btn to="/SelectProgram" text>Select program(s)</v-btn>
      <v-btn to="/Questionnaire" text>Questionnaire</v-btn>
      <v-btn to="/EndPage" text>Finalize Questionnaire</v-btn>
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
  methods: {
    isDisabled:function() {
      return this.$store.state.programSelection.size===0;
    },
    logout: function () {
      this.$store.state.token = "";
      this.$router.push("/LoginPage");
    }
  }
};
</script>
