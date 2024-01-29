<script setup lang="ts">
import { ref } from "vue"

const input_text = ref<string>("")

</script>

<template>
  <div class="flex bg-slate-600">
    <input class="h-screen w-full" type="text" v-model="input_text" />
    <div class="w-full">
      <p>
        {{ input_text }}
      </p>
    </div>
  </div>
</template>

