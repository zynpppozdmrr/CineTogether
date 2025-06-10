<template>
    <div>
        <div class="sticky top-0 z-10 px-4 py-2 bg-white/80 backdrop-blur-md dark:bg-dim-900/80 border-b dark:border-gray-700">
            <h2 class="text-xl font-bold text-gray-800 dark:text-white">Manage Users</h2>
        </div>

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
                    <NuxtLink :to="`/profile/${user.username}`">
                        <img :src="user.profile_picture_url" class="w-10 h-10 rounded-full hover:opacity-80" />
                    </NuxtLink>
                    <div>
                        <NuxtLink :to="`/profile/${user.username}`">
                            <p class="font-bold text-gray-900 dark:text-white hover:underline">{{ user.full_name }}</p>
                        </NuxtLink>
                        <p class="text-sm text-gray-500">@{{ user.username }}</p>
                    </div>
                </div>
                
                <div class="flex items-center space-x-4">
                    <div v-if="loggedInUser.id !== user.id">
                        <select @change="changeUserRole(user, $event.target.value)" :value="user.role" class="bg-gray-200 dark:bg-dim-400 border-gray-300 dark:border-gray-600 rounded-md text-sm">
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div>
                    <div v-else>
                        <p class="text-sm font-semibold text-blue-500">This is you</p>
                    </div>

                    <div v-if="loggedInUser.id !== user.id">
                        <button v-if="user.activated" @click="handleDeactivate(user)" class="px-3 py-1 text-xs font-semibold text-white bg-red-500 rounded-full hover:bg-red-600">
                            Deactivate
                        </button>
                        <button v-else @click="handleActivate(user)" class="px-3 py-1 text-xs font-semibold text-white bg-green-500 rounded-full hover:bg-green-600">
                            Activate
                        </button>
                    </div>
                    </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import UISpinner from '~/components/UI/Spinner.vue';
import { useAdmin } from '~/composables/useAdmin.js'; // Yeni composable'ı import et

const { useAuthUser, useAuthToken } = useAuth();
const { activateUser, deactivateUser } = useAdmin(); // Yeni fonksiyonları al
const loggedInUser = useAuthUser();
const authToken = useAuthToken();
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const { data: users, pending, refresh } = await useAsyncData(
    'admin-users',
    () => $fetch('/api/users/', { baseURL: apiBase }).then(res => res.data)
);

async function changeUserRole(userToUpdate, newRole) {
    try {
        const formData = new FormData();
        formData.append('role', newRole);

        await $fetch(`/api/users/${userToUpdate.username}`, {
            method: 'PUT',
            body: formData,
            baseURL: apiBase,
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });

        // Arayüzü anında güncellemek için listedeki kullanıcının rolünü değiştir
        const userInList = users.value.find(u => u.id === userToUpdate.id);
        if (userInList) {
            userInList.role = newRole;
        }

        // Başarı bildirimi göster
        triggerNotification(`User '${userToUpdate.username}' role has been updated to '${newRole}'.`);

    } catch (error) {
        console.error("Failed to update user role:", error);
        alert("Failed to update role.");
        // Hata durumunda dropdown'ı eski haline getirmek için sayfayı yenilemek iyi bir fikir olabilir
        refresh();
    }
}


// ================== YENİ FONKSİYONLAR ==================
async function handleDeactivate(userToUpdate) {
    try {
        await deactivateUser(userToUpdate.username);
        userToUpdate.activated = false; // Arayüzü anında güncelle
        triggerNotification(`User '${userToUpdate.username}' has been deactivated.`);
    } catch (error) {
        console.error("Failed to deactivate user:", error);
        alert("Action failed. The backend might require a password for this operation.");
    }
}

async function handleActivate(userToUpdate) {
    try {
        await activateUser(userToUpdate.username);
        userToUpdate.activated = true; // Arayüzü anında güncelle
        triggerNotification(`User '${userToUpdate.username}' has been activated.`);
    } catch (error) {
        console.error("Failed to activate user:", error);
        alert("Action failed.");
    }
}

// Bildirim gösterme fonksiyonu (mevcut)
const notificationMessage = ref('');
const showNotification = ref(false);
let notificationTimer = null;
function triggerNotification(message) {
    notificationMessage.value = message;
    showNotification.value = true;
    if (notificationTimer) clearTimeout(notificationTimer);
    notificationTimer = setTimeout(() => {
        showNotification.value = false;
    }, 4000);
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