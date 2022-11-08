<template>
  <v-row>
    <v-col md="3">
    </v-col>
    <v-col md="6">
      <v-card>
        <v-card-title class="justify-center">Please login with your username and password</v-card-title>
        <v-card-text>
          <v-row style="margin: 1px">
            <v-col md="3"></v-col>
            <v-col md="6">
              <v-text-field prepend-icon="mdi-account"
                            v-model="username"
                            name="user"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row style="margin: 1px">
            <v-col md="3"></v-col>
            <v-col md="6">
              <v-text-field prepend-icon="mdi-lock-outline"
                            v-model="password"
                            type="password"
                            name="password"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row style="margin: 1px;color: darkred" v-if="error">
            <v-col md="3"></v-col>
            <v-col md="6" class="text-right">
              <h3>Invalid username or password, please try again!</h3>
            </v-col>
          </v-row>
          <v-row style="margin: 1px">
            <v-col md="6"></v-col>
            <v-col md="3" class="text-right">
              <v-btn class="ma-2" right dark color="primary" @click="login">
                login
                <v-icon right>mdi-login</v-icon>
              </v-btn>
            </v-col>
          </v-row>

        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "LoginPage.vue",
  data() {
    return {
      username: "",
      password: "",
      error: false,
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
      let server = process.env.VUE_APP_BACKEND_URL
      let url = server + '/api/token-auth/';
      let response = await fetch(url, body);
      if (response.status !== 200) {
        this.error = true;
        return;
      }
      let jsonResponse = await response.json();
      this.$store.state.token = jsonResponse.token;

      const options = {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'Token ' + this.$store.state.token,
        },
      }
      let input = server + '/api/epicuser/self/';
      let res = await fetch(input, options);
      if (res.status !== 200) return;
      let data = await res.json();
      this.$store.state.advisor = data.is_advisor;


      await this.$router.push('/');
    }
  }
}
</script>

<style scoped>

</style>
