<template>
  <v-row>
    <v-col md="4">
      <v-btn text color="primary" @click='$emit("fromLinkagesToEvolution")'>
        <v-icon>mdi-step-backward</v-icon>
        Evolution
      </v-btn>
    </v-col>
    <v-col md="4"><h3 style="color: darkred">{{ this.$store.state.currentProgram.name }}</h3></v-col>
    <v-col md="4" class="text-right">
      <v-btn text color="primary" @click='$emit("fromLinkagesToReferences")'>References
        <v-icon>mdi-step-forward</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "LinkagesNavigation.vue"
}
</script>

<style scoped>

</style>
