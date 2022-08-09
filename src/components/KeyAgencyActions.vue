<template>
  <div>
    <v-row>
      <v-col md="6">
        <v-btn text color="primary" @click='$emit("fromKeyAgencyToNationalFramework")'>
          <v-icon>mdi-step-backward</v-icon>{{this.previousStepMessage()}}</v-btn>
      </v-col>
      <v-col md="6" class="text-right">
        <v-btn text color="primary" @click='$emit("fromKeyAgencyToEvolution")'>{{this.nextStepMessage()}}<v-icon>mdi-step-forward</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <h5>{{ page }} of {{ this.questions.length }} questions</h5>
    <h2 style="color: darkred">Key agencies actions</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <v-textarea rows=6 :value="displayDescription" readonly outlined></v-textarea>
    <v-row>
      <v-col md="8">
        <v-textarea rows=2 :value="displayedQuestion" readonly outlined></v-textarea>
      </v-col>
      <v-col md="4">
        <v-select
            :items="items"
            v-model="selectedAgreement"
            filled
            label="Select yes or no"
        ></v-select>
      </v-col>
    </v-row>
    <h3>Please justify your answer</h3>
    <v-textarea rows=4 outlined v-model="displayedJustification"></v-textarea>
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
    nextStepMessage() {
      let nextQuestion = this.page + 1;
      return this.page - 1 < this.questions.length - 1 ? "Question " + nextQuestion : "Evolution";
    }, previousStepMessage() {
      let previousQuestion = this.page - 1;
      return this.hasPreviousQuestion() ? "Question " + previousQuestion : "National framework";
    },
    hasNextQuestion() {
      return this.page - 1 < this.questions.length - 1;
    },
    hasPreviousQuestion() {
      return this.page > 1;
    },
    loadNextQuestion: async function () {
      await this.submitAnswer();
      this.page++;
      await this.loadAnswer();
    },
    loadPreviousQuestion: async function () {
      await this.submitAnswer();
      this.page--;
      await this.loadAnswer();
    },
    submitAnswer: async function () {
      await util.saveAgreementAnswer(this.answer[0].id, this.displayedJustification, this.selectedAgreement, this.$store.state.token);
      this.$emit("updateProgress");
    },
    loadAnswer: async function () {
      this.displayedQuestion = this.questions[this.page - 1].title;
      this.displayDescription = this.questions[this.page - 1].description;

      this.answer = await util.loadAnswer(this.questions[this.page - 1].id, this.$store.state.token);
      if (this.answer[0].id === undefined) return;

      this.displayedJustification = this.answer[0].justify_answer;
      if (this.answer[0].selected_choice === "") {
        this.selectedAgreement = "";
      }
      if (this.answer[0].selected_choice === "STRONGLYDISAGREE") {
        this.selectedAgreement = "Strongly disagree";
      }
      if (this.answer[0].selected_choice === "DISAGREE") {
        this.selectedAgreement = "Disagree";
      }
      if (this.answer[0].selected_choice === "NEITHERAGREENORDISAGREE") {
        this.selectedAgreement = "Neither agree nor disagree";
      }
      if (this.answer[0].selected_choice === "AGREE") {
        this.selectedAgreement = "Agree";
      }
      if (this.answer[0].selected_choice === "STRONGLYAGREE") {
        this.selectedAgreement = "Strongly agree";
      }
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
      await this.loadAnswer();

    }
  },
  data: () => ({
    items: ['Strongly agree', 'Agree', 'Neither agree nor disagree', 'Disagree', 'Strongly disagree'],
    selectedAgreement: "",
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
