<template>
  <div>
    <div class="sticky top-0 z-10 px-4 py-2 bg-white/80 backdrop-blur-md dark:bg-dim-900/80 border-b dark:border-gray-700">
      <div class="flex items-center">
        <button @click="router.back()" class="p-2 mr-4 rounded-full hover:bg-gray-100 dark:hover:bg-dim-800">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        </button>
        <div v-if="profileUser">
          <h2 class="text-lg font-bold">{{ profileUser.full_name }}</h2>
          <p v-if="posts" class="text-sm text-gray-500">{{ posts.length }} Posts</p>
        </div>
      </div>
    </div>
    
    <div v-if="pending" class="flex items-center justify-center p-8">
      <UISpinner />
    </div>

    <div v-else-if="error || !profileUser" class="p-4 text-center text-gray-500">
      <p>Could not load profile.</p>
    </div>

    <div v-else>
      <div class="border-b dark:border-gray-700">
        <div class="p-4">
          <img :src="profileUser.profile_picture_url || '/default-avatar.png'" class="w-24 h-24 rounded-full border-4 dark:border-dim-900" />
          <div class="mt-4">
            <p class="text-xl font-bold">{{ profileUser.full_name }}</p>
            <p class="text-sm text-gray-500">@{{ profileUser.username }}</p>
          </div>
          <p class="mt-2 text-gray-800 dark:text-gray-300">{{ profileUser.bio }}</p>
        </div>
      </div>

      <div v-if="posts && posts.length > 0">
        <PostCard
          v-for="post in posts"
          :key="post.id"
          :post="post"
          :author="profileUser" 
          :user="loggedInUser"
          :allUsers="allUsers"
        />
      </div>
      <div v-else class="p-4 text-center text-gray-500">
        <p>@{{ profileUser.username }} hasn't posted yet.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import PostCard from '~/components/Post/Card.vue';
import UISpinner from '~/components/UI/Spinner.vue';

const route = useRoute();
const router = useRouter();
const { useAuthUser } = useAuth();
const loggedInUser = useAuthUser();

const username = route.params.username;

// useAsyncData is the most robust way to fetch data.
const { data, pending, error } = await useAsyncData(
  `profile-${username}`,
  async () => {
    try {
      const [userRes, postsRes, allUsersRes] = await Promise.all([
        $fetch(`/api/users/${username}`, { baseURL: 'http://127.0.0.1:5000' }),
        $fetch(`/api/posts/${username}`, { baseURL: 'http://127.0.0.1:5000' }),
        $fetch('/api/users/', { baseURL: 'http://127.0.0.1:5000' }) // We need all users for the PostCard
      ]);

      const userPosts = postsRes.posts || [];
      // Enrich posts with like/comment data before displaying
      const likePromises = userPosts.map(post => $fetch(`/api/likes/post/${post.id}`, { baseURL: 'http://127.0.0.1:5000' }));
      const commentPromises = userPosts.map(post => $fetch(`/api/comments/post/${post.id}`, { baseURL: 'http://127.0.0.1:5000' }));
      
      const likeResults = await Promise.all(likePromises);
      const commentResults = await Promise.all(commentPromises);

      const enrichedPosts = userPosts.map((post, index) => ({
        ...post,
        likes: likeResults[index].likes || [],
        comments_count: commentResults[index].comments.length || 0,
      }));

      return {
        profileUser: userRes.data,
        posts: enrichedPosts,
        allUsers: allUsersRes.data // Return all users
      };
    } catch (e) {
      console.error('Error fetching profile data:', e);
      return { profileUser: null, posts: [], allUsers: [] };
    }
  }
);

// Computed properties to safely access the data from useAsyncData
const profileUser = computed(() => data.value?.profileUser);
const posts = computed(() => data.value?.posts || []);
const allUsers = computed(() => data.value?.allUsers || []);
</script>