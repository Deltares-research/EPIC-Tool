import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        selectedAgencies: new Set(),
        token: "",
        areas: [],
        groups: [],
        programs: [],
        programSelection: new Set(),
        currentProgram: {},
        initialized: false,
    },
    mutations: {
        toggleAgencySelection(state, agency) {
            let alreadySelected = state.selectedAgencies.has(agency.id);
            if (alreadySelected) {
                state.selectedAgencies.delete(agency.id);
            } else {
                state.selectedAgencies.add(agency.id);
            }
            for (const program of agency.programs) {
                alreadySelected ? state.programSelection.delete(program.id) : state.programSelection.add(program.id);
            }
        },
        select(state, programId) {
            state.programSelection.add(programId);
        },
        toggleSelection(state, programId) {
            if (state.programSelection.has(programId)) {
                state.programSelection.delete(programId);
            } else {
                state.programSelection.add(programId);
            }
        },
        init(state) {
            state.initialized = true;
        },
        updateAreas(state, areas) {
            areas.sort((a, b) => a.id - b.id);
            state.areas = areas;
            state.groups = [];
            state.programs = [];
            for (const area of state.areas) {
                for (const group of area.groups) {
                    group.area = area.id;
                    state.groups.push(group);
                    for (const program of group.programs) {
                        program.group = group.id;
                        program.area = area.id;
                        state.programs.push(program);
                    }
                }
            }
            state.programSelection = new Set();
        },
    },
    actions: {},
    modules: {}
})
