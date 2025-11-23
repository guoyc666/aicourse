<template>
  <div class="graph-page" :class="{ 'with-detail': selectedNode && !editMode }">
    <div class="graph-container">
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
      <template v-if="!editMode">
        <el-button class="edit-btn" style="right: 164px" @click="layoutAllNodes"
          >展开所有节点</el-button
        >
        <el-button
          class="edit-btn"
          style="right: 296px"
          @click="layoutFirstLevel"
          >只展开第一层</el-button
        >
        <el-button class="edit-btn" @click="enterEditMode"
          >进入编辑模式</el-button
        >
      </template>

      <!-- 编辑模式按钮 -->
      <template v-if="editMode">
        <el-button class="edit-btn" @click="saveAndExitEdit"
          >保存修改并退出</el-button
        >
        <el-button class="edit-btn" style="top: 88px" @click="exitEdit"
          >不保存直接退出</el-button
        >
        <el-button class="edit-btn" style="top: 144px" @click="editNode"
          >编辑</el-button
        >
        <el-button class="edit-btn" style="top: 200px" @click="deleteNode"
          >删除</el-button
        >
      </template>

      <!-- 创建课程弹窗 -->
      <el-dialog
        v-model="showCourseDialog"
        title="创建课程"
        align-center
        width="400px"
        :close-on-click-modal="false"
        :show-close="false"
      >
        <el-form :model="courseForm">
          <el-form-item label="课程名称" required>
            <el-input v-model="courseForm.name" placeholder="请输入课程名称" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input
              v-model="courseForm.description"
              type="textarea"
              placeholder="可选"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button type="primary" @click="submitCourseForm">创建</el-button>
        </template>
      </el-dialog>

      <!-- 编辑节点弹窗 -->
      <el-dialog
        v-model="showEditDialog"
        title="编辑节点"
        align-center
        width="400px"
      >
        <el-form :model="editForm">
          <!-- 名称和描述 -->
          <el-form-item label="名称">
            <el-input v-model="editForm.name" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="editForm.description" type="textarea" />
          </el-form-item>

          <!-- 父节点选择（autocomplete） -->
          <el-form-item label="父节点">
            <el-autocomplete
              v-model="editForm.parentName"
              :fetch-suggestions="queryParentNode"
              placeholder="选择父节点"
              @select="handleParentSelect"
              clearable
            />
          </el-form-item>

          <!-- 子节点管理 -->
          <el-form-item label="子节点">
            <div>
              <el-tag
                v-for="child in editForm.childNodes"
                :key="child.id"
                closable
                @close="removeChildNode(child.id)"
                :disable-transitions="true"
                style="margin-right: 4px"
              >
                {{ child.name }}
              </el-tag>
              <el-button
                size="small"
                type="primary"
                @click="showAddChildDialog = true"
                >新增子节点</el-button
              >
            </div>
          </el-form-item>

          <!-- 前置节点选择（autocomplete） -->
          <el-form-item label="前置节点">
            <el-autocomplete
              v-model="editForm.prerequisiteName"
              :fetch-suggestions="queryPrerequisiteNode"
              placeholder="选择前置节点"
              @select="handlePrerequisiteSelect"
              clearable
            />
            <div>
              <el-tag
                v-for="pre in editForm.prerequisiteNodes"
                :key="pre.id"
                closable
                @close="removePrerequisiteNode(pre.id)"
                style="margin-right: 4px"
              >
                {{ pre.name }}
              </el-tag>
            </div>
          </el-form-item>

          <!-- 关联资源选择（autocomplete） -->
          <el-form-item label="关联资源">
            <el-autocomplete
              v-model="editForm.resourceName"
              :fetch-suggestions="queryResourceNode"
              placeholder="选择资源"
              @select="handleResourceSelect"
              clearable
            />
            <div>
              <el-tag
                v-for="res in editForm.resourceNodes"
                :key="res.id"
                closable
                @close="removeResourceNode(res.id)"
                style="margin-right: 4px"
              >
                {{ res.name }}
              </el-tag>
            </div>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="submitEditNode">保存</el-button>
        </template>
      </el-dialog>

      <!-- 新增子节点弹窗 -->
      <el-dialog v-model="showAddChildDialog" title="新增子节点" width="300px">
        <el-form>
          <el-form-item label="名称">
            <el-input v-model="addChildName" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="handleCancelAddChild">取消</el-button>
          <el-button
            type="primary"
            @click="addChildNodeToEditForm(addChildName)"
            >添加</el-button
          >
        </template>
      </el-dialog>
    </div>
    <Siderbar v-if="graphStore.selectedNode && !graphStore.editMode" />
    <!-- <div class="detail-panel" v-if="selectedNode && !editMode">
      <h3>{{ selectedNode.name }}</h3>
      <div v-if="selectedNode.category === 'Concept'">
        <p>掌握度：{{ selectedNode.mastery ?? "-" }}%</p>
        <p>学习进度：{{ selectedNode.progress ?? "-" }}%</p>
        <p>难度：{{ selectedNode.difficulty ?? "-" }}</p>
        <p>描述：{{ selectedNode.description ?? "-" }}</p>
      </div>
      <div v-else-if="selectedNode.category === 'Resource'">
        <p>这是一个资源</p>
      </div>
      <div v-else>
        <p>描述：{{ selectedNode.description ?? "-" }}</p>
      </div>
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from "vue";
import cytoscape from "cytoscape";
import type { ConceptNode, KnowledgeLink, KnowledgeNode } from "@/types";
import { graphAPI } from "../../api";
import { ElMessage, ElMessageBox } from "element-plus";

import {
  styles,
  concentricOptions,
  createSvgCircleProgress,
} from "./composable/useCytoscape";
import { useAnalysisStore } from "../../stores/analysisStore";
import { useGraphStore } from "../../stores/graphStore";
import Siderbar from "./Siderbar.vue";

// 状态管理
const graphStore = useGraphStore();
// 获取学生学习记录
const analysisStore = useAnalysisStore();

// 从后端获取的节点和边数据
const nodes = ref<KnowledgeNode[]>([]);
const links = ref<KnowledgeLink[]>([]);

// 创建课程弹窗相关
const showCourseDialog = ref(false);
const courseForm = ref({
  name: "",
  description: "",
});

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

// 搜索相关
const searchText = ref("");
const nodeNames = computed(() =>
  editMode.value
    ? editingNodes.value.map((n) => n.name)
    : nodes.value.map((n) => n.name)
);

// 编辑模式
const editMode = ref(false);
const editingNodes = ref<KnowledgeNode[]>([]);
const editingLinks = ref<KnowledgeLink[]>([]);

// 编辑和添加弹窗显示控制
const showEditDialog = ref(false);

const addChildName = ref("");
const showAddChildDialog = ref(false);

// 编辑和添加表单数据
const editForm = ref({
  name: "",
  description: "",
  parentName: "",
  parentId: "",
  childNodes: [] as KnowledgeNode[],
  prerequisiteName: "",
  prerequisiteNodes: [] as KnowledgeNode[],
  resourceName: "",
  resourceNodes: [] as KnowledgeNode[],
});

// 提交创建课程表单
async function submitCourseForm() {
  try {
    // 创建课程节点
    const courseNode: KnowledgeNode = {
      id: "node_" + Date.now(),
      category: "Course",
      name: courseForm.value.name,
      description: courseForm.value.description,
      depth: 0,
    };
    await graphAPI.createNode(courseNode);
    // 刷新数据
    const data = await graphAPI.fetchKnowledgeGraph();
    nodes.value = data.nodes;
    links.value = data.links;
    showCourseDialog.value = false;
    elements.value = calcElements();
    await nextTick();
    renderCytoscape();
    ElMessage.success("课程创建成功！");
  } catch (e) {
    ElMessage.error("课程创建失败，请重试！");
  }
}

// cytoscape 相关
function calcElements(layoutMode: string = "all") {
  const nodeList = editMode.value ? editingNodes.value : nodes.value;
  const linkList = editMode.value ? editingLinks.value : links.value;

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
        ...nodeList
          .filter((n) => showLinks.some((l) => l.target === n.id))
          .map((n) => ({ ...n, expanded: false }))
      );
    }
  }

  return [
    ...showNodes.map((n) => ({
      data: {
        ...n,
        img:
          n.category === "Concept"
            ? createSvgCircleProgress(
                (n as ConceptNode).progress ?? 0,
                n.depth <= 4 ? 40 - n.depth * 5 : 20
              )
            : n.category === "Resource"
            ? "/assets/resource_icon.svg"
            : "/assets/course_icon.svg",
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
  const childLinks = links.value.filter(
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
  const parentNode = nodes.value.find((pn) => pn.id === parentId);
  const parentDepth =
    parentNode && "depth" in parentNode ? parentNode.depth : undefined;
  const layerNodeCount = nodes.value.filter(
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
      const node = nodes.value.find((n) => n.id === id);
      if (node) {
        if (node.category === "Concept") {
          node.progress = analysisStore.getProgressByKnowledgeId(node.id) * 100;
          node.mastery = analysisStore.getMasteryByKnowledgeId(node.id) * 100;
        }
        cy?.add({
          group: "nodes",
          data: {
            ...node,
            expanded: false,
            img: createSvgCircleProgress(
              (node as ConceptNode).progress ?? 0,
              (node as ConceptNode).depth <= 4
                ? 40 - (node as ConceptNode).depth * 5
                : 20
            ),
          },
          position: childPositions[idx],
        });
      }
    }
  });

  // 4. 添加相关边（包含和前置）
  links.value.forEach((link) => {
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
  const sectorAngle = Math.PI / 3;

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
  const childLinks = links.value.filter(
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

function layoutAllNodes() {
  if (!cy) return;
  elements.value = calcElements("all");
  cy.json({ elements: elements.value });
  cy.layout(concentricOptions).run();
}

function layoutFirstLevel() {
  if (!cy) return;
  const currentZoom = cy.zoom();
  elements.value = calcElements("first");
  cy.json({ elements: elements.value });
  cy.layout(concentricOptions).run();
  //cy.zoom(currentZoom*1.2);
  cy.center();
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
  const node = nodes.value.find((n) => n.name === item.value);
  if (!node) return;

  // 如果节点已在 Cytoscape 实例里
  const cyNode = cy?.getElementById(node.id);
  if (cyNode && cyNode.length) {
    // 展开该节点
    if (!editMode.value && node.category === "Concept") {
      collapseNodes(node.id);
      expandNodes(node.id);
      cyNode.data("expanded", true);
    }
    // 清空之前的选中状态
    cy?.nodes().unselect();
    cyNode.select();
    selectedNode.value = { ...node };
    nextTick().then(() => {
      cy?.animate({ center: { eles: cyNode } }, { duration: 400 });
    });
  } else {
    // 节点不在画布上，递归展开
    expandToNode(node.id);
  }
}

// 递归展开到目标节点
function expandToNode(targetId: string) {
  // 1. 构造从根到目标节点的路径
  const path: string[] = [];
  let currentId: string | null = targetId;
  while (currentId) {
    path.unshift(currentId);
    const parentLink = links.value.find(
      (l) => l.target === currentId && l.relation === "包含"
    );
    currentId = parentLink ? parentLink.source : null;
  }

  // 2. 找到路径中最后一个已经在 Cytoscape 实例里的节点
  let startIdx = 0;
  for (; startIdx < path.length; startIdx++) {
    if (!cy?.getElementById(path[startIdx]!).length) {
      break;
    }
  }
  startIdx--; // 回退到最后一个已存在节点

  // 3. 从最后一个已存在节点开始依次展开
  for (let i = startIdx; i < path.length; i++) {
    expandNodes(path[i]!);
    cy?.getElementById(path[i]!).data("expanded", true);
  }

  // 4. 选中目标节点并居中
  const targetNode = cy?.getElementById(targetId);
  if (targetNode && targetNode.length) {
    // 清空之前的选中状态
    cy?.nodes().unselect();
    targetNode.select();
    selectedNode.value = { ...targetNode.data() } as KnowledgeNode;
    nextTick().then(() => {
      cy?.animate({ center: { eles: targetNode } }, { duration: 400 });
    });
  }
}

async function enterEditMode() {
  editMode.value = true;
  selectedNode.value = null; // 进入编辑模式时清空选中节点

  graphStore.unSelectNode();
  graphStore.enterEditMode();

  editingNodes.value = JSON.parse(JSON.stringify(nodes.value));
  editingLinks.value = JSON.parse(JSON.stringify(links.value));
  elements.value = calcElements();
  await nextTick();
  renderCytoscape();
  if (cy) {
    cy.autoungrabify(true); // 禁止节点拖拽
  }
}

async function saveAndExitEdit() {
  try {
    // 提交到后端
    await graphAPI.updateKnowledgeGraph(editingNodes.value, editingLinks.value);
    // 本地同步
    nodes.value = JSON.parse(JSON.stringify(editingNodes.value));
    links.value = JSON.parse(JSON.stringify(editingLinks.value));
    editMode.value = false;
    selectedNode.value = null;

    graphStore.unSelectNode();
    graphStore.exitEditMode(true);

    if (cy) {
      cy.autoungrabify(false);
    }
    layoutAllNodes();
    ElMessage.success("保存成功！");
  } catch (e) {
    ElMessage.error("保存失败，请重试！");
  }
}

function exitEdit() {
  editingNodes.value = [];
  editingLinks.value = [];
  editMode.value = false;
  selectedNode.value = null; // 退出编辑模式时清空选中节点

  graphStore.unSelectNode();
  graphStore.exitEditMode();
  if (cy) {
    cy.autoungrabify(false);
  }
  layoutAllNodes();
}

function editNode() {
  if (!selectedNode.value) {
    ElMessage.warning("请先选中节点");
    return;
  }

  // 名称和描述
  editForm.value.name = selectedNode.value.name ?? "";
  editForm.value.description = selectedNode.value.description ?? "";

  // 父节点
  const parentLink = editingLinks.value.find(
    (l) => l.target === selectedNode.value!.id && l.relation === "包含"
  );
  if (parentLink) {
    const parentNode = editingNodes.value.find(
      (n) => n.id === parentLink.source
    );
    editForm.value.parentName = parentNode?.name ?? "";
    editForm.value.parentId = parentNode?.id ?? "";
  } else {
    editForm.value.parentName = "";
    editForm.value.parentId = "";
  }

  // 子节点
  const childLinks = editingLinks.value.filter(
    (l) => l.source === selectedNode.value!.id && l.relation === "包含"
  );
  editForm.value.childNodes = childLinks
    .map((l) => editingNodes.value.find((n) => n.id === l.target))
    .filter(Boolean) as KnowledgeNode[];

  // 前置节点
  const preLinks = editingLinks.value.filter(
    (l) => l.target === selectedNode.value!.id && l.relation === "前置"
  );
  editForm.value.prerequisiteNodes = preLinks
    .map((l) => editingNodes.value.find((n) => n.id === l.source))
    .filter(Boolean) as KnowledgeNode[];
  editForm.value.prerequisiteName = "";

  // 关联资源
  const resLinks = editingLinks.value.filter(
    (l) => l.source === selectedNode.value!.id && l.relation === "关联"
  );
  editForm.value.resourceNodes = resLinks
    .map((l) => editingNodes.value.find((n) => n.id === l.target))
    .filter(Boolean) as KnowledgeNode[];
  editForm.value.resourceName = "";

  showEditDialog.value = true;
}

// 自动补全编辑窗口中的父节点选择
function queryParentNode(query: string, cb: (results: any[]) => void) {
  const list = editingNodes.value
    .filter(
      (n) =>
        (n.category === "Course" || n.category === "Concept") &&
        n.id !== selectedNode.value?.id
    )
    .filter((n) => n.name.includes(query))
    .map((n) => ({ value: n.name, id: n.id }));
  cb(list);
}
// 处理父节点选择
function handleParentSelect(item: { value: string; id: string }) {
  editForm.value.parentName = item.value;
  editForm.value.parentId = item.id;
}
// 自动补全编辑窗口中前置节点选择
function queryPrerequisiteNode(query: string, cb: (results: any[]) => void) {
  const list = editingNodes.value
    .filter((n) => n.category === "Concept" && n.id !== selectedNode.value?.id)
    .filter((n) => n.name.includes(query))
    .map((n) => ({ value: n.name, id: n.id }));
  cb(list);
}
// 处理前置节点选择
function handlePrerequisiteSelect(item: { value: string; id: string }) {
  if (!editForm.value.prerequisiteNodes.some((n) => n.id === item.id)) {
    const node = editingNodes.value.find((n) => n.id === item.id);
    if (node) editForm.value.prerequisiteNodes.push(node);
  }
  editForm.value.prerequisiteName = "";
}
// 移除前置节点
function removePrerequisiteNode(id: string) {
  editForm.value.prerequisiteNodes = editForm.value.prerequisiteNodes.filter(
    (n) => n.id !== id
  );
}

function queryResourceNode(query: string, cb: (results: any[]) => void) {
  const list = editingNodes.value
    .filter((n) => n.category === "Resource")
    .filter((n) => n.name.includes(query))
    .map((n) => ({ value: n.name, id: n.id }));
  cb(list);
}
function handleResourceSelect(item: { value: string; id: string }) {
  if (!editForm.value.resourceNodes.some((n) => n.id === item.id)) {
    const node = editingNodes.value.find((n) => n.id === item.id);
    if (node) editForm.value.resourceNodes.push(node);
  }
  editForm.value.resourceName = "";
}
function removeResourceNode(id: string) {
  editForm.value.resourceNodes = editForm.value.resourceNodes.filter(
    (n) => n.id !== id
  );
}

// 子节点管理
function removeChildNode(id: string) {
  editForm.value.childNodes = editForm.value.childNodes.filter(
    (n) => n.id !== id
  );
}
function handleCancelAddChild() {
  showAddChildDialog.value = false;
  addChildName.value = ""; // 取消时也清空输入框
}
function addChildNodeToEditForm(name: string) {
  const newId = "node_" + Date.now();
  const parentDepth =
    selectedNode.value &&
    "depth" in selectedNode.value &&
    typeof selectedNode.value.depth === "number"
      ? selectedNode.value.depth
      : 1;
  const newNode: KnowledgeNode = {
    id: newId,
    name,
    category: "Concept",
    depth: parentDepth + 1,
    description: "",
  };
  editForm.value.childNodes.push(newNode);
  showAddChildDialog.value = false;
  addChildName.value = "";
}

async function submitEditNode() {
  const nodeId = selectedNode.value?.id;
  if (!nodeId) return;

  // 1. 修改节点基本信息
  const idx = editingNodes.value.findIndex((n) => n.id === nodeId);
  if (idx !== -1) {
    editingNodes.value[idx]!.name = editForm.value.name;
    editingNodes.value[idx]!.description = editForm.value.description;
  }

  // 2. 父节点关系（只允许一个父节点，“包含”关系）
  // 先移除原有父节点的“包含”边
  editingLinks.value = editingLinks.value.filter(
    (l) => !(l.target === nodeId && l.relation === "包含")
  );
  // 添加新的父节点边（如果有选择）
  if (editForm.value.parentId) {
    editingLinks.value.push({
      source: editForm.value.parentId,
      target: nodeId,
      relation: "包含",
    });
  }

  // 3. 子节点关系（全部替换为当前表单中的子节点，“包含”关系）
  // 先移除原有所有子节点的“包含”边，并递归删除这些子节点及其后代
  const oldChildLinks = editingLinks.value.filter(
    (l) => l.source === nodeId && l.relation === "包含"
  );
  const toDeleteIds: string[] = [];
  function collectDescendants(id: string) {
    toDeleteIds.push(id);
    editingLinks.value
      .filter((l) => l.source === id && l.relation === "包含")
      .forEach((l) => collectDescendants(l.target));
  }
  // 找出被移除的子节点（不在新 childNodes 列表里的）
  oldChildLinks.forEach((l) => {
    if (!editForm.value.childNodes.some((child) => child.id === l.target)) {
      collectDescendants(l.target);
    }
  });
  // 删除这些节点和相关边
  editingNodes.value = editingNodes.value.filter(
    (n) => !toDeleteIds.includes(n.id)
  );
  editingLinks.value = editingLinks.value.filter(
    (l) => !toDeleteIds.includes(l.source) && !toDeleteIds.includes(l.target)
  );
  // 再添加新的子节点边
  editForm.value.childNodes.forEach((child) => {
    if (!editingNodes.value.find((n) => n.id === child.id)) {
      editingNodes.value.push(child);
    }
    editingLinks.value.push({
      source: nodeId,
      target: child.id,
      relation: "包含",
    });
  });

  // 4. 前置节点关系（全部替换为当前表单中的前置节点，“前置”关系）
  editingLinks.value = editingLinks.value.filter(
    (l) => !(l.target === nodeId && l.relation === "前置")
  );
  editForm.value.prerequisiteNodes.forEach((pre) => {
    editingLinks.value.push({
      source: pre.id,
      target: nodeId,
      relation: "前置",
    });
  });

  // 5. 关联资源关系（全部替换为当前表单中的资源，“关联”关系）
  editingLinks.value = editingLinks.value.filter(
    (l) => !(l.source === nodeId && l.relation === "关联")
  );
  editForm.value.resourceNodes.forEach((res) => {
    editingLinks.value.push({
      source: nodeId,
      target: res.id,
      relation: "关联",
    });
  });

  showEditDialog.value = false;
  ElMessage.success("修改成功");
  elements.value = calcElements();
  await nextTick();
  renderCytoscape();
}

function deleteNode() {
  if (!selectedNode.value) {
    ElMessage.warning("请先选中节点");
    return;
  }
  ElMessageBox.confirm(
    "你确定要删除该节点吗？删除该节点将同步删除其所有子节点。",
    "删除确认",
    {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
    }
  )
    .then(() => {
      // 删除节点及其所有子节点
      const toDeleteIds: string[] = [];
      function collectDescendants(id: string) {
        toDeleteIds.push(id);
        editingLinks.value
          .filter((l) => l.source === id && l.relation === "包含")
          .forEach((l) => collectDescendants(l.target));
      }
      collectDescendants(selectedNode.value!.id);

      // 删除节点
      editingNodes.value = editingNodes.value.filter(
        (n) => !toDeleteIds.includes(n.id)
      );
      // 删除相关边
      editingLinks.value = editingLinks.value.filter(
        (l) =>
          !toDeleteIds.includes(l.source) && !toDeleteIds.includes(l.target)
      );

      selectedNode.value = null;
      ElMessage.success("删除成功");
      layoutAllNodes();
    })
    .catch(() => {
      // 用户取消，无操作
    });
}

function highlightNodeAndRelated(node: cytoscape.NodeSingular) {
  cy?.nodes().removeClass("highlight");
  cy?.nodes().removeClass("fade");
  node.addClass("highlight");
  node.connectedEdges().addClass("highlight");
  node.connectedEdges().connectedNodes().addClass("highlight");
  cy?.nodes().not(".highlight").addClass("fade");
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
    graphStore.selectNode(nodeData.id);

    // 给选中节点及其相关节点添加高亮，其他节点淡出
    highlightNodeAndRelated(evt.target);

    // 如果当前选中节点不是它，直接选中并展开
    if (!selectedNode.value || selectedNode.value.id !== nodeData.id) {
      selectedNode.value = { ...nodeData };
      await nextTick();
      cy?.animate({ center: { eles: evt.target } }, { duration: 400 });
      // 默认展开
      if (
        !editMode.value &&
        nodeData.category === "Concept" &&
        !nodeData.expanded
      ) {
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
      graphStore.unSelectNode();
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
    const percent = node.data("progress") ?? 0;
    node.data(
      "img",
      createSvgCircleProgress(
        percent,
        node.data("depth") <= 4 ? 40 - node.data("depth") * 5 : 20,
        true,
        node.data("mastery") ?? 0
      )
    );
    node.addClass("hover");
  });

  cy.on("mouseout", "node", (evt) => {
    const node = evt.target;
    const percent = node.data("progress") ?? 0;
    node.data(
      "img",
      createSvgCircleProgress(
        percent,
        node.data("depth") <= 4 ? 40 - node.data("depth") * 5 : 20,
        false
      )
    );
    node.removeClass("hover");
  });
  // 保证缩放比例不太大
  if (cy.zoom() > 3) {
    cy.zoom(3);
    cy.center();
  }
}

onMounted(async () => {
  const data = await graphAPI.fetchKnowledgeGraph();
  console.log("Fetched graph data:", data);
  nodes.value = data.nodes;
  links.value = data.links;

  // 检查是否有根节点
  const hasCourseNode = nodes.value.some((n) => n.category === "Course");
  if (!nodes.value.length || !hasCourseNode) {
    showCourseDialog.value = true;
    return;
  }

  // 为每个非根节点赋值 progress 和 mastery
  nodes.value.forEach((n) => {
    if (n.category === "Concept") {
      (n as ConceptNode).progress =
        analysisStore.getProgressByKnowledgeId(n.id) * 100;
      (n as ConceptNode).mastery =
        analysisStore.getMasteryByKnowledgeId(n.id) * 100;
    }
  });

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
.detail-panel {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 30%;
  background: #f7f7f7;
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
  z-index: 20;
}
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
