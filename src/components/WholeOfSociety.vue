<template>
  <div>
    <h2 style="color: darkred">Whole-of-Society</h2>
    <h3 style="color: darkred">River Basin Planning</h3>
    <v-row>
      <v-col md="2" v-for="(item,index) in this.titles" :key="item">
        <v-card>
          <v-card-title>{{ item }}</v-card-title>
          <v-card-actions>
            <v-btn color="gray lighten-2" text>Show description</v-btn>
            <v-spacer></v-spacer>
            <v-btn icon @click="switchShow(index)">
              <v-icon>{{ showLocal[index] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-card-actions>
          <v-expand-transition>
            <div v-show="showLocal[index]">
              <v-divider></v-divider>
              <v-card-text>{{ text[index] }}</v-card-text>
            </div>
          </v-expand-transition>
        </v-card>
      </v-col>
      <v-col md="2">
      </v-col>
    </v-row>
    <br>
    <v-textarea rows=4 :value="explanation[page-1]" readonly outlined></v-textarea>
    <v-row>
      <v-col md="8">
        <v-textarea rows=1 value="Is this element present in your Program ?" readonly outlined></v-textarea>
      </v-col>
      <v-col md="4">
        <v-select :items="items" filled label="Select yes or no"></v-select>
      </v-col>
    </v-row>
    <h3>Please elaborate</h3>
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
export default {
  name: "WholeOfSociety.vue",
  methods: {
    switchShow: function (index) {
      this.$set(this.showLocal,index,!this.showLocal[index])
    }
  },
  data: () => ({
    items: ['Yes', 'No'],
    titles: ['Local Governments', 'Public Participation', 'Social Inclusion', 'Education and Risk Communication', 'Scientific Collaboration', 'Open Information'],
    text: ['Local governments are the indispensable associates of national agencies in hydro-climatic risk management. For every program in the Framework, local governments are key stakeholders, and for many programs, local governments play a critical role in program implementation. National agencies should work in partnership with local governments, and as appropriate, assist them through capacity development, technical assistance, or grant funding. National agencies can also support legal and regulatory reforms that devolve an appropriate level of authority and responsibility to local governments.', 'The aim is to encourage the public and stakeholders to have meaningful input not only on program design and implementation (such as participation in river basin planning or social protection programs), but also in the overall public policy process to monitor, evaluate, and improve the performance of the program. Agencies should have dedicated public outreach staff who should work closely with technical staff to ensure meaningful participation.\n', 'Socially excluded individuals or groups—which could consist of women, ethnic or religious minorities, the poor, the elderly, people with disabilities, or other groups—are typically the most vulnerable to hydro-climatic risks. Agencies need to have dedicated social units that are trained and that preferably consist of staff from marginalized groups to help ensure social inclusion. Agencies should also have structured processes for ensuring social inclusion, including undertaking steps to identify and understand who these individuals and groups are, and then targeting efforts to ensure that these individuals or groups can benefit from hydro-climatic risk management programs. \n', 'Ensuring broad understanding of flood and drought risks at all levels of society helps people to make better informed decisions to enhance their climate resilience. That, in turn, helps ensure public safety, protect livelihoods, and safeguard assets. Agencies should have dedicated programs to promote education among the general public, along with targeted campaigns to provide flood and drought risk information to relevant stakeholders.\n', 'In addition to collaborating across national agencies, governments also need to collaborate with the scientific community, tapping into both scientific organizations and private sector technical expertise. The goal should be to have both science-informed policy and policy-informed science. There is also a need for more integrative and transdisciplinary hydro-climatic research that can feed into the policy-making process. Agencies should have a reserved budget for collaboration with the scientific community, including undertaking joint research projects when appropriate.\n', 'Information that governments produce, collect, or pay for acts as the currency for hydro-climatic risk management. Examples include geographical information, data collected from remote sensing and monitoring networks, or reports from publicly funded research projects. Access to this information will help agencies perform their tasks and collaborate with each other, enhance scientific research, and enable citizens to better engage in the public policy process. National governments can adopt legislation that requires open access to public information, and agencies should develop regulations to ensure the most appropriate manner of making their information available to serve the public interest\n', ''],
    showLocal: [false, false, false, false, false, false],
    page: 1,
    explanation: [
      "Highlight the importance of the core social dimensions in sector laws: " +
      "The laws governing the different programs in the EPIC Response Framework should highlight the importance of key elements for facilitating a whole-of-society approach, including public participation, social inclusion, education, communication, scientific collaboration, and open data. These elements should also be incorporated into the national strategic planning exercises for WRM, DRM, and Drought. National Strategic Plans provide opportunities to analyze how effectively these elements are being implemented and to identify actions for improvement.\n",
      "National Open Data Law or Policy: Since open data is a cross-government issue, there should ideally be a general open data law or policy providing general principles for improving public access to information. The law or policy should designate a lead agency or organization, for example a science agency, to provide guidelines to help sectoral agencies develop their own specific open data programs. The lead agency could also help establish cross-agency information platforms by creating standards for GIS, databases, and interagency data exchanges.\n",
      "Establish and maintain a public engagement or social unit: There should be a dedicated unit in the agency in the form of a department or office that is responsible for ensuring that the core social dimensions of local government liaison, public participation, social inclusion, education, and communication are mainstreamed into the agency operations. The unit should be sufficiently staffed with social and communication experts to meet the specific agency needs. Ideally, the unit should have staff from marginalized groups that the agency needs to involve, for example indigenous groups, ethnic minorities, or women. The agency should also strive to have representation from marginalized groups throughout the organization through an equal employment opportunity program. The agency might also benefit from including a community engagement help desk that citizens can have access to any time to obtain information, and to voice suggestions or grievances.\n"
    ],
  }),
}
</script>

<style scoped>

</style>
