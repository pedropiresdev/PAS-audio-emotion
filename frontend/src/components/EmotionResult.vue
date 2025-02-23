<template>
  <div v-if="emotion" class="mt-4 p-4 bg-green-100 border border-green-400 rounded-lg text-center text-green-700">
    <p class="text-lg font-semibold">Emoção detectada:</p>
    <p class="text-2xl font-bold">{{ emotion }}</p>
  </div>
</template>

<script>
export default {
  props: {
    emotion: String,
  },
};
</script>
