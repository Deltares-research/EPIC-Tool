<template>
  <div>
    <h2 style="color: darkred">Evolution</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <br>
    <h4>What is the level of development for {{ title }} in your country? </h4>
    <br>
    <v-row v-for=" (dimension,index) in dimensions" :key="dimension.title">
      <v-col md="12">
        <h4>{{ dimension.title }}</h4>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'nascent')"
                  @click="select('nascent',index)">
            <v-card-title>Nascent</v-card-title>
            <v-card-text>{{ dimension.nascent_description }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'engaged')"
                  @click="select('engaged',index)">
            <v-card-title>Engaged</v-card-title>
            <v-card-text>{{ dimension.engaged_description }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'Capable')"
                  @click="select('Capable',index)">
            <v-card-title>Capable</v-card-title>
            <v-card-text>{{ dimension.capable_description }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col md="3">
        <v-hover v-slot="{ hover }">
          <v-card height="200px" :elevation="hover ? 16 : 2" :key="update"
                  :color="isSelected(index,'Effective')"
                  @click="select('Effective',index)">
            <v-card-title>Effective</v-card-title>
            <v-card-text>{{ dimension.effective_description }}</v-card-text>
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
import loadQuestions from "@/assets/js/utils";

export default Vue.extend({
  name: 'Evolution',
  async mounted() {
    let program = this.$store.state.currentProgram;
    this.title = program.name;
    this.dimensions = await loadQuestions(program.id, 'evolution', this.$store.state.token);
    this.selected = [this.dimensions.length];

  },
  methods: {
    isSelected: function (index, selected) {
      return this.selected[index] === selected ? 'red lighten-5' : 'blue-grey lighten-4';
    },
    select: function (program, index) {
      this.selected[index] = program;
      this.update++;
    }
  },
  data: () => ({
    selected: [],
    update: 1,
    title: "",
    dimensions: []
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
