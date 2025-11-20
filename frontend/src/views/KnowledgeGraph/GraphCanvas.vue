<template>
  <div ref="cyRef" class="graph-canvas"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from "vue";
import cytoscape from "cytoscape";
import type { KnowledgeLink, KnowledgeNode } from "../../types";
import { useGraphStore } from "../../stores/graphStore";
import { useAnalysisStore } from "../../stores/analysisStore";

import { styles, concentricOptions } from "./composable/useCytoscape";

const graphStore = useGraphStore();
const analysisStore = useAnalysisStore();

// 画面中的元素
const elements = ref<cytoscape.ElementDefinition[]>([]);
// 选中的节点
const selectedNode = ref<KnowledgeNode | null>(null);

// dom 元素引用
const cyRef = ref<HTMLDivElement | null>(null);
// Cytoscape 实例
let cy: cytoscape.Core | null = null;

 // 手动控制展开节点时的每层节点距离差距
const radiusDiff = 100;

// 编辑模式
const editMode = ref(false);
const editingNodes = ref<KnowledgeNode[]>([]);
const editingLinks = ref<KnowledgeLink[]>([]);

// cytoscape 相关
function calcElements(layoutMode: string = "all") {
  const nodeList = editMode.value ? editingNodes.value : graphStore.nodes;
  const linkList = editMode.value ? editingLinks.value : graphStore.links;

  let showNodes: KnowledgeNode[] = [];
  let showLinks: KnowledgeLink[] = [];

  if (layoutMode === "all") {
    showNodes = nodeList.map((n) => ({ ...n, expanded: true }));
    showLinks = linkList;
  } else if (layoutMode === "first") {
    const root = nodeList.find((n) => n.category === "Course");
    if (root) {
      showNodes = [root];
      showLinks = linkList.filter(
        (l) => l.source === root.id && l.relation === "包含"
      );
      showNodes.push(
        ...nodeList.filter((n) => showLinks.some((l) => l.target === n.id))
                      .map((n) => ({ ...n, expanded: false }))
      );
    }
  }

  return [
    ...showNodes.map((n) => ({
      data: {
        ...n,
      },
    })),
    ...showLinks.map((l) => ({
      data: {
        id: `${l.source}_${l.target}`,
        ...l,
      },
    })),
  ];
}

function expandNodes(parentId: string) {
  if (!cy) return;

  // 1. 找出所有“包含”子节点
  const childLinks = graphStore.links.filter(
    (l) => l.source === parentId && l.relation === "包含"
  );
  const childNodeIds = childLinks.map((l) => l.target);
  if (childNodeIds.length === 0) return;

  // 2. 计算位置
  // 获取根节点和父节点位置，根节点的category为Course
  const rootPos = cy
    .nodes()
    .filter((n) => n.data("category") === "Course")
    .position();
  const parentPos = cy
    .nodes()
    .filter((n) => n.data("id") === parentId)
    .position();
  // 计算当前层节点总数（与parentId同层的节点数，也就是与父节点的depth相同的节点数）
  const parentNode = graphStore.nodes.find((pn) => pn.id === parentId);
  const parentDepth = parentNode && "depth" in parentNode ? parentNode.depth : undefined;
  const layerNodeCount = graphStore.nodes.filter(
    (n) => "depth" in n && n.depth === parentDepth
  ).length;
  const childPositions = calcChildPositions(
    rootPos,
    parentPos,
    childNodeIds.length,
    layerNodeCount
  );

  // 3. 添加子节点
  childNodeIds.forEach((id, idx) => {
    if (!cy?.getElementById(id).length) {
      const node = graphStore.nodes.find((n) => n.id === id);
      if (node) {
        cy?.add({
          group: "nodes",
          data: { ...node, expanded: false },
          position: childPositions[idx],
        });
      }
    }
  });

  // 4. 添加相关边（包含和前置）
  graphStore.links.forEach((link) => {
    if (
      (childNodeIds.includes(link.source) && link.relation === "前置") ||
      childNodeIds.includes(link.target)
    ) {
      const edgeId = `${link.source}_${link.target}`;
      if (!cy?.getElementById(edgeId).length) {
        cy?.add({
          group: "edges",
          data: { ...link, id: edgeId },
        });
      }
    }
  });
}

function calcChildPositions(
  rootPos: { x: number; y: number },
  parentPos: { x: number; y: number },
  childCount: number,
  layerNodeCount: number
) {
  const positions = [];

  // 计算 rootPos 到 parentPos 的夹角（弧度）
  const dx = parentPos.x - rootPos.x;
  const dy = parentPos.y - rootPos.y;
  const centerAngle = Math.atan2(dy, dx); // [-π, π]

  // 子节点均分的扇区角度（弧度）
  const sectorAngle = (2 * Math.PI) / layerNodeCount;

  // 每个子节点夹角（弧度）
  const angleStep = sectorAngle / childCount;

  // 起始角度，使子节点们居中分布在 centerAngle 附近
  const startAngle = centerAngle - (angleStep * (childCount - 1)) / 2;

  // 半径
  const radius = radiusDiff; // 可调整

  for (let i = 0; i < childCount; i++) {
    const angle = startAngle + i * angleStep;
    positions.push({
      x: parentPos.x + radius * Math.cos(angle),
      y: parentPos.y + radius * Math.sin(angle),
    });
  }
  return positions;
}

function collapseNodes(parentId: string) {
  if (!cy) return;
  // 找出所有直接子节点
  const childLinks = graphStore.links.filter(
    (l) => l.source === parentId && l.relation === "包含"
  );
  const childNodeIds = childLinks.map((l) => l.target);

  childNodeIds.forEach((id) => {
    // 递归移除该子节点的所有后代
    collapseNodes(id);
    // 移除当前子节点
    const node = cy?.getElementById(id);
    if (node && node.length) {
      cy?.remove(node);
    }
  });
}

function renderCytoscape() {
  if (!cyRef.value) return;
  // 初始化 Cytoscape
  cy = cytoscape({
    container: cyRef.value,
    elements: elements.value,
    style: styles,
    layout: concentricOptions,
    boxSelectionEnabled: false,
    autoungrabify: false,
  });

  // 节点点击事件
  cy.on("tap", "node", async (evt) => {
    // 选中节点
    const nodeData = evt.target.data();

    // 给选中节点及其相关节点添加高亮，其他节点淡出
    cy?.nodes().removeClass("highlight");
    cy?.nodes().removeClass("fade");
    evt.target.addClass("highlight");
    evt.target.connectedEdges().addClass("highlight");
    evt.target.connectedEdges().connectedNodes().addClass("highlight");
    cy?.nodes().not(".highlight").addClass("fade");

    // 如果当前选中节点不是它，直接选中并展开
    if (!selectedNode.value || selectedNode.value.id !== nodeData.id) {
      selectedNode.value = { ...nodeData };
      await nextTick();
      cy?.animate({ center: { eles: evt.target } }, { duration: 400 });
      // 默认展开
      if (!editMode.value && nodeData.category === "Concept" && !nodeData.expanded) {
        expandNodes(nodeData.id);
        evt.target.data("expanded", true);
      }
      return;
    }

    // 如果已经选中，再触发展开/收起逻辑
    if (!editMode.value && nodeData.category === "Concept") {
      const isExpanded = nodeData.expanded;
      if (isExpanded) {
        collapseNodes(nodeData.id);
        evt.target.data("expanded", false);
      } else {
        expandNodes(nodeData.id);
        evt.target.data("expanded", true);
      }
    }
  });

  // 点击空白关闭详情
  cy.on("tap", (evt) => {
    if (evt.target === cy) {
      selectedNode.value = null;
      // 移除高亮和淡出效果
      cy?.nodes().removeClass("highlight");
      cy?.nodes().removeClass("fade");
    }
  });
  cy.on("select", "edge", (evt) => {
    evt.target.unselect();
  });
  cy.on("mouseover", "node", (evt) => {
    const node = evt.target;
    // 处理悬停逻辑
    node.addClass("hover");
  });

  cy.on("mouseout", "node", (evt) => {
    const node = evt.target;
    node.removeClass("hover");
  });
  // 保证缩放比例不小于 4
  if (cy.zoom() > 4) {
    cy.zoom(4);
    cy.center();
  }
}

onMounted(async () => {
  // 从 store 获取数据
  if (graphStore.isEmpty) {
    await graphStore.fetchGraph();
  }
  elements.value = calcElements();
  await nextTick();
  renderCytoscape();
});

watch(selectedNode, () => {
  // 侧边栏出现或关闭时，强制 Cytoscape 重新适应容器
  if (cy) {
    cy.resize();
  }
});
</script>

<style scoped>
.graph-canvas {
  width: 100%;
  height: 100%;
}
</style>
