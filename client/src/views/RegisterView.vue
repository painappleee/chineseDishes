<script setup>
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import { onBeforeMount, ref } from 'vue';
    import router from '@/router';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)
    const registerData = ref({})
    const messageText = ref("")

    async function register() {
        if (!registerData.value.username || !registerData.value.password || registerData.value.username == "" || registerData.value.password == "" || registerData.value.password != registerData.value.password2)
            return

            try{
                await axios.post("api/user/register/", registerData.value)
                router.push("/")
            }
            catch(e){
                messageText.value = "Пользователь уже существует!"
            }                   
    }
    
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
    })
</script>

<template>
    <div class="d-flex align-items-center justify-content-center vh-100">
        <div class="border p-5 rounded shadow-lg bg-white" style="width: 100%; max-width: 400px;">
            {{ registerData }}
            <div class="mb-4 text-center">
                <h2 class="fw-bold">中国菜</h2>
            </div>

            <div class="form-outline mb-3">
                <input 
                    type="text" 
                    class="form-control" 
                    placeholder="Username" 
                    v-model="registerData.username"
                >
            </div>

            <div class="form-outline mb-3">
                <input 
                    type="text" 
                    class="form-control" 
                    placeholder="Email" 
                    v-model="registerData.email"
                >
            </div>

            <div class="form-outline mb-4">
                <input 
                    type="password" 
                    class="form-control" 
                    placeholder="Password" 
                    v-model="registerData.password"
                >
            </div>

            <div class="form-outline mb-4">
                <input 
                    type="password" 
                    class="form-control" 
                    placeholder="Repeat password" 
                    v-model="registerData.password2"
                >
            </div>
            
            <div class="d-flex justify-content-center">
                <button 
                    type="submit" 
                    class="btn btn-primary w-100" 
                    @click="register"
                >
                    Зарегестрироваться
                </button>
            </div>
        </div>
    </div>
</template>