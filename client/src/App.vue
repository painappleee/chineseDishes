<script setup>
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg">
      <a class="navbar-brand" href="/">中国菜</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
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
      </div>
    </nav>
  </div>
  <div class="container-fluid">
    <router-view/>
  </div>
</template>

<style scoped>

</style>

