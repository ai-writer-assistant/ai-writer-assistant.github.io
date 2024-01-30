<script setup lang="ts">
import { ref } from "vue"

import ollama from 'ollama'
const input_text = ref<string>("Why is the sky blue?")
const output_text = ref<string>("")
const is_loading = ref<boolean>(false)

// const modelfile = `
// FROM llama2
// SYSTEM "You are mario from super mario bros."
// `
// await ollama.create({ model: 'example', modelfile: modelfile })

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
  <div class="flex h-full">
    <div class="w-full h-full flex flex-col">
      <button class="bg-green-400 p-3 rounded-xl grow-0 disabled:bg-gray-400" :disabled="is_loading"
        @click="sendToModel()">Send</button>
      <div class="w-full grow">

        <input class="w-full h-full" type="text" v-model="input_text" />
      </div>
    </div>
    <div class="w-full h-fit">
      <p class="p-4 h-full">
        {{ output_text }}
      </p>
    </div>
  </div>
</template>

