<template>
  <div>
    <h2 style="color:darkred">Program description</h2>
    <div v-if="tabs==0">
      <h3 style="color: darkred" >River Basin Planning</h3>
      <v-textarea rows=20 value="River basin plans guide the development, management, allocation, and use of water and related resources within a specific geographical area. Ideally, this is an actual river basin, but in some cases the planning area may be limited due to transboundary constraints or in order to ensure a more tractable planning size. In some countries, a single river basin is simply too large to plan as a single unit, so it is necessary to divide it into sub-basins. River basin plans are typically integrated plans, addressing water quantity, water quality, surface water and groundwater, and the protection of water and aquatic ecosystems while enabling the integration of upstream and downstream interests. Basin plans should also include issues such as institutional responsibilities, implementation arrangements, budgets, and monitoring. It is important that droughts and floods are addressed in a river basin plan as set out in the following paragraphs:                                                                                                                                               •	Basin Drought Planning: A river basin plan should identify the impacts of various drought scenarios and recommend water resources-related mitigation strategies for minimizing drought impacts, including watershed management actions, the need for and location of new infrastructure, reservoir operations, and urban and agricultural water conservation and efficiency, as well as water allocation priorities. As part of, or in parallel to, the river basin management plan, a Basin Drought Contingency Plan should also be prepared that lays out specific actions to be taken at the basin level depending upon the level of drought severity. Those actions could include mandatory conservation measures, reallocation of water supplies, restrictions on agricultural production, different types of urban water use, or changes to reservoir operations. The Basin Drought Contingency Plan should be informed by assessments of risks and of vulnerable populations to help balance objectives and set priorities.

  •	Basin Flood Planning: A river basin management plan should also identify the potential impacts of various flood scenarios and recommend water resources-related mitigation strategies for minimizing flood risk, including watershed management actions, new water resource infrastructure, and protection of floodplains and wetlands as designated retention areas. As discussed in Chapter 10, the river basin management plan should inform land use planning and related decisions with respect to flood risks at the local level. As part of, or in parallel to the Basin Plan, a Basin Flood Contingency Plan should also be prepared. Such a plan should lay out specific actions to be taken depending upon the level of flood severity. Those actions could include emergency operations of reservoirs, decision rules on controlled flooding, and emergency actions such as mobilizing flood-fighting teams and evacuating populations.
    "></v-textarea>
    </div>
    <div v-if="tabs==1">
      <h3 style="color: darkred" >Coastal management planning</h3>
      <v-textarea rows=20 value="More than 600 million people, around 10 percent of the global population, live in coastal areas that are less than 10 meters above sea level (UN 2017). These areas are particularly vulnerable to flooding from storms and the associated storm surges that drive seawater onto coastal flood plains. Coastal zones can also be vulnerable to water shortages and droughts with the additional risk of saline intrusion (and therefore contaminated groundwater) as a result of groundwater over-abstraction. Climate change also directly impacts coastal communities due to rising sea levels and increasing storm frequencies and magnitudes in many areas.

The most comprehensive paradigm for coastal zone management is Integrated Coastal Zone Management (ICZM), a multi-sectoral, stakeholder-informed coastal zone equivalent of river basin planning, which seeks to promote economic development in the coastal zone while also protecting valuable coastal ecosystems. These ecosystems are often important for tourism and fisheries, and act as coastal barriers against storm surges. Unlike river basin planning, ICZM has not been fully mainstreamed into most countries’ planning processes, probably reflecting the complexity of the exercise.

Particularly in countries or coastal areas with extensive deltas, coastal zone planning must of necessity be linked to river basin management planning. That is because the delta represents the terminus of a river basin, where freshwater flows mix with seawater and bring sediments, nutrients, and pollutants that have a profound impact on coastal ecosystems. ICZM is also fundamentally intertwined with marine spatial planning by virtue of common geomorphological dynamics and the ecosystems providing services (such as flood protection) and goods to coastal economies.

Coastal zone management plans provide the overall framework for flood management programs operating in coastal areas and should help inform local flood management plans for jurisdictions located along the coastline. They also help in establishing priorities for investments related to coastal barrier management, including protection and restoration activities, and the prioritization of areas where “hard” coastal defenses such as sea dikes or flood walls may be necessary. Coastal zone management plans rely on information provided by the coastal floodplain mapping programs discussed in Chapter 10, and conversely should also help to prioritize areas for in-depth flood risk mapping.

It is important that coastal zone management plans are used to mainstream flood risk management considerations into the overall development objectives of the coastal zone and to ensure that the planning approach is tailored for the specific circumstances of each coastal stretch. A coastal zone management plan will normally address a variety of technical issues, such as coastal erosion, sea level rise, land subsidence, saltwater intrusion, pollution, management of coastal ecosystems, and coastal risk management associated with storms and tsunamis. The impacts of climate change, including changes in weather and sea levels, should also be considered in the plan to ensure robust and flexible approaches. Like river basin management plans, coastal zone management plans should ideally be updated periodically to adjust to changing circumstances and to incorporate lessons learned.

"></v-textarea>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'ProgramDescription',
  props: ['tabs'],
  methods: {
  },
  data: () => ({
  }),
})
</script>

<style scoped>
</style>
``
