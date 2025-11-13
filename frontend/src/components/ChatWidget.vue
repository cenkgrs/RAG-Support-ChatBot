<template>
    <div class="chat-widget">
        <div class="chat-box" v-if="isOpen">
            <div class="messages">
                <div v-for="(msg, index) in messages" :key="index" :class="msg.role">
                    <strong v-if="msg.role === 'assistant'">Bot:</strong>
                    <strong v-else>You:</strong>
                    <span>{{ msg.content }}</span>
                </div>
            </div>
            <div class="input-area">
                <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Mesajınızı yazın..." />
                <button @click="sendMessage">Gönder</button>
            </div>
        </div>
        <button class="chat-toggle" @click="isOpen = !isOpen">
            💬
        </button>
    </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const isOpen = ref(false);
const userInput = ref("");
const messages = ref([]);

const sendMessage = async () => {
    if (!userInput.value.trim()) return;

    const userMsg = { role: "user", content: userInput.value };
    messages.value.push(userMsg);

    try {
        const res = await axios.post("http://localhost:8000/chat", {
            message: userInput.value,
        });

        const botMsg = { role: "assistant", content: res.data.reply };
        messages.value.push(botMsg);
    } catch (err) {
        messages.value.push({
            role: "assistant",
            content: "Sunucuya bağlanırken hata oluştu.",
        });
    }

    userInput.value = "";
};
</script>

<style scoped>
.chat-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
}

.chat-toggle {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 50%;
    padding: 12px;
    cursor: pointer;
    font-size: 20px;
}

.chat-box {
    width: 300px;
    height: 400px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    padding: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 10px;
}

.user {
    text-align: right;
    margin: 5px 0;
}

.assistant {
    text-align: left;
    margin: 5px 0;
}

.input-area {
    display: flex;
    gap: 8px;
}

input {
    flex: 1;
    padding: 6px;
    border-radius: 6px;
    border: 1px solid #ccc;
}

button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
}
</style>
