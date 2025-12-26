<template>
    <DashboardLayout>
        <!-- Chat Widget -->
        <div class="fixed bottom-8 right-8 flex flex-col items-end gap-4 z-50">
        <div class="w-96 h-[500px] flex flex-col rounded-xl shadow-2xl bg-container-light  border border-border-light dark:border-border-dark overflow-hidden">
            <div class="flex items-center justify-between p-4 bg-background-light dark:bg-background-light border-b border-border-light dark:border-border-dark">
            <h3 class="font-bold text-text-light-primary dark:text-dark-primary">Arge Destek</h3>
            <button class="text-text-light-secondary dark:text-dark-secondary hover:text-text-light-primary dark:hover:text-dark-primary">
                <span class="material-symbols-outlined text-xl">close</span>
            </button>
            </div>
            <div class="flex-1 p-4 overflow-y-auto space-y-4">
            <!-- Bot Message -->
            <div class="flex items-start gap-3">
                <div class="flex items-center justify-center size-8 rounded-full bg-primary text-white flex-shrink-0">
                <span class="material-symbols-outlined text-lg">smart_toy</span>
                </div>
                <div class="flex flex-col gap-2">
                <div class="p-3 rounded-lg rounded-tl-none bg-background-light dark:bg-background-light text-text-light-primary dark:text-dark-primary text-sm">
                    <p>Merhabalar, Size nasıl yardımcı olabilirim ?</p>
                </div>
                <div class="flex flex-wrap gap-2">
                    <button class="px-3 py-1.5 text-xs rounded-full border border-border-light dark:border-border-dark text-text-light-secondary dark:text-dark-secondary hover:bg-primary/10 hover:border-primary/50 hover:text-primary">How do I add a new user?</button>
                    <button class="px-3 py-1.5 text-xs rounded-full border border-border-light dark:border-border-dark text-text-light-secondary dark:text-dark-secondary hover:bg-primary/10 hover:border-primary/50 hover:text-primary">Reset a password</button>
                </div>
                </div>
            </div>
            </div>
            <div class="p-4 border-t border-border-light dark:border-border-dark">
            <div class="relative">
                <input v-model="chatInput" class="w-full h-12 pr-12 text-sm rounded-lg bg-background-light dark:bg-background-light text-text-light-primary dark:text-dark-primary border border-border-light dark:border-border-dark focus:ring-1 focus:ring-primary focus:border-primary" placeholder="Type your message..." type="text"/>
                <button @click="sendMessage" class="absolute inset-y-0 right-0 flex items-center justify-center w-12 text-primary hover:text-primary/80">
                <span class="material-symbols-outlined">send</span>
                </button>
            </div>
            </div>
        </div>
        </div>
    </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { ref } from 'vue'

const search = ref('')
const chatInput = ref('')

const sendMessage = () => {
  if (!chatInput.value.trim()) return
  alert(`User Message: ${chatInput.value}`)
  chatInput.value = ''
}
</script>

<style scoped>
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
.size-2 { width: 0.5rem; height: 0.5rem; }
.size-8 { width: 2rem; height: 2rem; }
.size-10 { width: 2.5rem; height: 2.5rem; }
</style>
