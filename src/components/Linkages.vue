<template>
  <div>
    <h2 style="color:darkred">Linkages</h2>
    <h3 style="color: darkred">{{ title }}</h3>
    <br>
    <h3>Please select three programs that will help you deliver better results in your program if you could have better
      collaboration? </h3>
    <br>
    <v-card :elevation="2" color="blue-grey lighten-4" v-for="area in this.$store.state.areas" :key="area.id">
      <v-container fluid class="fill-height">
        <v-row no-gutters v-for="(group,index) in getGroupsForArea(area.id)" :key="group.id">
          <v-col md="2">
            <h3 v-if="index===0">{{ area.name }}</h3></v-col>
          <v-col md="4">
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>{{ group.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col md="6" v-if="group.showDetails">
            <v-list-item-group>
              <v-list-item dense v-for="(program) in getProgramsForGroup(group.id)" :key="program.id">
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

export default Vue.extend({
  name: 'SelectProgram',
  mounted() {
    let program = this.$store.state.programs.find(program => program.id === this.$store.state.currentProgramId);
    this.title = program.name;
  },
  methods: {
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
    getGroupsForArea: function (areaId) {
      return this.$store.getters.getGroupsForArea(areaId);
    },
    getProgramsForGroup: function (groupId) {
      return this.$store.getters.getProgramsForGroup(groupId);
    },
  },
  data: () => ({
    active: false,
    title:"",
    selectedPrograms: new Set(),
  }),
})
</script>

<style scoped>

</style>
``
