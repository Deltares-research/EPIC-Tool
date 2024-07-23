<template>
  <div>
    <h2 style="color: darkred" class="ma-5">Evolution Report</h2>
    <div style="margin-bottom: 100px;">

      <v-row class="custom-center">
        <v-btn class="primary" v-if="this.dataPieLoaded == false" @click="fetchPieData()">(Re)Generate interactive graph</v-btn>
      </v-row>

      <v-row
          class="ma-3"
      >

        <v-col>

          <div v-if="loading" class="mt-5">
            <h3>Generating evolution graph..</h3>
          </div>

          <v-row class="custom-center">
            <div v-if="!loading" class="custom-center ma-5">
              <h4 style="color: darkred; margin-bottom: 30px; max-width: 600px" v-if="this.dataPieLoaded == true">Please review the figure displaying your assessment results. To make adjustments, click on the relevant section to be directed back to the questionnaire. </h4>
              <h3 style="color: darkred; margin-bottom: 30px;" v-if="this.dataPieLoaded == true && this.clickedElementName == ''">Click on the graph to change an element</h3>
              <h3 style="color: darkred; margin-bottom: 30px;" v-if="this.dataPieLoaded == true && this.clickedElementName && !selectedProgramCheck">{{clickedElementName}} is not part of your selected programs.</h3>
              <v-btn class="primary" style="margin-bottom: 30px;" v-if="this.dataPieLoaded == true && this.clickedElementName !== '' && selectedProgramCheck" @click="goToQuestionnaire()">Change {{clickedElementName}}</v-btn>
              <v-btn class="primary" style="margin-bottom: 30px;" v-if="this.dataPieLoaded == true" @click="generateGraph()">Confirm graph</v-btn>
            </div>
          </v-row>

          <v-row>
            <v-chart
            v-if="this.dataPieLoaded == true && !loading"
            class="chart-area-bar"
            :init-options="initOptions"
            :option="optionBar"
            @click="onChartClick"
          />
          </v-row>

        </v-col>

        <v-col>
          
          <v-chart
            v-if="this.dataPieLoaded == true && !loading"
            class="chart-area-pie"
            :option="optionPie"
            @click="onChartClick"
          />

        </v-col>

      </v-row>

      <div v-if="this.dataImgLoaded" class="custom-center">
            <h3 style="color: darkred">Graph</h3>
            <v-img
              class="image-pie"
              max-height="1000px"
              max-width="1000px"
              :src="imageUrl"
            ></v-img>
            <a :href="pdfUrl" download target="_blank">Download graph</a>
          </div>

    </div>
    <!-- <h2 style="color: darkred">Evolution report</h2> -->
    <!-- <v-row
        align="center"
        justify="space-around"
    >
      <v-btn class="primary" @click="generateGraph()">Generate evolution graph</v-btn>
    </v-row> -->
    <!-- <div v-if="loading">
      <h3>Generating evolution graph..</h3>
    </div>
    <div v-if="this.dataLoaded">
      <h3 style="color: darkred">Graph</h3>
      <v-img
          max-height="1000px"
          max-width="1000px"
          :src="imageUrl"
      ></v-img>
      <a :href="pdfUrl" download target="_blank">Download graph</a>
    </div> -->
  </div>
</template>

<script>
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import { BarChart } from 'echarts/charts'
  import { PieChart } from 'echarts/charts'
  import { TooltipComponent } from 'echarts/components'
  import { LineChart } from 'echarts/charts'
  import { GridComponent } from 'echarts/components'
  import { ToolboxComponent } from 'echarts/components'
  import { mapState, mapMutations } from 'vuex'

  import VChart from 'vue-echarts'

  use([ CanvasRenderer, BarChart, PieChart, LineChart, GridComponent, TooltipComponent, ToolboxComponent ])

export default {
  components: {
    VChart,
  },
  name: "EvolutionOverview",
  mounted() {
    this.dataPieLoaded = false;
    this.dataImgLoaded = false;
    this.url = "";
  },
  computed: {
    ...mapState(['programs', 'programSelection', 'currentProgram']),
    selectedProgramCheck() {
      const arrayPrograms = Array.from(this.programSelection);
      return arrayPrograms.find(program => program === this.currentProgram.id)
    }
  },

  methods: {
    ...mapMutations(['updateCurrentProgram']),
    generateGraph: async function () {
      this.loading = true;
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
      try {
        let server = process.env.VUE_APP_BACKEND_URL;
        let programResponse = await fetch(server + '/api/summary/evolution-graph/', options);
        let res = await programResponse.json();
        this.dataImgLoaded = true;
      
        this.imageUrl = res.summary_graph;
        this.pdfUrl = res.summary_pdf.replace(server, "");
      } finally {
        this.loading = false;
        this.dataPieLoaded = false;
      }
    },
    fetchPieData: async function () {
      this.loading = true;
      this.dataImgLoaded = false;
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
      try {
        let server = process.env.VUE_APP_BACKEND_URL;
        let programResponse = await fetch(server + '/api/summary/evolution-graph/', options);
        let res = await programResponse.json();
        this.dataPieLoaded = true;

        
        let programArray = res.summary_data.map(element => element.program);
      
        let averageArray = res.summary_data.map(element => element.average);
       
        let areaArray = res.summary_data.map(element => element.area);
       
        let combinedArray = averageArray.map(function(x, i) {
          return [x, programArray[i], areaArray[i]]
        });
      
        let parameters = ["value", "name", "area"];

        this.optionPie.series[0].data = combinedArray.map(function(row) {
          return row.reduce(function(result, field, index) {
            result[parameters[index]] = field;
            return result;
          }, {});
        });
       

        let combinedData = combinedArray.map(function(row) {
          return row.reduce(function(result, field, index) {
            result[parameters[index]] = field;
            return result;
          }, {});

        });

        let groupedAreas = Object.groupBy(combinedData, ({ area }) => area);
        // console.log('groupedAreas.Enable[0].name', groupedAreas.Enable[0].name)

        // List of Whole of Society item names
        const wosItems = [
          'Local Government', 
          'Public Participation & Stakeholder Engagement', 
          'Social Inclusion', 
          'Education & Risk Communication', 
          'Scientific Collaboration', 
          'Open Data'
        ];

        this.optionPie.series[0].data = groupedAreas.Plan;
        this.optionPie.series[1].data = groupedAreas.Invest;
        this.optionPie.series[2].data = groupedAreas.Control;
        this.optionPie.series[3].data = groupedAreas.Respond;

        // Remove wosItems from Enable list
        const enableDataWithoutWos = groupedAreas.Enable.filter(item => !wosItems.includes(item.name));
        this.optionPie.series[4].data = enableDataWithoutWos;

        // Calculate mean value for Whole of Society
        const wosData = groupedAreas.Enable.filter(item => wosItems.includes(item.name));
        const wosMeanValue = wosData.reduce((sum, item) => sum + item.value, 0) / wosData.length;
        const wholeOfSocietyItem = { name: 'Whole of Society', value: wosMeanValue };

        // Add Whole of Society item to the Enable list
        this.optionPie.series[4].data.push(wholeOfSocietyItem);

        // Filter the series data and yAxis data
        const filteredData = groupedAreas.Enable.filter(item => wosItems.includes(item.name));

        this.optionBar.series[0].data = filteredData;
        this.optionBar.yAxis.data = filteredData.map(item => item.name);

        this.imageUrl = res.summary_graph;
        this.pdfUrl = res.summary_pdf.replace(server, "");
      } finally {
        this.loading = false;
      }
    },
    onChartClick(params) {
      this.clickedElementName = params.name;
      const selectedProgram = this.programs.find(program => program.name === params.name)
      this.updateCurrentProgram(selectedProgram)
      
    },
    goToQuestionnaire() {
      // Get the current URL
      const currentUrl = window.location.href;
      // Find the position of the last '/' in the URL
      const lastSlashIndex = currentUrl.lastIndexOf('/');
      // Create the new URL by slicing the current URL up to the last '/' and appending 'Questionnaire'
      const newUrl = `${currentUrl.slice(0, lastSlashIndex)}/Questionnaire`;
      // Open the new URL in the current tab
      window.location.href = newUrl;
  },
  },
  data() {
    return {
      loading: false,
      dataImgLoaded: false,
      dataPieLoaded: false,
      imageUrl: "",
      pdfUrl: "",
      clickedElementName: '',
      initOptions: { height: '500px', width:'700px' },
      optionPie : {
        tooltip: {
          trigger: "item"
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: true },
            // restore: { show: true },
            // saveAsImage: { show: true }
          }
        },
        series: [
          {
            name: 'Plan',
            id: 'Plan',
            type: 'pie',
            radius: [100, 300],
            center: ['50%', '50%'],
            roseType: 'radius',
            avoidLabelOverlap: true,
            itemStyle: {
              borderWidth: 3,
              borderRadius: 5,
              borderColor: '#FFF',
              borderCap: "square",
              color: "#66c2a5"
            },
            selectedMode: 'single',
            selectedOffset: '30',
            showEmptyCircle: true,
            label: {
              show: true,
              position: 'inside',
              rotate: true,
              fontSize: 10,
              height: 1,
              padding: [ 0, 0, 0, 260 ]
            },
            data: [],
            startAngle: 90,
            endAngle: 42.6315789474,
            minAngle: 100000
          },
          {
            name: 'Invest',
            id: 'Invest',
            type: 'pie',
            radius: [100, 300],
            center: ['50%', '50%'],
            roseType: 'radius',
            avoidLabelOverlap: true,
            itemStyle: {
              borderWidth: 3,
              borderRadius: 5,
              borderColor: '#FFF',
              borderCap: "square",
              color: "#a89bb0"
            },
            selectedMode: 'single',
            selectedOffset: '30',
            showEmptyCircle: true,
            label: {
              show: true,
              position: 'inside',
              rotate: true,
              fontSize: 10,
              height: 1,
              padding: [ 0, 0, 0, 260 ]
            },
            data: [],
            startAngle: 42.6315789474,
            endAngle: 326.842105263,
            minAngle: 100000
          },
          {
            name: 'Control',
            id: 'Control',
            type: 'pie',
            radius: [100, 300],
            center: ['50%', '50%'],
            roseType: 'radius',
            avoidLabelOverlap: true,
            itemStyle: {
              borderWidth: 3,
              borderRadius: 5,
              borderColor: '#FFF',
              borderCap: "square",
              color: "#c6b18b"
            },
            selectedMode: 'single',
            selectedOffset: '30',
            showEmptyCircle: true,
            label: {
              show: true,
              position: 'inside',
              rotate: true,
              fontSize: 10,
              height: 1,
              padding: [ 0, 0, 0, 260 ]
            },
            data: [],
            startAngle: 326.842105263,
            endAngle: 270,
            minAngle: 100000
          },
          {
            name: 'Respond',
            id: 'Respond',
            type: 'pie',
            radius: [100, 300],
            center: ['50%', '50%'],
            roseType: 'radius',
            avoidLabelOverlap: true,
            itemStyle: {
              borderWidth: 3,
              borderRadius: 5,
              borderColor: '#FFF',
              borderCap: "square",
              color: "#f8d348"
            },
            selectedMode: 'single',
            selectedOffset: '30',
            showEmptyCircle: true,
            label: {
              show: true,
              position: 'inside',
              rotate: true,
              fontSize: 10,
              height: 1,
              padding: [ 0, 260, 0, 0 ]
            },
            data: [],
            startAngle: 270,
            endAngle: 203.684210526,
            minAngle: 100000
          },
          {
            name: 'Enable',
            id: 'Enable',
            type: 'pie',
            radius: [100, 300],
            center: ['50%', '50%'],
            roseType: 'radius',
            avoidLabelOverlap: true,
            itemStyle: {
              borderWidth: 3,
              borderRadius: 5,
              borderColor: '#FFF',
              borderCap: "square",
              color: "#b3b3b3"
            },
            selectedMode: 'single',
            selectedOffset: '30',
            showEmptyCircle: true,
            label: {
              show: true,
              position: 'inside',
              rotate: true,
              fontSize: 10,
              height: 1,
              padding: [ 0, 260, 0, 0 ],
            },
            data: [],
            startAngle: 203.684210526,
            endAngle: 90,
            minAngle: 100000
          },
          {
            type: 'pie',
            radius: [95, 96],
            avoidLabelOverlap: true,
            padAngle: 8,
            itemStyle: {
              borderWidth: 2,
              borderRadius: 5,
              borderColor: '#000',
              borderCap: "square",
              color: '#FFF'
            },
            showEmptyCircle: true,
            data: [
              { value: 13.1578947368333},
              { value: 21.052631579},
              { value: 15.7894736841667},
              { value: 18.4210526316667},
              { value: 31.5789473683333}
            ],
            emphasis: {
              disabled: true,
            },
            tooltip: {
              show: false,
            },
            cursor: 'auto'
          },
          {
            type: 'pie',
            radius: [50, 95],
            avoidLabelOverlap: true,
            padAngle: 8,
            showEmptyCircle: true,
            label: {
              show: true,
              position: 'inner',
              fontSize: 24,
              padding: [0, 0, 0, 0]
            },
            data: [
              { value: 13.1578947368333, name: 'P' },
              { value: 21.052631579, name: 'I' },
              { value: 15.7894736841667, name: 'C' },
              { value: 18.4210526316667, name: 'R' },
              { value: 31.5789473683333, name: 'E' }
            ],
            color: '#FFF',
            emphasis: {
              disabled: true,
            },
            tooltip: {
              show: false,
            },
            cursor: 'auto',
            silent: 'true'
          }
        ]
      },
      optionBar : {
        tooltip: {
          trigger: "item"
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: true },
            // restore: { show: true },
            // saveAsImage: { show: true }
          }
        },
        xAxis: {
        type: 'value',
        min: 0,
        max: 4,
        interval: 1,
        axisLabel: {
          formatter: function(value) {
            var labels = ['N/A', 'Nascent', 'Engaged', 'Capable', 'Effective'];
            return labels[value] || value;
            }
          }
        },
        yAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            interval: 0, 
            show: true,
            width: 250,
            overflow: 'break'
          }
        },
        grid: {
          left: 300  // Adjust this value to provide enough space for the labels
        },
        series: [
          {
            name: 'Enable',
            id: 'Enable',
            type: 'bar',
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 5,
              borderCap: "square",
              color: "#b3b3b3"
            },
            selectedMode: 'single',
            selectedOffset: '30',
            showEmptyCircle: true,
            label: {
              show: false
            },
            data: [],
          }
        ]
      }
    }
  }

}
</script>

<style scoped>
.chart-area-bar {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center; /* Center buttons horizontally */
}
.chart-area-pie {
  padding-top: 20px;
  padding-bottom: 5px;
  position: flex;
  height: 800px;
}
.image-pie {
  padding-top: 20px;
  padding-bottom: 5px;
  position: flex;
  height: 800px;
}
.centered-column{
  position: absolute;
  left: 500px;
}
.custom-center {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center; /* Center buttons horizontally */
}
.button-container .v-btn {
  width: 200px; /* Fixed width for buttons */
}
</style>