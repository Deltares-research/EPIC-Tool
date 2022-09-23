import Vue from 'vue'
import VueRouter from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import SelectProgram from "@/views/SelectProgram";
import Questionnaire from "@/views/Questionnaire";
import EndPage from "@/views/EndPage";
import Answers from "@/views/Answers";
import LoginPage from "@/views/LoginPage";
import LinkagesOverview from "@/views/LinkagesOverview";
import store from '@/store';
import EvolutionOverview from "@/views/EvolutionOverview";  //or use a full path to ./store

Vue.use(VueRouter)

Vue.use(VueRouter)

const routes = [
    {
        path: '/EvolutionOverview',
        name: 'EvolutionOverview',
        component: EvolutionOverview
    },
    {
        path: '/LinkagesOverview',
        name: 'LinkagesOverview',
        component: LinkagesOverview
    },
    {
        path: '/LoginPage',
        name: 'LoginPage',
        component: LoginPage
    },
    {
        path: '/Answers',
        name: 'Answers',
        component: Answers
    },
    {
        path: '/EndPage',
        name: 'EndPage',
        component: EndPage
    },
    {
        path: '/Questionnaire',
        name: 'Questionnaire',
        component: Questionnaire
    },
    {
        path: '/',
        name: 'LandingPage',
        component: LandingPage
    }, {
        path: '/SelectProgram',
        name: 'SelectProgram',
        component: SelectProgram
    }
]

const router = new VueRouter({
    routes
})

router.beforeEach((to,from,next) => {
    if(store.state.token==="" && to.name !== "LoginPage"){
       next("/LoginPage");
    }
    next();
});

export default router
