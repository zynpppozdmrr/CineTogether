<template>
  <div>
    <div class="flex items-start p-4">
      <img
        :src="user?.profile_picture_url || '/default-avatar.png'"
        alt="User Profile Picture"
        class="w-10 h-10 rounded-full"
      />

      <div class="flex-1 w-full ml-4">
        <textarea
          v-model="text"
          class="w-full text-lg placeholder-gray-400 bg-transparent border-0 dark:text-white focus:ring-0"
          placeholder="What's happening?"
        ></textarea>

        <div v-if="imagePreviewUrl" class="relative mt-2">
          <img
            :src="imagePreviewUrl"
            class="w-full rounded-2xl"
            alt="Image Preview"
          />
          <button
            @click="removeSelectedImage"
            class="absolute top-2 right-2 p-1 bg-gray-800/75 rounded-full text-white hover:bg-gray-700"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div
      class="flex items-center justify-between p-2 pr-4 pl-16 border-b"
      :class="twitterBorderColor"
    >
      <div
        class="p-2 text-blue-400 rounded-full cursor-pointer hover:bg-blue-50 dark:hover:bg-dim-800"
        @click="handleImageSelectClick"
      >
        <IconPhoto class="w-6 h-6" />
        <input
          type="file"
          ref="imageInput"
          hidden
          accept="image/jpeg,image/png,image/gif"
          @change="handleFileChange"
        />
      </div>

      <button
        @click="handleFormSubmit"
        :disabled="isButtonDisabled"
        class="px-4 py-2 font-bold text-white bg-purple-500 rounded-full hover:bg-purple-600 disabled:bg-purple-300"
      >
        <span v-if="!loading">Post</span>
        <UISpinner v-else />
      </button>
    </div>
  </div>
</template>

<script setup>
import IconPhoto from "~/components/Icon/Photo.vue"; // Yeni ikonumuzu import edelim

const { twitterBorderColor } = useTailwindConfig();
const text = ref("");
const loading = ref(false);
const emits = defineEmits(["onSuccess"]);
const { useAuthUser, useAuthToken } = useAuth();
const user = useAuthUser();
const authToken = useAuthToken();

// Image upload refs
const imageInput = ref();
const selectedFile = ref(null);
const imagePreviewUrl = ref(null);

const isButtonDisabled = computed(
  () => loading.value || (!text.value && !selectedFile.value)
);

// Resim seçme ikonuna tıklanınca gizli dosya input'unu tetikler
function handleImageSelectClick() {
  imageInput.value.click();
}

// Kullanıcı bir dosya seçince çalışır
function handleFileChange(event) {
  const file = event.target.files[0];
  if (!file) return;

  selectedFile.value = file;

  // Önizleme için geçici bir URL oluşturur
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreviewUrl.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

function removeSelectedImage() {
  selectedFile.value = null;
  imagePreviewUrl.value = null;
}

async function handleFormSubmit() {
  loading.value = true;
  try {
    let uploadedImageUrl = null;

    // 1. Eğer resim seçildiyse, önce Cloudinary'e yükle
    if (selectedFile.value) {
      const cloudinaryFormData = new FormData();
      cloudinaryFormData.append("file", selectedFile.value);
      // 'upload_preset' değeri doğru görünüyor.
      cloudinaryFormData.append("upload_preset", "ml_default");

      // 'cloud_name'i sizin verdiğiniz 'dxlkdp8p9' ile güncelledik.
      const cloudinaryResponse = await $fetch(
        "https://api.cloudinary.com/v1_1/dxlkdp8p9/image/upload",
        {
          method: "POST",
          body: cloudinaryFormData,
        }
      );

      uploadedImageUrl = cloudinaryResponse.secure_url;
    }

    // 2. Kendi backend'imize post verisini gönder
    const postData = new FormData();
    postData.append("content", text.value);
    if (uploadedImageUrl) {
      postData.append("image_url", uploadedImageUrl);
    }

    await $fetch("/api/posts/create", {
      method: "POST",
      body: postData,
      baseURL: "http://127.0.0.1:5000",
      headers: {
        Authorization: `Bearer ${authToken.value}`,
      },
    });

    // Formu temizle ve anasayfayı yenile
    text.value = "";
    removeSelectedImage();
    emits("onSuccess");
  } catch (error) {
    console.error("Post oluşturma hatası:", error);
  } finally {
    loading.value = false;
  }
}
</script>
