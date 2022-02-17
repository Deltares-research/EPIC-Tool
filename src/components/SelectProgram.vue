<template>
  <div>
    <h2 style="color:darkred">Program selection</h2>
    <br>
    <h3>Please select 1 or more programs</h3>
    <br>
    <v-card :elevation="2" color="blue-grey lighten-4">
      <v-container fluid class="fill-height">
        <v-row no-gutters>
          <v-col md="3"><h3><span style="color: darkred">E</span>nable</h3></v-col>
          <v-col md="3">
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
          <v-col md="3">
            <v-list-item-group>
              <v-list-item dense>
                <v-list-item-content>
                  <v-list-item-title>Flood and Drought Risk Mitigation and Contingency Planning
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-col>
          <v-col md="4">
            <v-list-item-group v-model="selectedItem">
              <v-list-item dense>
                <v-list-item-action>
                  <v-checkbox :input-value="active"></v-checkbox>
                </v-list-item-action>
                <v-list-item-content>Integrated River Basin Planning Policy</v-list-item-content>
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
          <v-col md="2">
            <v-list-item-group v-model="selectedItem">
              <v-list-item dense>
                <v-list-item-content>
                  <v-dialog v-model="dialog" width="500">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn color="blue-grey lighten-3"  v-bind="attrs" v-on="on">Program description</v-btn>
                    </template>
                    <v-card>
                      <v-card-title class="text-h5 grey lighten-2">Integrated River Basin Planning Policy</v-card-title>
                      <v-card-text>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
                        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
                        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
                        voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
                        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                      </v-card-text>
                      <v-divider></v-divider>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="dialog = false">Close</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>

                </v-list-item-content>
              </v-list-item>
              <v-list-item dense>
              </v-list-item>
              <v-list-item dense>
              </v-list-item>
              <v-list-item dense>
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
    <v-row style="margin: 1px">
      <v-col md="5"></v-col>
      <v-col md="2">
        <v-btn to="HelloWorld" color="primary" style="align-content: center">Continue</v-btn>
      </v-col>
    </v-row>
  </div>

</template>
<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'SelectProgram',
  data: () => ({
    dialog: false,
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
