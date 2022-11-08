<template>
  <div>
    <div v-for="(reference,index) in this.$store.state.currentProgram.references" :key="index">
      <v-textarea rows=3 v-model="reference.description" dense readonly></v-textarea>
      <a :href="reference.link" target="_blank" >{{ reference.link }}</a>
    </div>
    <br>
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
