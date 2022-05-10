<template>
  <div>
    <h2 style="color:darkred">Program description</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <v-textarea rows=20 v-model="description"></v-textarea>
  </div>
</template>
<script>
export default {
  name: 'ProgramDescription',
  methods: {
    load: function () {
      let program = this.$store.state.currentProgram;
      this.title = program.name;
      this.description = program.description;
    }
  },
  data: () => ({
    title: "",
    description: ""
  }),
}
</script>
