<template>
  <landing-page/>
</template>

<script lang="ts">
  import Vue from 'vue'
  import HelloWorld from '../components/HelloWorld.vue'
  import LandingPage from "@/components/LandingPage.vue";

  export default Vue.extend({
    name: 'Home',

    components: {
      LandingPage,
    },
  })
</script>
