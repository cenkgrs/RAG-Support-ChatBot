<script setup>

import './assets/main.css'

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

});

marked.setOptions({ gfm: false })

const generateUserKey = () => {
	return crypto.randomUUID();
}

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

	const escapeHtml = (str) => 
        str.replace(/&/g, "&amp;")
           .replace(/</g, "&lt;")
           .replace(/>/g, "&gt;");
	
	const urlRegex = /(https?:\/\/[^\s)<]+)/g;

 	let formattedMessage = escapeHtml(botMessage)
        .replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>')
        .replace(/\n/g, "<br>");

	return { role: "assistant", content: '<span>'+ formattedMessage +'</span>' };
}

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
