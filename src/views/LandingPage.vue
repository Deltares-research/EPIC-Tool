<template>
  <div>
    <v-card elevation="13">
      <v-card-text>
        <h2 style="color: darkred">Background</h2>
        <p></p>
        <h3>The global flagship report “An EPIC Response: <a
            href="https://openknowledge.worldbank.org/handle/10986/35754">Innovative Governance for Flood and Drought
          Risk Management”</a> was launched in June 2021. The report provides a new perspective on hydro-climatic risks
          by looking at floods and droughts through the same lens. It identifies the roles of different government
          agencies in managing these risks and highlights where and how these agencies need to collaborate. It
          represents the most extensive compendium of flood and drought policies and programs that currently exists in
          the literature. The report audience includes country governments, development agencies, and the international
          flood and drought technical community. Responding to the feedback received by practitioners and knowledge
          partners during the EPIC Response report dissemination phase, this tool operationalizes the content of the
          EPIC Response Framework and helps apply it in specific country contexts with the goal of improving policy
          dialogue and operations.</h3>
        <p></p>
        <h2 style="color: darkred">Objective</h2>
        <p></p>
        <h3>The EPIC Response Assessment Tool aims at supporting clients and practitioners to assess the status of
          hydro-climatic risk management systems and identify areas where program components and the collaboration
          between could be strengthened. This EPIC Response Assessment Tool builds on the EPIC Response Framework
          technical content. This Tool can be used as a framework for having a structured analysis and discussion to
          inform the continuous evolution of flood and drought management systems; ultimately helping to deliver better
          services to communities increase resilience to hydro-climatic risk.</h3>
        <p></p>
        <h2 style="color: darkred">ERAM Main Uses</h2>
        <p></p>
        <h3>The ERAM has the following main uses:</h3>
        <p></p>
        <ul>
          <li>Level 1 Capacity Building: ERAM will be used as a learning support tool to disseminate and operationalize
            the content of the EPIC Response Framework.
          </li>
          <li>Level 2 Sector Level Assessment: ERAM is used as a framework for agencies or sector level specialists to
            understand their role within the EPIC Response Framework and the linkages with other the EPIC Response
            Programs.
          </li>
          <li>Level 3 Country Level Assessment: ERAM is used as a framework for National Government, Agencies or
            Committees to understand, assess and improve their overall national flood and drought risk management
            systems
          </li>
        </ul>
        <p></p>
        <h2 style="color: darkred">ERAM Audiences</h2>
        <p></p>
        <h3>This section describes how different users might interact with the ERAM:</h3>
        <ul>
          <li>Level 1 Technical Practitioners: users will use ERAM as a learning support tool, focusing on some or all
            the programs in the EPIC Response Framework generating a better understanding of their content and
            associated resources.
          </li>
          <li>Level 2 Sector Level Agencies: users will use ERAM as an assessment tool, focusing on those programs
            related to the specific agency (i.e. WRM, DRM, Agriculture, Natural Resources or Hydro-Met) to understand
            their role within the EPIC Response Framework and the linkages with the EPIC Response Programs.
          </li>
          <li>- Level 3 Country Level Agencies: users will use ERAM as an assessment tool, whereby Government and Sector
            Level Agencies go over all the programs of the EPIC Response as a team, to understand, assess and improve
            their overall national flood and drought risk management systems.
          </li>
        </ul>
        <v-row style="margin: 1px">
          <v-col md="3">
          </v-col>
          <v-col md="6">
            <v-img
                src="../../public/arrow.png"
            ></v-img>
          </v-col>
          <v-col md="3" class="text-right">
            <v-btn to="SelectProgram" text color="primary" @click="e1 = 2">Select program(s)
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
          <v-col md="5"></v-col>
        </v-row>
      </v-card-text>
    </v-card>

  </div>
</template>
<script>
export default {
  name: 'LandingPage',
  data: () => ({}),
}
</script>

<style scoped>
</style>
``
