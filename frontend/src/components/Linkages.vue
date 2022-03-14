<template>
  <div>
    <h2 style="color:darkred">Linkages</h2>
    <h3 style="color: darkred">River Basin Planning</h3>
    <br>
    <h3>Please select three programs that will help you deliver better results in your program if you could have better collaboration? </h3>
    <br>
    <v-card :elevation="2"
            color="blue-grey lighten-4">
      <v-container fluid class="fill-height">
        <v-row no-gutters>
          <v-col md="3"><h3><span style="color: darkred">E</span>nable</h3></v-col>
          <v-col md="9">
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>National Sectoral Frameworks</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Whole-of-Society Approach</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Hydrological and Meteorological Services</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card elevation="2" color="blue-grey lighten-4">
      <v-container fluid class="fill-height">
        <v-row no-gutters>
          <v-col md="3"><h3><span style="color: darkred">P</span>lan</h3></v-col>
          <v-col md="6">
            <v-list-item-group
            >
              <v-list-item dense>
                <v-list-item-content>
                  <v-list-item-title>Flood and Drought Risk Mitigation and Contingency Planning
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-col>
          <v-col md="3">
            <v-list-item-group v-model="selectedItem">
              <v-list-item dense @click="selectProgram">
                <v-list-item-action>
                  <v-checkbox :input-value="active"></v-checkbox>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>Integrated River Basin Planning</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item dense>
                <v-list-item-action>
                  <v-checkbox :input-value="active"></v-checkbox>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>Coastal Zone Management Planning</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item dense>
                <v-list-item-action>
                  <v-checkbox :input-value="active"></v-checkbox>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>Irrigation Water Supply Planning</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item dense>
                <v-list-item-action>
                  <v-checkbox :input-value="active"></v-checkbox>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>Local Flood Risk Mitigation Planning</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card elevation="2" color="blue-grey lighten-4">
      <v-container fluid class="fill-height">
        <v-row no-gutters>
          <v-col md="3"><h3><span style="color: darkred">I</span>nvest</h3></v-col>
          <v-col md="9">
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Healthy Watersheds</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Water Resources Infrastructure</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card elevation="2" color="blue-grey lighten-4">
      <v-container fluid class="fill-height">
        <v-row no-gutters>
          <v-col md="3"><h3><span style="color: darkred">C</span>ontrol</h3></v-col>
          <v-col md="9">
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Water Allocation and Groundwater Management</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Floodplain Management</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
    <v-card elevation="2" color="blue-grey lighten-4">
      <v-container fluid class="fill-height">
        <v-row no-gutters>
          <v-col md="3"><h3 style="color: darkred">RESPOND</h3></v-col>
          <v-col md="9">
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Drought Monitoring, Response and Recovery</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Flood Monitoring, Response and Recovery</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense>
              <v-list-item-content>
                <v-list-item-title>Disaster Risk Financing</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </div>

</template>
<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'SelectProgram',
  data: () => ({
    items: [
      {title: 'Integrated River Basin Planning'},
      {title: 'Coastal Zone Management Planning'},
      {title: 'Urban Water Supply Planning'},
      {title: 'Irrigation Water Supply Planning'},
      {title: 'Local Flood Risk Mitigation Planning'},
    ],
    selectedItem: {}
  }),
})
</script>

<style scoped>

.active {
  color: black;
  background-color: darkorange;
}

.v-card {
  transition: opacity .4s ease-in-out;
}

.v-card:not(.on-hover) {
  opacity: 0.6;
}

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
</style>
``
