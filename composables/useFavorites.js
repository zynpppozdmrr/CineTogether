// composables/useFavorites.js
export const useFavorites = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()

    // Helper function to create the request
    const makeFavoriteRequest = (endpoint, movieId) => {
        const formData = new FormData();
        formData.append('movie_id', movieId);

        return $fetch(endpoint, {
            method: 'POST',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: {
                'Authorization': `Bearer ${authToken.value}`
            }
        });
    }

    const addFavorite = (movieId) => {
        return makeFavoriteRequest('/api/favorites/add', movieId);
    }

    const removeFavorite = (movieId) => {
        return makeFavoriteRequest('/api/favorites/remove', movieId);
    }

    return {
        addFavorite,
        removeFavorite
    }
}