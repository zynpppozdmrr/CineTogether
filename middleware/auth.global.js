export default defineNuxtRouteMiddleware((to, from) => {
  const { useAuthUser, useAuthToken } = useAuth()
  const user = useAuthUser()
  const token = useAuthToken()

  const isAuthPage = to.path === '/login'

  // 1. Eğer route bir API endpoint'ine benziyorsa (örnek: /api/...)
  if (to.path.startsWith('/api/')) {
    return // middleware müdahale etmesin
  }

  // 2. Giriş yapılmışsa ve /login sayfasına gitmeye çalışıyorsa yönlendir
  if (user.value && isAuthPage) {
    return navigateTo('/')
  }

  // 3. Giriş yapılmamışsa ve /login dışında bir sayfaya gidiyorsa yönlendir
  if (!user.value && !isAuthPage) {
    return navigateTo('/login')
  }

  // 4. Admin kontrolü
  if (to.path.startsWith('/admin')) {
    if (user.value?.role !== 'admin') {
      return navigateTo('/')
    }
  }
})
