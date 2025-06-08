<template>
    <div>
        <transition name="fade">
            <div v-if="showNotification" class="fixed top-20 right-5 bg-green-500 text-white py-2 px-4 rounded-lg shadow-lg z-50">
                {{ notificationMessage }}
            </div>
        </transition>
        

        <div v-if="pending" class="flex items-center justify-center p-8">
            <UISpinner />
        </div>

        <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="user in users" :key="user.id" class="p-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-dim-800">
                <div class="flex items-center space-x-4">
                    <img :src="user.profile_picture_url || '/default-avatar.png'" class="w-10 h-10 rounded-full" />
                    <div>
                        <p class="font-bold text-gray-900 dark:text-white">{{ user.full_name }}</p>
                        <p class="text-sm text-gray-500">@{{ user.username }}</p>
                    </div>
                </div>
                
                <div v-if="loggedInUser.id !== user.id">
                    <select @change="changeUserRole(user, $event.target.value)" :value="user.role" class="bg-gray-200 dark:bg-dim-400 border-gray-300 dark:border-gray-600 rounded-md text-sm">
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>
                <div v-else>
                    <p class="text-sm font-semibold text-blue-500">This is you</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import UISpinner from '~/components/UI/Spinner.vue';

const { useAuthUser, useAuthToken } = useAuth();
const loggedInUser = useAuthUser();
const authToken = useAuthToken();

const { data: users, pending, refresh } = await useAsyncData(
    'admin-users',
    () => $fetch('/api/users/', { baseURL: 'http://127.0.0.1:5000' }).then(res => res.data)
);

// ================== YENİ: BİLDİRİM MANTIĞI ==================
const notificationMessage = ref('');
const showNotification = ref(false);
let notificationTimer = null;
// ==========================================================

// Function to update user role
async function changeUserRole(userToUpdate, newRole) {
    try {
        const formData = new FormData();
        formData.append('role', newRole);

        await $fetch(`/api/users/${userToUpdate.username}`, {
            method: 'PUT',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });

        const userInList = users.value.find(u => u.id === userToUpdate.id);
        if (userInList) {
            userInList.role = newRole;
        }

        // ================== YENİ: BİLDİRİMİ GÖSTERME ==================
        notificationMessage.value = `User '${userToUpdate.username}' role has been updated to '${newRole}'.`;
        showNotification.value = true;

        if (notificationTimer) {
            clearTimeout(notificationTimer);
        }

        notificationTimer = setTimeout(() => {
            showNotification.value = false;
        }, 5000); // 5 saniye sonra bildirimi gizle
        // ============================================================

    } catch (error) {
        console.error("Failed to update user role:", error);
        alert("Failed to update role.");
    }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>