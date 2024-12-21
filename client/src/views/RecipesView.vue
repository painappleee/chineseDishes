<script setup>
import { onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const recipes = ref()

async function fetchRecipes() {
  const r = await axios.get("/api/recipes/get")
  recipes.value = r.data
}

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

  fetchRecipes()
})
</script>

<template>
   <div class="container">
    <hr>
    <div class="row ms-3">
      <div class="col-md-auto mb-4" v-for="r in recipes">
        <div class="card" style="width: 18rem; min-height: 450px">
          <!-- Название блюда -->
          <div class="card-body text-center" style="height: 80px; flex-grow: 0;">
            <h5 class="card-title">{{ r.name }}</h5>
          </div>
          
          <!-- Картинка блюда -->
          <div class="card-img-top d-flex justify-content-center">
            <img :src="r.picture" alt="нет фото" class="img-fluid rounded" style="max-height: 220px; cursor: pointer; ">
          </div>
          
          <!-- Провинция -->
          <div class="card-body">
            <span class="badge bg-primary">{{ r.province}}</span>
          </div>
          
          <!-- Список ингредиентов -->
          <div class="card-body" style="flex-grow: 1;">
            <ul class="list-unstyled">
              <li v-for="ingredient in r.ingridients">
                <strong>{{ ingredient.ingridient }}</strong> - {{ ingredient.quantity }} {{ ingredient.typeQuantity }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>
  

<style scoped></style>
