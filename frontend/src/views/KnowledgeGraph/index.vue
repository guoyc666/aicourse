<template>
  <div class="graph-page" :class="{ 'with-detail': graphStore.selectedNodeID && !graphStore.editMode }">
    <div class="graph-container">
      <CytoGraph /> 
    </div>
    <Siderbar v-if="graphStore.selectedNodeID && !graphStore.editMode" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";

import CytoGraph from "./CytoGraph.vue";
import Siderbar from "./Siderbar.vue";


import { useGraphStore } from "../../stores/graphStore";
import { useAnalysisStore } from "../../stores/analysisStore";

const graphStore = useGraphStore();
const analysisStore = useAnalysisStore();

onMounted(async () => {
});
</script>

<style scoped>
.graph-page {
  position: relative;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}
.graph-container {
  position: relative;
  height: 100%;
  width: 100%;
  background: #fff;
  min-width: 0;
  box-sizing: border-box;
}
.graph-page.with-detail .graph-container {
  width: 70%;
}
</style>
