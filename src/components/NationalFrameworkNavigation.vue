<template>
  <v-row>
    <v-col md="6">
      <v-btn text color="primary" @click='$emit("fromNationalFrameworkToProgramDescription")'>
        <v-icon>mdi-step-backward</v-icon>
        Program description
      </v-btn>
    </v-col>
    <v-col md="6" class="text-right">
      <v-btn text color="primary" @click='$emit("fromNationalFrameworkToKeyAgency")'>Key agency actions
        <v-icon>mdi-step-forward</v-icon>
      </v-btn>
    </v-col>
  </v-row>

</template>

<script>
export default {
  name: "NationalFrameworkNavigation"
}
</script>

<style scoped>

</style>
