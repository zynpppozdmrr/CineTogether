// composables/useLikes.js
export const useLikes = () => {

    const { useAuthToken } = useAuth()
    const authToken = useAuthToken()

    const addLike = (postId) => {
        return new Promise(async (resolve, reject) => {
            try {
                const formData = new FormData();
                formData.append('post_id', postId);

                await $fetch('/api/likes/add', {
                    method: 'POST',
                    body: formData,
                    baseURL: 'http://127.0.0.1:5000',
                    headers: {
                        'Authorization': `Bearer ${authToken.value}`
                    }
                });
                resolve(true);
            } catch (error) {
                reject(error);
            }
        });
    }

    const removeLike = (postId) => {
        return new Promise(async (resolve, reject) => {
            try {
                const formData = new FormData();
                formData.append('post_id', postId);

                await $fetch('/api/likes/remove', {
                    method: 'POST',
                    body: formData,
                    baseURL: 'http://127.0.0.1:5000',
                    headers: {
                        'Authorization': `Bearer ${authToken.value}`
                    }
                });
                resolve(true);
            } catch (error) {
                reject(error);
            }
        });
    }


    return {
        addLike,
        removeLike
    }
}