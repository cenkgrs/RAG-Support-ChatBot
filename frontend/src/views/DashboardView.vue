<template>

	<DashboardLayout>

		<!-- Main Content -->
		<main class="flex-1 overflow-y-auto p-8">
			<div class="max-w-6xl">
				<!-- Page Heading -->
				<div class="flex flex-wrap items-start justify-between gap-4">
					<div class="flex flex-col gap-2">
						<h1 class="text-3xl font-bold text-gray-900 dark:text-white">Kurulum</h1>
						<p class="text-base font-normal leading-normal text-slate-500 dark:text-slate-400">
							Aşağıdaki adımları takip ederek kurulum işlemlerinizi gerçekleştirebilirsiniz
						</p>
					</div>
					<div class="flex flex-col">
						<label class="pb-2 text-sm font-medium leading-normal text-slate-700 dark:text-slate-300"
							for="language-select">Language</label>
						<select v-model="language" id="language-select"
							class="form-select w-48 rounded-lg border-slate-300 bg-white text-slate-800 shadow-sm focus:border-primary focus:ring-primary focus:ring-opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
							<option>JavaScript</option>
							<option>Vue.Js</option>
						</select>
					</div>
				</div>

				<div class="mt-10 flex gap-12">

					<!-- Content and Code Block -->
					<div class="w-full flex-1">
						<div
							class="rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
							<h3 class="text-lg font-bold text-slate-900 dark:text-white">Iframe Script
							</h3>
							<p class="mt-2 text-base font-normal leading-normal text-slate-600 dark:text-slate-400">
								Aşağıdaki komutu çalışmasını istediğiniz sayfanın içerisine eklemeniz yeterlidir.
							</p>
							<!-- Code Block -->
							<div class="relative mt-6 overflow-hidden rounded-lg bg-code-bg">
								<div class="flex items-center justify-between bg-slate-900/50 px-4 py-2">
									<span class="text-xs font-medium text-slate-400">Terminal</span>
									<button @click="copyCommand"
										class="flex items-center gap-2 rounded-md bg-slate-700 px-3 py-1.5 text-xs font-medium text-white hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-code-bg">
										<span class="material-symbols-outlined text-sm">content_copy</span>
										Kodu Kopyala
									</button>
								</div>
								<pre class="overflow-x-auto p-4 text-sm bg-slate-700">
									<code class="language-bash text-white">
										&lt;script 
											src="https://support.argevim.com.tr/widget.js"
											data-bot-id="ke01mv!*0kf33cs"
											data-header="Pin Drinks Canlı Destek"
											data-bg="#153258"
											data-text="#222"
											data-logo="https://cdn.pindrinks.com/storage/v2/pin-logo.webp"&gt;
										&lt;/script&gt;
									</code>
								</pre>
							</div>
						</div>

						<!-- Support Section -->
						<div
							class="mt-8 rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
							<h4 class="text-base font-semibold text-slate-800 dark:text-slate-200">Yardıma İhtiyacınız Var mı?</h4>
							<p class="mt-1 text-sm text-slate-600 dark:text-slate-400">
								Sormak istediğiniz herhangi bir soru varsa bizimle iletişime geçebilirsiniz.
							</p>
							<div class="mt-4 flex flex-wrap gap-4">
								<a class="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90"
									href="#">Destek</a>
								<a class="rounded-md bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
									href="#">Dökümantasyon</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</main>
	</DashboardLayout>

</template>

<script setup>
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { ref } from 'vue'

// reactive state
const language = ref('JavaScript')

// copy command to clipboard
const copyCommand = () => {
	navigator.clipboard.writeText('&lt;script src="http://localhost:5173/widget.js" data-bot-id="123" data-header="Pin Drinks Canlı Destek" data-bg="#153258" data-text="#222" data-logo="https://cdn.pindrinks.com/storage/v2/pin-logo.webp"&gt; &lt;/script&gt;')
	alert('Command copied!')
}


</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.material-symbols-outlined {
	font-variation-settings:
		'FILL' 0,
		'wght' 400,
		'GRAD' 0,
		'opsz' 24;
}
</style>
