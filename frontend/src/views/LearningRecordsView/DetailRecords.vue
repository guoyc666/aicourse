<template>
  <div class="timeline-chart">
    <div ref="chartRef" style="width:100%;height:100%;"></div>
    <div class="event-details">
      <div
        v-for="event in selectedEvents"
        :key="event.id"
        :class="['event-detail', event.id % 2 === 0 ? 'above' : 'below']"
        :style="{ left: calcLeft(event.time) }"
      >
        <strong>{{ event.time }}</strong> <br />
        时长：{{ event.duration }}分钟 <br />
        内容：{{ event.resource_name }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useAnalysisStore } from "../../stores/analysisStore";
import * as echarts from "echarts/core";
import { ScatterChart } from "echarts/charts";
import { TooltipComponent, GridComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import type { DailyEvent } from "../../types";

echarts.use([ScatterChart, TooltipComponent, GridComponent, CanvasRenderer]);

const chartRef = ref<HTMLDivElement | null>(null);
let myChart: echarts.ECharts | null = null;
let resizeObserver: ResizeObserver | null = null;

const analysisStore = useAnalysisStore();
const selectedEvents = ref<DailyEvent[]>([]);

function calcLeft(time: string) {
  const [hour, minute] = time.split(":").map(Number);
  const timeNum = hour! + (minute || 0) / 60;
  // grid 左右各10%，中间80%是时间轴
  const gridLeftPercent = 10;
  const gridRightPercent = 10;
  const gridWidthPercent = 100 - gridLeftPercent - gridRightPercent; // 80
  // time/24 映射到80%，再加左边距
  const percent = gridLeftPercent + (timeNum / 24) * gridWidthPercent;
  return `calc(${percent}% - 78px)`; // 78px为卡片宽度一半（含padding）
}

const option = {
  grid: {
    left: '10%',
    right: '10%',
    top: 40,
    bottom: 40,
    containLabel: false
  },
  xAxis: { min: 0, max: 24, type: "value", name: "时间（小时）" },
  yAxis: { min: -1, max: 1, show: false },
  series: [{
    type: "scatter",
    data: analysisStore.selectedDayRecords.map(e => {
      // time 格式 "HH:MM:SS"
      const [hour, minute] = e.time.split(":").map(Number);
      const timeNum = hour! + (minute || 0) / 60;
      return [timeNum, 0, e.duration, e.id];
    }),
    symbolSize: (d: any) => Math.min(d[2]+5,30),
  }],
  tooltip: {
    show: true,
    trigger: "item",
    formatter: function(params: any) {
      const id = params.value[3];
      const event = analysisStore.selectedDayRecords.find(e => e.id === id);
      if (!event) return "";
      return `
        <strong>${event.time}</strong><br/>
        时长：${event.duration}分钟<br/>
        内容：${event.resource_name}
      `;
    }
  }
};

// 监听 selectedDay，每次变化都刷新数据
watch(() => analysisStore.selectedDay, async (newDay) => {
  if (newDay) {
    await analysisStore.fetchSelectedDayRecords(analysisStore.selectedStudent??1);
    if (myChart) {
      myChart.setOption({
        series: [{
          data: analysisStore.selectedDayRecords.map(e => {
            const [hour, minute] = e.time.split(":").map(Number);
            const timeNum = hour! + (minute || 0) / 60;
            return [timeNum, 0, e.duration, e.id];
          })
        }]
      });
    }
    selectedEvents.value = [];
  }
}, { immediate: true });

onMounted(async () => {
  if (!chartRef.value) return;

  myChart = echarts.init(chartRef.value);
  myChart.setOption(option);

  // 点击事件：切换选中/取消
  // myChart.on("click", params => {
  //   const id = (params as any).value![3];
  //   const event = analysisStore.selectedDayRecords.find(e => e.id === id);
  //   if (!event) return;
  //   const idx = selectedEvents.value.findIndex(ev => ev.id === event.id);
  //   if (idx === -1) {
  //     selectedEvents.value.push(event);
  //   } else {
  //     selectedEvents.value.splice(idx, 1); // 再次点击则移除
  //   }
  // });

  // 监听容器大小变化
  resizeObserver = new ResizeObserver(() => {
    if (myChart) {
      myChart.resize();
    }
  });
  resizeObserver.observe(chartRef.value);
});

// 组件卸载时断开监听
onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect();
  if (myChart) {
    myChart.dispose();
    myChart = null;
  }
});
</script>

<style scoped>
.timeline-chart {
  width: 100%;
  height: 300px;
}
.event-details {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.event-detail {
  position: absolute;
  width: 140px;
  background: #fff;
  border-radius: 8px;
  padding: 8px;
  font-size: 13px;
  box-shadow: 0 2px 8px #0002;
  pointer-events: auto;
  z-index: 10;
}

.event-detail.above {
  bottom: 170px;
}
.event-detail.above::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 100%;
  transform: translateX(-50%);
  border-width: 8px;
  border-style: solid;
  border-color: #fff transparent transparent transparent;
}

.event-detail.below {
  top: 170px;
}
.event-detail.below::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 100%;
  transform: translateX(-50%);
  border-width: 8px;
  border-style: solid;
  border-color: transparent transparent #fff transparent;
}
</style>