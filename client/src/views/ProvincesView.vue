<script setup>
import { onBeforeMount, ref } from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

import { useUserStore } from '@/stores/userStore.js'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const userInfo = storeToRefs(userStore)


const provinces = ref([])
const provinceToAdd = ref({})
const provinceToEdit = ref({})
const provincePictureRef = ref()
const provincePicture = ref()
const provinceAddImageUrl = ref()

const provinceEditPictureRef = ref()
const provinceEditPicture = ref()

const pictureToBig = ref()

const stats = ref({})

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

    await fetchProvinces()
})

//#region CRUD for Provinces
async function fetchProvinces() {
    const r = await axios.get("/api/provinces/")
    provinces.value = r.data
}

async function onProvinceAdd() {
    const formData = new FormData()

    if (provincePicture.value) {
        formData.append('picture', provincePicture.value)
    }
    else {
        formData.append('picture', "")
    }


    formData.set('name', provinceToAdd.value.name)
    formData.set('capital', provinceToAdd.value.capital)
    formData.set('area', provinceToAdd.value.area)
    formData.set('population', provinceToAdd.value.population)

    await axios.post("/api/provinces/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    provinceToAdd.value = {}
    await fetchProvinces()
}

async function onRemoveClickProvince(province) {
    await axios.delete(`/api/provinces/${province.id}/`);
    await fetchProvinces(); // переподтягиваю
}

async function onProvinceEditClick(province) {
    provinceToEdit.value = { ...province };
}

async function onUpdateProvince() {
    const formData = new FormData()

    if (provinceEditPicture.value) {
        formData.append('picture', provinceEditPicture.value)
    }
    else {
        formData.append('picture', "")
    }

    formData.set('name', provinceToEdit.value.name)
    formData.set('capital', provinceToEdit.value.capital)
    formData.set('area', provinceToEdit.value.area)
    formData.set('population', provinceToEdit.value.population)
    formData.set('user', userInfo.value.user_id)

    await axios.put(`/api/provinces/${provinceToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchProvinces();
}

async function provinceAddPictureChange() {
    provincePicture.value = provincePictureRef.value.files[0]
    provinceAddImageUrl.value = URL.createObjectURL(provincePicture.value)
}

async function onRemoveNewPicture(event) {
    event.preventDefault()
    provinceAddImageUrl.value = ""
    provincePicture.value = ""
}

async function provinceEditPictureChange() {
    provinceEditPicture.value = provinceEditPictureRef.value.files[0]
    provinceToEdit.value.picture = URL.createObjectURL(provinceEditPicture.value)
}

async function onRemoveEditPicture(event) {
    event.preventDefault()
    provinceToEdit.value.picture = ""
    provinceEditPicture.value = ""

}

async function onSmallPictureClick(picture) {
    pictureToBig.value = picture
}


async function onStatsModelOpen() {
  const r = await axios.get("/api/provinces/stats")
  stats.value = r.data
}

//#endregion CRUD for Provinces end


</script>

<template>
        <div class="container">
        <!-- провинция -->
        <div class="d-flex justify-content-end">
        <button @click="onStatsModelOpen" data-bs-toggle="modal" data-bs-target="#statsModal" class="btn btn-warning">Статистика</button>
    </div>
        <hr>
        <h5>Провинция</h5>
        <form @submit.prevent.stop="onProvinceAdd">
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="provinceToAdd.name" required />
                        <label for="floatingInput">Название</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="provinceToAdd.capital" required />
                        <label for="floatingInput">Столица</label>
                    </div>
                </div>
                <div class="col-2">
                    <div class="form-floating">
                        <input type="number" class="form-control" v-model="provinceToAdd.population" min="0" required />
                        <label for="floatingInput">Население(чел.)</label>
                    </div>
                </div>
                <div class="col-2">
                    <div class="form-floating">
                        <input type="number" class="form-control" v-model="provinceToAdd.area" min="0" required />
                        <label for="floatingInput">Площадь(кв.км.)</label>
                    </div>
                </div>
                <div class="col-2">
                    <input class="form-control" type="file" ref="provincePictureRef" @change="provinceAddPictureChange">
                </div>
                <div class="col-auto">
                    <button v-if="provincePicture" class="btn btn-danger"
                        style="position: relative; zoom: 0.5; right: -50px; bottom: 35px"
                        @click="onRemoveNewPicture($event)">
                        <i class="bi bi-x"></i>
                    </button>
                    <img :src="provinceAddImageUrl" style="max-height: 60px" alt="">
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary">
                        Добавить
                    </button>
                </div>
            </div>
        </form>
        <br>
        <div class="row" v-for="p in provinces">
            <div class="card mb-3" style="max-width: 100%;">
                <div class="row g-0">
                    <!-- Картинка -->
                    <div class="col-md-3 d-flex align-items-center justify-content-center">
                        <div v-show="p.picture">
                            <img :src="p.picture" class="img-fluid rounded m-2"
                                style="max-width: 300px; cursor: pointer;" @click="onSmallPictureClick(p.picture)"
                                data-bs-toggle="modal" data-bs-target="#bigPictureModal" />
                        </div>
                    </div>
                    <!-- Контент -->
                    <div class="col-md-9">
                        <div class="card-body">
                            <h5 class="card-title mb-1">{{ p.name }}</h5>
                            <p class="card-text mb-2">
                                <strong>Столица:</strong> {{ p.capital }}
                            </p>
                            <p class="card-text mb-2">
                                <strong>Население:</strong> {{ p.population }} чел.
                            </p>
                            <p class="card-text mb-2">
                                <strong>Площадь:</strong> {{ p.area }} кв.км.
                            </p>
                            <!-- Кнопки -->
                            <div v-if="userInfo.isSuperuser.value == true || userInfo.username.value == p.user.username" class="mt-3 d-flex">
                                <button class="btn btn-success me-2" @click="onProvinceEditClick(p)"
                                    data-bs-toggle="modal" data-bs-target="#editProvinceModal">
                                    <i class="bi bi-pencil-fill"></i> Редактировать
                                </button>
                                <button class="btn btn-danger" @click="onRemoveClickProvince(p)">
                                    <i class="bi bi-x"></i> Удалить
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade" id="editProvinceModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">
                            Pедактировать
                        </h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="provinceToEdit.name" />
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="provinceToEdit.capital" required />
                                <label for="floatingInput">Столица</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input type="number" class="form-control" v-model="provinceToEdit.population" min="0"
                                    required />
                                <label for="floatingInput">Население(чел.)</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating">
                                <input type="number" class="form-control" v-model="provinceToEdit.area" min="0"
                                    required />
                                <label for="floatingInput">Площадь(кв.км.)</label>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="form-floating col-auto">
                                <input class="form-control" type="file" ref="provinceEditPictureRef"
                                    @change="provinceEditPictureChange">
                                <label for="floatingInput">Изображение</label>
                            </div>
                            <div class="col-auto">
                                <button v-if="provinceToEdit.picture" class="btn btn-danger"
                                    style="position: relative; zoom: 0.5; left:175px; bottom: 35px"
                                    @click="onRemoveEditPicture($event)">
                                    <i class="bi bi-x"></i>
                                </button>
                                <img :src="provinceToEdit.picture" style="max-height: 60px" alt="">
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateProvince">
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>


        <div class="modal fade" id="bigPictureModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                    </div>
                    <div class="modal-body">
                        <div v-show="pictureToBig">
                            <img :src="pictureToBig" style="width: 100%; object-fit: cover;">
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal fade" id="statsModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="statsModalLabel">Статистика провинций</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <ul class="list-group">
                    <li class="list-group-item">Количество: {{stats.count}}</li>
                    <li class="list-group-item">Максимальная популяция провинции: {{stats.maxPop}} чел.</li>
                    <li class="list-group-item">Минимальная популяция провинции: {{stats.minPop}} чел.</li>
                    <li class="list-group-item">Максимальная площадь провинции: {{stats.maxArea}} кв.км.</li>
                    <li class="list-group-item">Минимальная площадь провинции: {{stats.minArea}} кв.км.</li>
                    </ul>
                </div>
                </div>
            </div>
        </div>        


    </div>
</template>

<style scoped></style>