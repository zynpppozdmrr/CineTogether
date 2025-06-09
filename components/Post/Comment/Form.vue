<template>
    <div class="p-4 border-t border-b dark:border-gray-700">
        <textarea v-model="text" class="w-full p-2 bg-gray-100 dark:bg-dim-400 dark:text-gray-300 rounded-lg focus:outline-none" placeholder="Post your reply..."></textarea>
        <div class="text-right mt-2">
            <button @click="submitComment" :disabled="!text.trim()" class="px-4 py-2 font-bold text-white bg-purple-500 rounded-full hover:bg-purple-600 disabled:bg-purple-300">
                Reply
            </button>
        </div>
    </div>
</template>

<script setup>
const text = ref('');
const emits = defineEmits(['onSuccess']);
const props = defineProps({
    post: { type: Object, required: true }
});
const { useAuthToken } = useAuth();
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

async function submitComment() {
    if (!text.value) return;

    try {
        const formData = new FormData();
        formData.append('post_id', props.post.id);
        formData.append('text', text.value);

        const response = await $fetch('/api/comments/create', {
            method: 'POST',
            body: formData,
            baseURL: apiBase,
            headers: { 'Authorization': `Bearer ${useAuthToken().value}` }
        });
        
        emits('onSuccess', response.comment);
        text.value = '';

    } catch (error) {
        console.error("Comment could not be sent:", error);
    }
}
</script>