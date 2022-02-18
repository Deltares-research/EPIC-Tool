<template>
  <div>
    <p>Progress 45% 2 minutes left</p>
    <v-progress-linear value="45"></v-progress-linear>
    <br>
    <v-tabs color="darkred" left :value="selectedTab">
      <v-tab >
        <v-icon dark right v-if="showCheck">mdi-checkbox-marked-circle</v-icon>Integrated River Basin Planning
      </v-tab>
      <v-tab>Coastal Zone Management Planning</v-tab>
      <v-tab>Irrigation Water Supply Planning</v-tab>
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
          <program-description :tabs="selectedTab"></program-description>
          <v-card-actions>
            <v-row>
              <v-col md="10">
              </v-col>
              <v-col md="2">
                <v-btn text color="primary" @click="e1 = 2">National framework
                  <v-icon>mdi-step-forward</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-actions>
        </v-stepper-content>
        <v-stepper-content step="2">
          <national-frameworks></national-frameworks>
          <v-row>
            <v-col md="1">
              <v-btn text color="primary" @click="e1 = 1">
                <v-icon>mdi-step-backward</v-icon>
                Program description
              </v-btn>
            </v-col>
            <v-col md="9">
            </v-col>
            <v-col md="2">
              <v-btn text color="primary" @click="e1 = 3">Key agency actions
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="3">
          <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
          <v-row>
            <v-col md="1">
              <v-btn text color="primary" @click="e1 = 2">
                <v-icon>mdi-step-backward</v-icon>
                National framework
              </v-btn>
            </v-col>
            <v-col md="10">
            </v-col>
            <v-col md="1">
              <v-btn text color="primary" @click="e1 = 4">Evolution
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="4">
          <evolution></evolution>
          <v-row>
            <v-col md="1">
              <v-btn text color="primary" @click="e1 = 3">
                <v-icon>mdi-step-backward</v-icon>
                Key agency actions
              </v-btn>
            </v-col>
            <v-col md="10">
            </v-col>
            <v-col md="1">
              <v-btn text color="primary" @click="e1 = 5">Linkages
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="5">
          <linkages></linkages>
          <v-row>
            <v-col md="1">
              <v-btn text color="primary" @click="e1 = 4">
                <v-icon>mdi-step-backward</v-icon>
                Key agency actions
              </v-btn>
            </v-col>
            <v-col md="10">
            </v-col>
            <v-col md="1">
              <v-btn text color="primary" @click="e1 = 6">References
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
        <v-stepper-content step="6">
          <v-card class="mb-12" color="grey lighten-1" height="200px"></v-card>
          <v-row>
            <v-col md="10">
              <v-btn text color="primary" @click="e1 = 5"><v-icon>mdi-step-backward</v-icon>Linkages</v-btn>
            </v-col>
            <v-col md="1">
              <v-btn text color="primary" @click="selectProgram">Coastal management planning
                <v-icon>mdi-step-forward</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-stepper-content>
      </v-stepper-items>

    </v-stepper>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'
import SelectProgram from "@/components/SelectProgram.vue";
import ProgramDescription from "@/components/ProgramDescription.vue";
import NationalFrameworks from "@/components/NationalFrameworks.vue";
import Evolution from "@/components/Evolution.vue";
import Linkages from "@/components/Linkages.vue";

export default Vue.extend({
  name: 'HelloWorld',
  components: {Linkages, Evolution, NationalFrameworks, ProgramDescription},
  methods: {
    selectProgram: function () {
      this.showCheck = true;
      this.e1=1;
      this.selectedTab=1;
    }
  },
  data: () => ({
    e1: 1,
    showCheck: false,
    selectedTab: 0,
    ecosystem: [
      {
        text: 'vuetify-loader',
        href: 'https://github.com/vuetifyjs/vuetify-loader',
      },
      {
        text: 'github',
        href: 'https://github.com/vuetifyjs/vuetify',
      },
      {
        text: 'awesome-vuetify',
        href: 'https://github.com/vuetifyjs/awesome-vuetify',
      },
    ],
    importantLinks: [
      {
        text: 'Documentation',
        href: 'https://vuetifyjs.com',
      },
      {
        text: 'Chat',
        href: 'https://community.vuetifyjs.com',
      },
      {
        text: 'Made with Vuetify',
        href: 'https://madewithvuejs.com/vuetify',
      },
      {
        text: 'Twitter',
        href: 'https://twitter.com/vuetifyjs',
      },
      {
        text: 'Articles',
        href: 'https://medium.com/vuetify',
      },
    ],
    whatsNext: [
      {
        text: 'Explore components',
        href: 'https://vuetifyjs.com/components/api-explorer',
      },
      {
        text: 'Select a layout',
        href: 'https://vuetifyjs.com/getting-started/pre-made-layouts',
      },
      {
        text: 'Frequently Asked Questions',
        href: 'https://vuetifyjs.com/getting-started/frequently-asked-questions',
      },
    ],
  }),
})
</script>
``
