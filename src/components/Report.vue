<template>
  <div v-if="this.questions!==undefined">
    <div v-for="(question,index) in this.questions" :key="index">
      <v-card elevation="12" outlined>
        <v-card-title style="color: darkred">{{ question.name }}</v-card-title>
        <v-card-text>
          <div v-for="(question,index) in question.questions" :key="index">
            <div v-if="question.question_answers.summary.Strongly_disagree !== undefined">
              <br>
              <h3 style="color: darkred">Question</h3>
              <h3>{{ question.title }}</h3>
              <br>
              <h3 style="color: cornflowerblue">Answers</h3>
              <div v-for="(answer,index) in question.question_answers.answers" :key="index">
                <h5>{{ getAnswer(answer.selected_choice) }}</h5>
                <h5>{{ answer.justify_answer }}</h5>
                <br>
              </div>
              <h3 style="color: cornflowerblue">Summary</h3>
              <h5>Strongly disagree: {{ question.question_answers.summary.Strongly_disagree }}</h5>
              <h5>Disagree: {{ question.question_answers.summary.Disagree }}</h5>
              <h5>Disagree nor agree: {{ question.question_answers.summary.Neither_agree_nor_disagree }}</h5>
              <h5>Agree: {{ question.question_answers.summary.Agree }}</h5>
              <h5>Strongly agree: {{ question.question_answers.summary.Strongly_agree }}</h5>
            </div>
          </div>
        </v-card-text>
      </v-card>
      <br>
    </div>
  </div>
</template>

<script>
export default {
  name: "Report.vue",
  props: {
    questions: undefined,
  },
  methods: {
    getAnswer(choice) {
      if (choice === "STRONGLYDISAGREE") {
        return "Strongly disagree";
      }
      if (choice === "DISAGREE") {
        return "Disagree";
      }
      if (choice === "NEITHERAGREENORDISAGREE") {
        return "Neither agree nor disagree";
      }
      if (choice === "AGREE") {
        return "Agree";
      }
      if (choice === "STRONGLYAGREE") {
        return "Strongly agree";
      }
    },

  },
}
</script>

<style scoped>

</style>