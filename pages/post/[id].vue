<template>
    <div>
        <div class="sticky top-0 z-10 px-4 py-2 bg-white/80 backdrop-blur-md dark:bg-dim-900/80 border-b dark:border-gray-700">
            <div class="flex items-center">
                <button @click="router.back()" class="p-2 mr-4 rounded-full hover:bg-gray-100 dark:hover:bg-dim-800">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                </button>
                <h2 class="text-lg font-bold">Post</h2>
            </div>
        </div>

        <div v-if="loading" class="flex items-center justify-center p-8">
            <UISpinner />
        </div>

        <div v-else-if="post">
            <PostCard :post="post" :user="loggedInUser" :allUsers="users" />

            <PostCommentForm :user="loggedInUser" :post="post" @on-success="handleCommentSuccess" />
            
            <PostCommentCard 
                v-for="comment in comments" 
                :key="comment.id" 
                :comment="comment" 
                :allUsers="users" 
            />
        </div>

        <div v-else class="p-4 text-center text-gray-500">
            <p>Post not found.</p>
        </div>
    </div>
</template>

<script setup>
import PostCard from '~/components/Post/Card.vue';
import PostCommentForm from '~/components/Post/Comment/Form.vue';
import PostCommentCard from '~/components/Post/Comment/Card.vue';
import UISpinner from '~/components/UI/Spinner.vue';

const route = useRoute();
const router = useRouter();
const { useAuthUser } = useAuth();
const loggedInUser = useAuthUser();

const loading = ref(true);
const post = ref(null);
const comments = ref([]);
const users = ref([]); // We will fetch all users to pass them down

onBeforeMount(async () => {
    const postId = route.params.id;
    loading.value = true;
    try {
        // Fetch all necessary data in parallel
        const [postResponse, commentsResponse, usersResponse] = await Promise.all([
            useApiFetch(`/api/posts/${postId}`),
            useApiFetch(`/api/comments/post/${postId}`),
            useApiFetch('/api/users/') // Fetch all users
        ]);

        const fetchedPost = postResponse.data.value.post;
        users.value = usersResponse.data.value.data; // Store all users
        
        if (fetchedPost) {
            // Enrich the post with its likes
            const likesResponse = await useApiFetch(`/api/likes/post/${postId}`);
            fetchedPost.likes = likesResponse.data.value.likes || [];
            post.value = fetchedPost;
        }

        comments.value = commentsResponse.data.value.comments;

    } catch (error) {
        console.error("Failed to fetch page data:", error);
    } finally {
        loading.value = false;
    }
});

function handleCommentSuccess(newComment) {
    // Add the new comment to the top of the list for instant UI update
    comments.value.unshift(newComment);
}
</script>