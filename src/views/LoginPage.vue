<template>
  <div>
    <v-card>
      <v-card-title>Please login with your user name and password</v-card-title>
      <v-card-text>
        <v-row style="margin: 1px">
          <v-col md="3"></v-col>
          <v-col md="3">
            <v-text-field
                v-model="username"
                name="user"
            ></v-text-field>
          </v-col>
          <v-col md="3">
            <v-text-field
                v-model="password"
                type="password"
                name="password"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row style="margin: 1px">
          <v-col md="6"></v-col>
          <v-col md="3" class="text-right">
            <v-btn class="ma-2" right="true" color="primary" @click="login">login</v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "LoginPage.vue",
  data() {
    return {
      username: "",
      password: ""
    }
  },
  methods: {
    login: async function () {
      let credentials = {};
      credentials.username = this.username;
      credentials.password = this.password;
      const body = {
        headers: {
          'Access-Control-Request-Method': '*',
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(credentials),
      }
      console.log(credentials)
      let url = 'http://localhost:8000/api/token-auth/';
      let response = await fetch(url, body);
      if (response.status !== 200) return;
      let jsonResponse = await response.json();
      this.$store.state.token = jsonResponse.token;
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>

</style>
