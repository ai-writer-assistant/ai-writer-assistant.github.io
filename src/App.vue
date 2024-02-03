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
      <div class="w-full h-full flex justify-center" v-for="res_out in all_res_out" :key="res_out.id">
        <div class="h-full w-3/4 grid grid-cols-9 gap-x-4">
          <div class="bg-slate-400 rounded-2xl col-span-3 flex p-2 justify-center h-fit">
            <textarea class="w-full h-full min-h-24" type="text" v-model="res_out.message" />
            <div class="flex flex-col justify-center h-full min-h-24 m-1">
              <button class="bg-green-400 p-3 rounded-xl grow-0 disabled:bg-gray-400 w-12 h-12" :disabled="is_loading"
                @click="sendToModel(res_out.id)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              </button>
            </div>
          </div>
          <div class="col-span-6 h-full w-full">
            <p class="w-full p-4 bg-white h-full">
              {{ res_out.output }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

