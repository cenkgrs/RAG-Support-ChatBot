<template>
  <div class="relative flex min-h-screen w-full flex-col bg-background-light dark:bg-background-dark text-[#1e293b] dark:text-[#f8fafc] font-display">
    <div class="layout-container flex h-full grow flex-col">
      <div class="flex flex-1 items-center justify-center p-4 sm:p-6 lg:p-8">
        <div class="w-full max-w-5xl rounded-xl bg-white dark:bg-background-dark dark:border dark:border-[#1e293b] shadow-lg overflow-hidden grid grid-cols-1 md:grid-cols-2">

          <!-- Left Branding Column -->
          <div class="relative hidden h-full flex-col justify-between bg-background-light  p-8 text-white md:flex">
        
            <div class="relative z-10 flex items-center gap-3 text-2xl font-bold">
                <img src="/argevim_logo_original.png" alt="">
            </div>
            <div class="relative z-10 mt-auto">
              <h1 class="text-gray-700 tracking-light text-[32px] font-bold leading-tight">Ar-Ge Destek</h1>
              <p class="text-gray-700 text-[13px] font-normal leading-normal pt-2">RAG Tabanlı müşteri yardım ve etkileşim botu. Yapay zeka desteğiyle müşterilerin e-ticaret sitelerindeki 7/24 destek sorununu çözüyoruz.</p>
            </div>
          </div>

          <!-- Right Form Column -->
          <div class="flex flex-col justify-center p-8 sm:p-10 lg:p-12">
            <div class="w-full max-w-sm mx-auto">
              <div class="mb-8 text-center md:hidden">
                <div class="flex items-center justify-center gap-3 text-2xl font-bold text-slate-800 dark:text-white">
                  <svg class="h-8 w-8 text-primary" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M15.5 2H8.5a1 1 0 0 0-1 1v18a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1zM12 20a1 1 0 1 1 0-2 1 1 0 0 1 0 2zM12 6a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"></path>
                  </svg>
                  <span>V-Admin</span>
                </div>
              </div>
              <h1 class="text-slate-800 dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] text-left">Giriş Yap</h1>
              <p class="text-slate-600 dark:text-slate-400 text-base font-normal leading-normal pb-6 pt-1">Lütfen bilgilerinizi giriniz.</p>

              <form @submit.prevent="login" class="flex flex-col gap-4">
                <div class="flex flex-col">
                  <label for="email" class="text-slate-700 dark:text-slate-300 text-sm font-medium leading-normal pb-2">E-Posta / Email</label>
                  <div class="relative flex w-full items-stretch rounded-lg">
                    <span class="material-symbols-outlined text-slate-500 dark:text-slate-400 flex border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 items-center justify-center p-3 rounded-l-lg border-r-0">person</span>
                    <input v-model="email" id="email" type="text" placeholder="E-Posta Adresiniz"
                           class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-slate-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-slate-300 dark:border-slate-700 bg-transparent h-12 placeholder:text-slate-400 dark:placeholder:text-slate-500 px-3 text-sm font-normal leading-normal"/>
                  </div>
                </div>

                <div class="flex flex-col">
                  <label for="password" class="text-slate-700 dark:text-slate-300 text-sm font-medium leading-normal pb-2">Şifre</label>
                  <div class="relative flex w-full items-stretch rounded-lg">
                    <span class="material-symbols-outlined text-slate-500 dark:text-slate-400 flex border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 items-center justify-center p-3 rounded-l-lg border-r-0">lock</span>
                    <input v-model="password" id="password" type="password" placeholder="Hesap Şifreniz"
                           class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-slate-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-slate-300 dark:border-slate-700 bg-transparent h-12 placeholder:text-slate-400 dark:placeholder:text-slate-500 px-3 text-sm font-normal leading-normal"/>
                  </div>
                </div>

                <div class="flex items-center justify-between gap-4">
                  <div class="flex items-center">
                    <input v-model="rememberMe" id="remember-me" type="checkbox" 
                           class="form-checkbox h-4 w-4 rounded text-primary bg-slate-200 dark:bg-slate-700 border-slate-300 dark:border-slate-600 focus:ring-primary"/>
                    <label for="remember-me" class="ml-2 block text-sm text-slate-700 dark:text-slate-300">Beni Hatırla</label>
                  </div>
                  <a href="#" class="text-sm font-medium text-primary hover:underline">Şifremi Unuttum ?</a>
                </div>

                <button type="submit" :disabled="loading"
                        class="flex items-center justify-center text-center font-medium relative rounded-lg px-6 py-3 text-sm h-12 bg-primary text-white w-full hover:bg-primary/90 active:bg-primary/80 transition-colors mt-4">
                  {{ loading ? "Giriş yapılıyor..." : "Giriş Yap" }}
                </button>

              </form>

              <div class="text-center mt-8">
                <p class="text-xs text-slate-500 dark:text-slate-400">© 2025 Argevim. Tüm Hakları Saklıdır.</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref } from 'vue'
import { useRouter } from "vue-router";


const email = ref('')
const password = ref('')
const rememberMe = ref(false)

const loading = ref(false);
const message = ref("");
const success = ref(false);
const router = useRouter();

const API_BASE = "https://portal.argevim.com.tr";


const login = async () => {

    loading.value = true;
    message.value = "";
    success.value = false;

    try {
        const res = await axios.post(`${API_BASE}/api/login`, {
            email: email.value,
            password: password.value
        }, {
            headers: { "Content-Type": "application/json" }
        });

        if (res.data && res.data.success) {

            const userData = {
                user: res.data.user,
                expires: Date.now() + 1000 * 60 * 60 * 1 // 1 saat
            };

            localStorage.setItem("user", JSON.stringify(userData));

            router.push({ name: "dashboard" })

            return;

        } else {
            success.value = false;
            message.value = (res.data && res.data.message) || "Giriş başarısız";
        }
    } catch (err) {
        console.log(err);
        // hata kodlarına göre mesaj
        if (err.response && err.response.data && err.response.data.message) {
            message.value = err.response.data.message;
        } else {
            message.value = "Sunucuya bağlanırken hata oluştu";
        }
        success.value = false;
    } finally {
        loading.value = false;
    }
}
</script>

<style>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}
</style>
