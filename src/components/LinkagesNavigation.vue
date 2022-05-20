<template>
  <v-row>
    <v-col md="6">
      <v-btn text color="primary" @click='$emit("fromLinkagesToEvolution")'>
        <v-icon>mdi-step-backward</v-icon>
        Evolution
      </v-btn>
    </v-col>
    <v-col md="6" class="text-right">
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
