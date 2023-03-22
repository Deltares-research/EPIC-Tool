<template>
  <div>
    <v-dialog v-model="showDialog">
      <v-container fluid>
        <v-card color="grey lighten-2" style="padding: 20px" v-if="selectedGroup==='methodology'">
          <v-card-title class="text-h5 grey lighten-2"></v-card-title>
          <div v-if="selectedItem==='use'">
            <h3>In which ways can ERAM be used?</h3>
            ERAM can be used at the national level and at the sector agency level, as a framework to analyze and inform
            the continuous evolution of programs and the inter-agency collaboration required for the combined management
            of flood and drought.
            The ERAM has the following main uses:
            - Level 1 Capacity Building: ERAM will be used as a learning support tool to disseminate and operationalize
            the content of the EPIC Response Framework.
            - Level 2 Sector Level Assessment: ERAM is used as a framework for agencies or sector level specialists to
            understand their role within the EPIC Response Framework and the linkages with other the EPIC Response
            Programs.
            - Level 3 Country Level Assessment: ERAM is used as a framework for National Government, Agencies or
            Committees to understand, assess and improve their overall national flood and drought risk management
            systems

          </div>
          <div v-if="selectedItem==='audience'">
            <h3>What are the ERAM Main Audiences?</h3>
            This section describes how different users might interact with the ERAM:
            - Level 1 Technical Practitioners: users will use ERAM as a learning support tool, focusing on some or all
            the programs in the EPIC Response Framework generating a better understanding of their content and
            associated resources.
            - Level 2 Sector Level Agencies: users will use ERAM as an assessment tool, focusing on those programs
            related to the specific agency (i.e. WRM, DRM, Agriculture, Natural Resources or Hydro-Met) to understand
            their role within the EPIC Response Framework and the linkages with the EPIC Response Programs.
            - Level 3 Country Level Agencies: users will use ERAM as an assessment tool, whereby Government and Sector
            Level Agencies go over all the programs of the EPIC Response as a team, to understand, assess and improve
            their overall national flood and drought risk management systems.

          </div>
          <div v-if="selectedItem==='methodology'">
            <h3>Methodology</h3>
            The ERAM tool will systematically take users through the EPIC Response 43 programs grouped in the following
            five principles:
            - Enabling environment of policies, laws, agencies, climate science, information and participation of all
            segments of society, especially those more vulnerable.
            - Planning at multiple nested geographical level to ensure that flood and drought management are integrated
            and prioritized
            - Investing in healthy watersheds and green and grey water infrastructure to reduce flood and drought
            hazards
            - Controlling surface and groundwater use and floodplain development to reduce exposure and minimize
            vulnerabilities, and
            - Responding better to floods and droughts through continuously improved monitoring, response and recovery
            programs.
            The tool groups and pre-selects programs by agency – Water resources management, disaster risk management,
            hydrological and meteorological services, natural resources management, agriculture, social protection and
            finance. Based on this original pre-selection, the user can choose which programs apply to his/her agency.
            The tool is designed to walk the users through a series of steps to systematically look into the following
            aspects per program:
            <br>
            <br>
            <table>
              <th>Program aspects</th>
              <th>Users action</th>
              <tr>
                <td>Program description. This is a general overview highlighting key elements of an effective program
                  based on global experience. Each program is presented in a stylized manner, generally representing
                  global best practice. Most countries are currently not able to implement fully effective programs but
                  describing the key elements of a fully effective program, allows for a better appreciation of gaps,
                  constraints, and opportunities, which can then be addressed in the context of specific countries.
                </td>
                <td>Read the content.</td>
              </tr>
              <tr>
                <td>Linkage to sectoral frameworks. Each program in the Framework is authorized through national
                  legislation, typically tied to a specific sector, such as WRM, DRM, hydro-met, agriculture, natural
                  resources, social protection, and finance. The premise is that a well-developed sectoral framework is
                  necessary but not sufficient condition for an effective program.
                </td>
                <td>Evaluate the status of the program with respect to the description of linkages to sectoral
                  frameworks provided. The tool will pose a question and the user will respond by:
                  - Selecting one option of the drop-down menu
                  - Providing a written response to the question
                </td>
              </tr>
              <tr>
                <td>Key agency actions. This section provides a list of important functions that the responsible sector
                  agency should undertake to ensure an effective program. Many countries have well-developed national
                  legislation, but implementation may be lacking at the agency level. The list is meant to be
                  illustrative, but also serves as a guide to help assess the status of program implementation.
                </td>
                <td>Evaluate the status of the program with respect to the description of key agency action provided.
                  The tool will pose a question and the user will respond by:
                  - Selecting one option of the drop-down menu
                  - Providing a written response to the question
                </td>
              </tr>
              <tr>
                <td>Generic program evolution. Recognizing that program development is an evolutionary process, four
                  levels are described for each program. The general categories are summarized in Table 1 and can be
                  used to help evaluate program status.
                </td>
                <td>Evaluate the status of the program with respect to the generic program evolution, by selecting one
                  of the descriptions.
                </td>
              </tr>
              <tr>
                <td>Key references. Given the breadth of the EPIC Response programs, it is not possible review each
                  program in depth. Thus, each program includes references which provide more detailed information.
                </td>
                <td>Read the content.</td>
              </tr>
            </table>
          </div>
          <div v-if="selectedItem==='produce'">
            <h3>What kind of information will ERAM produce</h3>
            The tool will compile all users answers into a report including visual representations. The report will
            include
            the aggregated user responses highlighting the levels of development of the EPIC Response programs, the
            status of the
            linkages to national frameworks and key agency actions, as well as areas where users see value in
            strengthening collaboration
            between programs. The ERAM report can be used to facilitate a policy dialogue to help generate a common
            understanding of the status,
            challenges, and opportunities for enhancing flood and drought risk management systems.
          </div>
          <div v-if="selectedItem==='terminology'">
            <h3>Key Terminology </h3>
            <b>National sector framework</b> refers to national level laws, agencies, strategic plans, and policies
            pertaining to a specific sector. Law is used to mean a set of laws, acts, or codes adopted by the
            legislature (such as the national assembly or parliament) on a topic (such as WRM, DRM, or drought
            management). It also refers to a decree or formal decision relating to a program adopted at a high executive
            level (for example, by the president) above the level of the agency responsible for that program.
            <br>
            <br>
            <b>Agency</b> is used in a generic sense to mean the government or public entity that is responsible for the
            implementation of a law or a program. Such an entity could be a ministry, a department within a ministry, or
            a specialized agency or authority. For example, depending on the country, the WRM agency could be the
            ministry of water resources, a water resources department in another ministry (such as a ministry of natural
            resources) or a semi-autonomous water resources management agency.
            <br>
            <br>
            <b>Program</b> is a continuous set of activities undertaken by a national agency, authorized through
            national legislation with well-defined objectives, and funded by the national government. Regulations and
            technical guidelines are issued by the responsible sector agency to help implement specific programs.
            Regulations create legal rules that are legally binding while technical guidelines are not. Regulations and
            technical guidelines address technical issues such as procedures, standards, and incentives. They may apply
            to local or sub-national governments, businesses, or individuals, and may, in certain circumstances, apply
            to national other agencies.
            <br>
            <br>
            <b>National strategic plan</b> helps direct and coordinate the medium-term goals and objectives of a sector.
            The development of national strategic plans often follows the process of reviewing sector performance and
            proposing adjustments to the policies, laws, interagency collaboration, programs, regulations, or funding to
            ensure continuous advancement. A national strategic plan does not necessarily mandate actions or make
            project-specific recommendations, but rather provides a roadmap for policy makers and agencies to make
            program adjustments and to appropriate the necessary funds.
            <br>
            <br>
            <b>Policy</b> is used in a broad sense to refer to important decisions taken by the government in the
            formulation of laws, agencies, national strategic plans, programs, regulations, and guidelines. In some
            cases, there may also be standalone policy documents (such as a water policy) which provide overarching sets
            of principles and establish general plans of action.

          </div>
          <div v-if="selectedItem==='appliance'">
            <h3>Can ERAM be applied to Federal and Transboundary systems?</h3>
            The concept of a national framework can be complicated in countries with federal constitutions or
            transboundary water resources. In order to simplify the analysis, the ERAM will assume a unitary government
            system, with only national and local government levels. Federal and transboundary systems and add another
            level of complexity to interagency collaboration as national agencies need to interact with transboundary,
            federal and local agencies. The ERAM has been applied to federal systems with positive results. However,
            although in general terms the same EPIC Response principles can be extrapolated, more analysis is needed to
            fully operationalize ERAM to federal and transboundary system.
            In some federal countries, for example, WRM is entirely a state or province level responsibility. Elsewhere,
            the reach of the federal legislature may extend to interstate rivers. Alternatively, the constitution may
            recognize the fact that water resources do not recognize internal boundaries and provide that WRM is a
            federal responsibility. In some federal countries, the jurisdiction of the federal government over aspects
            of WRM has emerged from a broader environmental competence or, in a transboundary context, as a result of
            federal authority over international relations. However, even if the federal legislature lacks the authority
            or competence to legislate on WRM or DRM in terms of flood and drought risk management, this does
            necessarily mean that the federal government is precluded from adopting policies on the topic or of funding
            programs that may be implemented at a state or province level
            At the international level, the scope for developing and implementing water resources transboundary
            frameworks will depend on the existence of an international agreement relating to the concerned
            transboundary river basin, and on the mandate of the relevant river basin organization or commission.
            Priority program activities will typically focus on the collection and sharing, on a mutual basis, of
            information in the context of routine hydro-met data as well as flood and drought warning mechanisms.
            Thereafter, programs will more likely tend to focus on matters that have more evident transboundary
            implications in terms of planning, risk assessment, infrastructure, and water allocation (including
            navigation). Depending on the scope of different programs, commitments made at the international level may
            need to be implemented through the adoption of national laws.

          </div>

          <br>
          <br>
          <v-row class="text-center">
            <v-col md="2" class="d-flex justify-center ">
              <v-card height="100px" :elevation="10" @click="showDescription('use')"
                      class="cards d-flex justify-center align-center grey lighten-1 outlined"
                      rounded outlined>
                <v-card-title>Use of ERAM</v-card-title>
              </v-card>
            </v-col>
            <v-col md="2" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('audience')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Audiences</v-card-title>
              </v-card>
            </v-col>
            <v-col md="2" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('methodology')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Methodology</v-card-title>
              </v-card>
            </v-col>

            <v-col md="2" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('produce')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Information produced</v-card-title>
              </v-card>
            </v-col>
            <v-col md="2" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('terminology')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Key terminology</v-card-title>
              </v-card>
            </v-col>
            <v-col md="2" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('appliance')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Appliance of ERAM</v-card-title>
              </v-card>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="showDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
        <v-card color="grey lighten-2" style="padding: 20px" v-if="selectedGroup==='introducing'">
          <v-card-title class="text-h5 grey lighten-2"></v-card-title>
          <div v-if="selectedItem==='background'">
            <h3>Background</h3>
            The global flagship report “An EPIC Response: <a
              href='https://openknowledge.worldbank.org/handle/10986/35754'>Innovative Governance for Flood and Drought
            Risk Management</a>
            was launched in June 2021. The report provides a new perspective on hydro-climatic risks
            by looking at floods and droughts through the same lens. It identifies the roles of different government
            agencies in managing these risks and highlights where and how these agencies need to collaborate. It
            represents the most extensive compendium of flood and drought policies and programs that currently exists in
            the literature. The report audience includes country governments, development agencies, and the
            international
            flood and drought technical community. Responding to the feedback received by practitioners and knowledge
            partners during the EPIC Response report dissemination phase, this tool operationalizes the content of the
            EPIC Response Framework and helps apply it in specific country contexts with the goal of improving policy
            dialogue and operations.
          </div>
          <div v-if="selectedItem==='framework'">
            <h3>What is the EPIC Response Framework? </h3>
            The EPIC Response Framework provides a new perspective for the combined management of floods and droughts.
            The EPIC Response Framework:
            • Identifies the main government programs with a mandate in flood and drought management
            • Highlights how government programs evolve in time, and
            • The main linkages between the agencies implementing those programs.
          </div>
          <div v-if="selectedItem==='methodology'">
            <h3>What is the EPIC Response Assessment Methodology? </h3>
            The ERAM aims at supporting clients and practitioners to assess the status of hydro-climatic risk management
            systems and
            identify areas where program components and the collaboration between could be strengthened. This EPIC
            Response Assessment
            Tool builds on the EPIC Response Framework technical content.
          </div>
          <div v-if="selectedItem==='why'">
            <h3>Why using the ERAM?</h3>
            Floods and droughts are some of the most tangible – and devastating – consequences of the climate crisis.
            They increasingly affect communities across the planet. The toll in human suffering and in economic costs is
            staggering. It is crucial that societies adapt and that governments prioritize, accelerate, and scale up
            their response mechanisms in the coming decade.
            Floods and drought have traditionally managed separately. Yet there is a growing body of literature that
            looks at both the positive outcomes of managing both risks combined as well as the negative often unintended
            consequences the managing one hazard has on the other. The ERAM can be useful for government and sector
            agencies to break silos and generate a joined-up government response, that allows the government to work as
            a unit and present one unified front to the communities they serve. This joined-up government can in turn
            play a leading role in guiding a whole-of-society effort to manage floods and drought, bringing local
            government, the private sector, civil society, the scientific community and vulnerable communities.
            The EPIC Response Framework has the potential to not only reduce the toll in human suffering from
            increasingly severe floods and droughts, but also to bring significant economic benefits

          </div>
          <br>
          <br>
          <v-row class="text-center">
            <v-col md="3" class="d-flex justify-center ">
              <v-card height="100px" :elevation="10" @click="showDescription('background')"
                      class="cards d-flex justify-center align-center grey lighten-1 outlined"
                      rounded outlined>
                <v-card-title>Background</v-card-title>
              </v-card>
            </v-col>
            <v-col md="3" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('framework')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Framework</v-card-title>
              </v-card>
            </v-col>
            <v-col md="3" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('methodology')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Methodology</v-card-title>
              </v-card>
            </v-col>
            <v-col md="3" class="d-flex justify-center">
              <v-card height="100px" :elevation="10" @click="showDescription('why')"
                      class="cards d-flex justify-center grey lighten-1 "
                      rounded outlined>
                <v-card-title>Why using ERAM?</v-card-title>
              </v-card>
            </v-col>
          </v-row>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="showDialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-dialog>
    <v-container fluid class="background">
      <v-row>
        <v-col md="12" class="d-flex justify-center">
          <v-card height="300px" width="1200px" :elevation="10"
                  class="cards"
                  rounded outlined>
            <div style="text-align: left;padding: 3px">
              <h2>About the EPIC Response Framework:</h2>
              <br>
              <h4>The EPIC Response Framework is an innovative governance approach for the combined management of floods
                and drought.</h4>
              <h4>For more information on the EPIC Response Program please visit <a
                  href="https://www.deltares.nl/en/news/floods-and-droughts-an-epic-response-to-these-hazards-in-the-era-of-climate-change/">here</a>
              </h4>
              <h4>The EPIC Response Assessment Methodology (ERAM) portal offers a step wise approach to assess the
                status of hydro-climatic risk management systems and identify areas where floods and drought management
                programs and the collaboration between them could be strengthened.</h4>
              <h4>The ERAM can be used by practitioners, by sector agencies, and/or at the national level.</h4>
              <h4>Please look at the methodology section for a more in-depth information on the use of ERAM.</h4>
              <br>
              <h4>For technical question please contact: Ana Nunez Sanchez – ana.nunezsanchez@deltares.nl</h4>
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-row class="text-center">
        <v-col md="6" class="d-flex justify-center" style="padding-top: 200px">
          <v-card height="100px" width="400px" :elevation="10" @click="showPanel('introducing')"
                  class="cards d-flex justi fy-center align-center"
                  rounded outlined>
            <v-card-title>Introducing ERAM</v-card-title>
          </v-card>
        </v-col>
        <v-col md="6" class="d-flex justify-center" style="padding-top: 200px">
          <v-card height="100px" width="400px" :elevation="10" @click="showPanel('methodology')"
                  class="cards d-flex justify-center"
                  rounded outlined>
            <v-card-title>ERAM Methodology</v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>

export default {
  components: {
  },

  name: 'LandingPage',
  data: () => ({
    showDialog: false,
    selectedItem: "",
    selectedGroup: "",
  }),
  methods: {
    showPanel: function (selectedGroup) {
      this.selectedItem = selectedGroup === 'introducing' ? 'background' : 'use';
      this.selectedGroup = selectedGroup;
      this.showDialog = true;
    },
    showDescription: function (selectedItem) {
      this.selectedItem = selectedItem;
    }
  }
}
</script>

<style scoped>
.background {
  background-image: url("../assets/back.png");
  background-size: cover;
  height: 95vh;
  width: 100vw;

}

table, th, td {
  border: 1px solid black;
  padding: 3px;
}

.cards {
  color: darkred;
  background-color: white;
  text-align: center;
  opacity: 80%;
}
</style>
``
