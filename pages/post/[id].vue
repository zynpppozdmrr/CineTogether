<template>
    <div>
        

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

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

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