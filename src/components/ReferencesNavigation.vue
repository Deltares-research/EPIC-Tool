<template>
  <v-row>
    <v-col md="6">
      <v-btn text color="primary" @click='$emit("back")'>
        <v-icon>mdi-step-backward</v-icon>
        Linkages
      </v-btn>
    </v-col>
    <v-col md="6" class="text-right">
      <v-btn text color="primary" @click='$emit("forward")'><slot></slot>

        <v-icon>mdi-step-forward</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "ReferencesNavigation"
}
</script>

<style scoped>

</style>
