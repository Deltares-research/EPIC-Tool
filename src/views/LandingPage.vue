<template>
  <v-container fill-height>
    <v-layout row wrap align-center>
      <v-dialog v-model="showDialog" width="900">
        <v-card>
          <v-card-title class="text-h5 grey lighten-2"></v-card-title>
          <v-card-text><span v-html="description"></span></v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="showDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-row align="center" justify="center">
        <v-col md="2">
          <v-card height="100px" :elevation="10" @click="showDescription('background')" style="color: darkred" rounded>
            <v-card-title>Background</v-card-title>
          </v-card>
        </v-col>
        <v-col md="2">
          <v-card height="100px" :elevation="10" :key="update" style="color: darkred">
            <v-card-title>Objective</v-card-title>
          </v-card>
        </v-col>
        <v-col md="2">
          <v-card height="100px" :elevation="10" :key="update" style="color: darkred">
            <v-card-title>Methodology</v-card-title>
          </v-card>
        </v-col>
        <v-col md="2">
          <v-card height="100px" :elevation="10" :key="update" style="color: darkred">
            <v-card-title>Main uses</v-card-title>
          </v-card>
        </v-col>
        <v-col md="2">
          <v-card height="100px" :elevation="10" :key="update" style="color: darkred">
            <v-card-title>Main Audiences</v-card-title>
          </v-card>
        </v-col>
        <v-col md="2">
          <v-card height="100px" :elevation="10" :key="update" style="color: darkred">
            <v-card-title>Help desk and FAQ</v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </v-layout>
  </v-container>
  <!--    <v-card elevation="13">-->
  <!--      <v-card-text>-->
  <!--        <h2 style="color: darkred">Background</h2>-->
  <!--        <p></p>-->
  <!--        <h3>The global flagship report “An EPIC Response: <a-->
  <!--            href="https://openknowledge.worldbank.org/handle/10986/35754">Innovative Governance for Flood and Drought-->
  <!--          Risk Management”</a> was launched in June 2021. The report provides a new perspective on hydro-climatic risks-->
  <!--          by looking at floods and droughts through the same lens. It identifies the roles of different government-->
  <!--          agencies in managing these risks and highlights where and how these agencies need to collaborate. It-->
  <!--          represents the most extensive compendium of flood and drought policies and programs that currently exists in-->
  <!--          the literature. The report audience includes country governments, development agencies, and the international-->
  <!--          flood and drought technical community. Responding to the feedback received by practitioners and knowledge-->
  <!--          partners during the EPIC Response report dissemination phase, this tool operationalizes the content of the-->
  <!--          EPIC Response Framework and helps apply it in specific country contexts with the goal of improving policy-->
  <!--          dialogue and operations.</h3>-->
  <!--        <p></p>-->
  <!--        <h2 style="color: darkred">Objective</h2>-->
  <!--        <p></p>-->
  <!--        <h3>The EPIC Response Assessment Tool aims at supporting clients and practitioners to assess the status of-->
  <!--          hydro-climatic risk management systems and identify areas where program components and the collaboration-->
  <!--          between could be strengthened. This EPIC Response Assessment Tool builds on the EPIC Response Framework-->
  <!--          technical content. This Tool can be used as a framework for having a structured analysis and discussion to-->
  <!--          inform the continuous evolution of flood and drought management systems; ultimately helping to deliver better-->
  <!--          services to communities increase resilience to hydro-climatic risk.</h3>-->
  <!--        <p></p>-->
  <!--        <h2 style="color: darkred">ERAM Main Uses</h2>-->
  <!--        <p></p>-->
  <!--        <h3>The ERAM has the following main uses:</h3>-->
  <!--        <p></p>-->
  <!--        <ul>-->
  <!--          <li>Level 1 Capacity Building: ERAM will be used as a learning support tool to disseminate and operationalize-->
  <!--            the content of the EPIC Response Framework.-->
  <!--          </li>-->
  <!--          <li>Level 2 Sector Level Assessment: ERAM is used as a framework for agencies or sector level specialists to-->
  <!--            understand their role within the EPIC Response Framework and the linkages with other the EPIC Response-->
  <!--            Programs.-->
  <!--          </li>-->
  <!--          <li>Level 3 Country Level Assessment: ERAM is used as a framework for National Government, Agencies or-->
  <!--            Committees to understand, assess and improve their overall national flood and drought risk management-->
  <!--            systems-->
  <!--          </li>-->
  <!--        </ul>-->
  <!--        <p></p>-->
  <!--        <h2 style="color: darkred">ERAM Audiences</h2>-->
  <!--        <p></p>-->
  <!--        <h3>This section describes how different users might interact with the ERAM:</h3>-->
  <!--        <ul>-->
  <!--          <li>Level 1 Technical Practitioners: users will use ERAM as a learning support tool, focusing on some or all-->
  <!--            the programs in the EPIC Response Framework generating a better understanding of their content and-->
  <!--            associated resources.-->
  <!--          </li>-->
  <!--          <li>Level 2 Sector Level Agencies: users will use ERAM as an assessment tool, focusing on those programs-->
  <!--            related to the specific agency (i.e. WRM, DRM, Agriculture, Natural Resources or Hydro-Met) to understand-->
  <!--            their role within the EPIC Response Framework and the linkages with the EPIC Response Programs.-->
  <!--          </li>-->
  <!--          <li>- Level 3 Country Level Agencies: users will use ERAM as an assessment tool, whereby Government and Sector-->
  <!--            Level Agencies go over all the programs of the EPIC Response as a team, to understand, assess and improve-->
  <!--            their overall national flood and drought risk management systems.-->
  <!--          </li>-->
  <!--        </ul>-->
  <!--        <v-row style="margin: 1px">-->
  <!--          <v-col md="3">-->
  <!--          </v-col>-->
  <!--          <v-col md="6">-->
  <!--          </v-col>-->
  <!--          <v-col md="3" class="text-right">-->
  <!--            <v-btn to="SelectProgram" text color="primary" @click="e1 = 2">Select program(s)-->
  <!--              <v-icon>mdi-step-forward</v-icon>-->
  <!--            </v-btn>-->
  <!--          </v-col>-->
  <!--        </v-row>-->
  <!--        <v-row no-gutters>-->
  <!--          <v-col md="5"></v-col>-->
  <!--          <v-col md="2">-->
  <!--          </v-col>-->
  <!--          <v-col md="5"></v-col>-->
  <!--        </v-row>-->
  <!--      </v-card-text>-->
  <!--    </v-card>-->

</template>
<script>
export default {
  name: 'LandingPage',
  data: () => ({
    showDialog: false,
    description: "",
  }),
  methods: {
    showDescription: function (selectedItem) {
      if(selectedItem === 'background'){
        this.description = "The global flagship report “An EPIC Response: <a href=\"https://openknowledge.worldbank.org/handle/10986/35754\">Innovative Governance for Flood and Drought\n" +
            "Risk Management”</a> was launched in June 2021. The report provides a new perspective on hydro-climatic risks\n" +
            "by looking at floods and droughts through the same lens. It identifies the roles of different government\n" +
            "agencies in managing these risks and highlights where and how these agencies need to collaborate. It\n" +
            "represents the most extensive compendium of flood and drought policies and programs that currently exists in\n" +
            "the literature. The report audience includes country governments, development agencies, and the international\n" +
            "flood and drought technical community. Responding to the feedback received by practitioners and knowledge\n" +
            "partners during the EPIC Response report dissemination phase, this tool operationalizes the content of the\n" +
            "EPIC Response Framework and helps apply it in specific country contexts with the goal of improving policy\n" +
            "dialogue and operations."
      }
      this.showDialog = !this.showDialog;
    }
  }
}
</script>

<style scoped>
</style>
``
