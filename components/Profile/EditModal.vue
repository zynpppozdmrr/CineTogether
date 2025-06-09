<template>
    <UIModal :isOpen="props.isOpen" @on-close="handleClose">
        <div class="p-4">
            <h2 class="text-xl font-bold mb-4 dark:text-white">Edit Profile</h2>
            <form @submit.prevent="submitForm">
                <div class="space-y-4">

                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Profile Picture</label>
                        <div class="mt-2 flex items-center space-x-4">
                            <img :src="imagePreviewUrl || user.profile_picture_url || '/default-avatar.png'" class="w-20 h-20 rounded-full object-cover">
                            <button type="button" @click="handleImageSelectClick" class="px-3 py-2 bg-white dark:bg-dim-700 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50">
                                Change
                            </button>
                            <input type="file" ref="imageInput" hidden accept="image/jpeg,image/png" @change="handleFileChange" />
                        </div>
                    </div>

                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Full Name</label>
                        <input type="text" v-model="formData.full_name" id="name" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    </div>

                    <div>
                        <label for="bio" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Bio</label>
                        <textarea v-model="formData.bio" id="bio" rows="3" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500"></textarea>
                    </div>

                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">New Password (optional)</label>
                        <input type="password" v-model="formData.password" id="password" placeholder="Leave blank to keep current password" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    </div>

                </div>
                <div class="mt-6 flex justify-end space-x-3">
                    <button type="button" @click="handleClose" class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 dark:bg-dim-700 dark:text-gray-200">Cancel</button>
                    <button type="submit" :disabled="loading" class="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-md hover:bg-purple-700 disabled:opacity-50">
                        <span v-if="!loading">Save</span>
                        <UISpinner v-else />
                    </button>
                </div>
            </form>
        </div>
    </UIModal>
</template>

<script setup>
import UISpinner from '~/components/UI/Spinner.vue';

const props = defineProps({
    isOpen: { type: Boolean, required: true },
    user: { type: Object, required: true }
});
const emits = defineEmits(['onClose', 'onSuccess']);

const { useAuthToken } = useAuth();
const authToken = useAuthToken();
const loading = ref(false);
const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

// Form data
const formData = ref({
    full_name: props.user.full_name || '',
    bio: props.user.bio || '',
    password: '',
    profile_picture_url: props.user.profile_picture_url
});

// Image upload state
const imageInput = ref();
const selectedFile = ref(null);
const imagePreviewUrl = ref(null);

function handleImageSelectClick() {
    imageInput.value.click();
}

function handleFileChange(event) {
    const file = event.target.files[0];
    if (!file) return;
    selectedFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => { imagePreviewUrl.value = e.target.result; };
    reader.readAsDataURL(file);
}

async function submitForm() {
    loading.value = true;
    try {
        let newProfilePictureUrl = formData.value.profile_picture_url;

        // 1. If a new image is selected, upload to Cloudinary first
        if (selectedFile.value) {
            const cloudinaryFormData = new FormData();
            cloudinaryFormData.append('file', selectedFile.value);
            cloudinaryFormData.append('upload_preset', 'ml_default'); // Your upload preset

            const cloudinaryResponse = await $fetch(`https://api.cloudinary.com/v1_1/dxlkdp8p9/image/upload`, {
                method: 'POST',
                body: cloudinaryFormData
            });
            newProfilePictureUrl = cloudinaryResponse.secure_url;
        }

        // 2. Send updated data to your backend
        const backendFormData = new FormData();
        backendFormData.append('full_name', formData.value.full_name);
        backendFormData.append('bio', formData.value.bio);
        if (newProfilePictureUrl) {
            backendFormData.append('profile_picture_url', newProfilePictureUrl);
        }
        if (formData.value.password) {
            backendFormData.append('password', formData.value.password);
        }

        await $fetch(`/api/users/${props.user.username}`, {
            method: 'PUT',
            body: backendFormData,
            baseURL: apiBase,
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });

        emits('onSuccess');
    } catch (error) {
        console.error("Failed to update profile:", error);
    } finally {
        loading.value = false;
    }
}

function handleClose() {
    emits('onClose');
}

// Watch for user prop changes to reset form data if needed
watch(() => props.user, (newUser) => {
    if (newUser) {
        formData.value.full_name = newUser.full_name || '';
        formData.value.bio = newUser.bio || '';
        formData.value.profile_picture_url = newUser.profile_picture_url;
        formData.value.password = '';
        imagePreviewUrl.value = null;
        selectedFile.value = null;
    }
});
</script>