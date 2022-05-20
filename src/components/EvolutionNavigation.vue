<template>
  <v-row>
    <v-col md="6">
      <v-btn text color="primary" @click='$emit("fromEvolutionKeyAgency")'>
        <v-icon>mdi-step-backward</v-icon>
        Key agency actions
      </v-btn>
    </v-col>
    <v-col md="6" class="text-right">
      <v-btn text color="primary" @click='$emit("fromEvolutionToLinkages")'>Linkages
        <v-icon>mdi-step-forward</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "EvolutionNavigation"
}
</script>

<style scoped>

</style>
