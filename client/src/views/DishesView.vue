<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

import Choices from "../assets/choices-en-us.js"

const provinces = ref([])

const dishes = ref([])
const dishToAdd = ref({})
const dshCat = Choices.pairs("chineseDishes_dish_category")


onBeforeMount(async () => {
 axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
 
 await fetchProvinces()
 await fetchDishes()
})

//#region CRUD for Provinces
async function fetchProvinces() {
  const r = await axios.get("/api/provinces/")
  console.log(r.data)
  provinces.value = r.data
}
//#endregion CRUD for Provinces end 

//#region CRUD for Dishes
async function fetchDishes() {
  const r = await axios.get("/api/dishes/")
  console.log(r.data)
  dishes.value = r.data
}

async function onDishAdd() {
  console.log(dishToAdd.value)
  await axios.post("/api/dishes/", {
    ...dishToAdd.value,
  });
  await fetchDishes(); // переподтягиваю
}

async function onRemoveClickDish(dish) {
  await axios.delete(`/api/dishes/${dish.id}/`);
  await fetchDishes(); // переподтягиваю
}


//#endregion CRUD for Dishes end
</script>

<template>
<div class="container">  
  <!-- блюдо -->
    <hr>
  <h5>Блюдо</h5>
  <form @submit.prevent.stop="onDishAdd" >
    <div class="row">
      <div class="col-2">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ dishToAdd.name -->
          <input
            type="text"
            class="form-control"
            v-model="dishToAdd.name"
            required
          />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col-4">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ dishToAdd.description -->
          <input
            type="text"
            class="form-control"
            v-model="dishToAdd.description"
            required
          />
          <label for="floatingInput">Описание</label>
        </div>
      </div>
      <div class="col-2">
          <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
        <div class="form-floating">
          <select class="form-select" v-model="dishToAdd.province" required>
            <option :value="p.id" v-for="p in provinces">{{ p.name }}</option>
          </select>
          <label for="floatingInput">Провинция</label>
        </div>
      </div>
      <div class="col-1">
          <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
        <div class="form-floating">
          <select class="form-select" v-model="dishToAdd.category" required>
            <option :value="c.value" v-for="c in dshCat">{{ c.label }}</option>
          </select>
          <label for="floatingInput">Категория</label>
        </div>
      </div>
      <div class="col-2">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ dishToAdd.spice_level -->
          <input
            type="number"
            class="form-control"
            v-model="dishToAdd.spice_level"
            min = "0"
            max = "10"
            required
          />
          <label for="floatingInput">Уровень остроты</label>
        </div>
      </div>
      <div class="col-1">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>
  <hr>
  <div class="row" v-for="d in dishes">
    <div class="col-2" >{{ d.name}}</div>
    <div class="col-4" >{{ d.description }}</div>
    <div class="col-2" >{{ d.province.name }} </div>
    <div class="col-2" >{{ d.category }} </div>
    <div class="col-1" >{{ d.spice_level }} </div>
    <div class="col-1 mb-1">
      <button class="btn btn-danger" @click="onRemoveClickDish(d)">
        <i class="bi bi-x">x</i>
      </button>
    </div>
    <hr>
  </div>
</div>
</template>

<style scoped>
</style>

