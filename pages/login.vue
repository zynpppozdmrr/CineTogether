<template>
    <div class="flex h-screen">
         <div 
            class="relative flex-1 hidden w-0 lg:block bg-cover bg-center" 
            :style="{ backgroundImage: `url('https://res.cloudinary.com/dxlkdp8p9/image/upload/v1749474346/bgLogin_kgvc3t.png')` }"
        >
            <div class="absolute inset-0 bg-black opacity-25"></div>
            
            
        </div>


        <div class="flex flex-col justify-center flex-1 px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
            <div class="w-full max-w-sm mx-auto lg:w-96">
                
                <div class="flex border-b border-gray-200 dark:border-gray-700 mb-6">
                    <button @click="selectedTab = 'login'" :class="tabClass('login')" class="flex-1 py-2 text-center font-medium">
                        Sign In
                    </button>
                    <button @click="selectedTab = 'register'" :class="tabClass('register')" class="flex-1 py-2 text-center font-medium">
                        Create Account
                    </button>
                </div>

                <div v-if="selectedTab === 'login'">
                    <h2 class="text-3xl font-extrabold text-gray-900 dark:text-white">Sign in to your account</h2>
                    <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
                        <div class="space-y-1">
                            <label for="login-username" class="dark:text-gray-200">Username</label>
                            <input v-model="loginData.username" id="login-username" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-purple-500 focus:border-purple-500">
                        </div>
                        <div class="space-y-1">
                            <label for="login-password" class="dark:text-gray-200">Password</label>
                            <input v-model="loginData.password" id="login-password" type="password" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-purple-500 focus:border-purple-500">
                        </div>

                        <button type="submit" :disabled="loading" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-sm text-sm font-medium text-white bg-purple-500 hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed">
                            {{ loading ? 'Signing in...' : 'Sign In' }}
                        </button>
                        <p v-if="authError" class="text-red-500 text-sm mt-2">{{ authError }}</p>
                    </form>
                </div>

                <div v-if="selectedTab === 'register'">
                     <h2 class="text-3xl font-extrabold text-gray-900 dark:text-white">Create a new account</h2>
                    <form @submit.prevent="handleRegister" class="mt-8 space-y-6">
                        <div class="space-y-1">
                            <label for="reg-username" class="dark:text-gray-200">Username</label>
                            <input v-model="registerData.username" id="reg-username" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-purple-500 focus:border-purple-500">
                        </div>
                        <div class="space-y-1">
                            <label for="reg-email" class="dark:text-gray-200">Email</label>
                            <input v-model="registerData.email" id="reg-email" type="email" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-purple-500 focus:border-purple-500">
                        </div>
                        <div class="space-y-1">
                            <label for="reg-fullname" class="dark:text-gray-200">Full Name</label>
                            <input v-model="registerData.fullName" id="reg-fullname" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-purple-500 focus:border-purple-500">
                        </div>
                         <div class="space-y-1">
                            <label for="reg-password" class="dark:text-gray-200">Password</label>
                            <input v-model="registerData.password" id="reg-password" type="password" required class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-purple-500 focus:border-purple-500">
                        </div>

                        <button type="submit" :disabled="loading" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-sm text-sm font-medium text-white bg-purple-500 hover:bg-purple-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed">
                            {{ loading ? 'Creating...' : 'Create Account' }}
                        </button>
                        <p v-if="authError" class="text-red-500 text-sm mt-2">{{ authError }}</p>
                    </form>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({ layout: 'auth' });

const selectedTab = ref('login'); // 'login' or 'register'

const { login, registerUser } = useAuth();
const loading = ref(false);
const authError = ref(null);

// Data for Login Form
const loginData = reactive({
    username: '',
    password: ''
});

// Data for Register Form
const registerData = reactive({
    username: '',
    email: '',
    password: '',
    fullName: ''
});

// Dynamic class for active tab
const tabClass = (tabName) => {
    return selectedTab.value === tabName
        ? 'border-b-2 border-purple-500 text-purple-500'
        : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300';
};

async function handleLogin() {
    loading.value = true;
    authError.value = null;
    try {
        await login({
            username: loginData.username,
            password: loginData.password
        });
        await navigateTo('/');
    } catch (error) {
        authError.value = 'Invalid username or password.';
    } finally {
        loading.value = false;
    }
}

async function handleRegister() {
    loading.value = true;
    authError.value = null;
    try {
        await registerUser(registerData);
        await login({
            username: registerData.username,
            password: registerData.password
        });
        await navigateTo('/');
    } catch (error) {
        authError.value = 'Registration failed. Username or email may already be taken.';
    } finally {
        loading.value = false;
    }
}
</script>
