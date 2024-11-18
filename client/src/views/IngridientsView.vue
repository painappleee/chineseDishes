<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

import Choices from "../assets/choices-en-us.js"

onBeforeMount(async () => {
 axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

 await fetchIngridients()
})

const ingridients = ref([])
const ingridientToAdd = ref({})
const ingrCat =  Choices.pairs("chineseDishes_ingridient_category")


//#region CRUD for Ingridients
async function fetchIngridients() {
  const r = await axios.get("/api/ingridients/")
  console.log(r.data)
  ingridients.value = r.data
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
</script>

<template>
    <div class="container">
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
            <div class="col-1">
                <button class="btn btn-primary">
                Добавить
                </button>
            </div>
            </div>
        </form>
        <hr>
        <div class="row" v-for="i in ingridients">
            <div class="col-7" >{{ i.name}}</div>
            <div class="col-4" >{{ i.category }}</div>
            <div class="col-1 mb-1">
            <button class="btn btn-danger" @click="onRemoveClickIngridient(i)">
                <i class="bi bi-x">x</i>
            </button>
            </div>
            <hr>
        </div>
    </div>
</template>

<style scoped>

</style>