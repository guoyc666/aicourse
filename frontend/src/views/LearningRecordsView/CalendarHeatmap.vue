<template>
  <div class="echarts-graph">
    <div class="selector">
      <el-select v-model="calendarYear" style="width: 120px;">
        <el-option v-for="y in years" :key="y" :label="y" :value="String(y)" />
      </el-select>
      <el-select
        v-if="!isStudent"
        v-model="analysisStore.selectedStudent"
        style="width: 120px; margin-left: 16px;"
        placeholder="选择学生"
      >
        <el-option
          v-for="student in students"
          :key="student.id"
          :value="student.id"
          :label="student.name"
        />
      </el-select>
    </div>
    <div ref="chartRef" style="width:100%;height:100%;"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from "vue";
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  CalendarComponent,
  TooltipComponent,
  VisualMapComponent
} from 'echarts/components';
import { HeatmapChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { useAnalysisStore } from "../../stores/analysisStore";
import { getStudents } from "../../api/users";
import { useUserStore } from "../../stores/user";

const userStore = useUserStore();
const isStudent = userStore.hasRole("student");
const students = ref<{ id: number; name: string }[]>([]);

const chartRef = ref<HTMLDivElement | null>(null);
let myChart: echarts.ECharts | null = null;
let resizeObserver: ResizeObserver | null = null;

echarts.use([
  TitleComponent,
  CalendarComponent,
  TooltipComponent,
  VisualMapComponent,
  HeatmapChart,
  CanvasRenderer
]);

const currentYear = new Date().getFullYear();
const years = Array.from({ length: 5 }, (_, i) => currentYear - i); // 最近5年
const calendarYear = ref(currentYear);

const analysisStore = useAnalysisStore();

const option = {
  title: {
    top: 30,
    left: 'center',
    text: '学习时长追踪'
  },
  tooltip: {
    formatter: function (params: any) {
      const date = params.value[0];
      const duration = params.value[1]; // 直接就是分钟数
      return `${date}<br/>学习时长：${duration} 分钟`;
    }
  },
  visualMap: {
    min: 0,
    max: 600, // 10小时
    type: 'piecewise',
    orient: 'horizontal',
    left: 'center',
    top: 60,
    pieces: [
      { min: 240, label: '超过4小时', color: '#5070dd' },
      { min: 120, max: 240, label: '2-4 小时', color: '#718be4' },
      { min: 60, max: 120, label: '1-2 小时', color: '#94a6ea' },
      { min: 30, max: 60, label: '0.5-1 小时', color: '#b3c1f1' },
      { max: 30, label: '低于0.5小时', color: '#d4dcf7' }
    ],
  },
  calendar: {
    top: 130,
    left: 30,
    right: 30,
    cellSize: ['auto', 20],
    range: calendarYear.value,
    itemStyle: {
      borderWidth: 0.5
    },
    yearLabel: { show: true }
  },
  series: {
    type: 'heatmap',
    coordinateSystem: 'calendar',
    data: analysisStore.calendarDurationRecords
  }
};

onMounted(async () => {
  if (isStudent) {
    analysisStore.selectedStudent = userStore.user.id;
  } else {
    const res = await getStudents();
    //console.log('获取学生列表:', res);
    students.value = res;
    // 默认选第一个学生
    if (students.value.length > 0) {
      analysisStore.selectedStudent = students.value[0]!.id;
    }
  }

  await analysisStore.fetchCalendarDurations(calendarYear.value, analysisStore.selectedStudent!);
  if (!chartRef.value) return;
  myChart = echarts.init(chartRef.value);
  myChart.setOption(option);

  // 监听年份和学生变化
  watch([calendarYear, analysisStore.selectedStudent], async ([newYear, newStudent]) => {
    const year = Number((newYear as any)?.value ?? newYear ?? 0);
    const student = Number((newStudent as any)?.value ?? newStudent ?? 0);
    option.calendar.range = year;
    await analysisStore.fetchCalendarDurations(year, student);
    option.series.data = analysisStore.calendarDurationRecords;
    if (myChart) myChart.setOption(option, true);
  }, { immediate: true });

  // 监听日历格子点击事件
  myChart.on('click', function (params: any) {
    if (params.componentType === 'series' && params.seriesType === 'heatmap') {
      // params.value[0] 是日期，params.value[1] 是时长
      const date = params.value[0];
      //const duration = params.value[1];
      //console.log('点击日期:', date, '学习时长:', duration);
      analysisStore.setSelectedDay(date);
    }
  });

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
.echarts-graph{
  position: relative;
  width: 100%;
  height: 300px;
}
.selector {
  position: absolute;
  left: 40px;
  top: 60px;
  z-index: 100;
}
</style>
