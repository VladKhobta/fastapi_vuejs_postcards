<!-- <template>
  <div>
    <button @click="downloadImages">Выбрать открытки</button>
    <button @click="startSlideshow">Начать слайд-шоу</button>
    <div v-if="!slideshowActive">
      <div class="image-container">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="image-wrapper"
        >
          <img :src="image.url" alt="Изображение" class="small-image" />
          <button @click="toggleLike(index)" class="like-button">
            {{ image.liked ? "Убрать лайк" : "Лайк" }}
          </button>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="slideshow-container">
        <img
          v-for="(image, index) in likedImages"
          :key="index"
          class="slideshow-image"
          :src="image.url"
          :style="imageStyle(index)"
        />
      </div>
    </div>
  </div>
</template> -->

<template>
  <div>
    <button @click="downloadImages">
      Скачать и отобразить изображения
    </button>
    <div v-if="!slideshowActive">
      <div class="image-container">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="image-wrapper"
        >
          <img :src="image.url" alt="Изображение" class="small-image" />
          <div class="like-button" @click="toggleLike(index)">
            {{ image.liked ? "Убрать лайк" : "Лайк" }}
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="slideshow-container">
        <img
          v-for="(image, index) in likedImages"
          :key="index"
          class="slideshow-image"
          :src="image.url"
          :style="imageStyle(index)"
        />
      </div>
    </div>
    <button @click="toggleSlideshow">Начать слайд-шоу</button>
  </div>
</template>

<script>
import axios from "axios";
import JSZip from "jszip";

export default {
  data() {
    return {
      images: [],
      slideshowActive: false,
      slideshowInterval: null,
      currentSlideIndex: 0,
    };
  },
  methods: {
    async downloadImages() {
      try {
        // Скачайте архив с изображениями с сервера
        const response = await axios.get("/postcards/", {
          responseType: "blob",
        });

        if (response.status === 200) {
          // Разархивируйте архив с использованием JSZip
          const zip = new JSZip();
          const zipData = await zip.loadAsync(response.data);

          // Обработайте файлы из архива
          this.images = [];
          for (const fileName in zipData.files) {
            if (!zipData.files[fileName].dir) {
              const imageBlob = await zipData.files[fileName].async("blob");
              const imageUrl = URL.createObjectURL(imageBlob);
              this.images.push({ url: imageUrl });
            }
          }
        }
      } catch (error) {
        console.error("Ошибка при загрузке или обработке изображений", error);
      }
    },
    toggleLike(index) {
      // Переключение лайка для изображения с индексом index
      this.images[index].liked = !this.images[index].liked;
    },
    toggleSlideshow() {
      // Включение/выключение слайд-шоу
      this.slideshowActive = !this.slideshowActive;
      if (this.slideshowActive) {
        this.startSlideshow();
      } else {
        this.stopSlideshow();
      }
    },
    startSlideshow() {
      // Настройте интервал для автокарусели (например, 3 секунды между слайдами)
      this.slideshowInterval = setInterval(() => {
        this.nextSlide();
      }, 3000);
    },
    stopSlideshow() {
      // Остановите автокарусель
      if (this.slideshowInterval) {
        clearInterval(this.slideshowInterval);
      }
    },
    nextSlide() {
      // Переключение на следующий слайд из понравившихся изображений
      const likedImages = this.images.filter((image) => image.liked);
      if (likedImages.length > 0) {
        this.currentSlideIndex =
          (this.currentSlideIndex + 1) % likedImages.length;
      }
    },
    imageStyle(index) {
      // Стиль для каждого изображения в слайд-шоу
      return { display: index === this.currentSlideIndex ? "block" : "none" };
    },
  },
  computed: {
    likedImages() {
      // Отфильтруйте изображения, чтобы включить только понравившиеся
      return this.images.filter((image) => image.liked);
    },
  },
  beforeDestroy() {
    // Остановите автокарусель при уничтожении компонента
    this.stopSlideshow();
  },
};
</script>

<style>
.image-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.image-wrapper {
  width: calc(33.33% - 10px);
  margin-bottom: 20px;
  position: relative;
}

.small-image {
  max-width: 100%;
  height: auto;
  display: block;
}

.like-button {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
}

.slideshow-container {
  /* Стили для контейнера слайд-шоу */
}

.slideshow-image {
  /* Стили для изображений в слайд-шоу */
  max-width: 100%;
  height: auto;
  display: block;
}

.like-button {
  /* Стили для кнопки "Лайк/Убрать лайк" в контейнере слайд-шоу */
  background-color: #3498db;
  color: #fff;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
  display: block;
  margin: 0 auto; /* Центрирование кнопки "Лайк" по горизонтали */
  margin-top: 5px;
}

@keyframes fade {
  0% { opacity: 0; }
  20% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; }
}
</style>