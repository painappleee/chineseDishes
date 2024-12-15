<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

const provinces = ref([])
const provinceToAdd = ref({})
const provinceToEdit = ref({})
const provincePictureRef = ref()
const provincePicture = ref()
const provinceAddImageUrl = ref()

const provinceEditPictureRef = ref()
const provinceEditPicture = ref() 

const pictureToBig = ref()

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

    if (provincePicture.value){
        formData.append('picture', provincePicture.value)
    }
    else {
         formData.append('picture',"")
    }


    formData.set('name', provinceToAdd.value.name)
    formData.set('capital', provinceToAdd.value.capital)
    formData.set('area', provinceToAdd.value.area)
    formData.set('population', provinceToAdd.value.population)

    await axios.post("/api/provinces/", formData, {
    headers:{
        'Content-Type' : 'multipart/form-data'      
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
  provinceToEdit.value = { ...province};
}

async function onUpdateProvince() {
    const formData = new FormData() 

    if (provinceEditPicture.value){
        formData.append('picture',provinceEditPicture.value)
    } 
    else {
         formData.append('picture',"")
    }

    formData.set('name', provinceToEdit.value.name)
    formData.set('capital', provinceToEdit.value.capital)
    formData.set('area', provinceToEdit.value.area)
    formData.set('population', provinceToEdit.value.population)

  await axios.put(`/api/provinces/${provinceToEdit.value.id}/`, formData, {
    headers:{
        'Content-Type' : 'multipart/form-data'      
    }
  });
  await fetchProvinces();
}

async function provinceAddPictureChange() 
{
  provincePicture.value = provincePictureRef.value.files[0]
  provinceAddImageUrl.value = URL.createObjectURL(provincePicture.value)    
}

async function onRemoveNewPicture(event) {
  event.preventDefault()
  provinceAddImageUrl.value = ""
  provincePicture.value = "" 
}

async function provinceEditPictureChange() 
{
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
            <div class="col-2">
                <input class="form-control" type="file" ref="provincePictureRef" @change="provinceAddPictureChange">
            </div>
            <div class="col-auto">
                <button v-if="provincePicture" class="btn btn-danger" style="position: relative; zoom: 0.5; left:175px; bottom: 35px" @click="onRemoveNewPicture($event)">
                    <i class="bi bi-x"></i>
                </button>
                <img :src = "provinceAddImageUrl" style="max-height: 60px"  alt="">
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
            <div class="col-2" >{{ p.name}}</div>
            <div class="col-2" >{{ p.capital }}</div>
            <div class="col-2" >{{ p.population}} чел.</div>
            <div class="col-auto" >{{ p.area }} кв.км.</div>
            <div class="col-auto m-2">
                <div v-show="p.picture" >
                    <img :src="p.picture" style="max-height: 60px "  @click="onSmallPictureClick(p.picture)" 
                    data-bs-toggle="modal" data-bs-target="#bigPictureModal" >
                </div>
            </div>
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
                        <div class="row mb-2">
                            <div class="form-floating col-auto">
                                <input class="form-control" type="file" ref="provinceEditPictureRef" @change="provinceEditPictureChange">
                                <label for="floatingInput">Изображение</label>
                            </div>
                            <div class="col-auto">
                                <button v-if="provinceToEdit.picture" class="btn btn-danger" style="position: relative; zoom: 0.5; left:175px; bottom: 35px" @click="onRemoveEditPicture($event)">
                                    <i class="bi bi-x"></i>
                                </button>
                                <img :src = "provinceToEdit.picture" style="max-height: 60px"  alt="">
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
    

        <div class="modal fade" id="bigPictureModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                    </div>
                    <div class="modal-body">
                        <div v-show="pictureToBig" >
                            <img :src="pictureToBig" style="width: 100%; object-fit: cover;" >
                        </div>
                    </div>
                </div>
            </div>
        </div>


    </div>
</template>

<style scoped>

</style>