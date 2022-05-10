<template>
  <div>
    <h2 style="color:darkred">Linkages</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <br>
    <h3>{{ question }}</h3>
    <br>
    <v-card :elevation="2" color="blue-grey lighten-4" v-for="area in this.$store.state.areas" :key="area.id">
      <v-container fluid class="fill-height">
        <v-row no-gutters v-for="(group,index) in area.groups" :key="group.id">
          <v-col md="2">
            <h3 v-if="index===0">{{ area.name }}</h3></v-col>
          <v-col md="4">
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>{{ group.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col md="6">
            <v-list-item-group>
              <v-list-item dense v-for="(program) in group.programs" :key="program.id">
                <v-list-item-action>
                  <v-checkbox :input-value="isSelected(program.id)"
                              @click="selectProgram(program.id)"></v-checkbox>
                </v-list-item-action>
                <v-btn color="black" x-small text @click="showProgramDescription(program.name)">{{ program.name }}
                </v-btn>
              </v-list-item>
            </v-list-item-group>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>
<script>
import Vue from 'vue'
import * as util from "@/assets/js/utils";

export default Vue.extend({
  name: 'SelectProgram',
  methods: {
    submitAnswer: async function () {
      await util.saveSelectedProgramsAnswer(this.answer[0].id, [...this.selectedPrograms], this.$store.state.token)
    },
    load: async function () {
      let program = this.$store.state.currentProgram;
      this.title = program.name;

      let questions = await util.loadQuestions(program.id, 'linkages', this.$store.state.token);
      this.question = questions[0].title;

      this.answer = await util.loadAnswer(questions[0].id, this.$store.state.token);
      this.selectedPrograms = new Set();
      for (let i = 0; i < this.answer[0].selected_programs.length; i++) {
        this.selectedPrograms.add(this.answer[0].selected_programs[i]);
      }
    },
    selectProgram: function (programId) {
      if (this.selectedPrograms.has(programId)) {
        this.selectedPrograms.delete(programId);
      } else {
        this.selectedPrograms.add(programId);
      }
    },
    isSelected(programId) {
      return this.selectedPrograms.has(programId);
    },
  },
  data: () => ({
    active: false,
    title: "",
    answer: "",
    question: "",
    selectedPrograms: new Set(),
  }),
})
</script>

<style scoped>

</style>
``
