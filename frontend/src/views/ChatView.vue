<script setup>

import '../assets/main.css'

import { ref, onMounted, defineProps } from "vue";
import axios from "axios";
import { marked } from "marked";
const props = defineProps({ text: String });

const bgColor = ref("#fa4238");
const header = ref("Evia Home");
const logo = ref("https://www.eviahome.com.tr/storage/evia300-1.png");

const userInput = ref("");
const messages = ref([]);

const isTyping = ref(false);

const userKey = crypto.randomUUID();

onMounted(() => {
	// URL'i tam al
	const fullUrl = window.location.href;
	const queryString = fullUrl.split("?")[1] || "";
	const params = new URLSearchParams(queryString);

	bgColor.value = params.get("bg") || "#fa4238";
	header.value = params.get("header") || "Evia Home";
	logo.value = "/argedestek-transparent.png";

	document.addEventListener("change", async (e) => {
		if (e.target && e.target.id === "chatUpload") {
			handleImageUploadFromChat(e.target.files[0]);
		}
	});

});

marked.setOptions({ gfm: false })

const sendMessage = async () => {
	if (!userInput.value.trim()) return;

	const userMsg = { role: "user", content: userInput.value };
	userInput.value = "";

	messages.value.push(userMsg);

	toggleTyping();

	scrollToMessage();

	try {
		const res = await axios.post("http://localhost:8000/chat", {
			userKey: userKey,
			messages: [...messages.value],
		});

		const botMsg = formatBotMessage(res.data.reply);

		messages.value.push(botMsg);
	} catch (err) {
		messages.value.push({
			role: "assistant",
			content: "Sunucuya bağlanırken hata oluştu.",
		});
	}

	toggleTyping();

	scrollToMessage();

};

const formatBotMessage = (botMessage) => {
    const inputTag = `<input type="file" id="chatUpload" accept="image/*">`;
    const placeholder = "___CHAT_UPLOAD_INPUT___";

    let tempMessage = botMessage.replace(inputTag, placeholder);

    // Markdown resimleri ![Alt](URL) → <img>
    const markdownImageRegex = /!\[([^\]]*?)\]\((https?:\/\/[^\s)]+)\)/g;
    tempMessage = tempMessage.replace(markdownImageRegex, (match, alt, url) => {
        return `<img src="${url}" alt="${alt || 'image'}" />`;
    });

    // Markdown linkleri [Text](URL) → <a>
    const markdownLinkRegex = /\[([^\]]*?)\]\((https?:\/\/[^\s)]+)\)/g;
    tempMessage = tempMessage.replace(markdownLinkRegex, (match, text, url) => {
        const linkText = text.trim() ? text : "Ürün Linki";
        return `<a href="${url}" target="_blank" rel="noopener noreferrer">${linkText}</a>`;
    });

    // Normal URL'leri <a> tag'ine çevir (resim olmayanlar)
    const urlRegex = /(?<!href="|src=")(https?:\/\/[^\s<]+)/g;
    tempMessage = tempMessage.replace(urlRegex, (match) => {
        if (match.match(/\.(webp|png|jpg|jpeg)$/i)) {
            return `<img src="${match}" alt="image" />`;
        }
        return `<a href="${match}" target="_blank" rel="noopener noreferrer">${match}</a>`;
    });

    // Satır sonlarını <br> ile değiştir ve başlıkları temizle
	tempMessage = tempMessage
		.replace(/\n/g, "<br>")       // \n → <br>
		.replace(/###/g, "")          // başlıkları temizle
		.replace(/---/g, "")          // --- temizle
		.replace(/(<br>\s*){3,}/g, "<br><br>") // üst üste 2+ <br> → 1 <br>
		.replace(/(<br>\s*)+(?=<img[^>]*>)/gi, "")
		.replace(/(?<=<img[^>]*>)(\s*<br>)+/gi, "");

    // Input tag’ini geri ekle
    tempMessage = tempMessage.replace(placeholder, inputTag);

    return { role: "assistant", content: '<span>'+ tempMessage +'</span>' };
};


const toggleTyping = () => {
	isTyping.value = !isTyping.value;
}

const scrollToMessage = () => {
	setTimeout(function () {
		const lastMessage = document.getElementsByClassName('message')[document.getElementsByClassName('message').length - 1];

		if (typeof lastMessage !== 'undefined') {
			lastMessage.scrollIntoView({ behavior: 'smooth' })
		}
	}, 100);
}

const closeWidget = () => {
	window.parent.postMessage({ type: 'CLOSE_CHAT_WIDGET' }, '*');
};

const handleImageUploadFromChat = async (file) => {
	if (!file) return;

	const base64 = await toBase64(file);

	// backend'e yükle
	const res = await axios.post("http://localhost:8000/upload-image", {
		userKey: userKey,
		image: base64
	});

	const imageUrl = res.data.url;

	const userMsg = { role: "user", content: imageUrl };

	messages.value.push(userMsg);

	try {
		const res = await axios.post("http://localhost:8000/chat", {
			userKey: userKey,
			messages: [...messages.value],
		});

		const botMsg = formatBotMessage(res.data.reply);

		messages.value.push(botMsg);
	} catch (err) {
		messages.value.push({
			role: "assistant",
			content: "Sunucuya bağlanırken hata oluştu.",
		});
	}

	scrollToMessage()
	
};

function toBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}


</script>



<template>
	<div class="chat-box">
		<div class="chat-header" :style="{ backgroundColor: bgColor }">
			<!--<img :src="logo" alt="">-->
			<h3>{{ header }}</h3>
			<button class="close-btn" id="close-button" @click="closeWidget">×</button>
		</div>

		<div class="messages">
			<div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
				<div class="bubble"
					:style="msg.role == 'user' ? { backgroundColor: bgColor, boxShadow: '0 0 1px 1px ' + bgColor } : ''"
					v-html="marked(msg.content)">
				</div>
			</div>

			<div v-if="isTyping" class="assistant message fade-in">
				<div class="bubble">
					<div class="typing-dots">
						<span :style="{ backgroundColor: bgColor }"></span><span
							:style="{ backgroundColor: bgColor }"></span><span
							:style="{ backgroundColor: bgColor }"></span>
					</div>
				</div>

			</div>
		</div>

		<div class="composer-inner">
			<input v-model="userInput" @keyup.enter="sendMessage" placeholder="Mesajınızı yazın..." />
			<button class="send" :style="{ backgroundColor: bgColor }" @click="sendMessage">Gönder</button>
		</div>
	</div>
</template>
