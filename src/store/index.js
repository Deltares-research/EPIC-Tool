import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: "",
        areas: [],
        groups: [],
        programs: [],
        programSelection: {},
        currentProgram: {},
        initialized: false,
    },
    mutations: {
        selectProgram(state, programId) {
            const currentSelection = state.programSelection[programId] === undefined ? false : state.programSelection[programId];
            state.programSelection[programId] = !currentSelection;
        },
        init(state) {
            state.initialized = true;
        },
        updateAreas(state, areas) {
            state.areas = areas;
            state.groups = [];
            state.programs = [];
            for (const area of state.areas) {
                for (const group of area.groups) {
                    state.groups.push(group);
                    for (const program of group.programs) {
                        state.programs.push(program);
                    }
                }
            }
            state.programSelection = {};
        },
    },
    actions: {},
    modules: {}
})
