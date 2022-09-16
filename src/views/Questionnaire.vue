<template>
  <div>
    <h3 v-if="this.$store.state.programSelection.size === 0">Please select 1 or more programs in the select programs
      tab</h3>
    <div v-if="this.$store.state.programSelection.size > 0">
      <v-expansion-panels class="mb-6">
        <v-expansion-panel>
          <v-expansion-panel-header expand-icon="mdi-menu-down">
            <p>Estimated remaining time
              {{ this.$store.state.remainingQuestions }} minutes ({{ this.$store.state.progress }}%)</p>
            <br>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-progress-linear :value="this.$store.state.progress"></v-progress-linear>
            <v-tabs v-model="selectedAreaIndex">
              <v-tab v-for="(area) in this.$store.state.areas" :key="area.id"
                     @change="updateVisibleProgramsAfterAreaChange(area.id)"
                     :disabled="disableArea(area.id)">
                {{ area.name }}
                <v-icon v-if="isAreaCompleted(area.id)" right>mdi-checkbox-marked-circle</v-icon>
              </v-tab>
            </v-tabs>
            <v-tabs v-model="selectedGroupIndex">
              <v-tab v-for="(group) in this.visibleGroups" :key="group.id"
                     @change="updateVisibleProgramsAfterGroupChange(group.id)"
                     :disabled="disableEvents">
                {{ group.name }}
                <v-icon v-if="isGroupCompleted(group.id)" right>mdi-checkbox-marked-circle</v-icon>
              </v-tab>
            </v-tabs>
            <v-tabs v-model="selectedProgramIndex">
              <v-tab v-for="program in this.visiblePrograms" :key="program.id" @change="updateSelectedProgram(program)"
                     :disabled="disableEvents">
                {{ program.name }}
                <v-icon v-if="isProgramCompleted(program.id)" right>mdi-checkbox-marked-circle</v-icon>
              </v-tab>
            </v-tabs>
            <br>
            <h3 style="color: darkred">Program description {{this.$store.state.currentProgram.name}}</h3>
            <v-textarea rows="10" :value="this.$store.state.currentProgram.description"></v-textarea>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
      <br>
      <v-stepper v-model="e1" >
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

            <national-frameworks ref="nationalFramework" @updateProgress="updateProgress"
                                 @fromNationalFrameworkToProgramDescription="fromNationalFrameworkToProgramDescription"
                                 @fromNationalFrameworkToKeyAgency="fromNationalFrameworkToKeyAgency"></national-frameworks>
          </v-stepper-content>
          <v-stepper-content step="3">
            <key-agency-actions ref="keyAgency" @updateProgress="updateProgress"
                                @fromKeyAgencyToNationalFramework="fromKeyAgencyToNationalFramework"
                                @fromKeyAgencyToEvolution="fromKeyAgencyToEvolution"/>

          </v-stepper-content>
          <v-stepper-content step="4">
            <evolution-navigation @fromEvolutionKeyAgency="fromEvolutionKeyAgency"
                                  @fromEvolutionToLinkages="fromEvolutionToLinkages"/>
            <evolution ref="evolution" @updateProgress="updateProgress"></evolution>
            <evolution-navigation @fromEvolutionKeyAgency="fromEvolutionKeyAgency"
                                  @fromEvolutionToLinkages="fromEvolutionToLinkages"/>
          </v-stepper-content>
          <v-stepper-content step="5">
            <linkages-navigation @fromLinkagesToEvolution="fromLinkagesToEvolution"
                                 @fromLinkagesToReferences="fromLinkagesToReferences"/>
            <linkages ref="linkages" @updateProgress="updateProgress"></linkages>
            <linkages-navigation @fromLinkagesToEvolution="fromLinkagesToEvolution"
                                 @fromLinkagesToReferences="fromLinkagesToReferences"/>
          </v-stepper-content>
          <v-stepper-content step="6">
            <references-navigation @back="e1=5" @forward="gotoNextProgram">
              {{ nextProgram !== null ? nextProgram.name : "finalize questionnaire" }}
            </references-navigation>
            <references ref="references"/>
            <references-navigation @back="e1=5" @forward="gotoNextProgram">
              {{ nextProgram !== null ? nextProgram.name : "finalize questionnaire" }}
            </references-navigation>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </div>
  </div>
</template>
<script>
import References from "@/components/References";
import LinkagesNavigation from '../components/LinkagesNavigation'
import ProgramDescriptionNavigation from '../components/ProgramDescriptionNavigation'
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
    ReferencesNavigation,
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
    let area = this.$store.state.areas[this.selectedAreaIndex];
    this.visibleGroups = this.getVisibleGroups(area);
    this.visiblePrograms = this.getVisibleProgramsForAreaAndGroup(area.id, this.visibleGroups[0].id);
    this.$store.commit("updateCurrentProgram", this.visiblePrograms[0]);
    this.nextProgram = this.getNextProgram();
    await this.$refs.programDescription.load();
  },
  data() {
    return {
      e1: 1,
      selectedAreaIndex: 0,
      selectedGroupIndex: 0,
      selectedProgramIndex: 0,
      visiblePrograms: [],
      visibleGroups: [],
      disableEvents: false,
      nextProgram: null
    }
  },
  methods: {
    isAreaCompleted(areaId) {
      return !this.$store.state.unCompleteAreas.has(areaId) &&!this.disableArea(areaId);
    },
    isGroupCompleted(groupId) {
      return !this.$store.state.unCompleteGroups.has(groupId);
    },
    isProgramCompleted(programId) {
      return this.$store.state.completedPrograms.has(programId);
    },
    async updateProgress() {
      await this.$store.dispatch('updateProgress');
    },
    fromProgramDescriptionToNationalFramework: async function () {
      await this.$refs.nationalFramework.load();
      this.e1 = 2;
    },
    fromNationalFrameworkToKeyAgency: async function () {
      if (this.$refs.nationalFramework.hasNextQuestion()) {
        await this.$refs.nationalFramework.loadNextQuestion();
        return;
      }
      await this.$refs.nationalFramework.submitAnswer();
      await this.$refs.keyAgency.load();
      this.e1 = 3;
    },
    fromKeyAgencyToEvolution: async function () {
      if (this.$refs.keyAgency.hasNextQuestion()) {
        await this.$refs.keyAgency.loadNextQuestion();
        return
      }
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
      await this.$refs.references.load();
      this.e1 = 6;
    },
    fromNationalFrameworkToProgramDescription: async function () {
      if (this.$refs.nationalFramework.hasPreviousQuestion()) {
        await this.$refs.nationalFramework.loadPreviousQuestion();
        return;
      }
      await this.$refs.nationalFramework.submitAnswer();
      await this.$refs.programDescription.load();
      this.e1 = 1;
    },
    fromKeyAgencyToNationalFramework: async function () {
      if (this.$refs.keyAgency.hasPreviousQuestion()) {
        await this.$refs.keyAgency.loadPreviousQuestion();
        return;
      }
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
        await this.$router.push("EndPage");
        return;
      }
      this.$store.state.currentProgram = this.nextProgram;
      this.e1 = 1;
      let newGroup = this.$store.state.groups.find(group => group.id === this.nextProgram.group);
      let newArea = this.$store.state.areas.find(area => area.id === newGroup.area);
      this.selectedAreaIndex = this.$store.state.areas.indexOf(newArea);
      this.visiblePrograms = this.getVisibleProgramsForAreaAndGroup(newArea.id, newGroup.id);
      this.visibleGroups = this.getVisibleGroups(newArea);
      this.selectedProgramIndex = this.visiblePrograms.indexOf(this.nextProgram);
      this.selectedGroupIndex = this.visibleGroups.indexOf(newGroup);

      this.nextProgram = this.getNextProgram();
      await this.forceUpdate();
    },
    getNextProgram: function () {
      let programs = [];
      for (const area of this.$store.state.areas) {
        let visiblePrograms = this.getVisibleProgramsForArea(area.id);
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
        let visiblePrograms = this.getVisibleProgramsForArea(area.id);
        if (visiblePrograms.length > 0) {
          return i;
        }
      }
      return null;
    },
    updateVisibleProgramsAfterGroupChange: async function (groupId) {
      if (this.disableEvents) {
        return;
      }
      try {
        this.disableEvents = true;
        const selectedArea = this.$store.state.areas[this.selectedAreaIndex];
        this.visibleGroups = this.getVisibleGroups(this.$store.state.areas.find(area => area.id === selectedArea.id));
        this.visiblePrograms = this.getVisibleProgramsForAreaAndGroup(selectedArea.id, groupId);
        await this.updateSelectedProgram(this.visiblePrograms[0]);
        this.selectedProgramIndex = 0;
        await this.forceUpdate();
      } finally {
        this.disableEvents = false;
      }
    },
    updateVisibleProgramsAfterAreaChange: async function (areaId) {
      if (this.disableEvents) {
        return;
      }
      try {
        this.disableEvents = true;
        this.visibleGroups = this.getVisibleGroups(this.$store.state.areas.find(area => area.id === areaId));
        this.visiblePrograms = this.getVisibleProgramsForAreaAndGroup(areaId, this.visibleGroups[0].id);
        await this.updateSelectedProgram(this.visiblePrograms[0]);
        this.selectedProgramIndex = 0;
        this.selectedGroupIndex = 0;
        await this.forceUpdate();
      } finally {
        this.disableEvents = false;
      }
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
      if (this.e1 === 6) {
        await this.$refs.references.load();
      }
    },
    updateSelectedProgram: async function (program) {
      this.$store.state.currentProgram = program;
      this.nextProgram = this.getNextProgram();
      await this.forceUpdate();
    },
    disableArea: function (areaId) {
      if (this.disableEvents) return true;
      return this.getVisibleProgramsForArea(areaId).length === 0;
    },
    getVisibleGroups: function (area) {
      let visibleGroups = [];
      for (const group of area.groups) {
        const visiblePrograms = group.programs.filter(program => this.$store.state.programSelection.has(program.id)).length;
        if (visiblePrograms !== 0) visibleGroups.push(group);
      }
      return visibleGroups;
    },
    getVisibleProgramsForArea: function (areaId) {
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
    },
    getVisibleProgramsForAreaAndGroup: function (areaId, groupId) {
      let programs = [];
      for (const area of this.$store.state.areas) {
        if (area.id !== areaId) continue;
        for (const group of area.groups) {
          if (group.id !== groupId) continue;
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

