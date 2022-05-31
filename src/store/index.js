import Vue from 'vue'
import Vuex from 'vuex'
import * as util from "@/assets/js/utils";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        selectedAgency: {},
        token: "",
        areas: [],
        groups: [],
        programs: [],
        progress: 0,
        programSelection: new Set(),
        currentProgram: {},
        completedPrograms: new Set(),
        completedAreas: new Set(),
        initialized: false,
    },

    mutations: {
        updateCompletedAreas(state, completedAreas) {
            state.completedAreas.clear();
            completedAreas.forEach(program => {
                state.completedAreas.add(program);
            })
        },
        updateCompletedPrograms(state, completedPrograms) {
            state.completedPrograms.clear();
            completedPrograms.forEach(program => {
                state.completedPrograms.add(program);
            })
        },
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
    actions: {
        async updateProgress(context){
            let totalProgress = 0;
            const completedPrograms = new Set();
            for (let program of context.state.programSelection) {
                const progress = await util.loadProgress(program, context.state.token);
                if (progress === 1) completedPrograms.add(program);
                totalProgress = totalProgress + progress;
            }
            totalProgress = totalProgress / context.state.programSelection.size;
            context.state.progress = (totalProgress * 100).toFixed(0);
            context.commit("updateCompletedPrograms", completedPrograms);
        }
    },
    modules: {}
})
