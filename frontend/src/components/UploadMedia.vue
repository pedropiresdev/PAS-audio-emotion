<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-300 via-purple-300 to-pink-300 p-4">
    <div class="w-full max-w-md p-6 bg-white rounded-lg shadow-xl border border-gray-200">
      <h2 class="text-2xl font-bold text-center text-indigo-700 mb-4">Upload de Áudio/Vídeo</h2>

      <!-- Input para upload -->
      <label class="block w-full cursor-pointer border border-dashed border-indigo-400 rounded-lg p-4 text-center text-indigo-600 bg-indigo-50 hover:bg-indigo-100">
        <input type="file" accept="audio/*,video/*" @change="handleFileChange" class="hidden" />
        <span v-if="!file">Clique para selecionar um arquivo</span>
        <span v-else class="text-indigo-700">{{ file.name }}</span>
      </label>

      <!-- Botão de envio -->
      <button @click="handleUpload" :disabled="uploading || !file"
              class="w-full mt-4 bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 disabled:bg-gray-400 transition duration-300">
        {{ uploading ? "Enviando..." : "Enviar" }}
      </button>

      <!-- Barra de progresso -->
      <div v-if="uploading" class="w-full bg-gray-300 rounded-full h-3 mt-3 overflow-hidden">
        <div class="bg-gradient-to-r from-green-400 to-green-600 h-3 rounded-full" :style="{ width: uploadProgress + '%' }"></div>
      </div>

      <p v-if="message" class="text-sm text-center text-gray-700 mt-2 font-medium">{{ message }}</p>

      <!-- Exibe o resultado da análise -->
      <EmotionResult :emotion="emotionResult" />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import EmotionResult from "./EmotionResult.vue";

export default {
  components: { EmotionResult },

  setup() {
    const file = ref(null);
    const uploading = ref(false);
    const message = ref("");
    const uploadProgress = ref(0);
    const emotionResult = ref("");

    // Captura o arquivo selecionado
    const handleFileChange = (event) => {
      const selectedFile = event.target.files[0];
      if (selectedFile && (selectedFile.type.startsWith("audio") || selectedFile.type.startsWith("video"))) {
        file.value = selectedFile;
        message.value = "";
      } else {
        message.value = "Por favor, selecione um arquivo de áudio ou vídeo válido.";
        file.value = null;
      }
    };

    // Envia o arquivo para o backend
    const handleUpload = async () => {
      if (!file.value) {
        message.value = "Nenhum arquivo selecionado.";
        return;
      }

      uploading.value = true;
      uploadProgress.value = 0;
      const formData = new FormData();
      formData.append("file", file.value);

      try {
        const response = await fetch("http://localhost:8000/upload", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          message.value = "Upload realizado com sucesso!";
          emotionResult.value = data.emotion; // Captura o resultado da análise
        } else {
          message.value = "Erro no upload. Tente novamente.";
        }
      } catch (error) {
        message.value = "Erro ao conectar com o servidor.";
      }

      uploading.value = false;
    };

    return {file, uploading, message, uploadProgress, emotionResult, handleFileChange, handleUpload};
  },
};
</script>