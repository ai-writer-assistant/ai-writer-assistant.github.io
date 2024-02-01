<script setup lang="ts">
import { ref } from "vue"

import ollama from 'ollama'
const input_text = ref<string>("Why is the sky blue?")
const output_text = ref<string>("")
const is_loading = ref<boolean>(false)

interface ResOut {
  id: number,
  message: string,
  output: string,
}

const all_res_out = ref<Array<ResOut>>([])
all_res_out.value.push({
  id: 1,
  message: "Why is the sky blue?",
  output: "Because it is"
})
all_res_out.value.push({
  id: 2,
  message: "Why is chess fun?",
  output: "Because it is fun"
})
all_res_out.value.push({
  id: 3,
  message: "Why am I blue?",
  output: "You are not"
})
async function sendToModel() {
  is_loading.value = true

  const response = await ollama.chat({
    model: 'blog',
    messages: [{ role: 'user', content: input_text.value }],
    stream: true
  })
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
      <div class="w-full grow" v-for="res_out in all_res_out" :key="res_out.id">
        <div class="flex h-full">
          <input class="w-1/2 h-full" type="text" v-model="input_text" />
          <p class="w-1/2 p-4 h-full">
            {{ res_out.output }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

