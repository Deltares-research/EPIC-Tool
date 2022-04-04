<template>
  <div>
    <h2 style="color:darkred">Program selection</h2>
    <br>
    <h3>Please select 1 or more programs</h3>
    <br>
    <v-dialog v-model="showDialog" width="500">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">{{ programDescriptionTitle }}</v-card-title>
        <v-card-text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
          labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
          laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
          voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
          non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="showDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-card :elevation="2" color="blue-grey lighten-4" v-for="area in this.$store.state.areas" :key="area.id">
      <v-container fluid class="fill-height">
        <v-row no-gutters v-for="(group,index) in getGroupsForArea(area.id)" :key="group.id">
          <v-col md="2">
            <h3 v-if="index===0">{{ area.name }}</h3></v-col>
          <v-col md="4">
            <v-list-item dense @click="showGroup(group.id)">
              <v-list-item-content>
                <v-list-item-title>{{ group.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col md="6" v-if="group.showDetails">
            <v-list-item-group>
              <v-list-item dense v-for="(program) in getProgramsForGroup(group.id)" :key="program.id">
                <v-list-item-action>
                  <v-checkbox :input-value="getCheckBoxValue(program.id)"
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
    <v-row style="margin: 1px">
      <v-col md="3"></v-col>
      <v-col md="5">
        <v-img
            src="../../public/arrow.png"
        ></v-img>
      </v-col>
      <v-col md="3"></v-col>
      <v-col md="1">
        <v-btn to="Questionnaire" text color="primary">Start
          <v-icon>mdi-step-forward</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col md="5"></v-col>
      <v-col md="2">
        <v-img max-width="200px"
               src="../../public/people.png"
        ></v-img>
      </v-col>
      <v-col md="5">
      </v-col>
    </v-row>
  </div>

</template>
<script>

export default {
  name: 'SelectProgram',
  mounted() {

    if (this.$store.state.initialized) return;
    this.$store.commit("init");
    let areas = [
      {"id": 0, "name": "12"},
      {"id": 1, "name": "34"},
      {"id": 2, "name": "56"},
      {"id": 3, "name": "78"},
      {"id": 4, "name": "98"}
    ];
    this.$store.commit("updateAreas", areas);

    let groups = [
      {"id": 0, "areaId": 0, "name": "groupA", "showDetails": true},
      {"id": 1, "areaId": 0, "name": "groupB", "showDetails": false},
      {"id": 2, "areaId": 0, "name": "groupC", "showDetails": false},
      {"id": 3, "areaId": 0, "name": "groupD", "showDetails": false},
      {"id": 4, "areaId": 1, "name": "groupE", "showDetails": false},
      {"id": 5, "areaId": 1, "name": "groupF", "showDetails": false},
    ];
    this.$store.commit("updateGroups", groups);

    let programs = [
      {"id": 0, "groupId": 0, "name": "test1", "selected": false},
      {"id": 1, "groupId": 0, "name": "test2", "selected": false},
      {"id": 2, "groupId": 1, "name": "abc0", "selected": false},
      {"id": 3, "groupId": 1, "name": "abc1", "selected": false},
      {"id": 4, "groupId": 4, "name": "abc111", "selected": false},
      {"id": 5, "groupId": 4, "name": "abc1222", "selected": false}];

    this.$store.commit("updatePrograms", programs);

  },
  data() {
    return {
      showDialog: false,
      programDescriptionTitle: "",
    }
  },
  methods: {
    getCheckBoxValue: function (programId) {
      let program = this.$store.state.programs.find(program => program.id === programId);
      return program.selected;
    },
    selectProgram: function (programId) {
      this.$store.commit("selectProgram", programId);
    },
    getGroupsForArea: function (areaId) {
      return this.$store.getters.getGroupsForArea(areaId);
    },
    getProgramsForGroup: function (groupId) {
      return this.$store.getters.getProgramsForGroup(groupId);
    },
    showGroup: function (groupId) {
      for (let group of this.$store.state.groups) {
        if (group.id !== groupId) continue;
        this.$set(group, "showDetails", !group.showDetails);
      }
    },
    showProgramDescription: function (program) {
      this.showDialog = true;
      this.programDescriptionTitle = program;
    }
  },
  components: {}
  ,
}
</script>

