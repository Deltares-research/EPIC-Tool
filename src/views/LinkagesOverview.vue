<template>
  <v-card>
    <v-card-title><h3 style="color: darkred">Linkages report</h3>
    </v-card-title>
    <v-content>
      <a @click.prevent="generateReport()" href="#">Download report</a>
      <v-data-table
          :headers="headers"
          :items="linkagesValues"
          :items-per-page="5"
          class="elevation-1"
      >
        <template
            v-for="program in this.programs"
            v-slot:[`item.${program.id}`]="{ item }"
        >
          <v-icon :key="item[program.id]" color="blue" v-if="item[program.id]==='1'">
            mdi-checkbox-marked-circle
          </v-icon>
          <slot :name="program.id" :item="item"/>
        </template>
      </v-data-table>

    </v-content>
  </v-card>
</template>

<script>
import * as util from "@/assets/js/utils";

export default {
  name: "LinkagesOverview.vue",
  methods: {
    generateReport: function () {
      let csvData = "program,";
      for (let i = 0; i < this.programs.length; i++) {
        csvData = csvData + '"'+this.programs[i].name + '"'+",";
      }
      csvData=csvData+"\n";
      for (let i = 0; i < this.linkagesValues.length; i++) {
        csvData = csvData + '"'+this.linkagesValues[i].name + '"'+",";
        for (let j = 0; j < this.programs.length; j++) {
          const value = this.linkagesValues[i][this.programs[j].id] !== undefined ? "1" : "0";
          csvData = csvData + value + ",";
        }
        csvData = csvData + "\n";
      }
      var hiddenElement = document.createElement('a');
      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvData);
      hiddenElement.target = '_blank';
      hiddenElement.download = 'EPIC-Response-linkages-report.csv';
      hiddenElement.click();
    },
  },
  mounted: async function () {
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
    let programResponse = await fetch(server + '/api/program/?format=json', options);
    this.programs = await programResponse.json();
    this.programs.sort((a, b) => a.id - b.id);

    let newHeader = [];
    newHeader.push({"text": "Program", "value": "name"})
    for (const program of this.programs) {
      let columnHeader = {};
      columnHeader.text = program.name;
      columnHeader.value = program.id.toString();
      newHeader.push(columnHeader);
    }
    this.headers = newHeader;
    const response = await util.loadLinkages(this.$store.state.token);

    for (let i = 0; i < response.length; i++) {
      console.log(response[i])
      let valueRow = {};
      valueRow.name = this.programs.find(program => program.id === response[i].id).name;
      for (let j = 0; j < response[i].selected_programs.length; j++) {
        let selectedProgramId = response[i].selected_programs[j];
        valueRow[selectedProgramId] = "1";
      }
      this.linkagesValues.push(valueRow);
    }


  },
  data() {
    return {
      programs: [],
      headers: [],
      linkagesValues: [],
    }
  }
}
</script>

<style scoped>

</style>