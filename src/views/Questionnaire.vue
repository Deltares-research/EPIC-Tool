<template>
  <div>
    <br>
    <p>Progress {{ this.$store.state.progress }}%</p>
    <v-progress-linear :value="this.$store.state.progress"></v-progress-linear>
    <br>
    <v-tabs v-model="selectedAreaIndex" >
      <v-tab v-for="(area) in this.$store.state.areas" :key="area.id" @change="updateVisiblePrograms(area.id)"
             :disabled="getVisiblePrograms(area.id).length===0">
        {{ area.name }}
        <v-icon v-if="isAreaCompleted(area.id)" right>mdi-checkbox-marked-circle</v-icon>
      </v-tab>
    </v-tabs>
    <v-tabs v-model="selectedProgramIndex" >
      <v-tab v-for="program in this.visiblePrograms" :key="program.id" @change="updateSelectedProgram(program)">
        {{ program.name }}
        <v-icon v-if="isProgramCompleted(program.id)" right>mdi-checkbox-marked-circle</v-icon>
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
          <program-description-navigation
              @fromProgramDescriptionToNationalFramework="fromProgramDescriptionToNationalFramework"/>
          <program-description ref="programDescription"></program-description>
          <program-description-navigation
              @fromProgramDescriptionToNationalFramework="fromProgramDescriptionToNationalFramework"/>
        </v-stepper-content>
        <v-stepper-content step="2">
          <national-framework-navigation
              @fromNationalFrameworkToProgramDescription="fromNationalFrameworkToProgramDescription"
              @fromNationalFrameworkToKeyAgency="fromNationalFrameworkToKeyAgency"/>
          <national-frameworks ref="nationalFramework"></national-frameworks>
          <national-framework-navigation
              @fromNationalFrameworkToProgramDescription="fromNationalFrameworkToProgramDescription"
              @fromNationalFrameworkToKeyAgency="fromNationalFrameworkToKeyAgency"/>
        </v-stepper-content>
        <v-stepper-content step="3">
          <key-agency-navigation @fromKeyAgencyToNationalFramework="fromKeyAgencyToNationalFramework"
                                 @fromKeyAgencyToEvolution="fromKeyAgencyToEvolution"/>
          <key-agency-actions ref="keyAgency"/>
          <key-agency-navigation @fromKeyAgencyToNationalFramework="fromKeyAgencyToNationalFramework"
                                 @fromKeyAgencyToEvolution="fromKeyAgencyToEvolution"/>
        </v-stepper-content>
        <v-stepper-content step="4">
          <evolution-navigation @fromEvolutionKeyAgency="fromEvolutionKeyAgency"
                                @fromEvolutionToLinkages="fromEvolutionToLinkages"/>
          <evolution ref="evolution"></evolution>
          <evolution-navigation @fromEvolutionKeyAgency="fromEvolutionKeyAgency"
                                @fromEvolutionToLinkages="fromEvolutionToLinkages"/>
        </v-stepper-content>
        <v-stepper-content step="5">
          <linkages-navigation @fromLinkagesToEvolution="fromLinkagesToEvolution"
                               @fromLinkagesToReferences="fromLinkagesToReferences"/>
          <linkages ref="linkages"></linkages>
          <linkages-navigation @fromLinkagesToEvolution="fromLinkagesToEvolution"
                               @fromLinkagesToReferences="fromLinkagesToReferences"/>
        </v-stepper-content>
        <v-stepper-content step="6">
          <references-navigation @back="e1=5" @forward="gotoNextProgram">
            {{ nextProgram !== null ? nextProgram.name : "finalize questionnaire" }}
          </references-navigation>
          <references/>
          <references-navigation @back="e1=5" @forward="gotoNextProgram">
            {{ nextProgram !== null ? nextProgram.name : "finalize questionnaire" }}
          </references-navigation>
        </v-stepper-content>
      </v-stepper-items>

    </v-stepper>
  </div>
</template>
<script>
import References from "@/components/References";
import LinkagesNavigation from '../components/LinkagesNavigation'
import ProgramDescriptionNavigation from '../components/ProgramDescriptionNavigation'
import NationalFrameworkNavigation from "@/components/NationalFrameworkNavigation";
import KeyAgencyNavigation from "@/components/KeyAgencyNavigation";
import ProgramDescription from '../components/ProgramDescription.vue'
import EvolutionNavigation from "@/components/EvolutionNavigation";
import ReferencesNavigation from "@/components/ReferencesNavigation";
import Linkages from '../components/Linkages'
import NationalFrameworks from '../components/NationalFrameworks'
import Evolution from '../components/Evolution'
import KeyAgencyActions from "@/components/KeyAgencyActions";

export default {
  name: 'Questionnaire',
  components: {
    References,
    KeyAgencyNavigation,
    ReferencesNavigation,
    NationalFrameworkNavigation,
    LinkagesNavigation,
    EvolutionNavigation,
    ProgramDescriptionNavigation,
    KeyAgencyActions,
    ProgramDescription,
    Linkages,
    NationalFrameworks,
    Evolution
  },
  async mounted() {
    await this.updateProgress();
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
    isAreaCompleted(areaId) {
      return this.$store.state.completedAreas.has(areaId);
    },
    isProgramCompleted(programId) {
      return this.$store.state.completedPrograms.has(programId);
    },
    async updateProgress() {
      await this.$store.dispatch('updateProgress');
      let completedAreas = new Set();
      for (let i = 0; i < this.$store.state.areas.length; i++) {
        let area = this.$store.state.areas[i];
        let visiblePrograms = this.getVisiblePrograms(area.id);
        if (visiblePrograms.length === 0) continue;
        let unCompletedPrograms = visiblePrograms.filter(program => !this.isProgramCompleted(program.id));
        if (unCompletedPrograms.length !== 0) continue;
        completedAreas.add(area.id);
      }
      this.$store.commit("updateCompletedAreas", completedAreas);
    },
    fromProgramDescriptionToNationalFramework: async function () {
      await this.$refs.nationalFramework.load();
      this.e1 = 2;
    },
    fromNationalFrameworkToKeyAgency: async function () {
      await this.$refs.nationalFramework.submitAnswer();
      await this.$refs.keyAgency.load();
      this.e1 = 3;
      await this.updateProgress();
    },
    fromKeyAgencyToEvolution: async function () {
      await this.$refs.keyAgency.submitAnswer();
      await this.$refs.evolution.load();
      await this.updateProgress();
      this.e1 = 4;
    },
    fromEvolutionToLinkages: async function () {
      await this.$refs.evolution.submitAnswer();
      await this.$refs.linkages.load();
      await this.updateProgress();
      this.e1 = 5;

    },
    fromLinkagesToReferences: async function () {
      await this.$refs.linkages.submitAnswer();
      await this.updateProgress();
      this.e1 = 6;
    },
    fromNationalFrameworkToProgramDescription: async function () {
      await this.$refs.nationalFramework.submitAnswer();
      await this.$refs.programDescription.load();
      await this.updateProgress();
      this.e1 = 1;
    },
    fromKeyAgencyToNationalFramework: async function () {
      await this.$refs.keyAgency.submitAnswer();
      await this.$refs.nationalFramework.load();
      await this.updateProgress();
      this.e1 = 2;
    },
    fromEvolutionKeyAgency: async function () {
      await this.$refs.evolution.submitAnswer();
      await this.$refs.keyAgency.load();
      await this.updateProgress();
      this.e1 = 3;
    },
    fromLinkagesToEvolution: async function () {
      await this.$refs.linkages.submitAnswer();
      await this.$refs.evolution.load();
      await this.updateProgress();
      this.e1 = 4;
    },
    gotoNextProgram: async function () {
      if (this.nextProgram === null) {
        await this.$router.push("EndPage");
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
      await this.updateProgress();
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

