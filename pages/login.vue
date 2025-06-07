<template>
    <div class="flex h-screen">
        <div class="relative flex-1 hidden w-0 lg:block bg-gray-100 dark:bg-dim-900">
            <div class="flex items-center justify-center h-full">
                <h1 class="text-6xl font-bold text-blue-500">CineTogether</h1>
            </div>
        </div>

        <div class="flex flex-col justify-center flex-1 px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
            <div class="w-full max-w-sm mx-auto lg:w-96">
                <div>
                    <h2 class="mt-6 text-3xl font-extrabold text-gray-900 dark:text-white">Sign in to your account</h2>
                </div>

                <div class="mt-8">
                    <form @submit.prevent="handleLogin" class="space-y-6">
                        <div>
                            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-200">
                                Username
                            </label>
                            <div class="mt-1">
                                <input v-model="data.username" id="username" name="username" type="text" autocomplete="username" required
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                            </div>
                        </div>

                        <div>
                            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-200">
                                Password
                            </label>
                            <div class="mt-1">
                                <input v-model="data.password" id="password" name="password" type="password" autocomplete="current-password" required
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm dark:bg-dim-400 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                            </div>
                        </div>

                        <div>
                            <button type="submit" :disabled="loading"
                                class="flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300">
                                {{ loading ? 'Signing in...' : 'Sign In' }}
                            </button>
                        </div>
                        <div v-if="loginError" class="text-red-500 text-sm mt-2">
                            {{ loginError }}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    layout: 'auth'
})

const data = reactive({
    username: '',
    password: '',
})
const loading = ref(false)
const loginError = ref(null)

const { login } = useAuth()

async function handleLogin() {
    loading.value = true
    loginError.value = null
    try {
        await login({
            username: data.username,
            password: data.password
        })
        await navigateTo('/')
    } catch (error) {
        console.error(error)
        loginError.value = 'Invalid username or password.'
    } finally {
        loading.value = false
    }
}
</script>