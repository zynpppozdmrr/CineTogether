<template>
  <div>
   

    <div v-if="pending" class="flex items-center justify-center p-8">
      <UISpinner />
    </div>

    <div
      v-else-if="error || !profileUser"
      class="p-4 text-center text-gray-500"
    >
      <p>Could not load profile.</p>
    </div>

    <div v-else>
      <div class="border-b dark:border-gray-700 p-4">
     <div class="flex items-center justify-between">
    <img :src="profileUser.profile_picture_url || 'https://res.cloudinary.com/dxlkdp8p9/image/upload/v1749477965/default_user_lagwqj.png'" class="w-24 h-24 rounded-full border-4 dark:border-dim-900" />
    
    <div v-if="loggedInUser && profileUser" class="mt-4">
        
        <button v-if="loggedInUser.id === profileUser.id" @click="openEditModal" class="px-4 py-1.5 font-bold text-sm text-gray-800 dark:text-white bg-transparent border-2 border-gray-300 dark:border-gray-700 rounded-full hover:bg-gray-100 dark:hover:bg-dim-800">
            Edit Profile
        </button>

        <div v-else>
            <button v-if="isFollowing" @click="handleUnfollow" 
                class="group px-4 py-1.5 font-bold text-sm text-black dark:text-white bg-transparent border-2 border-gray-300 dark:border-gray-700 rounded-full hover:border-red-500 hover:bg-red-50 dark:hover:bg-red-500/10">
                <span class="group-hover:hidden">Following</span>
                <span class="hidden group-hover:block text-red-500">Unfollow</span>
            </button>
            
            <button v-else @click="handleFollow" class="px-4 py-1.5 font-bold text-sm text-white bg-black dark:bg-white dark:text-black rounded-full hover:opacity-90">
                Follow
            </button>
        </div>
    </div>
    </div>
        
        <div class="mt-4">
          <FullNameDisplay :user="profileUser" class="text-xl font-bold" />
          <p class="text-sm text-gray-500">@{{ profileUser.username }}</p>
        </div>
        <p class="mt-2 text-gray-800 dark:text-gray-300">
          {{ profileUser.bio }}
        </p>

        <div class="flex space-x-4 mt-4">
            <div class="flex items-center text-sm text-gray-500">
                <span class="font-bold text-black dark:text-white mr-1">{{ followingCount }}</span>
                <span>Following</span>
            </div>
             <div class="flex items-center text-sm text-gray-500">
                <span class="font-bold text-black dark:text-white mr-1">{{ followersCount }}</span>
                <span>Followers</span>
            </div>
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

  <ProfileEditModal
    v-if="profileUser"
    :isOpen="isEditModalOpen"
    :user="profileUser"
    @onClose="closeEditModal"
    @onSuccess="handleFormSuccess"
  />
  
</template>

<script setup>
import PostCard from "~/components/Post/Card.vue";

import UISpinner from "~/components/UI/Spinner.vue";

import { useFollows } from "~/composables/useFollows.js";

import ProfileEditModal from '~/components/Profile/EditModal.vue';
import FullNameDisplay from '@/components/FullNameDisplay.vue';

const route = useRoute();

const router = useRouter();

const { useAuthUser } = useAuth();

const { followUser, unfollowUser } = useFollows(); // unfollowUser'ı da alıyoruz

const loggedInUser = useAuthUser();

const username = route.params.username;

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const { data, pending, error, refresh } = await useAsyncData(
  `profile-${username}`,

  async () => {
    try {
      const [userRes, postsRes, allUsersRes] = await Promise.all([
        $fetch(`/api/users/${username}`, { baseURL: apiBase }),

        $fetch(`/api/posts/${username}`, { baseURL: apiBase }),

        $fetch("/api/users/", { baseURL: apiBase }),
      ]);

      const profileUser = userRes.data;

      if (!profileUser) throw new Error("User not found");

      

      // Takipçi bilgisini de çekiyoruz

      // Takipçi ve takip edilen verilerini aynı anda çekiyoruz
      const [followersRes, followingRes] = await Promise.all([
        $fetch(`/api/follows/followers/${profileUser.id}`, { baseURL: apiBase }),
        $fetch(`/api/follows/following/${profileUser.id}`, { baseURL: apiBase })
      ]);

      const userPosts = postsRes.posts || [];

      const likePromises = userPosts.map((post) =>
        $fetch(`/api/likes/post/${post.id}`, {
          baseURL: apiBase,
        })
      );

      const commentPromises = userPosts.map((post) =>
        $fetch(`/api/comments/post/${post.id}`, {
          baseURL: apiBase,
        })
      );

      const likeResults = await Promise.all(likePromises);

      const commentResults = await Promise.all(commentPromises);

      const enrichedPosts = userPosts.map((post, index) => ({
        ...post,

        likes: likeResults[index].likes || [],

        comments_count: commentResults[index].comments.length || 0,
      }));

      return {
        profileUser,

        posts: enrichedPosts,
        allUsers: allUsersRes.data,

        followers: followersRes.followers,
        following: followingRes.following

      };
    } catch (e) {
      console.error("Error fetching profile data:", e);

      return { profileUser: null, posts: [], allUsers: [], followers: [] };
    }
  }
);

const profileUser = computed(() => data.value?.profileUser);

const posts = computed(() => data.value?.posts || []);

const allUsers = computed(() => data.value?.allUsers || []);
// Takipçileri reaktif bir değişkene atıyoruz

const followers = ref(data.value?.followers || []);
const following = ref(data.value?.following || []);

const followersCount = computed(() => followers.value?.length || 0);
const followingCount = computed(() => following.value?.length || 0);
// ============== GÜNCELLENMİŞ BÖLÜM ==============

const isFollowing = computed(() => {
  if (!loggedInUser.value || !followers.value) return false;
  return followers.value.some((f) => f.follower_id === loggedInUser.value.id);
});

async function handleFollow() {
  if (!profileUser.value) return;

  try {
    await followUser(profileUser.value.id);

    // Arayüzü anında güncelle

    followers.value.push({ follower_id: loggedInUser.value.id });
  } catch (err) {
    console.error("Failed to follow user:", err);
  }
}

async function handleUnfollow() {
  if (!profileUser.value) return;

  try {
    await unfollowUser(profileUser.value.id);

    // Arayüzü anında güncelle

    const index = followers.value.findIndex(
      (f) => f.follower_id === loggedInUser.value.id
    );

    if (index !== -1) {
      followers.value.splice(index, 1);
    }
  } catch (err) {
    console.error("Failed to unfollow user:", err);
  }
}

const isEditModalOpen = ref(false);
function openEditModal() {
    isEditModalOpen.value = true;
}
function closeEditModal() {
    isEditModalOpen.value = false;
}
function handleFormSuccess() {
    closeEditModal();
    refresh(); // Sayfadaki veriyi yenilemek için useAsyncData'nın refresh fonksiyonunu çağır
}
</script>
