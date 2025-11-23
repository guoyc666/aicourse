<template>
  <div class="container">
    <div class="sider">
      <ConversationList />
    </div>
    <div class="main">
      <ChatPanel />
    </div>
  </div>
</template>

<script setup lang="ts">
import ChatPanel from "./ChatPanel.vue";
import ConversationList from "./ConversationList.vue";


</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  display: flex;
}
.sider {
  width: 280px;
  height: 100%;
  background-color: #f0f2f5;
  flex-shrink: 0;
}

.main {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  width: calc(100% - 280px);
}
</style>