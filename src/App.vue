<template>
  <v-app>
    <v-app-bar elevation="4" dense app>
      <v-spacer></v-spacer>
        <v-icon color="gray darken-2" @click="logout">mdi-logout</v-icon>
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
    logout: function () {
      this.$store.state.token = "";
      this.$router.push("/LoginPage");
    }
  }
};
</script>
