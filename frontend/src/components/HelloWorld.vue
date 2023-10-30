<template>
  <div>
    <!-- Загрузка фото -->
    <input type="file" @change="handleImageUpload" accept="image/*" />

    <!-- Отображение загруженного фото -->
    <img v-if="imageUrl" :src="imageUrl" alt="Загруженное фото" />

    <!-- Поле для ввода текста -->
    <input v-model="textInput" type="text" placeholder="Введите текст" />

    <!-- Кнопка для предпросмотра -->
    <button @click="previewImage">Предпросмотр</button>

    <!-- Отображение фото с текстом после предпросмотра -->
    <img v-if="finalImageUrl" :src="finalImageUrl" alt="Фото с текстом" />
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      imageUrl: null,
      textInput: "",
      finalImageUrl: null,
    };
  },
  methods: {
    handleImageUpload(event) {
      // Обработка загрузки фото и отображение его
      const file = event.target.files[0];
      this.imageUrl = URL.createObjectURL(file);
    },
    async previewImage() {
      // Отправка изображения и текста на бэкенд
      if (this.imageUrl && this.textInput) {
        const formData = new FormData();
        formData.append("image", this.imageUrl);
        formData.append("text", this.textInput);

        // Отправка запроса на бэкенд
        // Вам нужно заменить URL на свой бэкенд-сервер
        await axios
          .post("/postcards/prewiew/", formData)
          .then((response) => {
            this.finalImageUrl = request.data.finalImageUrl;
          })
          .catch((error) => {
            console.error("BAD ANSWER" + error);
          });
      }
    },
  },
};
</script>
