<template>
     <div>
        <div class="sticky top-0 px-4 py-3 bg-white/80 backdrop-blur-md dark:bg-dim-900/80">
            <div class="flex items-center">
                <button @click="goBack" class="p-2 mr-2 rounded-full hover:bg-gray-200 dark:hover:bg-dim-800">
                    <svg class="w-6 h-6 text-gray-800 dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                </button>
                <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100">Post</h2>
            </div>
        </div>

        <div v-if="loading" class="flex items-center justify-center p-4">
            <UISpinner />
        </div>
        <div v-else>
            <PostCard v-if="post" :post="post" :author="getAuthor(post)" :user="user" />

            <PostCommentForm v-if="user" :user="user" :post="post" @on-success="handleCommentSuccess" />
            
            <PostCommentCard v-for="comment in comments" :key="comment.id" :comment="comment" :author="getAuthor(comment)" />
        </div>
    </div>
</template>

<script setup>
import PostCard from '~/components/Post/Card.vue';
import PostCommentForm from '~/components/Post/Comment/Form.vue';
import PostCommentCard from '~/components/Post/Comment/Card.vue';
import UISpinner from '~/components/UI/Spinner.vue';

const { useAuthUser } = useAuth();
const route = useRoute();
const user = useAuthUser();

const router = useRouter();

function goBack() {
    router.push('/');
}

const loading = ref(false);
const post = ref(null);
const comments = ref([]);
const users = ref([]); // Yorum yapanları bulmak için

// Sayfa yüklendiğinde verileri çek
onBeforeMount(async () => {
    loading.value = true;
    const postId = route.params.id;
    try {
        // Post'u, yorumları, kullanıcıları VE BEĞENİLERİ aynı anda çek
        const [postResponse, commentsResponse, usersResponse, likesResponse] = await Promise.all([
            useApiFetch(`/api/posts/${postId}`),
            useApiFetch(`/api/comments/post/${postId}`),
            useApiFetch('/api/users/'),
            useApiFetch(`/api/likes/post/${postId}`) // BU SATIRI EKLEDİK
        ]);

        // Gelen beğeni verisini post nesnesine ekliyoruz
        const fetchedPost = postResponse.data.value.post;
        fetchedPost.likes = likesResponse.data.value.likes || []; // BU SATIRI EKLEDİK

        post.value = fetchedPost;
        comments.value = commentsResponse.data.value.comments;
        users.value = usersResponse.data.value.data;

    } catch (error) {
        console.error("Veri alınırken hata:", error);
    } finally {
        loading.value = false;
    }
});

function getAuthor(item) { // Hem post hem de yorum için çalışır
    if (!item || !users.value) return null;
    return users.value.find(u => u.id === item.user_id);
}

// Yeni yorum yapıldığında listeyi yenile
function handleCommentSuccess(newComment) {
    comments.value.unshift(newComment);
}
</script>