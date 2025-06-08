<template>
    <div v-if="author" class="border-b dark:border-gray-700">
        <NuxtLink :to="`/post/${props.post.id}`" class="block p-4 hover:bg-gray-50 dark:hover:bg-dim-900/50" :class="defaultTransition">
            <div class="flex">
                <div class="flex-shrink-0 mr-4">
                    <NuxtLink :to="`/profile/${author.username}`" @click.stop>
                        <img :src="author.profile_picture_url || '/default-avatar.png'" class="w-12 h-12 rounded-full hover:opacity-90" alt="profile">
                    </NuxtLink>
                </div>
                <div class="flex-1">
                    <div class="flex items-center space-x-1">
                        <NuxtLink :to="`/profile/${author.username}`" @click.stop>
                             <p class="font-bold text-gray-900 dark:text-white hover:underline">{{ author.full_name || author.username }}</p>
                        </NuxtLink>
                        <p class="text-sm text-gray-500">@{{ author.username }}</p>
                        <p class="text-sm text-gray-500">·</p>
                        <p class="text-sm text-gray-500">{{ timeAgo(props.post.created_at) }}</p>
                    </div>
                    <p class="mt-1 text-gray-800 dark:text-gray-300 whitespace-pre-wrap">{{ props.post.content }}</p>
                    <div v-if="props.post.image_url" class="my-3 border rounded-2xl dark:border-gray-700">
                        <img :src="props.post.image_url" class="w-full h-auto max-h-96 object-cover rounded-2xl" />
                    </div>
                    <div class="flex items-center mt-3 space-x-20">
                        <div @click.stop.prevent class="flex items-center text-gray-400 group">
                             <IconChat class="w-5 h-5 group-hover:text-purple-400" />
                            <p class="ml-1 text-sm group-hover:text-purple-400">{{ props.post.comments_count }}</p>
                        </div>
                         <div @click.stop.prevent="handleLike" class="flex items-center text-gray-400 group cursor-pointer">
                             <IconHeart class="w-5 h-5 group-hover:text-red-400" :class="{'fill-current text-red-500': isLiked}" />
                            <p class="ml-1 text-sm group-hover:text-red-400" :class="{'text-red-500': isLiked}">{{ likeCount }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </NuxtLink>
    </div>
</template>
<script setup>
import { useTimeAgo } from '~/composables/useTimeAgo.js';
import IconChat from '~/components/Icon/Chat.vue';
import IconHeart from '~/components/Icon/Heart.vue';

const { defaultTransition } = useTailwindConfig();
const { addLike, removeLike } = useLikes();
const timeAgo = useTimeAgo;

const props = defineProps({
    post: { type: Object, required: true },
    user: { type: Object, required: true },
    allUsers: { type: Array, required: true }
});

const author = computed(() => {
    if (!props.post || !props.allUsers) return null;
    return props.allUsers.find(u => u.id === props.post.user_id);
});

const likeCount = ref(props.post.likes?.length || 0);
const isLiked = computed(() => {
    if (!props.post.likes || !props.user) return false;
    return props.post.likes.some(like => like.user_id === props.user.id);
});

async function handleLike() {
    if (isLiked.value) await removeLike(props.post.id);
    else await addLike(props.post.id);
    const likedIndex = props.post.likes.findIndex(like => like.user_id === props.user.id);
    if (likedIndex !== -1) {
        props.post.likes.splice(likedIndex, 1);
        likeCount.value--;
    } else {
        props.post.likes.push({ user_id: props.user.id });
        likeCount.value++;
    }
}
</script>