<template>
  <div>
    <h2 style="color: darkred">Linkage with National Frameworks</h2>
    <h3 style="color: darkred">{{title}}</h3>
    <v-textarea rows=4 :value="explanation[page-1]" readonly outlined></v-textarea>
    <v-row>
      <v-col md="8">
        <v-textarea rows=1 :value="questions[page-1]" readonly outlined></v-textarea>
      </v-col>
      <v-col md="4">
        <v-select
            :items="items"
            filled
            label="Select yes or no"
        ></v-select>
      </v-col>
    </v-row>
    <h3>Please justify your answer</h3>
    <v-textarea rows=5 outlined></v-textarea>
    <v-row>
      <v-col md="4">
      </v-col>
      <v-col md="1">
        <v-btn color="info" @click="page--">Previous question</v-btn>
      </v-col>
      <v-col md="1"></v-col>
      <v-col md="1">
        <v-btn color="info" @click="page++">Next question</v-btn>
      </v-col>
    </v-row>
    <br/>
    <br/>
    <br/>
    <h5>{{ page }} of 3 questions</h5>
    <br/>
    <br/>
  </div>
</template>
<script>
import Vue from 'vue'

export default Vue.extend({
  name: 'NationalFrameworks',
  methods: {},
  mounted() {
    let program = this.$store.state.currentProgram;
    this.title = program.name;
  },
  data: () => ({
    items: ['Yes', 'No'],
    title: "",
    page: 1,
    explanation: [
      "The preparation and periodic revision (at say five-year intervals) of a river basin management plan is typically required by the water resources law. Such a law will also typically specify the minimum content of river basin management plans and their legal relationship with other relevant plans (such as which has priority). It also will specify the plans’ role in the implementation of the water resources law itself, for example in the setting of priorities and decisions on water allocation as discussed in more detail below.",
      "The water resources law will also typically set out the procedure for the development of river basin management plans, which given their cross-cutting nature should involve broad stakeholder consultation including with agencies responsible for elements of the hydro-climatic risk framework. The law will also typically specify who is to adopt such a plan.",
      "Water resources laws typically require the plans to be approved at a high level through adoption by the government (the cabinet) or by the high-level inter-ministerial body (if one exists), such as a national water council or a national water resources committee. Such a requirement should enable the effective participation of agencies involved in hydro-climatic risk management, particularly as regards the elements of primary concern to them (such as industry, agriculture, power generation, and environment)"
    ],
    questions: [
      "Does the Water Law require the preparation and describes the minimal content of basin management plans?",
      "Does the Water Law set up the procedure and main responsibility for the development of river basin management plans?",
      "Does the Water Law require high level approval of the basin management plan?"
    ]
  }),

})
</script>

<style scoped>
</style>
``
