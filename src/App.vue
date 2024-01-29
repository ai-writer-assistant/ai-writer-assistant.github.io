<script setup lang="ts">
import { ref } from "vue"

import ollama from 'ollama'
const input_text = ref<string>("Why is the sky blue?")
const output_text = ref<string>("")


async function sendToModel() {
  console.log("Send message")

  const response = await ollama.chat({ model: 'llama2', messages: [{ role: 'user', content: input_text.value }], stream: true })
  for await (const part of response) {
    output_text.value += part.message.content
  }
}
</script>

<template>
  <div class="flex bg-slate-600">
    <div class="w-full h-screen">
      <button class="bg-green-400 p-3 rounded-xl" @click="sendToModel()">Send</button>
      <input class="w-full h-full" type="text" v-model="input_text" />
    </div>
    <div class="w-full">
      <p>
        {{ output_text }}
      </p>
    </div>
  </div>
</template>

