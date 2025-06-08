<template>
    <NuxtLink :to="`/movies/${movie.id}`" class="group block text-left">
        <div class="overflow-hidden rounded-lg bg-white dark:bg-gray-800 shadow-md hover:shadow-xl border border-gray-200 dark:border-gray-700 transition-all duration-300 ease-in-out flex flex-col h-full">
            
            <div class="aspect-[2/3] w-full bg-gray-100 dark:bg-gray-700">
                <img 
                    :src="movie.image" 
                    :alt="movie.title" 
                    class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" 
                    @error="onImageError"
                />
            </div>
            
            <div class="p-3 flex flex-col flex-grow">
                <h3 class="font-bold text-xs sm:text-xs text-gray-900 dark:text-white truncate group-hover:text-blue-600" :title="movie.title">
                    {{ movie.title }}
                </h3>
                <div class="mt-auto pt-2 flex justify-between items-center">
                    <p class="text-xs text-gray-500">{{ movie.year }}</p>
                    <div class="flex items-center">
                        <svg class="w-3 h-3 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                        <p class="ml-1 text-xs text-gray-600 dark:text-gray-400">{{ movie.rating }}</p>
                    </div>
                </div>
            </div>
        </div>
    </NuxtLink>
</template>

<script setup>
defineProps({
    movie: {
        type: Object,
        required: true
    }
});

// onImageError fonksiyonunu sizin istediğinizle güncelliyoruz.
const onImageError = (event) => {
    event.target.src = 'https://media.istockphoto.com/id/1396814518/vector/image-coming-soon-no-photo-no-thumbnail-image-available-vector-illustration.jpg?s=612x612&w=0&k=20&c=hnh2OZgQGhf0b46-J2z7aHbIWwq8HNlSDaNp2wn_iko='; 
};
</script>