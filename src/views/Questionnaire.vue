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
          <program-description ref="programDescription"></program-description>
          <v-card-actions>
            <v-row>
              <v-col md="6">
              </v-col>
              <v-col md="6" class="text-right">
                <v-btn text color="primary" @click="fromProgramDescriptionToNationalFramework">National framework
                  <v-icon>mdi-step-forward</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-actions>
        </v-stepper-content>
        <v-stepper-content step="2">
          <national-frameworks ref="nationalFramework"></national-frameworks>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="fromNationalFrameworkToProgramDescription">
                <v-icon>mdi-step-backward</v-icon>
                Program description
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="fromNationalFrameworkToKeyAgency">Key agency actions
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="3">
          <key-agency-actions ref="keyAgency"/>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="fromKeyAgencyToNationalFramework">
                <v-icon>mdi-step-backward</v-icon>
                National framework
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="fromKeyAgencyToEvolution">Evolution
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="4">
          <evolution ref="evolution"></evolution>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="fromEvolutionKeyAgency">
                <v-icon>mdi-step-backward</v-icon>
                Key agency actions
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="fromEvolutionToLinkages">Linkages
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="5">
          <linkages ref="linkages"></linkages>
          <v-row>
            <v-col md="6">
              <v-btn text color="primary" @click="fromLinkagesToEvolution">
                <v-icon>mdi-step-backward</v-icon>
                Key agency actions
              </v-btn>
            </v-col>
            <v-col md="6" class="text-right">
              <v-btn text color="primary" @click="fromLinkagesToReferences">References
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
import KeyAgencyActions from "@/components/KeyAgencyActions";

export default {
  name: 'Questionnaire',
  components: {
    KeyAgencyActions,
    ProgramDescription,
    Linkages,
    NationalFrameworks,
    Evolution
  },
  async mounted() {
    this.selectedAreaIndex = this.getFirstAreaToDisplay();
    this.visiblePrograms = this.getVisiblePrograms(this.$store.state.areas[this.selectedAreaIndex].id);
    this.$store.state.currentProgram = this.visiblePrograms[0];
    this.nextProgram = this.getNextProgram();
    await this.$refs.programDescription.load();
  },
  data() {
    return {
      e1: 1,
      selectedAreaIndex: 0,
      selectedAreaId: "",
      selectedProgramIndex: 0,
      visiblePrograms: [],
      nextProgram: null
    }
  },
  methods: {
    fromProgramDescriptionToNationalFramework: async function () {
      this.e1 = 2;
      await this.$refs.nationalFramework.load();
    },
    fromNationalFrameworkToKeyAgency: async function () {
      await this.$refs.nationalFramework.submitAnswer();
      await this.$refs.keyAgency.load();
      this.e1 = 3;
    },
    fromKeyAgencyToEvolution: async function () {
      await this.$refs.keyAgency.submitAnswer();
      await this.$refs.evolution.load();
      this.e1 = 4;
    },
    fromEvolutionToLinkages: async function () {
      await this.$refs.evolution.submitAnswer();
      await this.$refs.linkages.load();
      this.e1 = 5;
    },
    fromLinkagesToReferences: async function () {
      await this.$refs.linkages.submitAnswer();
      this.e1 = 6;
    },
    fromNationalFrameworkToProgramDescription: async function () {
      await this.$refs.nationalFramework.submitAnswer();
      await this.$refs.programDescription.load();
      this.e1 = 1;
    },
    fromKeyAgencyToNationalFramework: async function () {
      await this.$refs.keyAgency.submitAnswer();
      await this.$refs.nationalFramework.load();
      this.e1 = 2;
    },
    fromEvolutionKeyAgency: async function () {
      await this.$refs.evolution.submitAnswer();
      await this.$refs.keyAgency.load();
      this.e1 = 3;
    },
    fromLinkagesToEvolution: async function () {
      await this.$refs.linkages.submitAnswer();
      await this.$refs.evolution.load();
      this.e1 = 4;
    },
    gotoNextProgram: async function () {
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
      await this.forceUpdate();
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
    updateVisiblePrograms: async function (areaId) {
      this.visiblePrograms = this.getVisiblePrograms(areaId);
      await this.updateSelectedProgram(this.visiblePrograms[0]);
      this.selectedProgramIndex = 0;
      await this.forceUpdate();
    },
    forceUpdate: async function () {
      if (this.e1 === 1) {
        await this.$refs.programDescription.load();
      }

      if (this.e1 === 2) {
        await this.$refs.nationalFramework.submitAnswer();
        await this.$refs.nationalFramework.load();
      }
      if (this.e1 === 3) {
        await this.$refs.keyAgency.submitAnswer();
        await this.$refs.keyAgency.load();
      }
      if (this.e1 === 4) {
        await this.$refs.evolution.submitAnswer();
        await this.$refs.evolution.load();
      }
      if (this.e1 === 5) {
        await this.$refs.linkages.submitAnswer();
        await this.$refs.linkages.load();
      }
    },
    updateSelectedProgram: async function (program) {
      this.$store.state.currentProgram = program;
      this.nextProgram = this.getNextProgram();
      await this.forceUpdate();
    },
    getVisiblePrograms: function (areaId) {
      let programs = [];
      for (const area of this.$store.state.areas) {
        if (area.id !== areaId) continue;
        for (const group of area.groups) {
          for (const program of group.programs) {
            if (!this.$store.state.programSelection.has(program.id)) continue
            programs.push(program);
          }
        }
      }
      return programs;
    }
  }
}
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

