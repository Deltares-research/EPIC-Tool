import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

export default new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        token: "",
        areas: [],
        groups: [],
        programs: [],
        currentProgramId: 0,
        initialized: false,
        selectedProgram: "",
    },
    getters: {
        getGroupsForArea: (state) => (areaId) => {
            let groups = [];
            for (let group of state.groups) {
                if (group.areaId !== areaId) continue;
                groups.push(group);
            }
            return groups;
        },
        getProgramsForGroup: (state) => (groupId) => {
            let programs = [];
            for (let program of state.programs) {
                if (program.groupId !== groupId) continue;
                programs.push(program);
            }
            return programs;
        },
    },
    mutations: {
        selectProgram(state, programId) {
            let program = state.programs.find(program => program.id === programId);
            program.selected = !program.selected;
        },
        init(state) {
            state.initialized = true;
        },
        updateAreas(state, areas) {
            state.areas = areas;
        },
        updateGroups(state, groups) {
            state.groups = groups;
        },
        updatePrograms(state, programs) {
            state.programs = programs;
        }
    },
    actions: {},
    modules: {}
})
