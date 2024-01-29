<script setup lang="ts">
import { ref } from "vue"

import ollama from 'ollama'
const input_text = ref<string>("Why is the sky blue?")
const output_text = ref<string>("")
const is_loading = ref<boolean>(false)

async function sendToModel() {
  is_loading.value = true

  const response = await ollama.chat({ model: 'llama2', messages: [{ role: 'user', content: input_text.value }], stream: true })
  for await (const part of response) {
    output_text.value += part.message.content
  }
  is_loading.value = false
}
</script>

<template>
  <div class="flex bg-slate-600">
    <div class="w-full h-screen">
      <button :disabled="is_loading" class="bg-green-400 p-3 rounded-xl disabled:bg-gray-400"
        @click="sendToModel()">Send</button>
      <input class="w-full h-full" type="text" v-model="input_text" />
    </div>
    <div class="w-full">
      <p>
        {{ output_text }}
      </p>
    </div>
  </div>
</template>

