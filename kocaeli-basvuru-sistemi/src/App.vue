<script setup>
import ConfirmDialog from 'primevue/confirmdialog';
</script>

<template>
  <div id="app">
    <ConfirmDialog />
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}
</style>
