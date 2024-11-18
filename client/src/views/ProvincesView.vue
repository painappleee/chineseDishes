<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const provinces = ref([])
const provinceToAdd = ref({})

onBeforeMount(async () => {
 axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

 await fetchProvinces()
})

//#region CRUD for Provinces
async function fetchProvinces() {
  const r = await axios.get("/api/provinces/")
  console.log(r.data)
  provinces.value = r.data
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


</script>

<template>
    <div class="container">
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
        <hr>
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
            <hr>
        </div>
    </div>
</template>

<style scoped>

</style>