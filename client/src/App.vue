<script setup>
    import axios from 'axios';
    import { computed } from 'vue';
    import { useRoute } from 'vue-router';
    import router from '@/router';   

    const route = useRoute();

    const isAuthPage = computed(() =>
      ['/login', '/register'].includes(route.path)
    );

    async function logout() {
      await axios.post("api/user/logout/")
      router.push("/login")
    }

</script>



<template>
  <div v-if="!isAuthPage" class="container">
    <nav class="navbar navbar-expand-lg">
        <a class="navbar-brand" href="/">中国菜</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item active">
              <router-link class="nav-link" to="/" >Блюда</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/provinces" >Провинции</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/ingridients" >Ингридиенты</router-link>
            </li>   
            <li class="nav-item">
              <router-link class="nav-link" to="/dish_ingridients" >Блюдо-ингридиенты</router-link>
            </li>       
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
                <li><a class="dropdown-item" @click="logout()">Выйти</a></li>
              </ul>    
                                  
            </li>
          </ul>
        </div>
    </nav>
  </div>  
  <div class="container-fluid">
    <router-view/>
  </div>
</template>

<style scoped>

</style>

