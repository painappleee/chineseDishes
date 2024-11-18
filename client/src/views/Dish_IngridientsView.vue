<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

import Choices from "../assets/choices-en-us.js"

const dishIngridients = ref([])
const dishIngridientToAdd = ref({})
const qntType = Choices.pairs("chineseDishes_dish_ingridient_typeQuantity")

const ingridients = ref([])

onBeforeMount(async () => {
 axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

 await fetchIngridients()
 await fetchDishIngridients()
})

//#region CRUD for Ingridients
async function fetchIngridients() {
  const r = await axios.get("/api/ingridients/")
  console.log(r.data)
  ingridients.value = r.data
}
//#endregion CRUD for Inrgidients end

//#region CRUD for DishIngridients
async function fetchDishIngridients() {
  const r = await axios.get("/api/dish_ingridients/")
  console.log(r.data)
  dishIngridients.value = r.data
}
async function onRemoveClickDishIngridient(dishIngridient) {
  await axios.delete(`/api/dish_ingridients/${dishIngridient.id}/`);
  await fetchDishIngridients(); // переподтягиваю
}
async function onDishIngridientAdd() {
  console.log(dishIngridientToAdd.value)
  await axios.post("/api/dish_ingridients/", {
    ...dishIngridientToAdd.value,
  });
  await fetchDishIngridients(); // переподтягиваю
}
//#endregion CRUD for DishIngridients end
</script>

<template>
    <div class="container">
        <hr>
        <h5>Блюдо-ингридиент</h5>
        <form @submit.prevent.stop="onDishIngridientAdd" >
            <div class="row">
            <div class="col-3">
                <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
                <div class="form-floating">
                <select class="form-select" v-model="dishIngridientToAdd.dish" required>
                    <option :value="d.id" v-for="d in dishes">{{ d.name }}</option>
                </select>
                <label for="floatingInput">Блюдо</label>
                </div>
            </div>
            <div class="col-3">
                <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
                <div class="form-floating">
                <select class="form-select" v-model="dishIngridientToAdd.ingridient" required>
                    <option :value="i.id" v-for="i in ingridients">{{ i.name }}</option>
                </select>
                <label for="floatingInput">Ингридиент</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                <!-- ТУТ ПОДКЛЮЧИЛ dishIngridientToAdd.quantity -->
                <input
                    type="number"
                    class="form-control"
                    v-model="dishIngridientToAdd.quantity"
                    min = "0"
                    required
                />
                <label for="floatingInput">Количество</label>
                </div>
            </div>
            
            <div class="col-2">
                <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
                <div class="form-floating">
                <select class="form-select" v-model="dishIngridientToAdd.typeQuantity" required>
                    <option :value="q.value" v-for="q in qntType">{{ q.label }}</option>
                </select>
                <label for="floatingInput">Измерение</label>
                </div>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">
                Добавить
                </button>
            </div>
            </div>
        </form>
        <hr>
        <div class="row" v-for="di in dishIngridients">
            <div class="col-4" >{{ di.dish.name}}</div>
            <div class="col-4" >{{ di.ingridient.name}}</div>
            <div class="col-2" >{{ di.quantity }}</div>
            <div class="col-1" >{{ di.typeQuantity }}</div>
            <div class="col-1 mb-1">
            <button class="btn btn-danger" @click="onRemoveClickDishIngridient(di)">
                <i class="bi bi-x">x</i>
            </button>
            </div>
            <hr>
        </div>
    </div>
</template>

<style scoped>

</style>