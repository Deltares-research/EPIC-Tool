<template>
  <div>
    <h2 style="color: darkred">Linkage with Key agencies</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <v-textarea rows=6 :value="displayDescription" readonly outlined></v-textarea>
    <v-row>
      <v-col md="8">
        <v-textarea rows=2 :value="displayedQuestion" readonly outlined></v-textarea>
      </v-col>
      <v-col md="4">
        <v-select
            :items="items"
            v-model="yesNoValue"
            filled
            label="Select yes or no"
        ></v-select>
      </v-col>
    </v-row>
    <h3>Please justify your answer</h3>
    <v-textarea rows=4 outlined v-model="displayedJustification"></v-textarea>
    <v-row>
      <v-col md="4">
      </v-col>
      <v-col md="1">
        <v-btn :disabled="page===1" color="info" @click="loadPreviousQuestion">Previous question</v-btn>
      </v-col>
      <v-col md="1"></v-col>
      <v-col md="1">
        <v-btn :disabled="page>=questions.length" color="info" @click="loadNextQuestion">Next question</v-btn>
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
import * as util from '../assets/js/utils'

export default Vue.extend({
  name: 'KeyAgencyActions',
  methods: {
    loadNextQuestion: async function () {
      await this.submitAnswer();
      this.page++;
    },
    loadPreviousQuestion: async function () {
      await this.submitAnswer();
      this.page--;
    },
    submitAnswer: async function () {
      await util.saveYesNoAnswer(this.answer[0].id, this.displayedJustification, this.yesNoValue === this.items[0] ? "Y" : "N", this.$store.state.token)
    },
    load: async function () {
      let program = this.$store.state.currentProgram;
      this.title = program.name;

      this.questions = await util.loadQuestions(program.id, 'keyagencyactions', this.$store.state.token);
      if (this.questions.length === 0) {
        this.displayedQuestion = "";
        this.displayDescription = "";
        return;
      }
      this.page = 1;
      this.displayedQuestion = this.questions[0].title;
      this.displayDescription = this.questions[0].description;

      this.answer = await util.loadAnswer(this.questions[this.page - 1].id, this.$store.state.token);
      if (this.answer[0].id === undefined) return;

      this.displayedJustification = this.answer[0].justify_answer;
      if (this.answer[0].short_answer === "Y") {
        this.yesNoValue = this.items[0];
      } else {
        this.yesNoValue = this.items[1];
      }
    }
  },
  data: () => ({
    items: ['Yes', 'No'],
    yesNoValue: "",
    title: "",
    page: 1,
    questions: [],
    displayedQuestion: "",
    displayDescription: "",
    displayedJustification: "",

    answer: {}
  }),

})
</script>

<style scoped>
</style>
``
