<template>
    <div class="p-4 border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-dim-800 cursor-pointer" :class="defaultTransition" @click="navigateToPost">
        <div class="flex">
            <div class="flex-shrink-0 mr-4">
                 <img :src="props.author.profile_picture_url || '/default-avatar.png'" class="w-12 h-12 rounded-full" alt="profile">
            </div>

            <div class="flex-1">
                <div class="flex items-center space-x-1">
                    <p class="font-bold text-gray-900 dark:text-white">{{ props.author.full_name || props.author.username }}</p>
                    <p class="text-sm text-gray-500">@{{ props.author.username }}</p>
                    <p class="text-sm text-gray-500">·</p>
                    <p class="text-sm text-gray-500">{{ timeAgo(props.post.created_at) }}</p>
                </div>

                <p class="mt-2 text-gray-800 dark:text-gray-300">{{ props.post.content }}</p>

                <div v-if="props.post.image_url" class="my-3 mr-2 border rounded-2xl dark:border-gray-700">
                    <img :src="props.post.image_url" class="w-full rounded-2xl" />
                </div>

                <div class="flex items-center mt-4 space-x-16">
                    <div class="flex items-center space-x-2 group">
                         <IconChat class="w-5 h-5 text-gray-500 group-hover:text-blue-400" />
                        <p class="text-sm text-gray-500 group-hover:text-blue-400">{{ props.post.comments_count }}</p>
                    </div>

                    <div @click.stop.prevent="handleLike" class="flex items-center space-x-2 group cursor-pointer">
                         <IconHeart class="w-5 h-5 text-gray-500 group-hover:text-red-400" :class="{'text-red-500': isLiked}" />
                        <p class="text-sm text-gray-500 group-hover:text-red-400" :class="{'text-red-500': isLiked}">{{ likeCount }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useTimeAgo } from '~/composables/useTimeAgo'
import IconChat from '~/components/Icon/Chat.vue'
import IconHeart from '~/components/Icon/Heart.vue'

const { defaultTransition } = useTailwindConfig()
const { addLike, removeLike } = useLikes()
const router = useRouter()
const timeAgo = useTimeAgo

const props = defineProps({
    post: { type: Object, required: true },
    author: { type: Object, required: true },
    user: { type: Object, required: true }
})

const likeCount = ref(props.post.likes?.length || 0)

const isLiked = computed(() => {
    if (!props.post.likes) return false
    return props.post.likes.some(like => like.user_id === props.user.id)
})

async function handleLike() {
    if (isLiked.value) {
        await removeLike(props.post.id)
    } else {
        await addLike(props.post.id)
    }

    const likedIndex = props.post.likes.findIndex(like => like.user_id === props.user.id);
    if (likedIndex !== -1) {
        props.post.likes.splice(likedIndex, 1);
        likeCount.value--;
    } else {
        props.post.likes.push({ user_id: props.user.id });
        likeCount.value++;
    }
}

function navigateToPost() {
    router.push(`/post/${props.post.id}`)
}
</script>