<template>
    <div v-if="author" class="p-4 border-b dark:border-gray-700">
        <div class="flex">
            <img :src="author.profile_picture_url || '/default-avatar.png'" class="w-10 h-10 rounded-full mr-3">
            <div class="flex-1">
                <div class="flex items-center space-x-1">
                    <p class="font-bold dark:text-white">{{ author.full_name }}</p>
                    <p class="text-sm text-gray-500">@{{ author.username }}</p>
                    <p class="text-sm text-gray-500">·</p>
                    <p class="text-sm text-gray-500">{{ timeAgo(comment.created_at) }}</p>
                </div>
                <p class="text-gray-800 dark:text-gray-300">{{ comment.text }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useTimeAgo } from '~/composables/useTimeAgo.js';
const timeAgo = useTimeAgo;

defineProps({
    comment: { type: Object, required: true },
    author: { type: Object, required: true }
});
</script>