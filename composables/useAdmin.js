// composables/useAdmin.js
export const useAdmin = () => {
    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()

    const activateUser = (username) => {
        const formData = new FormData();
        formData.append('username', username);

        return $fetch('/api/users/activate', {
            method: 'POST',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

     const deactivateUser = (username) => {
        const formData = new FormData();
        formData.append('username', username);

        // Artık '/deactivate' endpoint'ine POST isteği gönderiyoruz
        return $fetch(`/api/users/deactivate`, {
            method: 'POST',
            body: formData,
            baseURL: 'http://127.0.0.1:5000',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });
    }

    return {
        activateUser,
        deactivateUser
    }
}