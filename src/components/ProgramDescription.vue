<template>
  <div>
    <v-textarea rows=20 v-model="description" readonly dense></v-textarea>
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
