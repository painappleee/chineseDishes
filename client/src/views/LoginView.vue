<script setup>
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import { onBeforeMount, ref } from 'vue';
    import router from '@/router';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';
    

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    const loginData = ref({})
    const messageText = ref("")

    async function login() {
        if(!loginData.value.username || !loginData.value.password || loginData.value.username == "" || loginData.value.password == "")
            return

        try{
            await axios.post("api/user/login/", loginData.value)
            router.push("/")
        }
        catch(e){
            messageText.value = "Неверный логин или пароль"
        }
    }
</script>

<template>
    <div class="d-flex align-items-center justify-content-center vh-100">
        <div class="border p-5 rounded shadow-lg bg-white" style="width: 100%; max-width: 400px;">
            <div class="mb-4 text-center">
                <h2 class="fw-bold">中国菜</h2>
            </div>

            <div class="form-outline mb-3">
                <input 
                    type="text" 
                    class="form-control" 
                    placeholder="Username" 
                    v-model="loginData.username"
                >
            </div>

            <div class="form-outline mb-4">
                <input 
                    type="password" 
                    class="form-control" 
                    placeholder="Password" 
                    v-model="loginData.password"
                >
            </div>
            
            <div class="d-flex justify-content-center">
                <button 
                    type="submit" 
                    class="btn btn-primary w-100" 
                    @click="login()"
                >
                    Войти
                </button>
            </div>

            <div class="text-center mt-3">
                <p class="mb-0">Ещё нет аккаунта? 
                    <a href="/register" class="text-decoration-none text-primary">Зарегестрироваться</a>
                </p>
            </div>
        </div>
    </div>
</template>