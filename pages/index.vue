<template>
    <div>
        <PostForm v-if="user && user.role === 'admin'" @on-success="handleFormSuccess" />

        <div v-if="loading" class="flex items-center justify-center p-4 border-b" :class="twitterBorderColor">
             <UISpinner />
        </div>

        <div v-else>
            <div v-for="post in homePosts" :key="post.id">

    <PostCard 
        v-for="post in homePosts" 
        :key="post.id" 
        :post="post" 
        :user="user"
        :allUsers="users"
    />
           </div>
        </div>
    </div>
</template>

<script setup>
import PostForm from '~/components/Post/Form.vue';
import PostCard from '~/components/Post/Card.vue';
import UISpinner from '~/components/UI/Spinner.vue';

const { twitterBorderColor } = useTailwindConfig();
const { useAuthUser } = useAuth(); // We already have this

const homePosts = ref([]);
const users = ref([]);
const loading = ref(false);
const user = useAuthUser(); // We get the logged-in user here

async function getPosts() {
    loading.value = true;
    try {
        const [postsResponse, usersResponse] = await Promise.all([
            useApiFetch('/api/posts/'),
            useApiFetch('/api/users/')
        ]);

        const posts = postsResponse.data.value.posts;
        users.value = usersResponse.data.value.data;

        const likePromises = posts.map(post => useApiFetch(`/api/likes/post/${post.id}`));
        const commentPromises = posts.map(post => useApiFetch(`/api/comments/post/${post.id}`));

        const [likeResponses, commentResponses] = await Promise.all([Promise.all(likePromises), Promise.all(commentPromises)]);

        const enrichedPosts = posts.map((post, index) => {
            return {
                ...post,
                likes: likeResponses[index].data.value.likes || [],
                comments_count: commentResponses[index].data.value.comments.length || 0
            };
        });
        
        homePosts.value = enrichedPosts;

    } catch (error) {
        console.log(error);
    } finally {
        loading.value = false;
    }
}

function getAuthor(post) {
    if (!post || !users.value) return null;
    return users.value.find(u => u.id === post.user_id);
}

function handleFormSuccess() {
    getPosts();
}

onBeforeMount(() => {
    getPosts();
});
</script>