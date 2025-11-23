<template>
  <div class="records-layout">
    <CalendarHeatmap />
    <DetailRecords />
  </div>
</template>

<script setup lang="ts">
import CalendarHeatmap from './CalendarHeatmap.vue';
import DetailRecords from './DetailRecords.vue';
</script>

<style scoped>
.records-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #ffffff;
  justify-content: center;
  align-items: center;
  gap: 32px; 
}
</style>