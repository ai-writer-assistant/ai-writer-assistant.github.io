<script setup lang="ts">
import { ref } from "vue"

import ollama from 'ollama'
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
async function sendToModel(id: Number) {
  if (is_loading.value) {
    return
  }
  is_loading.value = true
  const _res_out = all_res_out.value.find((res_out) => res_out.id === id)
  if (!_res_out) {
    is_loading.value = false
    return
  }

  _res_out.output = ""
  const response = await ollama.chat({
    model: 'blog',
    messages: [{ role: 'user', content: _res_out.message }],
    stream: true
  })
  for await (const part of response) {
    _res_out.output += part.message.content
  }
  is_loading.value = false
}
</script>

<template>
  <div class="flex h-full">
    <div class="w-full h-full flex flex-col">
      <div class="w-full grow" v-for="res_out in all_res_out" :key="res_out.id">
        <div class="flex h-full">
          <textarea class="w-1/2 h-full" type="text" v-model="res_out.message" />
          <button class="bg-green-400 p-3 rounded-xl grow-0 disabled:bg-gray-400" :disabled="is_loading"
            @click="sendToModel(res_out.id)">Send</button>
          <p class="w-1/2 p-4 h-full">
            {{ res_out.output }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

