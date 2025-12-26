<template>
  <aside
    class="w-64 flex-shrink-0 bg-white dark:bg-[#111418] flex flex-col border-r border-gray-200 dark:border-gray-800"
  >
    <div class="flex h-full flex-col justify-between p-4">
      <div class="flex flex-col gap-4">
        <div class="flex items-center gap-3 px-3">
          <img src="/argevim_logo_original.png" alt="">
        </div>

        <nav class="flex flex-col gap-2 mt-4">
          <router-link
            v-for="item in menuItems"
            :key="item.label"
            :to="item.to"
            class="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 
                   dark:hover:bg-gray-800"
            :class="[
              $route.path === item.to
                ? 'bg-primary/10 text-primary'
                : 'text-gray-700 dark:text-gray-300'
            ]"
          >
            <span class="material-symbols-outlined">
              {{ item.icon }}
            </span>
            <p class="text-sm font-medium">{{ item.label }}</p>
          </router-link>
        </nav>
      </div>

      <div class="flex flex-col gap-1">
        <a
          class="flex items-center gap-3 px-3 py-2 text-gray-700 dark:text-gray-300 
                 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
          href="#"
        >
          <span class="material-symbols-outlined">help_center</span>
          <p class="text-sm font-medium">Help Center</p>
        </a>
      </div>
    </div>
  </aside>
</template>

<script setup>
const menuItems = [
  { label: "Dashboard", to: "/dashboard", icon: "dashboard" },
  { label: "Test Arayüzü", to: "/test-arayuzu", icon: "smart_toy" },
  { label: "ChatBot Ayarları", to: "/chatbot-ayar", icon: "chat" },
  { label: "İçerik Dökümanları", to: "/icerik-dokuman", icon: "article" },
  { label: "Analiz", to: "/analiz", icon: "analytics" },
  { label: "Tema Ayarları", to: "/tema-ayar", icon: "settings" }
]
</script>
