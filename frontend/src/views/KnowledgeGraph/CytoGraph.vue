<template>
  <CreateCourse />
  <EditGraph v-model:elements="elements" :cy="cy" :expandToNode="expandToNode" :collapseNode="collapseNode" :selectNode="selectNode" />
  <div ref="cyRef" class="graph-canvas"></div>
  <!-- 搜索框 -->
  <div class="search-box">
    <el-autocomplete
      v-model="searchText"
      :fetch-suggestions="querySearch"
      clearable
      placeholder="搜索知识点"
      @select="handleSearchSelect"
    />
  </div>

  <!-- 工具栏 -->
  <template v-if="!graphStore.editMode">
    <el-button class="edit-btn"
      style="right: 428px"
      @click="enterEditMode"
      v-if="userStore.hasRole('teacher') || userStore.hasRole('admin')"
    >
      进入编辑模式
    </el-button>

    <el-button
      class="edit-btn"
      style="right: 296px"
      @click="layoutFirstLevel"
    >
      只展开第一层
    </el-button>

    <el-button
      class="edit-btn"
      style="right: 164px"
      @click="layoutAllNodes"
    >
      展开所有节点
    </el-button>

    <el-button
      class="edit-btn"
      @click="toggleStudyStatusMode"
    >
      {{ studyStatusMode ? "返回普通视图" : "查看学习情况" }}
    </el-button>
  </template>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from "vue";
import CreateCourse from "./CreateCourse.vue";
import EditGraph from "./EditGraph.vue";
import cytoscape from "cytoscape";

import {
  styles,
  concentricOptions,
  convertGraphToElements,
  convertElementsToGraph,
} from "./composable/useCytoscape";
import { useAnalysisStore } from "../../stores/analysisStore";
import { useGraphStore } from "../../stores/graphStore";
import { useUserStore } from "../../stores/user";
import type { CytoscapeEdge, CytoscapeElements, CytoscapeNode } from "../../types";
import { ElMessage } from "element-plus";

// 状态管理
const graphStore = useGraphStore();
// 获取学生学习记录
const analysisStore = useAnalysisStore();
// 获取用户信息
const userStore = useUserStore();

// 维护当前渲染的知识图谱
const elements = ref<CytoscapeElements>({nodes: [], edges: []});

// dom 元素引用
const cyRef = ref<HTMLDivElement | null>(null);
// Cytoscape 实例
let cy: cytoscape.Core;

// 手动控制展开节点时的每层节点距离差距
const radiusDiff = 80;

// 搜索相关
const searchText = ref("");
const nodeNames = computed(() =>
  elements.value.nodes.map((n) => n.data.name)
);

// 学习情况查看模式
const studyStatusMode = ref(false);

// cytoscape 相关
function calcElements(layoutMode: string = "all") {
  let showNodes: CytoscapeNode[] = [];
  let showedges: CytoscapeEdge[] = [];

  if (layoutMode === "all") {
    showNodes = elements.value.nodes.map((n) => ({ data: { ...n.data, expanded: true } }));
    showedges = elements.value.edges.filter(e => e.data.relation !== "关联");
  } else if (layoutMode === "first") {
    const root = elements.value.nodes.find((n) => n.data.category === "Course");
    if (root) {
      showNodes = [root];
      showedges = elements.value.edges.filter(
        (l) => l.data.source === root.data.id && l.data.relation === "包含"
      );
      showNodes.push(
        ...elements.value.nodes.filter((n) => showedges.some((l) => l.data.target === n.data.id))
                      .map((n) => ({ data: { ...n.data, expanded: false } }))
      );
      showedges = showedges.concat(
        elements.value.edges.filter(
          (l) =>
            l.data.relation === "前置" &&
            showNodes.some((n) => n.data.id === l.data.source) &&
            showNodes.some((n) => n.data.id === l.data.target)
        )
      );
    }
  }

  return {
    nodes: showNodes,
    edges: showedges,
  };
}

async function selectNode(node: cytoscape.NodeSingular) {
  if (!cy) return;
  //console.log("选中节点：", node.data());
  await graphStore.selectNode(node.id());
  // 清空之前的选中状态
  cy.nodes().unselect();
  node.select();
  cy.nodes().removeClass("highlight");
  cy.nodes().removeClass("fade");
  node.addClass("highlight");
  node.connectedEdges().addClass("highlight");
  node.connectedEdges().connectedNodes().addClass("highlight");
  cy.nodes().not(".highlight").addClass("fade");
  nextTick().then(() => {
    cy.animate({ center: { eles: node } }, { duration: 400 });
  });
}

async function unselectNode() {
  if (!cy) return;
  graphStore.unSelectNode();
  // 移除高亮和淡出效果
  cy.nodes().removeClass("highlight");
  cy.nodes().removeClass("fade");
  cy.nodes().unselect();
}

function expandNode(parentId: string) {
  if (!cy) return;
  const parentNode = cy.getElementById(parentId);
  if (parentNode.data("expanded")) return; // 已展开
  parentNode.data("expanded", true);

  // 1. 找出所有“包含”子节点
  const childedges = elements.value.edges.filter(
    (l) => l.data.source === parentId && l.data.relation === "包含"
  );
  const childNodeIds = childedges.map((l) => l.data.target);
  if (childNodeIds.length === 0) return;

  // 2. 计算位置
  // 获取根节点和父节点位置，根节点的category为Course
  const rootPos = cy
    .nodes()
    .filter((n) => n.data("category") === "Course")
    .position();
  const parentPos = parentNode.position();
  // 计算当前层节点总数（与parentId同层的节点数，也就是与父节点的depth相同的节点数）
  const childPositions = calcChildPositions(
    rootPos,
    parentPos,
    childNodeIds.length
  );

  // 3. 添加子节点
  childNodeIds.forEach((id, idx) => {
    if (!cy.getElementById(id).length) {
      const node = elements.value.nodes.find((n) => n.data.id === id);
      if (node) {
        cy.add({
          data: {
            ...node.data,
            expanded: false,
          },
          position: childPositions[idx],
        });
      }
    }
  });

  // 4. 添加相关边（包含和前置）
  elements.value.edges.forEach((l) => {
    if ((l.data.relation === "包含" && l.data.source === parentId)) {
      cy.add({
        data: {
          ...l.data,
        },
      });
    } else if (
      l.data.relation === "前置" &&
      childNodeIds.includes(l.data.source) &&
      cy.getElementById(l.data.target).length
    ) {
      cy.add({
        data: {
          ...l.data,
        },
      });
    } else if (
      l.data.relation === "前置" &&
      childNodeIds.includes(l.data.target) &&
      cy.getElementById(l.data.source).length
    ) {
      cy.add({
        data: {
          ...l.data,
        },
      });
    }
  });
}

function calcChildPositions(
  rootPos: { x: number; y: number },
  parentPos: { x: number; y: number },
  childCount: number,
) {
  const positions = [];
  // 动态调整扇区角度和半径
  const minSectorAngle = Math.PI / 4;
  const maxSectorAngle = Math.PI;
  const sectorAngle = Math.min(maxSectorAngle, minSectorAngle + childCount * (Math.PI / 18));
  const minRadius = radiusDiff;
  const radius = minRadius + Math.max(0, (childCount - 4) * 15);

  // 计算 rootPos 到 parentPos 的夹角（弧度）
  const dx = parentPos.x - rootPos.x;
  const dy = parentPos.y - rootPos.y;
  const centerAngle = Math.atan2(dy, dx);

  if (childCount === 1) {
    // 只有一个子节点，直接放在连线上
    positions.push({
      x: parentPos.x + radius * Math.cos(centerAngle),
      y: parentPos.y + radius * Math.sin(centerAngle),
    });
    return positions;
  }

  // 每个子节点夹角
  const angleStep = sectorAngle / Math.max(childCount - 1, 1);
  const startAngle = centerAngle - sectorAngle / 2;

  for (let i = 0; i < childCount; i++) {
    const angle = startAngle + i * angleStep;
    positions.push({
      x: parentPos.x + radius * Math.cos(angle),
      y: parentPos.y + radius * Math.sin(angle),
    });
  }
  return positions;
}

function collapseNode(parentId: string) {
  if (!cy) return;
  const parentNode = cy.getElementById(parentId);
  if (!parentNode.data("expanded")) return; // 已收起
  parentNode.data("expanded", false);

  // 找出所有直接子节点
  const childedges = elements.value.edges.filter(
    (l) => l.data.source === parentId && l.data.relation === "包含"
  );
  const childNodeIds = childedges.map((l) => l.data.target);

  childNodeIds.forEach((id) => {
    // 递归移除该子节点的所有后代
    collapseNode(id);
    // 移除当前子节点
    const node = cy.getElementById(id);
    if (node && node.length) {
      cy.remove(node);
    }
  });
}

async function layoutAllNodes() {
  if (!cy) return;
  await unselectNode();
  cy.json({ elements: calcElements("all") });
  cy.layout(concentricOptions).run();
  cy.center();
  // 保证缩放比例不太大
  if (cy.zoom() > 3) {
    cy.zoom(3);
    cy.center();
  }
}

async function layoutFirstLevel() {
  if (!cy) return;
  await unselectNode();
  cy.json({ elements: calcElements("first") });
  cy.layout(concentricOptions).run();
  cy.center();
  // 保证缩放比例不太大
  if (cy.zoom() > 3) {
    cy.zoom(3);
    cy.center();
  }
}

function toggleStudyStatusMode() {
  studyStatusMode.value = !studyStatusMode.value;
  if (cy) {
    if (studyStatusMode.value) {
      // 进入学习视图
      cy.nodes().forEach((node) => {
        if (node.data("category") !== "Course") {
          node.addClass("study_status_view");
        }
      });
    } else {
      // 退出学习视图
      cy.nodes().removeClass("study_status_view");
    }
  }
}

async function enterEditMode() {
  if (!userStore.hasRole('teacher') && !userStore.hasRole('admin')) {
    ElMessage.warning("只有老师和管理员才能进入编辑模式！");
    return;
  }
  graphStore.enterEditMode();
  nextTick().then(renderCytoscape);
}

// 自动补全建议
function querySearch(queryString: string, cb: (results: any[]) => void) {
  const results = nodeNames.value
    .filter((name) => name.toLowerCase().includes(queryString.toLowerCase()))
    .map((name) => ({ value: name }));
  cb(results);
}

// 选中建议时的处理
async function handleSearchSelect(item: { value: string }) {
  const node = elements.value.nodes.find((n) => n.data.name === item.value)?.data;
  if (!node) return;
  expandToNode(node.id);
  const cyNode = cy.getElementById(node.id);
  selectNode(cyNode);
}

// 递归展开到目标节点
function expandToNode(targetId: string) {
  if (!cy) return;
  const cyNode = cy.getElementById(targetId);
  if (cyNode && cyNode.length) {
    expandNode(targetId);
    return; // 已存在，无需展开
  }
  // 1. 构造从根到目标节点的路径
  const path: string[] = [];
  let currentId: string | null = targetId;
  while (currentId) {
    path.unshift(currentId);
    const parentEdge = elements.value.edges.find(
      (l) => l.data.target === currentId && l.data.relation === "包含"
    )?.data;
    currentId = parentEdge ? parentEdge.source : null;
  }

  // 2. 找到路径中最后一个已经在 Cytoscape 实例里的节点
  let startIdx = 0;
  for (; startIdx < path.length; startIdx++) {
    if (!cy.getElementById(path[startIdx]!).length) {
      break;
    }
  }
  startIdx--; // 回退到最后一个已存在节点

  // 3. 从最后一个已存在节点开始依次展开
  for (let i = startIdx; i < path.length; i++) {
    expandNode(path[i]!);
  }
}

function renderCytoscape() {
  if (!cyRef.value) return;
  // 初始化 Cytoscape
  cy = cytoscape({
    container: cyRef.value,
    elements: calcElements("all"),
    style: styles,
    layout: concentricOptions,
    boxSelectionEnabled: false,
    autoungrabify: false,
  });

  // 节点点击事件
  cy.on("tap", "node", async (evt) => {
    // 选中节点
    const nodeData = evt.target.data();

    // 如果当前选中节点不是它，直接选中并展开
    if ( graphStore.selectedNodeID !== nodeData.id) {
      expandNode(nodeData.id);
      selectNode(evt.target);
      //await nextTick();
      return;
    }

    // 如果已经选中，再触发展开/收起逻辑
    if (nodeData.category === "Concept") {
      if (nodeData.expanded) {
        collapseNode(nodeData.id);
      } else {
        expandNode(nodeData.id);
      }
    }
  });

  // 点击空白关闭详情
  cy.on("tap", (evt) => {
    if (evt.target === cy) {
      graphStore.unSelectNode();
      // 移除高亮和淡出效果
      cy.nodes().removeClass("highlight");
      cy.nodes().removeClass("fade");
    }
  });
  cy.on("select", "edge", (evt) => {
    evt.target.unselect();
  });
  cy.on("mouseover", "node", (evt) => {
    const node = evt.target;
    node.addClass("hover");
  });

  cy.on("mouseout", "node", (evt) => {
    const node = evt.target;
    node.removeClass("hover");
  });
  // 保证缩放比例不太大
  if (cy.zoom() > 3) {
    cy.zoom(3);
    cy.center();
  }
}

async function initCytoscape() {
  graphStore.editMode = false;
  await graphStore.fetchGraph();

  if (userStore.hasRole("student")) {
    await analysisStore.fetchStudentRecords();
  } else {
    await analysisStore.fetchAverageRecords();
  }

  elements.value = convertGraphToElements(
    graphStore.nodes,
    graphStore.edges,
    analysisStore.progressRecords,
    analysisStore.masteryRecords,
  );

  await nextTick();
  renderCytoscape();
  await nextTick();
}

onMounted(async () => {
  initCytoscape();

  watch(
    () => graphStore.editMode,
    async (newVal, oldVal) => {
      // 只有从 true 变为 false 时触发
      if (oldVal === true && newVal === false) {
        if (graphStore.updating) {
          const {nodes, edges} = convertElementsToGraph(elements.value);
          graphStore.nodes = nodes;
          graphStore.edges = edges;
          // 推送 elements 到后端
          await graphStore.postGraph();
          //console.log(graphStore.nodes, graphStore.edges);
          graphStore.updating = false;
        }
        // 刷新知识图谱
        initCytoscape();
      }
    }
  );

  watch(
    () => graphStore.selectedNodeID,
    () => {
      if (cy) {
        cy.resize();
      }
    }
  );
});
</script>

<style scoped>
.graph-canvas {
  width: 100%;
  height: 100%;
}
.edit-btn {
  position: absolute;
  right: 32px;
  top: 32px;
  z-index: 20;
}
.search-box {
  position: absolute;
  left: 32px;
  top: 32px;
  z-index: 30;
  width: 240px;
}
</style>