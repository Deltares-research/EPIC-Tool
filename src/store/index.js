import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        selectedAgency: {},
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
            if (state.selectedAgency.programs !== undefined) {
                for (const program of state.selectedAgency.programs) {
                    state.programSelection.delete(program.id);
                }
            }
            const alreadySelected = agency.id === state.selectedAgency.id;
            if (alreadySelected) {
                state.selectedAgency = {};
            } else {
                for (const program of agency.programs) {
                    state.programSelection.add(program.id);
                }
                state.selectedAgency = agency;
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
