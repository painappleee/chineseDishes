<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

import Choices from "../assets/choices-en-us.js"

const dishIngridients = ref([])
const dishIngridientToAdd = ref({})
const qntType = Choices.pairs("chineseDishes_dish_ingridient_typeQuantity")
const dishIngridientToEdit = ref({})

const ingridients = ref([])
const dishes = ref([])

onBeforeMount(async () => {
 axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

 await fetchIngridients()
 await fetchDishes()
 await fetchDishIngridients()
})

//#region CRUD for Ingridients
async function fetchIngridients() {
  const r = await axios.get("/api/ingridients/")
  console.log(r.data)
  ingridients.value = r.data
}
//#endregion CRUD for Inrgidients end

//#region CRUD for Dishes
async function fetchDishes() {
  const r = await axios.get("/api/dishes/")
  console.log(r.data)
  dishes.value = r.data
}
//#endregion CRUD for Dishes end

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
  dishIngridientToAdd.value = {}
  await fetchDishIngridients(); 
}

async function onDishIngridientEditClick(dishIngridient) {
  dishIngridientToEdit.value = { ...dishIngridient, dish: dishIngridient.dish.id, ingridient: dishIngridient.ingridient.id};
}

async function onUpdateDishIngridient() {
  await axios.put(`/api/dish_ingridients/${dishIngridientToEdit.value.id}/`, {
    ...dishIngridientToEdit.value,
  });
  await fetchDishIngridients();
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
                <button
                    class="btn btn-success"
                    style="margin-right: 2px;"
                    @click="onDishIngridientEditClick(di)"
                    data-bs-toggle="modal"
                    data-bs-target="#editDishIngridientModal"
                >
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button class="btn btn-danger" @click="onRemoveClickDishIngridient(di)">
                    <i class="bi bi-x"></i>
                </button>
            </div>
            <hr>
        </div>

        <div class="modal fade" id="editDishIngridientModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    {{ dishToEdit }}
                    <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Pедактировать
                    </h1>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                    </div>
                    <div class="modal-body">
                        <div class="row mb-2">
                            <div class="form-floating">
                                <select class="form-select" v-model="dishIngridientToEdit.dish">
                                <option :value="d.id" v-for="d in dishes">
                                    {{ d.name }}
                                </option>
                                </select>
                                <label for="floatingInput">Блюдо</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <select class="form-select" v-model="dishIngridientToEdit.ingridient">
                                <option :value="i.id" v-for="i in ingridients">
                                    {{ i.name }}
                                </option>
                                </select>
                                <label for="floatingInput">Ингридиент</label>
                            </div>
                        </div>                        
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input
                                    type="number"
                                    class="form-control"
                                    v-model="dishIngridientToEdit.quantity"
                                    min = "0"
                                    required
                                />
                                <label for="floatingInput">Количество</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <select class="form-select" v-model="dishIngridientToEdit.typeQuantity" required>
                                <option :value="q.value" v-for="q in qntType">{{ q.label }}</option>
                                </select>
                                <label for="floatingInput">Измерение</label>
                            </div>
                        </div>                        
                    </div>
                    <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-secondary"
                        data-bs-dismiss="modal"
                    >
                        Закрыть
                    </button>
                    <button
                        data-bs-dismiss="modal"
                        type="button"
                        class="btn btn-primary"
                        @click="onUpdateDishIngridient"
                    >
                        Сохранить
                    </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>