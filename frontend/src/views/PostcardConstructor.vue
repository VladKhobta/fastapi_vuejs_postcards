<template>
  <div class="row">
    <div class="col-8">
      <input type="file" @change="handleImageUpload" accept="image/*" />
      <img
        v-if="imageUrl"
        :src="imageUrl"
        ref="image"
        alt="Загруженное фото"
        @load="getImageSize"
      />
      <p>{{ imageSize }}</p>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <div class="col-2">
      <h5>Настройки названия</h5>
      <input
        v-model="titleInput"
        type="text"
        placeholder="Введите название"
        required
      />
      <label>Шрифт названия</label>
      <select id="font" v-model="titleFont" required>
        <option value="Arial">Arial</option>
        <option value="Times New Roman">Times New Roman</option>
        <option value="Courier New">Courier New</option>
      </select>

      <hr />

      <h5>Общие настройки:</h5>
      <label>Цвет</label>
      <br />
      <select v-model="textColor" required>
        <option value="black">Black</option>
        <option value="white">White</option>
        <option value="red">Red</option>
      </select>
      <br />
      <label>Соотношение сторон</label>
      <br />
      <select v-model="ratio">
        <option value="1">1</option>
        <option value="1.6">1.6</option>
        <option value="3">3</option>
      </select>
      <hr />

      <button @click="previewImage">Предпросмотр</button>
      <button @click="saveImage">Сохранить открытку</button>
    </div>
    <div class="col-2">
      <h5>Настройки послания</h5>
      <input
        v-model="textInput1"
        @input="validateInput(1)"
        type="text"
        placeholder="Введите текст"
        required
      />
      <input
        v-model="textInput2"
        @input="validateInput(2)"
        type="text"
        placeholder="Введите текст 2"
        required
      />
      <input
        v-model="textInput3"
        @input="validateInput(3)"
        type="text"
        placeholder="Введите текст 3"
        required
      />
      <input
        v-model="textInput4"
        @input="validateInput(4)"
        type="text"
        placeholder="Введите текст 4"
        required
      />
      <input
        v-model="textInput5"
        @input="validateInput(5)"
        type="text"
        placeholder="Введите текст 5"
        required
      />
      <label>Выравнивание содержания</label>
      <select v-model="align">
        <option value="L">L</option>
        <option value="C">C</option>
        <option value="R">R</option>
      </select>
      <br />
      <label>Шрифт содержания</label>
      <select id="font" v-model="textFont" required>
        <option value="Arial">Arial</option>
        <option value="Times New Roman">Times New Roman</option>
        <option value="Courier New">Courier New</option>
      </select>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      imageUrl: null,
      imageBlob: null,
      imageSize: null,
      textInput1: "",
      textInput2: "",
      textInput3: "",
      textInput4: "",
      textInput5: "",
      titleInput: "",
      align: "L",
      ratio: 1.6,
      font: "Times New Roman",
      textColor: "black",
      titleFont: "Times New Roman",
      textFont: "Times New Roman",
      maxLength: 40,
      error: "",
    };
  },
  methods: {
    handleImageUpload(event) {
      this.file = event.target.files[0];
      console.log(this.file);
    },
    getImageSize() {
      const img = this.$refs.image;
      const width = img.naturalWidth;
      const height = img.naturalHeight;
      this.imageSize = `${width}x${height}`;
    },
    async previewImage() {
      if (this.file && this.textInput1) {
        const formData = new FormData();
        formData.append("file", this.file);
        formData.append("text_list", [
          this.textInput1,
          this.textInput2,
          this.textInput3,
          this.textInput4,
          this.textInput5,
        ]);

        await axios
          .post(
            `/postcards/preview` +
              `?title=${this.titleInput}` +
              `&title_font=${this.titleFont}` +
              `&text_font=${this.textFont}` +
              `&text_align=${this.align}` +
              `&letter_color=${this.textColor}` +
              `&ratio=${this.ratio}`,
            formData,
            {
              responseType: "blob",
            }
          )
          .then((response) => {
            this.imageBlob = new Blob([response.data]);
            this.imageUrl = URL.createObjectURL(this.imageBlob);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
    async saveImage() {
      if (this.imageUrl) {
        const formData = new FormData();
        formData.append("file", this.imageBlob);
        axios
          .post("/postcards", formData)
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
    validateInput(inputNumber) {
      const input = this[`textInput${inputNumber}`];
      if (input.length > this.maxLength) {
        this.error = `Строка номер ${inputNumber}: Слишком много символов`;
        this[`textInput${inputNumber}`] = input.slice(0, this.maxLength);
      } else {
        this.error = "";
      }
    },
  },
};
</script>

<style>
.error-message {
  color: red;
}
</style>
