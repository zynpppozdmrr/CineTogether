<template>
    <div v-if="author" class="p-4 border-b dark:border-gray-700">
        <div class="flex space-x-3">
            <NuxtLink :to="`/profile/${author.username}`">
                <img :src="author.profile_picture_url || '/default-avatar.png'" class="w-10 h-10 rounded-full">
            </NuxtLink>
            <div class="flex-1">
                <div class="flex items-center space-x-2">
                    <NuxtLink :to="`/profile/${author.username}`">
                        <p class="font-bold dark:text-white hover:underline">{{ author.full_name }}</p>
                    </NuxtLink>
                    <p class="text-sm text-gray-500">@{{ author.username }}</p>
                    <p class="text-sm text-gray-500">·</p>
                    <p class="text-sm text-gray-500">{{ timeAgo(comment.created_at) }}</p>
                </div>
                <p class="mt-1 text-gray-800 dark:text-gray-300">{{ comment.text }}</p>
            </div>
        </div>
    </div>
</template>
<script setup>
import { useTimeAgo } from '~/composables/useTimeAgo.js';
const timeAgo = useTimeAgo;

const props = defineProps({
    comment: { type: Object, required: true },
    allUsers: { type: Array, required: true }
});

const author = computed(() => {
    return props.allUsers.find(u => u.id === props.comment.user_id);
});
</script>