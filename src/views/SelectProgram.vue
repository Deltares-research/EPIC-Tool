<template>
  <div>
    <h2 style="color:darkred">Program selection</h2>
    <br>
    <h3>Click on an agency or select manually the programs to assess</h3>
    <br>
    <v-dialog v-model="showDialog" width="500">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">{{ title }}</v-card-title>
        <v-card-text>{{ description }}</v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="showDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showHelpDialog" width="500">
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">Program selection</v-card-title>
        <v-card-text> <br> Click on an agency or select manually the programs to assess. </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="showHelpDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-row>
      <v-col md="12" :key="updateCheckBox">
        <v-btn :color="isAgencySelected(agency)?'red lighten-5':'blue-grey lighten-4'" small class="ma-2"
               v-for="agency in agencies" :key="agency.id" elevation="3"
               @click="selectProgramsForAgency(agency)">{{ agency.name }}
        </v-btn>
      </v-col>
    </v-row>
    <br>
    <v-row style="margin: 1px">
      <v-col md="3"></v-col>
      <v-col md="5">
      </v-col>
      <v-col md="3"></v-col>
      <v-col md="1">
        <v-btn to="Questionnaire" text color="primary" :disabled="this.$store.state.programSelection.size===0">Start
          <v-icon>mdi-step-forward</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-card :elevation="2" color="blue-grey lighten-4" v-for="area in this.$store.state.areas" :key="area.id">
      <v-container fluid class="fill-height">
        <v-row no-gutters v-for="(group,index) in area.groups" :key="group.id">
          <v-col md="2">
            <h3 v-if="index===0">{{ area.name }}</h3>
          </v-col>
          <v-col md="4">
            <v-list-item dense style="font-size: 1px" @click="showGroup(group.id)">
              <v-list-item-content>
                     <v-list-item-title>{{ group.name }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-icon>
                <v-icon v-if="isAnyProgramSelected(group)" color="blue darken-2">mdi-checkbox-marked</v-icon>
              </v-list-item-icon>
              <v-list-item-icon>
                <v-icon v-if="!isGroupSelected(group.id)">mdi-plus</v-icon>
                <v-icon v-if="isGroupSelected(group.id)">mdi-minus</v-icon>
              </v-list-item-icon>
            </v-list-item>
          </v-col>
          <v-col md="6">
            <v-list-item-group v-if="isGroupSelected(group.id)">
              <v-list-item dense v-for="(program) in group.programs" :key="program.id">
                <v-list-item-action>
                  <v-checkbox :key="updateCheckBox" :input-value="getCheckBoxValue(program.id)"
                              @click="selectProgram(program.id)"></v-checkbox>
                </v-list-item-action>
                <v-btn color="black" x-small text @click="showProgramDescription(program)">{{ program.name }}
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

export default {
  name: 'SelectProgram',
  async mounted() {
    //TODO: Luis. Check if possible to move the api call to home. 
    // we need to have the programs populated before we click the select program tab probably.
    const token = this.$store.state.token;
    const options = {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token,
      },
    }
    let server = process.env.VUE_APP_BACKEND_URL;
    let response = await fetch(server + '/api/agency/?format=json', options);
    this.agencies = await response.json();
    this.agencies.sort((a, b) => a.id - b.id);

    if (this.$store.state.initialized) return;
    response = await fetch(server + '/api/area/?format=json', options);
    let areas = await response.json();
    this.$store.commit("updateAreas", areas);
    this.$store.commit("init");
  },
  data() {
    return {
      updateCheckBox: 0,
      agencies: [],
      groupSelection: new Set(),
      showDialog: false,
      showHelpDialog: true,
      title: "",
      description: "",
    }
  },
  methods: {
    isAgencySelected: function (agency) {
      if (this.$store.state.selectedAgency === undefined) return false;
      return this.$store.state.selectedAgency.id === agency.id;
    },
    selectProgramsForAgency: function (agency) {
      this.$store.commit("toggleAgencySelection", agency);
      this.$store.state.programSelection.forEach(programId => {
        let program = this.$store.state.programs.filter(program => program.id === programId);
        this.groupSelection.add(program[0].group);
      })
      this.updateCheckBox++;
    },
    getCheckBoxValue: function (programId) {
      return this.$store.state.programSelection.has(programId);
    },
    selectProgram: function (programId) {
      this.$store.commit("toggleSelection", programId);
      this.updateCheckBox++;
    },
    isGroupSelected: function (groupId) {
      return this.groupSelection.has(groupId);
    },
    isAnyProgramSelected: function (group) {
      for (let program of group.programs) {
        let selected = this.$store.state.programSelection.has(program.id);
        if (selected) return true;
      }
      return false;
    },
    showGroup: function (groupId) {
      const selected = this.groupSelection.has(groupId);
      if (selected) {
        this.groupSelection.delete(groupId);
      } else {
        this.groupSelection.add(groupId);
      }
      this.updateCheckBox++;
    },
    showProgramDescription: function (program) {
      this.showDialog = true;
      this.title = program.name;
      this.description = program.description;
    }
  },
  components: {}
  ,
}
</script>

