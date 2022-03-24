<template>
  <div>
    <h2 style="color:darkred">Answers</h2>
    <br>
    <h3>Create, Read, Update or Delete answers</h3>
    <h4>answers</h4>
    <v-row style="margin: 1px">
      <v-col md="3">id</v-col>
      <v-col md="3">short answer</v-col>
      <v-col md="3">long answer</v-col>
      <v-col md="2">
      </v-col>
    </v-row>
    <v-row style="margin: 1px" v-for="answer in this.answers" :key="answer.id">
      <v-col md="3">{{ answer.id }}</v-col>
      <v-col md="3">{{ answer.long_answer }}</v-col>
      <v-col md="3">{{ answer.long_answer }}</v-col>
      <v-col md="3">
        <v-btn @click="deleteAnswer(answer.id)">Delete</v-btn>
      </v-col>
      <v-col md="2">
      </v-col>
    </v-row>
    <h3>add a new answer</h3>
    <v-row>
      <v-col md="3">
        <v-text-field label="short answer" v-model="new_short_answer"></v-text-field>
      </v-col>
      <v-col md="6">
        <v-text-field label="long answer" v-model="new_lang_answer"></v-text-field>
      </v-col>
      <v-col md="3">
        <v-btn @click="addAnswer">Add</v-btn>
      </v-col>
    </v-row>

  </div>
</template>
<script>

export default {
  name: 'Answers',
  async mounted() {
    await this.loadAnswers();
  },
  data() {
    return {
      answers: [],
      new_short_answer: null,
      new_lang_answer: null,
    }
  },
  methods: {
    addAnswer: async function () {
      let answer = {};
      answer.short_answer = this.new_short_answer;
      answer.long_answer = this.new_lang_answer;
      const putMethod = {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(answer),
      }
      let url = 'http://localhost:8000/answer/';
      await fetch(url, putMethod);
      await this.loadAnswers();
    },
    deleteAnswer: async function (id) {
      const deleteMethod = {
        method: 'DELETE',
      }
      let url = 'http://localhost:8000/answer/' + id;
      await fetch(url, deleteMethod);
      await this.loadAnswers();
    },
    loadAnswers: async function () {
      let rawData = await fetch('http://localhost:8000/answer/?format=json', {mode: 'cors'});
      this.answers = await rawData.json();
      console.log(this.answers)
    }
  },
  components: {}
}
</script>

