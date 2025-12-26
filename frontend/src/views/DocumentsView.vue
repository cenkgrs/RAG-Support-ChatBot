<template>

    <DashboardLayout>
        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto">
            <div class="mx-auto max-w-7xl p-6 lg:p-8">

                <!-- Page Heading -->
                <div class="flex flex-wrap items-start justify-between gap-4">
                <div class="flex flex-col gap-2">
                    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Döküman Yönetimi</h1>
                    <p class="text-slate-600 dark:text-slate-400">İçerik dökümanlarını manuel olarak yükleyebilir veya yeni belgeler oluşturarak knowledge base ekleyebilirsiniz.</p>
                </div>
                <button class="flex h-10 min-w-[84px] items-center justify-center gap-2 rounded-lg bg-primary px-4 text-sm font-bold text-white shadow-sm hover:bg-primary/90">
                    <span class="material-symbols-outlined text-base">add</span>
                    <span class="truncate">New File</span>
                </button>
                </div>

                <!-- File Upload Section -->
                <div class="mt-8 grid grid-cols-1 gap-8">
                <div class="flex flex-col items-center gap-6 rounded-xl border-2 border-dashed border-slate-300 bg-white p-14 dark:border-slate-700 dark:bg-slate-900/50">
                    <div class="flex max-w-md flex-col items-center gap-2 text-center">
                    <span class="material-symbols-outlined text-5xl text-slate-400 dark:text-slate-500">upload_file</span>
                    <p class="text-lg font-bold tracking-tight text-slate-900 dark:text-white">Dosyaları buraya sürükleyip bırakın</p>
                    <p class="text-sm text-slate-600 dark:text-slate-400">veya tıklayarak göz atın. PDF, TXT, DOCX formatlarını destekler.</p>
                    </div>
                    <button class="flex h-10 min-w-[84px] max-w-[480px] items-center justify-center rounded-lg bg-slate-100 px-4 text-sm font-bold text-slate-800 hover:bg-slate-200 dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700">
                    <span class="truncate">Gözat</span>
                    </button>
                </div>

                <!-- Example Progress Bar -->
                <div class="flex flex-col gap-2 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900/50">
                    <div class="flex items-center justify-between gap-6">
                    <p class="text-sm font-medium text-slate-800 dark:text-white">Uploading document</p>
                    <p class="text-sm text-slate-600 dark:text-slate-400">{{ uploadProgress }}%</p>
                    </div>
                    <div class="h-2 rounded-full bg-slate-200 dark:bg-slate-700">
                    <div class="h-2 rounded-full bg-primary" :style="{ width: uploadProgress + '%' }"></div>
                    </div>
                    <p class="text-xs text-slate-500 dark:text-slate-400">1.2MB / 1.6MB</p>
                </div>

                <!-- Manual Document Form -->
                <div class="rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900/50">
                    <h2 class="text-lg font-bold tracking-tight text-slate-900 dark:text-white">Yeni Döküman Oluştur</h2>
                    <div class="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
                    <!-- Document ID -->
                    <div class="md:col-span-1">
                        <label for="doc-id" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Döküman ID</label>
                        <div class="relative mt-2 flex items-stretch">
                        <input class="block w-full rounded-l-lg border-0 bg-slate-100 py-2.5 pl-4 pr-12 text-slate-500 ring-1 ring-inset ring-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:ring-slate-700 sm:text-sm" id="doc-id" type="text" :value="newDoc.id"/>
                        <button @click="copyDocId" class="absolute inset-y-0 right-0 flex items-center rounded-r-lg px-3 text-slate-400 hover:text-primary dark:text-slate-500 dark:hover:text-primary">
                            <span class="material-symbols-outlined text-base">content_copy</span>
                        </button>
                        </div>
                    </div>

                    <!-- Document Name -->
                    <div class="md:col-span-1">
                        <label for="doc-name" class="block text-sm font-medium text-slate-700 dark:text-slate-300">Döküman İsmi</label>
                        <div class="mt-2">
                        <input v-model="newDoc.name" id="doc-name" placeholder="e.g., Product Document"
                                class="block w-full rounded-lg border-0 bg-white py-2.5 pl-4 text-slate-900 ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-primary/50 dark:bg-slate-800/50 dark:text-white dark:ring-slate-700 sm:text-sm"/>
                        </div>
                    </div>

                    <!-- Content -->
                    <div class="md:col-span-2">
                        <label for="doc-text" class="block text-sm font-medium text-slate-700 dark:text-slate-300">İçerik</label>
                        <small>Bu kısma firmanın SSS verileri, iletişim bilgileri, önemli sorular, ürünlerle ilgili detaylar gibi verileri ekleyebilirsiniz.</small>
                        <div class="mt-2">
                        <textarea v-model="newDoc.content" id="doc-text" rows="8" placeholder="Eklemek istediğiniz içerik verilerini satır satır ekleyebilirsiniz."
                                    class="block w-full rounded-lg border-0 bg-white py-2.5 pl-4 text-slate-900 ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-primary/50 dark:bg-slate-800/50 dark:text-white dark:ring-slate-700 sm:text-sm"></textarea>
                        </div>
                    </div>
                    </div>

                    <!-- Form Buttons -->
                    <div class="mt-8 flex justify-end gap-3">
                    <button @click="resetForm" class="flex h-10 min-w-[84px] items-center justify-center rounded-lg bg-slate-100 px-4 text-sm font-bold text-slate-800 hover:bg-slate-200 dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700">Temizle</button>
                    <button @click="saveDocument" class="flex h-10 min-w-[84px] items-center justify-center rounded-lg bg-primary px-4 text-sm font-bold text-white shadow-sm hover:bg-primary/90">Kaydet</button>
                    </div>
                </div>

                </div>

                <!-- Document List Section -->
                <div class="mt-12">
                <div class="mb-6">
                    <h2 class="text-xl font-bold tracking-tight text-slate-900 dark:text-white">Mevcut Dökümanlar</h2>
                    <p class="text-sm text-slate-600 dark:text-slate-400">Showing {{ totalDocuments }} documents</p>
                </div>

                <!-- Data Table -->
                <div class="overflow-hidden rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900/50">
                    <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
                    <thead class="bg-slate-50 dark:bg-slate-900">
                        <tr>
                        <th class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-slate-900 dark:text-white sm:pl-6">ID</th>
                        <th class="px-3 py-3.5 text-left text-sm font-semibold text-slate-900 dark:text-white">Döküman Adı</th>
                        <th class="px-3 py-3.5 text-left text-sm font-semibold text-slate-900 dark:text-white">Durum</th>
                        <th class="px-3 py-3.5 text-left text-sm font-semibold text-slate-900 dark:text-white">Eklenme Tarihi</th>
                        <th class="relative py-3.5 pl-3 pr-4 sm:pr-6"><span class="sr-only">Actions</span></th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
                        <tr v-for="doc in documents" :key="doc.id">
                        <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-mono text-slate-500 sm:pl-6">{{ doc.id }}</td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm font-medium text-slate-900 dark:text-white">{{ doc.name }}</td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-slate-500 dark:text-slate-400">{{ doc.status ? 'Aktif' : 'Pasif' }}</td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-slate-500 dark:text-slate-400">{{ doc.date }}</td>
                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                            <div class="flex items-center justify-end gap-2">
                            <button class="flex h-8 w-8 items-center justify-center rounded-md hover:bg-slate-100 dark:hover:bg-slate-800">
                                <span class="material-symbols-outlined text-base text-slate-500">visibility</span>
                            </button>
                            <button class="flex h-8 w-8 items-center justify-center rounded-md hover:bg-slate-100 dark:hover:bg-slate-800">
                                <span class="material-symbols-outlined text-base text-slate-500">edit</span>
                            </button>
                            <button class="flex h-8 w-8 items-center justify-center rounded-md hover:bg-slate-100 dark:hover:bg-slate-800">
                                <span class="material-symbols-outlined text-base text-red-500">delete</span>
                            </button>
                            </div>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                </div>

                </div>

            </div>
        </main>
    </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { reactive, ref } from 'vue'

// User info
const user = reactive({
  name: 'Admin Panel',
  role: 'Vue.js App',
  avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBJaoQxEEL1zpK51FMqdrR5BSpWoKLzFHTU7CcVEKEnTwW_m92Jr_6DfEB8ijFybgEpGSPp6xBBN5TtdQL3HOtNfPd92u9KbG_Hk2PHVwj9yKWbVLBt7zOSc4VaTR-8YaZzvvzd-TFWxxv3V4kLKwR9bGfnwPTco1D75qisiYQ-ducoQ6IbK_qxum6lfTroaFdYnFr-eEfj-Vek2h6qFMrdtvZObTs0pWjPV3oLCnaNufddRTU7BfuYGiRhPpJ8Zv36mzKmsFcfAcIM'
})

// Upload progress
const uploadProgress = ref(75)

// New Document Form
const newDoc = reactive({
  id: '',
  name: '',
  content: ''
})

// Documents list
const documents = reactive([
  { id: 'doc_123', name: 'Products.jsonl', status: true, date: '25.11.2025'},
  { id: 'doc_231', name: 'contacts.jsonl', status: true, date: '25.11.2025' },
  { id: 'doc_432', name: 'sss.jsonl', status: true, date: '26.11.2025' }
])
const totalDocuments = 3

// Methods
const copyDocId = () => navigator.clipboard.writeText(newDoc.id)
const resetForm = () => {
  newDoc.name = ''
  newDoc.content = ''
}
const saveDocument = () => {
  alert(`Document "${newDoc.name}" saved!`)
}

// NavItem component
const NavItem = {
  props: { icon: String, label: String, active: Boolean },
  template: `
    <a :class="['flex items-center gap-3 rounded-lg px-3 py-2', active ? 'bg-primary/20 text-white' : 'text-slate-300 hover:bg-slate-800']" href="#">
      <span class="material-symbols-outlined" :class="active ? 'text-white' : 'text-slate-300'" style="font-variation-settings: 'FILL' 0;">{{ icon }}</span>
      <p class="text-sm font-medium leading-normal">{{ label }}</p>
    </a>
  `
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
