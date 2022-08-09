<template>
  <div>
    <h2 style="color:darkred">References</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <a :href="link" target="_blank" v-if="link !== ''">{{ link }}</a>
    <v-textarea rows=20 v-model="description"></v-textarea>
  </div>
</template>

<script>
export default {
  name: 'References',
  methods: {
    load: function () {
      console.log(this.$store.state.currentProgram)
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
