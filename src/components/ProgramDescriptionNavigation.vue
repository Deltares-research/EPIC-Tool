<template>
  <v-row>
    <v-col md="4">
    </v-col>
    <v-col>
      <h3 style="color: darkred">{{ this.$store.state.currentProgram.name }}</h3>
    </v-col>
    <v-col md="4" class="text-right">
      <v-btn text color="primary" @click='$emit("fromProgramDescriptionToNationalFramework")'>National framework
        <v-icon>mdi-step-forward</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "ProgramDescriptionNavigation"
}
</script>

<style scoped>

</style>
