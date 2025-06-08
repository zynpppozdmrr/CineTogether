// composables/useWatched.js
export const useWatched = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()

    const markAsWatched = (movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);

        return $fetch('/api/watched/add', {
            method: 'POST',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

    const removeFromWatched = (movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);

        return $fetch('/api/watched/remove', {
            method: 'POST',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

    return {
        markAsWatched,
        removeFromWatched
    }
}