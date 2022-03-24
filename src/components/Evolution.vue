<template>
  <div>
    <h2 style="color: darkred">Evolution</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <br>
    <h4>What is the level of development for River Basin Planning programs in your country? </h4>
    <br>
    <v-row>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="350px" :elevation="hover ? 16 : 2"
                  :color="selected==='nascent'?'red lighten-5':'blue-grey lighten-4'"
                  @click="select('nascent')">
            <v-card-title>Nascent</v-card-title>
            <v-card-text>No water resources law in place and so no river basin plans are prepared. Water resources
              development and management takes place in an ad hoc and uncoordinated manner.
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="350px" :elevation="hover ? 16 : 2"
                  :color="selected==='engaged'?'red lighten-5':'blue-grey lighten-4'"
                  @click="select('engaged')">
            <v-card-title>Engaged</v-card-title>
            <v-card-text>Water resources law in force that requires preparation of basin plans. Several plans prepared
              but without involvement of stakeholders, and do not comprehensively address flood and drought risk
              management. No linkage with water use (urban and agriculture) or local flood plans.

            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="350px" :elevation="hover ? 16 : 2"
                  :color="selected==='Capable'?'red lighten-5':'blue-grey lighten-4'"
                  @click="select('Capable')">
            <v-card-title>Capable</v-card-title>
            <v-card-text>Basin plans promote stakeholder engagement through formal mechanisms, such as basin committees
              or
              authorities. Drought and flood risk management are incorporated into basin plans or undertaken in a
              parallel
              process. Some linkage with water use (urban and agriculture) and local flood plans.
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="350px" :elevation="hover ? 16 : 2"
                  :color="selected==='Effective'?'red lighten-5':'blue-grey lighten-4'"
                  @click="select('Effective')">
            <v-card-title>Effective</v-card-title>
            <v-card-text>Basin plans formulated with active engagement by all stakeholders through formal mechanisms.
              Adaptive planning process utilized. Standalone basin flood management and drought management plans
              prepared
              and integrated into overall basin plan. Close linkages with water user and local flood plans.
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
    <br>
    <h3>Please justify your answer</h3>
    <v-textarea rows=5 outlined></v-textarea>
  </div>
</template>
<script>
import Vue from 'vue'

export default Vue.extend({
  name: 'Evolution',
  mounted() {
    let program = this.$store.state.programs.find(program => program.id === this.$store.state.currentProgramId);
    this.title = program.name;
  },
  methods: {
    select: function (program) {
      this.selected = program
    }
  },
  data: () => ({
    selected: "",
    title: ""
  }),

})
</script>

<style scoped>
</style>
``
