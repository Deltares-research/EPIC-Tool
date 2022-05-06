<template>
  <div>
    <h2 style="color: darkred">Linkage with Key agencies</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <v-textarea rows=4 :value="explanation[page-1]" readonly outlined></v-textarea>
    <v-row>
      <v-col md="8">
        <v-textarea rows=1 :value="questions[page-1]" readonly outlined></v-textarea>
      </v-col>
      <v-col md="4">
        <v-select
            :items="items"
            filled
            label="Select yes or no"
        ></v-select>
      </v-col>
    </v-row>
    <h3>Please justify your answer</h3>
    <v-textarea rows=5 outlined></v-textarea>
    <v-row>
      <v-col md="4">
      </v-col>
      <v-col md="1">
        <v-btn :disabled="page===1" color="info" @click="page--">Previous question</v-btn>
      </v-col>
      <v-col md="1"></v-col>
      <v-col md="1">
        <v-btn :disabled="page>=questions.length" color="info" @click="page++">Next question</v-btn>
      </v-col>
    </v-row>
    <br/>
    <br/>
    <br/>
    <h5>{{ page }} of {{ this.questions.length }} questions</h5>
    <br/>
    <br/>
  </div>
</template>
<script>
import Vue from 'vue'
import loadQuestions from "@/assets/js/utils";

export default Vue.extend({
  name: 'KeyAgencyActions',
  methods: {},
  async mounted() {
    let program = this.$store.state.currentProgram;
    this.title = program.name;

    let questions = await loadQuestions(program.id, 'keyagencyactions', this.$store.state.token);
    this.explanation = [questions.length];
    this.questions = [questions.length];
    for (let i = 0; i < questions.length; i++) {
      this.explanation[i] = questions[i].description;
      this.questions[i] = questions[i].title;
    }

  },
  data: () => ({
    items: ['Yes', 'No'],
    title: "",
    page: 1,
    explanation: [],
    questions: []
  }),

})
</script>

<style scoped>
</style>
``
