<template>
  <div>
    <a :href="link" target="_blank" v-if="link !== ''">{{ link }}</a>
    <v-textarea rows=20 v-model="description" dense readonly></v-textarea>
  </div>
</template>

<script>
export default {
  name: 'References',
  methods: {
    load: function () {
      let program = this.$store.state.currentProgram;
      this.title = program.name;
      this.link = program.reference_link
      this.description = program.reference_description;
    }
  },
  data: () => ({
    title: "",
    link: "",
    description: ""
  }),
}
</script>

<style scoped>

</style>
