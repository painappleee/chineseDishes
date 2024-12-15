<script setup>
import {onBeforeMount, ref} from 'vue'
import axios from "axios"
import Cookies from 'js-cookie'

import Choices from "../assets/choices-en-us.js"

const provinces = ref([])

const dishes = ref([])
const dishToAdd = ref({})
const dshCat = Choices.pairs("chineseDishes_dish_category")
const dishToEdit = ref({})
const dishesPictureRef = ref()
const dishPicture = ref()
const dishAddImageUrl = ref()

const dishEditPictureRef = ref()
const dishEditPicture = ref() 

const pictureToBig = ref()

onBeforeMount(async () => {
 axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
 
 await fetchProvinces()
 await fetchDishes()
})

//#region CRUD for Provinces
async function fetchProvinces() {
  const r = await axios.get("/api/provinces/")
  provinces.value = r.data
}
//#endregion CRUD for Provinces end 

//#region CRUD for Dishes
async function fetchDishes() {
  const r = await axios.get("/api/dishes/")
  dishes.value = r.data
}

async function onDishAdd() {

  const formData = new FormData() 

  if (dishPicture.value){
    formData.append('picture', dishPicture.value)
  }
  else{
    formData.append('picture', "")
  }  

  formData.set('name', dishToAdd.value.name)
  formData.set('description', dishToAdd.value.description)
  formData.set("province", dishToAdd.value.province)
  formData.set("category", dishToAdd.value.category)
  formData.set("spice_level", dishToAdd.value.spice_level)


  await axios.post("/api/dishes/", formData, {
    headers:{
      'Content-Type' : 'multipart/form-data'      
    }
  }) 
  await fetchDishes()  
}

async function onRemoveClickDish(dish) {
  await axios.delete(`/api/dishes/${dish.id}/`) 
  await fetchDishes()  
}

async function onDishEditClick(dish) {
  dishToEdit.value = { ...dish, province: dish.province.id } 
}

async function onUpdateDish() {
  console.log("gvfdhbjsfknlma;,")
  const formData = new FormData() 

    if (dishEditPicture.value){
        formData.append('picture',dishEditPicture.value)
    } 
    else {
         formData.append('picture',"")
    }

    formData.set('name', dishToEdit.value.name)
    formData.set('description', dishToEdit.value.description)
    formData.set("province", dishToEdit.value.province)
    formData.set("category", dishToEdit.value.category)
    formData.set("spice_level", dishToEdit.value.spice_level)


  await axios.put(`/api/dishes/${dishToEdit.value.id}/`, formData, {
    headers:{
        'Content-Type' : 'multipart/form-data'      
    }
  });
  await fetchDishes() 
}

async function dishAddPictureChange() 
{
  dishPicture.value = dishesPictureRef.value.files[0]
  dishAddImageUrl.value = URL.createObjectURL(dishPicture.value)    
}

async function onRemoveNewPicture(event) {
  event.preventDefault()
  dishAddImageUrl.value = ""
  dishPicture.value = ""
  
}

async function dishEditPictureChange() 
{
  dishEditPicture.value = dishEditPictureRef.value.files[0]
  dishToEdit.value.picture = URL.createObjectURL(dishEditPicture.value)
}

async function onRemoveEditPicture(event) {
  event.preventDefault()
  dishToEdit.value.picture = ""
  dishEditPicture.value = ""
  
}

async function onSmallPictureClick(picture) {
    pictureToBig.value = picture
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
      <div class="col-1">
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            v-model="dishToAdd.name"
            required
          />
          <label for="floatingInput">Название</label>
        </div>
      </div>
      <div class="col-1">
        <div class="form-floating">
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
        <div class="form-floating">
          <select class="form-select" v-model="dishToAdd.province" required>
            <option :value="p.id" v-for="p in provinces">{{ p.name }}</option>
          </select>
          <label for="floatingInput">Провинция</label>
        </div>
      </div>
      <div class="col-2">
        <div class="form-floating">
          <select class="form-select" v-model="dishToAdd.category" required>
            <option :value="c.value" v-for="c in dshCat">{{ c.label }}</option>
          </select>
          <label for="floatingInput">Категория</label>
        </div>
      </div>
      <div class="col-auto">
        <div class="form-floating">
          <input
            type="number"
            class="form-control"
            v-model="dishToAdd.spice_level"
            min = "0"
            max = "10"
            required
          />
          <label for="floatingInput">Острота</label>
        </div>
      </div>
      <div class="col-2">
        <input class="form-control" type="file" ref="dishesPictureRef" @change="dishAddPictureChange">
      </div>
      <div class="col-auto">
        <button v-if="dishPicture" class="btn btn-danger" style="position: relative; zoom: 0.5; left:140px; bottom: 35px" @click="onRemoveNewPicture($event)">
          <i class="bi bi-x"></i>
        </button>
        <img :src = "dishAddImageUrl" style="max-height: 60px"  alt="">
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>
  <hr>
  <div class="row" v-for="d in dishes">
    <div class="col-auto" >{{ d.name}}</div>
    <div class="col-4" >{{ d.description }}</div>
    <div class="col-auto" >{{ d.province.name }} </div>
    <div class="col-auto" >{{ d.category }} </div>
    <div class="col-auto" >{{ d.spice_level }} </div>
    <div class="col-auto">
      <div v-show="d.picture">
        <img :src="d.picture" style="max-height: 60px " @click="onSmallPictureClick(d.picture)" 
        data-bs-toggle="modal" data-bs-target="#bigPictureModal"  >
      </div>
    </div>
    <div class="col-auto">
      <button
        class="btn btn-success"
        style="margin-right: 2px "
        @click="onDishEditClick(d)"
        data-bs-toggle="modal"
        data-bs-target="#editDishModal"
      >
        <i class="bi bi-pencil-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClickDish(d)">
        <i class="bi bi-x"></i>
      </button>
    </div>
    <hr class="mt-2">
  </div>
  <div class="modal fade" id="editDishModal" tabindex="-1">
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
                <input
                  type="text"
                  class="form-control"
                  v-model="dishToEdit.name"
                />
                <label for="floatingInput">Название</label>
              </div>
            </div>
            <div class="row mb-2">
              <div class="form-floating">
                <input
                  type="text"
                  class="form-control"
                  v-model="dishToEdit.description"
                />
                <label for="floatingInput">Описание</label>
              </div>
            </div>
            <div class="row mb-2">
              <div class="form-floating">
                <select class="form-select" v-model="dishToEdit.category" required>
                  <option :value="c.value" v-for="c in dshCat">{{ c.label }}</option>
                </select>
                <label for="floatingInput">Категория</label>
              </div>
            </div>
            <div class="row mb-2">
              <div class="form-floating">
                <select class="form-select" v-model="dishToEdit.province">
                  <option :value="p.id" v-for="p in provinces">
                    {{ p.name }}
                  </option>
                </select>
                <label for="floatingInput">Провинция</label>
              </div>
            </div>
            <div class="row mb-2">
              <div class="form-floating">
                <input
                  type="number"
                  class="form-control"
                  v-model="dishToEdit.spice_level"
                  min = "0"
                  max = "10"
                  required
                />
                <label for="floatingInput">Уровень остроты</label>
              </div>
            </div>
            <div class="row mb-2">
              <div class="form-floating col-auto">
                <input class="form-control" type="file" ref="dishEditPictureRef" @change="dishEditPictureChange">
                <label for="floatingInput">Изображение</label>
              </div>
              <div class="col-auto">
                <button v-if="dishToEdit.picture" class="btn btn-danger" style="position: relative; zoom: 0.5; left:140px; bottom: 35px" @click="onRemoveEditPicture($event)">
                  <i class="bi bi-x"></i>
                </button>
                <img :src = "dishToEdit.picture" style="max-height: 60px"  alt="">
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
            @click="onUpdateDish()">
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

