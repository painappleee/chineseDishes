<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const provinces = ref([])
const provinceToAdd = ref({})
const provinceToEdit = ref({})

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
  provinceToAdd.value = {}
  await fetchProvinces(); // переподтягиваю
}

async function onRemoveClickProvince(province) {
  await axios.delete(`/api/provinces/${province.id}/`);
  await fetchProvinces(); // переподтягиваю
}

async function onProvinceEditClick(province) {
  provinceToEdit.value = { ...province};
}

async function onUpdateProvince() {
  await axios.put(`/api/provinces/${provinceToEdit.value.id}/`, {
    ...provinceToEdit.value,
  });
  await fetchProvinces();
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
                <button
                    class="btn btn-success"
                    style="margin-right: 2px;"
                    @click="onProvinceEditClick(p)"
                    data-bs-toggle="modal"
                    data-bs-target="#editProvinceModal"
                >
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button class="btn btn-danger" @click="onRemoveClickProvince(p)">
                    <i class="bi bi-x"></i>
                </button>
            </div>
            <hr>
        </div>

        <div class="modal fade" id="editProvinceModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    {{ provinceToEdit }}
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
                                <input
                                type="text"
                                class="form-control"
                                v-model="provinceToEdit.name"
                                />
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input
                                type="text"
                                class="form-control"
                                v-model="provinceToEdit.capital"
                                required
                                />
                                <label for="floatingInput">Столица</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input
                                type="number"
                                class="form-control"
                                v-model="provinceToEdit.population"
                                min = "0"
                                required
                                />
                                <label for="floatingInput">Население(чел.)</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input
                                type="number"
                                class="form-control"
                                v-model="provinceToEdit.area"
                                min = "0"
                                required
                                />
                                <label for="floatingInput">Площадь(кв.км.)</label>
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
                        @click="onUpdateProvince"
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