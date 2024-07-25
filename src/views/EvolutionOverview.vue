<template>
  <div>
    <h2 style="color: darkred" class="ma-5">Evolution Report</h2>
    <div>

      <v-row class="custom-center">
        <v-btn class="primary" v-if="this.dataPieLoaded == false" @click="fetchPieData()">(Re)Generate interactive graph</v-btn>
      </v-row>

      <div class="scroll-container">
      <v-row
          class="ma-3"
      >

        <v-col cols="12" md="6">

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

          <v-row class="custom-center">
            <div v-if="this.dataPieLoaded == true && !loading" class="border-wos">
              <v-chart
              v-if="this.dataPieLoaded == true && !loading"
              class="chart-area-bar"
              :init-options="initOptionsBar"
              :option="optionBar"
              @click="onChartClick"
            />
            </div>
          </v-row>

        </v-col>

        <v-col cols="12" md="6">
          <div class="chart-container">
            <v-chart
              v-if="this.dataPieLoaded == true && !loading"
              class="chart-area-pie"
              :init-options="initOptionsPie"
              :option="optionPie"
              @click="onChartClick"
            />
          </div>

        </v-col>

      </v-row>
    </div>

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
  import { TitleComponent } from 'echarts/components'
  import { mapState, mapMutations } from 'vuex'

  import VChart from 'vue-echarts'

  use([ CanvasRenderer, BarChart, PieChart, LineChart, GridComponent, TooltipComponent, ToolboxComponent, TitleComponent ])

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
          if (groupedAreas && groupedAreas.Control) {
            const controlData = groupedAreas.Control.map(item => {
              if (item.name === 'Floodplain Regulation' || item.name === 'Local Flood Mitigation Planning') {
                return {
                  ...item,
                  label: {
                    ...this.optionPie.series[2].label, // Copy other label properties
                    padding: [0, 0, 0, -210], // Different padding
                  } // TODO: also make the align property to change to 'right' for these two items
                };
              }
              return item;
            });
            // Update the series data
            this.optionPie.series[2].data = controlData;
          }

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
        if (groupedAreas && groupedAreas.Enable && this.optionPie.series[4].data) {
            const enableData = this.optionPie.series[4].data.map(item => {
              if (item.name === 'Whole of Society') {
                return {
                  ...item,
                  itemStyle: {
                    ...this.optionPie.series[4].itemStyle, // Copy other itemStyle properties
                      borderColor: '#484848',
                      color: '#E1BA96'
                  }
                };
              }
              return item;
            });

            // Update the series data
            this.optionPie.series[4].data = enableData;
          }



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
      initOptionsBar: { height: '350px', width:'600px' },
      initOptionsPie: { height: '900px', width:'900px' },
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
              color: "#426275"
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
              padding: [ 0, 0, 0, 110],
              width: 135,
              overflow: 'break',
              color: '#000000'
            },
            labelLayout: {
              align: 'left'
            },
            data: [],
            startAngle: 90,
            endAngle: 35.4545454545455,
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
              color: "#91A99B"
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
              padding: [ 0, 0, 0, 110],
              width: 135,
              overflow: 'break',
              color: '#000000'
            },
            labelLayout: {
              align: 'left'
            },
            data: [],
            startAngle: 35.4545454545455,
            endAngle: 308.181818181818,
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
              color: "#AE1F23"
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
              padding: [0, 0, 0, 110],
              width: 135,
              overflow: 'break',
              color: '#000000'
            },
            labelLayout: {
              align: 'left'
            },
            data: [],
            startAngle: 308.181818181818,
            endAngle: 253.636363636364,
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
              color: "#225F3A"
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
              padding: [ 0, 110, 0, 0],
              width: 135,
              overflow: 'break',
              color: '#000000'
            },
            labelLayout: {
              align: 'right'
            },
            data: [],
            startAngle: 253.636363636364,
            endAngle: 166.363636363636,
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
              color: "#DC7F29"
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
              padding: [ 0, 110, 0, 0],
              width: 135,
              overflow: 'break',
              color: '#000000'
            },
            labelLayout: {
              align: 'right'
            },
            data: [],
            startAngle: 166.363636363636,
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
              { value: 15.1515151515152},
              { value: 24.2424242424242},
              { value: 15.1515151515152},
              { value: 24.2424242424242},
              { value: 21.2121212121212}
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
              { value: 15.1515151515152, name: 'P' },
              { value: 24.2424242424242, name: 'I' },
              { value: 15.1515151515152, name: 'C' },
              { value: 24.2424242424242, name: 'R' },
              { value: 21.2121212121212, name: 'E' }
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
        title: {
          text: "Whole of Society breakdown",
          left: 'center',
          top: 10,
          show: true
        },
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
              color: "#E1BA96"
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

.scroll-container {
  overflow-x: auto; /* Enable horizontal scrolling */
  padding-bottom: 1px; /* Ensure scrollbar is visible */
}
.chart-area-bar {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center; /* Center buttons horizontally */
}
.border-wos{
  border: 3px solid #484848;
  border-radius: 5px;
}
.chart-area-pie {
  padding-top: 0px;
  margin-top: -60px;
  padding-bottom: 5px;
  position: relative;
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