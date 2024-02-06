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

async function addParagraph() {
  const maxId = Math.max(...all_res_out.value.map(resOut => resOut.id))
  all_res_out.value.push({
    id: maxId + 1,
    message: "",
    output: ""
  })
}

async function dropParagraph(id: Number) {
  if (is_loading.value) {
    return
  }
  is_loading.value = true
  all_res_out.value = all_res_out.value.filter((res_out) => res_out.id !== id)
  is_loading.value = false
}

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

      <!-- Top -->
      <div class="w-full h-fit flex justify-center">
        <div class="h-fit w-3/4 grid grid-cols-9 gap-x-4">
          <div class="col-span-3 flex p-2 justify-center h-fit text-slate-100">
            <h1 class="text-2xl font-bold">Inputs</h1>
          </div>
          <div class="col-span-6 flex justify-center h-fit">
            <div class="bg-white h-12 p-2 rounded-t-full flex flex-col w-full justify-center">
              <h1 class="text-2xl font-bold text-center">Generated blog</h1>
            </div>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="w-full h-full flex justify-center" v-for="res_out in all_res_out" :key="res_out.id">
        <div class="h-full w-3/4 grid grid-cols-9 gap-x-4">
          <div class="bg-slate-400 rounded-2xl col-span-3 flex p-2 justify-center h-fit">
            <textarea class="w-full h-full min-h-24" type="text" v-model="res_out.message" />
            <div class="flex flex-col justify-center h-full min-h-24 m-1">
              <button class="bg-green-400 p-3 rounded-xl grow-0 disabled:bg-gray-400 w-12 h-12 mb-2"
                :disabled="is_loading" @click="sendToModel(res_out.id)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              </button>
              <button class="bg-red-500 p-3 rounded-xl grow-0 disabled:bg-gray-400 w-12 h-12" :disabled="is_loading"
                @click="dropParagraph(res_out.id)">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-full h-full">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
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

      <!-- Bottom -->
      <div class="w-full h-fit flex justify-center">
        <div class="h-fit w-3/4 grid grid-cols-9 gap-x-4">
          <div class="col-span-3 flex p-2 justify-center h-fit text-slate-100">
          </div>
          <div class="col-span-6 flex justify-center h-fit">
            <div class="bg-white h-12 p-2 rounded-b-full flex flex-col w-full justify-center">
            </div>
          </div>
        </div>
      </div>

      <!-- Add paragraph -->
      <div class="w-full h-fit flex justify-center">
        <div class="bg-green-400 rounded-full w-4/5 p-2 m-2 text-center font-bold" @click="addParagraph()">+ Add paragraph
        </div>

      </div>
    </div>
  </div>
</template>

