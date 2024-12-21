import {ref} from "vue"
import axios from "axios"
import { defineStore } from "pinia"

export const useUserStore = defineStore("UserStore", ()=>{
    const isAuthenticated = ref(false)
    const isSuperuser = ref(false)
    const username = ref("")

    async function getInfo() {
        const r = await axios.get('/api/user/info/')
        isAuthenticated.value = r.data.is_authenticated
        isSuperuser.value = r.data.is_superuser
        username.value = r.data.username
        
    }

    getInfo()

    return{
        isAuthenticated, isSuperuser, username,
        getInfo
    }
})