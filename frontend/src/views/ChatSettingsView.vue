<template>

    <DashboardLayout>
        <!-- Main Content -->
        <main class="flex-1 p-8 overflow-y-auto pb-28">
            <div class="mx-auto">
                <!-- Page Heading -->
                <div class="flex flex-wrap justify-between gap-3 pb-8">
                    <p
                        class="text-3xl font-bold text-gray-900 dark:text-white">
                        Asistan Ayarları
                    </p>
                </div>

                <!-- Settings Sections -->
                <div class="space-y-8">
                    <!-- General Settings -->
                    <div class="bg-white dark:bg-[#111418] rounded-xl border border-gray-200 dark:border-[#3b4754]/40">
                        <h2
                            class="text-gray-900 dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-6 pb-3 pt-5 border-b border-gray-200 dark:border-[#3b4754]/40">
                            Genel Ayarlar
                        </h2>
                        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                            <label class="flex flex-col">
                                <p class="text-gray-700 dark:text-white text-base font-medium leading-normal pb-2">
                                    Asistan İsmi</p>
                                <input v-model="settings.name" type="text"
                                    class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary h-12 placeholder:text-gray-400 dark:placeholder:text-[#9dabb9] px-4 text-base font-normal leading-normal" />
                            </label>

                            <label class="flex flex-col">
                                <p class="text-gray-700 dark:text-white text-base font-medium leading-normal pb-2">
                                    Dil Seçimi</p>
                                <select v-model="settings.language"
                                    class="form-select flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary h-12 placeholder:text-gray-400 dark:placeholder:text-[#9dabb9] px-4 text-base font-normal leading-normal">
                                    <option value="en">English (US)</option>
                                    <option value="tr">Türkçe</option>
                                </select>
                            </label>

                            <div class="md:col-span-2">
                                <label class="flex flex-col">
                                    <p class="text-gray-700 dark:text-white text-base font-medium leading-normal pb-2">
                                        Cevap Karakter Limiti</p>
                                    <input v-model.number="settings.characterLimit" type="number"
                                        class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary h-12 placeholder:text-gray-400 dark:placeholder:text-[#9dabb9] px-4 text-base font-normal leading-normal" />
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Features -->
                    <div class="bg-white dark:bg-[#111418] rounded-xl border border-gray-200 dark:border-[#3b4754]/40">
                        <h2
                            class="text-gray-900 dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-6 pb-3 pt-5 border-b border-gray-200 dark:border-[#3b4754]/40">
                            Özellikler
                        </h2>
                        <div class="p-6 space-y-4">
                            <div class="flex items-center justify-between" v-for="(feature, index) in features"
                                :key="index">
                                <p class="text-gray-700 dark:text-white">{{ feature.label }}</p>
                                <label class="relative inline-flex items-center cursor-pointer">
                                    <input type="checkbox" v-model="feature.enabled" class="sr-only peer" />
                                    <div
                                        class="w-11 h-6 bg-gray-200 dark:bg-[#3b4754] peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary/50 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary">
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Conversation Content -->
                    <div class="bg-white dark:bg-[#111418] rounded-xl border border-gray-200 dark:border-[#3b4754]/40">
                        <h2
                            class="text-gray-900 dark:text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-6 pb-3 pt-5 border-b border-gray-200 dark:border-[#3b4754]/40">
                            Sohbet İçeriği
                        </h2>
                        <div class="p-6 space-y-6">
                            <label class="flex flex-col">
                                <p class="text-gray-700 dark:text-white text-base font-medium leading-normal pb-2">
                                    Açılış Mesajı</p>
                                <textarea v-model="settings.welcomeMessage" rows="3"
                                    class="form-textarea flex w-full min-w-0 flex-1 resize-y overflow-hidden rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary placeholder:text-gray-400 dark:placeholder:text-[#9dabb9] p-4 text-base font-normal leading-normal">
                                </textarea>
                            </label>

                             <div>
                                <p class="text-gray-700 dark:text-white text-base font-medium leading-normal pb-2">
                                    Hazır Sorular</p>
                                <small class="space-y-4">En çok gelen soruları kullanıcılara önermek için buraya ekleyebilirsiniz.</small>
                                <div class="space-y-4">
                                    <div class="flex items-start gap-4" v-for="(reply, index) in settings.questions"
                                        :key="index">
                                        <input v-model="reply.keyword" placeholder="Keyword (e.g., shipping)"
                                            class="form-input flex-1 rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary h-12 px-4" />
                                        <input v-model="reply.response" placeholder="Bot Response"
                                            class="form-input flex-1 rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary h-12 px-4" />
                                        <button @click="removeReply(index)"
                                            class="flex-shrink-0 size-12 flex items-center justify-center rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-500">
                                            <span class="material-symbols-outlined">delete</span>
                                        </button>
                                    </div>
                                    <button @click="addReply"
                                        class="w-full flex items-center justify-center gap-2 py-3 rounded-lg border-2 border-dashed border-gray-300 dark:border-[#3b4754] text-gray-600 dark:text-[#9dabb9] hover:bg-gray-100 dark:hover:bg-primary/10 hover:border-primary/50 hover:text-primary dark:hover:text-primary transition-colors">
                                        <span class="material-symbols-outlined">add</span> Soru Ekle
                                    </button>
                                </div>
                            </div>

                            <div>
                                <p class="text-gray-700 dark:text-white text-base font-medium leading-normal pb-2">
                                    Otomatik Cevaplar</p>
                                <small class="space-y-4">** Bu alanda belli başlı konularda katı cevaplar verdirebilirsiniz. Fakat asistanın doğallığınına zarar gelmemesi için çok fazla otomatik mesaj eklenmesini önermiyoruz.</small>
                                <div class="space-y-4">
                                    <div class="flex items-start gap-4" v-for="(reply, index) in settings.autoReplies"
                                        :key="index">
                                        <input v-model="reply.keyword" placeholder="Keyword (e.g., shipping)"
                                            class="form-input flex-1 rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary h-12 px-4" />
                                        <input v-model="reply.response" placeholder="Bot Response"
                                            class="form-input flex-1 rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4754] bg-gray-50 dark:bg-[#1c2127] focus:border-primary h-12 px-4" />
                                        <button @click="removeReply(index)"
                                            class="flex-shrink-0 size-12 flex items-center justify-center rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-500">
                                            <span class="material-symbols-outlined">delete</span>
                                        </button>
                                    </div>
                                    <button @click="addReply"
                                        class="w-full flex items-center justify-center gap-2 py-3 rounded-lg border-2 border-dashed border-gray-300 dark:border-[#3b4754] text-gray-600 dark:text-[#9dabb9] hover:bg-gray-100 dark:hover:bg-primary/10 hover:border-primary/50 hover:text-primary dark:hover:text-primary transition-colors">
                                        <span class="material-symbols-outlined">add</span> Cevap Ekle
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </main>

        <div
            class="fixed bottom-0 left-0 lg:left-64 right-0 bg-white/80 dark:bg-[#111418]/80 backdrop-blur-sm border-t border-gray-200 dark:border-[#3b4754]/40 p-4">
            <div class="max-w-4xl mx-auto flex justify-end gap-4">
                <button @click="saveSettings" :disabled="disabled"
                    class="px-6 py-3 rounded-lg text-white bg-primary hover:bg-primary/90 font-semibold transition-colors disabled:bg-primary/50 disabled:cursor-not-allowed">
                    Kaydet
                </button>
            </div>
        </div>

    </DashboardLayout>

</template>

<script setup>
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import { reactive } from 'vue';

const settings = reactive({
    name: 'Ar-Ge Destek',
    language: 'tr',
    characterLimit: 300,
    welcomeMessage: 'Merhabalar! Size nasıl yardımcı olabilirim ?',
    autoReplies: [
        { keyword: 'shipment_reply', response: 'Kargo teslimatımız 2-4 iş günü sürmektedir.' },
        { keyword: 'refund_reply', response: 'İade talebi kargo teslimatından 15 gün içerisinde verilebilir.' }
    ],
    questions: [
        { keyword: 'shipment_question', response: 'Kargom Nerede ?' },
        { keyword: 'refund_question', response: 'İade süreci hakkında bilgi almak istiyorum.' }
    ]
});

const features = reactive([
    { label: 'İade Yönetimi', enabled: true },
    { label: 'Sepete Ekle Yönetimi', enabled: true },
    { label: 'Mesajlarda resim gösterilmesi', enabled: false }
]);

function addReply() {
    settings.autoReplies.push({ keyword: '', response: '' });
}

function removeReply(index) {
    settings.autoReplies.splice(index, 1);
}

function saveSettings() {
    console.log('Saved settings:', settings, features);
    alert('Settings saved successfully!');
}
</script>
