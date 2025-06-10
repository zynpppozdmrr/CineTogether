<template>
    <div v-if="isVisible">
        <NuxtLink :to="`/post/${post.id}`" class="block p-4 border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-dim-900/50" :class="defaultTransition">
            <div class="flex">
                <div class="flex-shrink-0 mr-4">
                    <NuxtLink :to="`/profile/${author.username}`" @click.stop>
                        <img :src="author.profile_picture_url || '/default-avatar.png'" class="w-12 h-12 rounded-full hover:opacity-90" alt="profile">
                    </NuxtLink>
                </div>
                <div class="flex-1">
                    <div class="flex items-center space-x-1">
                        <NuxtLink :to="`/profile/${author.username}`" @click.stop>
                            <FullNameDisplay 
                            :user="author"
                             outerClass="font-bold text-gray-900 dark:text-white hover:underline"
                            />
                        </NuxtLink>
                        <p class="text-sm text-gray-500">@{{ author.username }}</p>
                        <p class="text-sm text-gray-500">·</p>
                        <p class="text-sm text-gray-500">{{ timeAgo(post.created_at) }}</p>
                    </div>
                    <p class="mt-1 text-gray-800 dark:text-gray-300 whitespace-pre-wrap">{{ post.content }}</p>
                    <div v-if="post.image_url" class="my-3 border rounded-2xl dark:border-gray-700">
                        <img :src="post.image_url" class="w-full h-auto max-h-96 object-cover rounded-2xl" />
                    </div>

                    <div class="flex items-center justify-between mt-3">
                        <div class="flex items-center space-x-20">
                            <div @click.stop.prevent class="flex items-center text-gray-400 group">
                                 <IconChat class="w-5 h-5 group-hover:text-purple-400" />
                                <p class="ml-1 text-sm group-hover:text-purple-400">{{ post.comments_count }}</p>
                            </div>
                             <div @click.stop.prevent="handleLike" class="flex items-center text-gray-400 group cursor-pointer">
                                 <IconHeart class="w-5 h-5 group-hover:text-red-400" :class="{'fill-current text-red-500': isLiked}" />
                                <p class="ml-1 text-sm group-hover:text-red-400" :class="{'text-red-500': isLiked}">{{ likeCount }}</p>
                            </div>
                        </div>
                        
                        <div v-if="user && user.role === 'admin'" class="flex items-center">
                            <div v-if="deleteConfirmationActive" class="flex items-center space-x-2">
                                <button @click.stop.prevent="handleDeletePost" class="text-xs font-bold text-red-500 hover:underline">Confirm Delete</button>
                                <button @click.stop.prevent="deleteConfirmationActive = false" class="text-xs text-gray-500 hover:underline">Cancel</button>
                            </div>
                            <button v-else @click.stop.prevent="deleteConfirmationActive = true" class="p-2 text-gray-400 rounded-full hover:bg-red-50 dark:hover:bg-red-500/20 hover:text-red-500">
                                <TrashIcon class="w-5 h-5" />
                            </button>
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
import { TrashIcon } from '@heroicons/vue/outline'; // TrashIcon import
import { usePosts } from '~/composables/usePosts.js'; // Yeni composable'ı import et

const { defaultTransition } = useTailwindConfig();
const { addLike, removeLike } = useLikes();
const { deletePost } = usePosts(); // deletePost fonksiyonunu al
const timeAgo = useTimeAgo;

const isVisible = ref(true); // Kartın görünürlüğünü kontrol etmek için
const deleteConfirmationActive = ref(false); // Silme onayı durumunu kontrol etmek için

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

async function handleDeletePost() {
    try {
        await deletePost(props.post.id);
        isVisible.value = false;
    } catch (error) {
        console.error("Failed to delete post:", error);
    }
}
</script>