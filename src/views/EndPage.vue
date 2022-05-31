<template>
  <div style="text-align: center">
    <h2 style="color: black;font-size: xxx-large;text-align: center">Thank you!</h2>
    <h3>You have completed {{this.$store.state.progress}}% of the questions.</h3>
    <p></p>
    <div style="text-align: center"><v-btn @click="logout" color="primary">exit questionnaire</v-btn></div>
  </div>
</template>
<script>
export default {
  name: 'EndPage',
  data: () => ({}),
  methods: {
    logout: function () {
      this.$store.state.token = "";
      this.$router.push("/LoginPage");
    }
  }

}
</script>

<style scoped>
</style>
``
