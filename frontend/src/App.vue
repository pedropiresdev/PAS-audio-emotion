<template>
  <div id="app">
    <UploadMedia />
  </div>
</template>

<script>
import UploadMedia from "./components/UploadMedia.vue";

export default {
  components: {
    UploadMedia,
  },
};
</script>

<style>
/* Estilos globais */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(to right, #a18cd1, #fbc2eb);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>
