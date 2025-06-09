export default defineNuxtRouteMiddleware((to, from) => {
    const { useAuthUser, useAuthToken } = useAuth()
    const user = useAuthUser()
    const token = useAuthToken()

    const isAuthPage = to.path === '/login'

    // Eğer kullanıcı giriş yapmışsa ve login sayfasına gitmeye çalışıyorsa,
    // onu anasayfaya yönlendir.
    if (user.value && isAuthPage) {
        return navigateTo('/')
    }

    // Eğer kullanıcı giriş yapmamışsa ve login sayfası dışında bir yere
    // gitmeye çalışıyorsa, onu login sayfasına yönlendir.
    if (!user.value && !isAuthPage) {
        return navigateTo('/login')
    }

     // YENİ BÖLÜM: Admin Rota Koruması
    // Eğer gidilecek yol '/admin' ile başlıyorsa
    if (to.path.startsWith('/admin')) {
        // Ve kullanıcı admin değilse, anasayfaya yönlendir.
        if (user.value?.role !== 'admin') {
            return navigateTo('/')
        }
    }
})