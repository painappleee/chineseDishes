import { createRouter, createWebHistory } from 'vue-router'

import DishesView from '../views/DishesView.vue'
import ProvincesView from '@/views/ProvincesView.vue'
import IngridientsView from '@/views/IngridientsView.vue'
import Dish_IngridientsView from '@/views/Dish_IngridientsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "DishesView",
      component: DishesView
    },
    {
      path: "/provinces",
      name: "ProvincesView",
      component: ProvincesView
    },
    {
      path: "/ingridients",
      name: "IngridientsView",
      component: IngridientsView
    },
    {
      path: "/dish_ingridients",
      name: "DishIngridientsView",
      component: Dish_IngridientsView
    }

  ]
})

export default router
