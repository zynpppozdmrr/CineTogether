// composables/usePosts.js
export const usePosts = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const deletePost = (postId) => {
        return $fetch(`/api/posts/${postId}`, {
            method: 'DELETE',
            baseURL: apiBase,
            headers: {
                'Authorization': `Bearer ${authToken.value}`
            }
        });
    }

    return {
        deletePost
    }
}