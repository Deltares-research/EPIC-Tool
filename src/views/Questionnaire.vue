<template>
  <div>
    <p>Progress 45% 2 minutes left</p>
    <v-progress-linear value="45"></v-progress-linear>
    <br>
    <v-tabs v-model="selectedAreaIndex">
      <v-tab v-for="(area) in this.$store.state.areas" :key="area.id" @change="updateVisiblePrograms(area.id)"
             :disabled="getVisiblePrograms(area.id).length===0">
        {{ area.name }}
      </v-tab>
    </v-tabs>
    <v-tabs v-model="selectedProgramIndex">
      <v-tab v-for="program in this.visiblePrograms" :key="program.id" @change="updateSelectedProgram(program)">{{
          program.name
        }}
      </v-tab>
    </v-tabs>
    <br>
    <v-stepper v-model="e1">
      <v-stepper-header>
        <v-stepper-step :complete="e1 > 1" step="1">Program description</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="e1 > 2" step="2">National framework</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="e1 > 3" step="3">Key agency actions</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="e1 > 4" step="4">Evolution</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="e1 > 5" step="5">Linkages</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="e1 > 6" step="6">References</v-stepper-step>
      </v-stepper-header>
      <v-stepper-items>
        <v-stepper-content step="1">
          <program-description :key="forceUpdateProgramDescription"></program-description>
          <v-card-actions>
            <v-row>
              <v-col md="6">
              </v-col>
              <v-col md="6"  class="text-right">
                <v-btn text color="primary" @click="e1 = 2">National framework
                  <v-icon>mdi-step-forward</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-actions>
        </v-stepper-content>
        <v-stepper-content step="2">
          <national-frameworks :key="forceUpdateNationalFramework"></national-frameworks>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="e1 = 1">
                <v-icon>mdi-step-backward</v-icon>
                Program description
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="e1 = 3">Key agency actions
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="3">
          <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="e1 = 2">
                <v-icon>mdi-step-backward</v-icon>
                National framework
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="e1 = 4">Evolution
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="4">
          <evolution :key="forceUpdateEvolution"></evolution>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="e1 = 3">
                <v-icon>mdi-step-backward</v-icon>
                Key agency actions
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="e1 = 5">Linkages
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="5">
          <linkages :key="forceUpdateLinkages"></linkages>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="e1 = 4">
                <v-icon>mdi-step-backward</v-icon>
                Key agency actions
              </v-btn>
            </v-col>
            <v-col md="6"  class="text-right">
              <v-btn text color="primary" @click="e1 = 6">References
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="6">
          <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="e1 = 5">
                <v-icon>mdi-step-backward</v-icon>
                Linkages
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="gotoNextProgram">
                {{ nextProgram !== null ? nextProgram.name : "finalize questionnaire" }}
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
      </v-stepper-items>

    </v-stepper>
  </div>
</template>
<script>
import ProgramDescription from '../components/ProgramDescription.vue'
import Linkages from '../components/Linkages'
import NationalFrameworks from '../components/NationalFrameworks'
import Evolution from '../components/Evolution'

export default {
  name: 'Questionnaire',
  components: {
    ProgramDescription, Linkages, NationalFrameworks, Evolution
  },
  mounted() {
    this.selectedAreaIndex = this.getFirstAreaToDisplay();
    this.visiblePrograms = this.getVisiblePrograms(this.$store.state.areas[this.selectedAreaIndex].id);
    this.$store.state.currentProgram = this.visiblePrograms[0];
    this.nextProgram = this.getNextProgram();
  },
  data() {
    return {
      e1: 1,
      selectedAreaIndex: 0,
      selectedAreaId: "",
      selectedProgramIndex: 0,
      visiblePrograms: [],
      forceUpdateProgramDescription: 0,
      forceUpdateNationalFramework: 0,
      forceUpdateEvolution: 0,
      forceUpdateKeyAgencyAction: 0,
      forceUpdateLinkages: 0,
      forceUpdateReferences: 0,
      nextProgram: null
    }
  },
  methods: {
    gotoNextProgram: function () {
      if (this.nextProgram === null) {
        this.$router.push("EndPage");
        return;
      }
      this.$store.state.currentProgram = this.nextProgram;
      this.e1 = 1;
      let newGroup = this.$store.state.groups.find(group => group.id === this.nextProgram.group);
      let newArea = this.$store.state.areas.find(area => area.id === newGroup.area);
      this.selectedAreaIndex = this.$store.state.areas.indexOf(newArea);
      this.visiblePrograms = this.getVisiblePrograms(newArea.id);
      this.selectedProgramIndex = this.visiblePrograms.indexOf(this.nextProgram);

      this.nextProgram = this.getNextProgram();
      this.forceUpdate();
    },
    getNextProgram: function () {
      let programs = [];
      for (const area of this.$store.state.areas) {
        let visiblePrograms = this.getVisiblePrograms(area.id);
        for (const program of visiblePrograms) {
          programs.push(program);
        }
      }
      let index = programs.indexOf(this.$store.state.currentProgram);
      if (index === programs.length - 1) {
        return null;
      }
      return programs[index + 1];
    },
    getFirstAreaToDisplay: function () {
      for (let i = 0; i < this.$store.state.areas.length; i++) {
        let area = this.$store.state.areas[i];
        let visiblePrograms = this.getVisiblePrograms(area.id);
        if (visiblePrograms.length > 0) {
          return i;
        }
      }
      return null;
    },
    updateVisiblePrograms: function (areaId) {
      this.visiblePrograms = this.getVisiblePrograms(areaId);
      this.updateSelectedProgram(this.visiblePrograms[0]);
      this.selectedProgramIndex = 0;
      this.forceUpdate();
    },
    forceUpdate: function () {
      this.forceUpdateProgramDescription++;
      this.forceUpdateNationalFramework++;
      this.forceUpdateKeyAgencyAction++;
      this.forceUpdateEvolution++;
      this.forceUpdateLinkages++;
      this.forceUpdateReferences++;
    },
    updateSelectedProgram: function (program) {
      this.$store.state.currentProgram = program;
      this.nextProgram = this.getNextProgram();
      this.forceUpdate();
    },
    getVisiblePrograms: function (areaId) {
      let programs = [];
      for (const area of this.$store.state.areas) {
        if (area.id !== areaId) continue;
        for (const group of area.groups) {
          for (const program of group.programs) {
            if (!this.$store.state.programSelection[program.id]) continue
            programs.push(program);
          }
        }
      }
      return programs;
    }
  }
}
</script>

