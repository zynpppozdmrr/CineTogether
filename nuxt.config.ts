// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  
    compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  postcss: {
   plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }, 
  },  
  
  runtimeConfig: {
    jwtAccessSecret: process.env.JWT_ACCESS_TOKEN_SECRET,
    jwtRefreshSecret: process.env.JWT_REFRESH_TOKEN_SECRET,

    cloudinaryCloudName: process.env.CLOUDINARY_CLOUD_NAME,
    cloudinaryApiKey: process.env.CLOUDINARY_API_KEY,
    cloudinaryApiSecret: process.env.CLOUDINARY_API_SECRET,

     public: {
      rapidApiKey: process.env.NUXT_PUBLIC_RAPIDAPI_KEY,
      rapidApiHost: process.env.NUXT_PUBLIC_RAPIDAPI_HOST,
      rapidApiBaseUrl: process.env.NUXT_PUBLIC_RAPIDAPI_BASE_URL,
      apiBase: process.env.NUXT_API_BASE_URL 
    }
    
  }
})
