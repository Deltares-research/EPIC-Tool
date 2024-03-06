<template>
  <div>
    <h2 style="color: darkred">Test interactive pie evolution graph</h2>
    <div style="margin-bottom: 100px;">
      <v-row
          align="center"
          justify="space-around"
      >
        <v-btn class="primary" @click="fetchPieData()">Get data for test pie graph</v-btn>
      </v-row>
      <br>

      <v-chart
        class="chart-area"
        :option="optionPie"
      />

      <br>
    </div>
    <h2 style="color: darkred">Test interactive bar evolution graph</h2>
    <div style="margin-bottom: 100px;">
      <v-row
          align="center"
          justify="space-around"
      >
        <v-btn class="primary" @click="fetchGraphData()">Get data for test bar graph</v-btn>
      </v-row>
      <br>

      <v-chart
        class="chart-area"
        :option="optionBar"
      />

      <br>
    </div>
    <h2 style="color: darkred">Evolution report</h2>
    <v-row
        align="center"
        justify="space-around"
    >
      <v-btn class="primary" @click="generateGraph()">Generate evolution graph</v-btn>
    </v-row>
    <div v-if="loading">
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
    </div>
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

  import VChart from 'vue-echarts'

  use([ CanvasRenderer, BarChart, PieChart, LineChart, GridComponent, TooltipComponent ])

export default {
  components: {
    VChart,
  },
  name: "EvolutionOverview",
  mounted() {
    this.dataLoaded = false;
    this.url = "";
  },
  methods: {
    generateGraph: async function () {
      this.loading = true;
      this.dataLoaded = false;
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
        this.dataLoaded = true;
        console.log(res)
        this.imageUrl = res.summary_graph;
        this.pdfUrl = res.summary_pdf.replace(server, "");
      } finally {
        this.loading = false;
      }
    },
    fetchGraphData: async function () {
      this.loading = true;
      this.dataLoaded = false;
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
        this.dataLoaded = true;

        console.log(res)
        this.optionBar.xAxis.data = res.summary_data.map(element => element.program);
        console.log('this.optionBar.xAxis.data', this.optionBar.xAxis.data);
        this.optionBar.series[0].data = res.summary_data.map(element => element.average);
        console.log('this.optionBar.series[0].data', this.optionBar.series[0].data);

        this.imageUrl = res.summary_graph;
        this.pdfUrl = res.summary_pdf.replace(server, "");
      } finally {
        this.loading = false;
      }
    },
    fetchPieData: async function () {
      this.loading = true;
      this.dataLoaded = false;
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
        this.dataLoaded = true;

        console.log(res)
        let programArray = res.summary_data.map(element => element.program);
        console.log('programArray', programArray);
        let averageArray = res.summary_data.map(element => element.average);
        console.log('averageArray', averageArray);
        let areaArray = res.summary_data.map(element => element.area);
        console.log('areaArray', areaArray);
        let combinedArray = averageArray.map(function(x, i) {
          return [x, programArray[i], areaArray[i]]
        });
        console.log('combinedArray', combinedArray);
        let parameters = ["value", "name", "area"];

        this.optionPie.series[0].data = combinedArray.map(function(row) {
          return row.reduce(function(result, field, index) {
            result[parameters[index]] = field;
            return result;
          }, {});
        });
        console.log('this.optionPie.series[0].data', this.optionPie.series[0].data);

        let combinedData = combinedArray.map(function(row) {
          return row.reduce(function(result, field, index) {
            result[parameters[index]] = field;
            return result;
          }, {});

        });

        let groupedAreas = Object.groupBy(combinedData, ({ area }) => area);
        console.log('groupedAreas', groupedAreas);

        this.optionPie.series[0].data = groupedAreas.Plan
        this.optionPie.series[1].data = groupedAreas.Invest
        this.optionPie.series[2].data = groupedAreas.Control
        this.optionPie.series[3].data = groupedAreas.Respond
        this.optionPie.series[4].data = groupedAreas.Enable

        console.log('groupedAreas.Control', groupedAreas.Control);

        this.imageUrl = res.summary_graph;
        this.pdfUrl = res.summary_pdf.replace(server, "");
      } finally {
        this.loading = false;
      }
    }

  },
  data() {
    return {
      loading: false,
      dataLoaded: false,
      imageUrl: "",
      pdfUrl: "",
      optionBar : {
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: { interval: 0, rotate: 60 }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'bar'
          }
        ],
        itemStyle: {
          borderCap: 'round'
        },
        grid: {
          containLabel: true
        }
      },
      optionPie : {
        tooltip: {
          trigger: "item"
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            restore: { show: true },
            saveAsImage: { show: true }
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
              padding: [ 0, 0, 0, 250 ]
            },
            data: [
              { value: 40, name: 'rose 1' },
              { value: 38, name: 'rose 2' },
              { value: 32, name: 'rose 3' },
              { value: 30, name: 'rose 4' },
              { value: 60, name: 'rose 5' },
              { value: 26, name: 'rose 6' },
              { value: 22, name: 'rose 7' },
              { value: 18, name: 'rose 8' }
            ],
            startAngle: 90,
            endAngle: 42.6315789474,
            minAngle: 9.47368421053
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
              padding: [ 0, 0, 0, 250 ]
            },
            data: [
              { value: 40, name: 'rose 1' },
              { value: 38, name: 'rose 2' },
              { value: 32, name: 'rose 3' },
              { value: 30, name: 'rose 4' },
              { value: 60, name: 'rose 5' },
              { value: 26, name: 'rose 6' },
              { value: 22, name: 'rose 7' },
              { value: 18, name: 'rose 8' }
            ],
            startAngle: 42.6315789474,
            endAngle: 326.842105263,
            minAngle: 9.47368421053
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
              padding: [ 0, 0, 0, 250 ]
            },
            data: [
              { value: 40, name: 'rose 1' },
              { value: 38, name: 'rose 2' },
              { value: 32, name: 'rose 3' },
              { value: 30, name: 'rose 4' },
              { value: 60, name: 'rose 5' },
              { value: 26, name: 'rose 6' },
              { value: 22, name: 'rose 7' },
              { value: 18, name: 'rose 8' }
            ],
            startAngle: 326.842105263,
            endAngle: 270,
            minAngle: 9.47368421053
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
              padding: [ 0, 250, 0, 0 ]
            },
            data: [
              { value: 40, name: 'rose 1' },
              { value: 38, name: 'rose 2' },
              { value: 32, name: 'rose 3' },
              { value: 30, name: 'rose 4' },
              { value: 60, name: 'rose 5' },
              { value: 26, name: 'rose 6' },
              { value: 22, name: 'rose 7' },
              { value: 18, name: 'rose 8' }
            ],
            startAngle: 270,
            endAngle: 203.684210526,
            minAngle: 9.47368421053
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
              padding: [ 0, 250, 0, 0 ],
            },
            data: [
              { value: 40, name: 'rose 1' },
              { value: 38, name: 'rose 2' },
              { value: 32, name: 'rose 3' },
              { value: 30, name: 'rose 4' },
              { value: 60, name: 'rose 5' },
              { value: 26, name: 'rose 6' },
              { value: 22, name: 'rose 7' },
              { value: 18, name: 'rose 8' }
            ],
            startAngle: 203.684210526,
            endAngle: 90,
            minAngle: 9.47368421053
          },
          {
            type: 'pie',
            radius: [99.5, 100],
            avoidLabelOverlap: true,
            padAngle: 8,
            itemStyle: {
              borderWidth: 3,
              borderRadius: 5,
              borderColor: '#000',
              borderCap: "square",
              color: '#FFF'
            },
            showEmptyCircle: true,
            label: {
              show: true,
              position: 'inner',
              fontSize: 24,
            //   padding: function(params) {
            //     // Define different padding values for each data point
            //     var paddingValues = [
            //       [0, 0, 0, 10],  // Padding for the first data point
            //       [0, 10, 0, 0],  // Padding for the second data point
            //       [10, 0, 0, 0],  // Padding for the third data point
            //       [0, 0, 10, 0],  // Padding for the fourth data point
            //       [0, 0, 0, 0]    // Padding for the fifth data point
            //     ];
            //     return paddingValues[params.dataIndex] || [0, 0, 0, 0]; // Default to no padding if no value is found
            //   }
            // },
              padding: [0, 0, 0, 0]
            },
            data: [
              { value: 13.1578947368333, name: 'E' },
              { value: 21.052631579, name: 'P' },
              { value: 15.7894736841667, name: 'I' },
              { value: 18.4210526316667, name: 'C' },
              { value: 31.5789473683333, name: 'R' }
            ]
          }
        ]
      }
    }
  }

}
</script>

<style scoped>
  .chart-area {
    padding-top: 5px;
    padding-bottom: 5px;
    position: flex;
    height: 700px;
  }
</style>