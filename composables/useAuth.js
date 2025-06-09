// composables/useAuth.js

export default () => {
    // 1. DEĞİŞİKLİK: Token'ı useState yerine useCookie ile saklıyoruz.
    const useAuthToken = () => useCookie('auth_token');
    const useAuthUser = () => useState('auth_user');
    const useAuthLoading = () => useState('auth_loading', () => true);
    const config = useRuntimeConfig()
    console.log("BaseURL:", config.public.apiBase);

    const setToken = (newToken) => {
        const authToken = useAuthToken();
        authToken.value = newToken;
    };

    const setUser = (newUser) => {
        const authUser = useAuthUser();
        authUser.value = newUser;
    };

    const login = ({ username, password }) => {
        return new Promise(async (resolve, reject) => {
            try {
                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);

                const data = await $fetch(`${config.public.apiBase}/api/users/login`, {
                    method: 'POST',
                    body: formData
                });

                setToken(data.access_token);
                setUser(data.user);

                resolve(true);
            } catch (error) {
                reject(error);
            }
        });
    };

     const registerUser = (registerData) => {
        return new Promise(async (resolve, reject) => {
            try {
                const formData = new FormData();
                formData.append('username', registerData.username);
                formData.append('email', registerData.email);
                formData.append('password', registerData.password);
                formData.append('full_name', registerData.fullName);

                const response = await $fetch(`${config.public.apiBase}/api/users/addUser`, {
                    method: 'POST',
                    body: formData
                });
                
                resolve(response);
            } catch (error) {
                reject(error);
            }
        });
    };

    // 2. YENİ FONKSİYON: Çıkış yapma
    const logout = () => {
        return new Promise((resolve) => {
            setToken(null);
            setUser(null);
            resolve();
        });
    };


    const refreshToken = () => {
        return new Promise(async (resolve, reject) => {
            try {
                const token = useAuthToken().value;

                // Token yoksa direkt reddet, boşuna istek atma
                if (!token) {
                    return reject('No token found');
                }
                
                // Artık useApiFetch'i kullanabiliriz veya $fetch ile devam edebiliriz
                const data = await $fetch(`${config.public.apiBase}/api/users/me`, {
                     headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                // Gelen data'nın içinde user objesi var varsayıyoruz
                setUser(data.data); 
                resolve(true);
            } catch (error) {
                // Token geçersizse veya başka bir hata olursa, çıkış yap
                logout();
                reject(error);
            }
        });
    };
    
    const initAuth = () => {
        return new Promise(async (resolve, reject) => {
            useAuthLoading().value = true;
            try {
                await refreshToken();
                resolve(true);
            } catch (error) {
                reject(error);
            } finally {
                useAuthLoading().value = false;
            }
        });
    };

    return {
        login,
        logout,
        registerUser, // Logout fonksiyonunu dışarı açtık
        initAuth,
        useAuthUser,
        useAuthToken,
        useAuthLoading
    };
};