<template>
  <NuxtLink :to="to" class="flex items-center p-3 text-black rounded-full w-full hover:bg-gray-200 dark:hover:bg-dim-200 dark:text-white" :class="defaultTransition">
    <div class="w-7 h-7">
      <div v-if="active">
        <slot name="activeIcon"></slot>
      </div>
      <div v-else>
        <slot name="icon"></slot>
      </div>
    </div>
    <div class="ml-4 text-xl hidden xl:block" :class="{ 'font-bold': active }">
      <slot name="name"></slot>
    </div>
  </NuxtLink>
</template>

<script setup>
const { defaultTransition } = useTailwindConfig()

defineProps({
  to: {
    type: String,
    required: true
  },
  active: {
    type: Boolean,
    default: false
  }
})
</script>