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
          <div class="card-body text-center" style="height: 60px; flex-grow: 0;">
            <h5 class="card-title">{{ r.name }}</h5>
          </div>
          
          <!-- Картинка блюда -->
          <div class="card-img-top d-flex justify-content-center">
            <img :src="r.picture" alt="нет фото" class="img-fluid rounded" style="max-height: 220px; cursor: pointer; ">
          </div>
          
          <!-- Провинция -->
          <div class="card-body pb-0">
            <span class="badge bg-primary">{{ r.province}}</span>
          </div>
          
          <!-- Список ингредиентов -->
          <div class="card-body pt-0" style="flex-grow: 1;">
            <ul class="list-unstyled">
              <li v-for="ingredient in r.ingridients" class="d-flex justify-content-between">
                <strong>{{ ingredient.ingridient }}</strong>
                <div class="dots"></div>
                {{ ingredient.quantity }}{{ ingredient.typeQuantity }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>
  

<style scoped>
.dots {
  flex-grow: 1;  /* Заполняет всё пространство между элементами */
  background: url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5ZHgc-sDZ9f5ETYh9OZQoEACKH5GbuZa8Vg&s) repeat-x center;
  background-size: 7px 7px;  /* Задаём размер точки */
  margin-top: 10px;
  margin-left: 3px;
  margin-right: 3px;
}
</style>
