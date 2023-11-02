<template>
  <div>
    <button @click="downloadImages">Просмотреть все заготовки</button>
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
      <div
        v-for="(slide, index) in likedImages"
        :key="index"
      >
        <transition name="slide-fade" mode="out-in">
          <div class="slideshow-image" v-show="index === currentSlideIndex">
            <img :src="slide.url" alt="Слайд" />
          </div>
        </transition>
      </div>
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
        const response = await axios.get("/postcards/", {
          responseType: "blob",
        });

        if (response.status === 200) {
          const zip = new JSZip();
          const zipData = await zip.loadAsync(response.data);

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
      this.slideshowInterval = setInterval(() => {
        this.nextSlide();
      }, 3000);
    },
    stopSlideshow() {
      if (this.slideshowInterval) {
        clearInterval(this.slideshowInterval);
      }
    },
    nextSlide() {
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
      return this.images.filter((image) => image.liked);
    },
  },
  beforeDestroy() {
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
  background-color: #3498db;
  color: #fff;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
  display: block;
  margin: 0 auto;
  margin-top: 5px;
}

.like-button:hover {
  background-color: #2684c7;
}
.slideshow-image {
  max-width: 100%;
  height: auto;
  display: block;
  position: relative;
}

</style>
