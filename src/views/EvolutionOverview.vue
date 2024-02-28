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
        let combinedArray = averageArray.map(function(x, i) {
          return [x, programArray[i]]
        });
        console.log('combinedArray', combinedArray);
        let parameters = ["value", "name"];
        this.optionPie.series[0].data = combinedArray.map(function(row) {
          return row.reduce(function(result, field, index) {
            result[parameters[index]] = field;
            return result;
          }, {});
        });
        console.log('this.optionPie.series[0].data', this.optionPie.series[0].data);

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
            name: 'Nightingale Chart',
            type: 'pie',
            radius: [60, 300],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: {
              borderWidth: 15,
              borderRadius: 5,
              borderColor: '#FFF',
              borderCap: "square"
            },
            selectedMode: 'single',
            selectedOffset: '30',
            showEmptyCircle: true,
            data: []
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