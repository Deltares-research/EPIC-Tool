<template>
  <v-row>
    <v-col md="6">
      <v-btn text color="primary" @click='$emit("fromKeyAgencyToNationalFramework")'>
        <v-icon>mdi-step-backward</v-icon>
        National framework
      </v-btn>
    </v-col>
    <v-col md="6" class="text-right">
      <v-btn text color="primary" @click='$emit("fromKeyAgencyToEvolution")'>Evolution
        <v-icon>mdi-step-forward</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "KeyAgencyNavigation"
}
</script>

<style scoped>

</style>
