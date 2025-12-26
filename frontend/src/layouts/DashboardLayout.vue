<template>
  <div class="flex min-h-screen">
    <Sidebar />

    <main class="flex-1 flex flex-col">
      <TopNavbar />

      <div class="flex-1 p-6 lg:p-8 overflow-y-auto dark:bg-[#101922]">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue"
</script>
