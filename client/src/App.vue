<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

import Choices from "./assets/choices-en-us.js"
 
onBeforeMount(()=>{
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
})

const loading = ref()

const provinces = ref([])
const provinceToAdd = ref({})

const dishes = ref([])
const dishToAdd = ref({})
const dshCat = Choices.pairs("chineseDishes_dish_category")

const ingridients = ref([])
const ingridientToAdd = ref({})
const ingrCat =  Choices.pairs("chineseDishes_ingridient_category")

const dishIngridients = ref([])
const dishIngridientToAdd = ref({})
const qntType = Choices.pairs("chineseDishes_dish_ingridient_typeQuantity")

async function onLoadClick() {
  await fetchDishIngridients()
}

onBeforeMount(async () => {
 await fetchProvinces()
 await fetchDishes()
 await fetchIngridients()
 await fetchDishIngridients()
})

//#region CRUD for Provinces
async function fetchProvinces() {
  loading.value = true
  const r = await axios.get("/api/provinces/")
  console.log(r.data)
  provinces.value = r.data
  loading.value = false
}

async function onProvinceAdd() {
  console.log(provinceToAdd.value)
  await axios.post("/api/provinces/", {
    ...provinceToAdd.value,
  });
  await fetchProvinces(); // переподтягиваю
}

async function onRemoveClickProvince(province) {
  await axios.delete(`/api/provinces/${province.id}/`);
  await fetchProvinces(); // переподтягиваю
}
//#endregion CRUD for Provinces end 

//#region CRUD for Dishes
async function fetchDishes() {
  loading.value = true
  const r = await axios.get("/api/dishes/")
  console.log(r.data)
  dishes.value = r.data
  loading.value = false
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

//#region CRUD for Ingridients
async function fetchIngridients() {
  loading.value = true
  const r = await axios.get("/api/ingridients/")
  console.log(r.data)
  ingridients.value = r.data
  loading.value = false
}

async function onIngridientAdd() {
  console.log(ingridientToAdd.value)
  await axios.post("/api/ingridients/", {
    ...ingridientToAdd.value,
  });
  await fetchIngridients(); // переподтягиваю
}

async function onRemoveClickIngridient(ingridient) {
  await axios.delete(`/api/ingridients/${ingridient.id}/`);
  await fetchIngridients(); // переподтягиваю
}
//#endregion CRUD for Inrgidients end

//#region CRUD for DishIngridients
async function fetchDishIngridients() {
  loading.value = true
  const r = await axios.get("/api/dish_ingridients/")
  console.log(r.data)
  dishIngridients.value = r.data
  loading.value = false
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
<div class="container-fluid">
  <!-- провинция -->
  <hr>
  <h5>Провинция</h5>
  <form @submit.prevent.stop="onProvinceAdd" >
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ provinceToAdd.name -->
          <input
            type="text"
            class="form-control"
            v-model="provinceToAdd.name"
            required
          />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ provinceToAdd.description -->
          <input
            type="text"
            class="form-control"
            v-model="provinceToAdd.capital"
            required
          />
          <label for="floatingInput">Столица</label>
        </div>
      </div>
      <div class="col-2">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ dishToAdd.populationn -->
          <input
            type="number"
            class="form-control"
            v-model="provinceToAdd.population"
            min = "0"
            required
          />
          <label for="floatingInput">Население(чел.)</label>
        </div>
      </div>
      <div class="col-2">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ dishToAdd.area -->
          <input
            type="number"
            class="form-control"
            v-model="provinceToAdd.area"
            min = "0"
            required
          />
          <label for="floatingInput">Площадь(кв.км.)</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

  <div class="row" v-for="p in provinces">
    <div class="col-4" >{{ p.name}}</div>
    <div class="col-3" >{{ p.capital }}</div>
    <div class="col-2" >{{ p.population}} чел.</div>
    <div class="col-2" >{{ p.area }} кв.км.</div>
    <div class="col-1 mb-1">
      <button class="btn btn-danger" @click="onRemoveClickProvince(p)">
        <i class="bi bi-x">x</i>
      </button>
    </div>
  </div>

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
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

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
  </div>

  <!-- ингридиент -->
  <hr>
  <h5>Ингридиент</h5>
  <form @submit.prevent.stop="onIngridientAdd" >
    <div class="row">
      <div class="col-7">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ ingridientToAdd.name -->
          <input
            type="text"
            class="form-control"
            v-model="ingridientToAdd.name"
            required
          />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col-4">
          <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
        <div class="form-floating">
          <select class="form-select" v-model="ingridientToAdd.category" required>
            <option :value="c.value" v-for="c in ingrCat">{{ c.label }}</option>
          </select>
          <label for="floatingInput">Категория</label>
        </div>
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

  <div class="row" v-for="i in ingridients">
    <div class="col-7" >{{ i.name}}</div>
    <div class="col-4" >{{ i.category }}</div>
    <div class="col-1 mb-1">
      <button class="btn btn-danger" @click="onRemoveClickIngridient(i)">
        <i class="bi bi-x">x</i>
      </button>
    </div>
  </div>

  <!-- блюдо-ингридиент -->
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
  </div>
  <hr>

</div>
</template>

<style scoped>
</style>

