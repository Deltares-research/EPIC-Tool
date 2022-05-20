<template>
  <div>
    <h2 style="color: darkred">Evolution</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <br>
    <h4>What is the level of development for {{ title }} in your country? </h4>
    <br>
    <v-row v-for=" (dimension,index) in dimensions" :key="dimension.title">
      <v-col md="12" v-if="dimensions.length>1">
        <h4>{{ dimension.title }}</h4>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'NASCENT')"
                  @click="select('NASCENT',index)">
            <v-card-title>Nascent</v-card-title>
            <v-card-text>{{ dimension.nascent_description }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'ENGAGED')"
                  @click="select('ENGAGED',index)">
            <v-card-title>Engaged</v-card-title>
            <v-card-text>{{ dimension.engaged_description }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'CAPABLE')"
                  @click="select('CAPABLE',index)">
            <v-card-title>Capable</v-card-title>
            <v-card-text>{{ dimension.capable_description }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'EFFECTIVE')"
                  @click="select('EFFECTIVE',index)">
            <v-card-title>Effective</v-card-title>
            <v-card-text>{{ dimension.effective_description }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
    <br>
    <h3>Please justify your answer</h3>
    <v-textarea rows=5 outlined v-model="displayedJustification"></v-textarea>
  </div>
</template>
<script>
import Vue from 'vue'
import * as util from "@/assets/js/utils";

export default Vue.extend({
  name: 'Evolution',
  methods: {
    submitAnswer: async function () {
      for (let i = 0; i < this.dimensions.length; i++) {
        let choice = this.selected[i];
        if (choice === undefined) continue;
        if (this.answers[i] === undefined) {
          continue
        }
        let justification = i === this.dimensions.length - 1 ? this.displayedJustification : "";
        await util.saveSelectedChoiceAnswer(this.answers[i][0].id, justification, choice, this.$store.state.token);
        this.$emit("updateProgress");
      }
    },
    load: async function () {
      let program = this.$store.state.currentProgram;
      this.title = program.name;
      this.dimensions = await util.loadQuestions(program.id, 'evolution', this.$store.state.token);
      this.answers = [this.dimensions.length];
      for (let i = 0; i < this.dimensions.length; i++) {
        this.answers[i] = await util.loadAnswer(this.dimensions[i].id, this.$store.state.token);
      }
      this.selected = [this.answers.length];
      for (let i = 0; i < this.answers.length; i++) {
        if (this.answers[i][0] === undefined) return;
        this.selected[i] = this.answers[i][0].selected_choice;
      }
      this.displayedJustification = this.answers[this.answers.length - 1][0].justify_answer;
    },
    isSelected: function (index, selected) {
      return this.selected[index] === selected ? 'red lighten-5' : 'blue-grey lighten-4';
    },
    select: function (program, index) {
      if (this.selected[index] === program) {
        this.selected[index] = "";
        this.update++;
        return;
      }
      this.selected[index] = program;
      this.update++;
    }
  },
  data: () => ({
    selected: [],
    displayedJustification: "",
    update: 1,
    title: "",
    dimensions: [],
    answers: [],
  }),

})
</script>

<style scoped>
html {
  overflow: hidden !important;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}
</style>
``
