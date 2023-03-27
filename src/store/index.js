import Vue from 'vue'
import Vuex from 'vuex'
import * as util from "@/assets/js/utils";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        selectedAgency: {},
        advisor: false,
        token: "",
        areas: [],
        groups: [],
        programs: [],
        progress: 0,
        remainingQuestions: 0,
        remainingTime: 0,
        programSelection: new Set(),
        currentProgram: {},
        completedPrograms: new Set(),
        unCompleteAreas: new Set(),
        unCompleteGroups: new Set(),
        initialized: false,
    },

    mutations: {
        updateCurrentProgram(state, program) {
            state.currentProgram = program;
        },
        updateUnCompletedGroups(state, unCompletedGroups) {
            state.unCompleteGroups.clear();
            unCompletedGroups.forEach(group => {
                state.unCompleteGroups.add(group)
            })
        },
        updateUnCompletedAreas(state, unCompletedAreas) {
            state.unCompleteAreas.clear();
            unCompletedAreas.forEach(area => {
                state.unCompleteAreas.add(area)
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
            for (let area of areas) {
                area.groups.sort((a, b) => a.id - b.id)
                for (let group of area.groups) {
                    group.programs.sort((a, b) => a.id - b.id)
                }
            }
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
        async updateProgress(context) {
            let totalProgress = 0;
            const completedPrograms = new Set();
            let unansweredQuestions = 0;
            let uncompleteGroups = new Set();
            let uncompleteAreas = new Set();
            for (let programId of context.state.programSelection) {
                const response = await util.loadProgress(programId, context.state.token);
                if (response.progress === 1) {
                    completedPrograms.add(programId);
                } else {
                    const program = context.state.programs.filter(program => program.id === programId);
                    const group = context.state.groups.filter(group => group.id === program[0].group);
                    uncompleteAreas.add(group[0].area);
                    uncompleteGroups.add(program[0].group);
                }
                totalProgress = totalProgress + response.progress;
                unansweredQuestions = unansweredQuestions + (1 - response.progress) * response.questions_answers.length;
            }
            totalProgress = totalProgress / context.state.programSelection.size;
            context.state.progress = (totalProgress * 100).toFixed(0);
            context.state.remainingQuestions = Math.round(unansweredQuestions);
            context.state.remainingTime = Math.round(unansweredQuestions / 3);
            context.commit("updateCompletedPrograms", completedPrograms);
            context.commit("updateUnCompletedGroups", uncompleteGroups);
            context.commit("updateUnCompletedAreas", uncompleteAreas);
        }
    },
    modules: {}
})
