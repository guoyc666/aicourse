<template>
  <!-- 编辑模式按钮 -->
  <template v-if="graphStore.editMode">
    <el-button class="edit-btn" @click="graphStore.exitEditMode(true)"
      >保存修改并退出</el-button
    >
    <el-button class="edit-btn" style="top: 88px" @click="graphStore.exitEditMode(false)"
      >不保存直接退出</el-button
    >
    <el-button class="edit-btn" style="top: 144px" @click="startEdit"
      >编辑</el-button
    >
    <el-button class="edit-btn" style="top: 200px" @click="addChildNode"
      >添加子节点</el-button
    >
    <el-button class="edit-btn" style="top: 256px" @click="deleteNode"
      >删除</el-button
    >
  </template>

  <!-- 编辑节点弹窗 -->
  <el-dialog
    v-model="showEditDialog"
    title="编辑节点"
    align-center
    width="400px"
  >
    <el-form
      ref="editFormRef"
      :model="editForm"
      :rules="rules"
    >
      <!-- 名称和描述 -->
      <el-form-item label="名称" prop="name">
        <el-input v-model="editForm.name" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="editForm.description" type="textarea" />
      </el-form-item>
      <!-- 父节点选择 -->
      <el-form-item label="父节点" v-if="!showAddChildDialog" prop="parentId">
        <el-select v-model="editForm.parentId" placeholder="选择父节点" clearable>
          <el-option
            v-for="node in parentNodeList"
            :key="node.id"
            :label="node.name"
            :value="node.id"
          />
        </el-select>
      </el-form-item>
      <!-- 前置节点选择（autocomplete） -->
      <el-form-item label="前置节点">
        <div style="display: flex; gap: 8px; width: 100%;">
          <el-select v-model="editForm.prerequisiteID" placeholder="选择前置节点" clearable>
            <el-option
              v-for="node in preNodeList"
              :key="node.id"
              :label="node.name"
              :value="node.id"
            />
          </el-select>
          <el-button @click="handlePrerequisiteSelect">添加</el-button>
        </div>
        <div>
          <el-tag
            v-for="(name, id) in filteredPrerequisiteNodes"
            :key="id"
            closable
            @close="removePrerequisiteNode(String(id))"
            style="margin-right: 4px"
          >
            {{ name }}
          </el-tag>
        </div>
      </el-form-item>
      <!-- 关联资源选择（autocomplete） -->
      <el-form-item label="关联资源">
        <div style="display: flex; gap: 8px; width: 100%;">
          <el-select v-model="editForm.resourceID" placeholder="选择关联资源" clearable>
            <el-option
              v-for="node in resNodeList"
              :key="node.id"
              :label="node.name"
              :value="node.id"
            />
          </el-select>
          <el-button @click="handleResourceSelect">添加</el-button>
        </div>
        <div>
          <el-tag
            v-for="(name, id) in editForm.resourceNodes"
            :key="id"
            closable
            @close="removeResourceNode(id)"
            style="margin-right: 4px"
          >
            {{ name }}
          </el-tag>
        </div>
      </el-form-item>
      <el-form-item>
        <el-button @click="handleCancelEdit">取消</el-button>
        <el-button type="primary" @click="submitForm(editFormRef)">保存</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>

  <!-- 添加子节点弹窗 -->
  <el-dialog
    v-model="showAddChildDialog"
    title="添加子节点"
    align-center
    width="400px"
  >
    <el-form>
      <el-form-item label="名称">
        <el-input v-model="addChildName" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="addChildDescription" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button @click="showAddChildDialog = false">取消</el-button>
        <el-button type="primary" @click="startEditChildNode">下一步</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, nextTick, computed } from "vue";
import cytoscape from "cytoscape";
import type { CytoscapeElements, CytoscapeNode } from '../../types';
import { ElMessage, ElMessageBox } from "element-plus";
import { useGraphStore } from "../../stores/graphStore";
import type { FormInstance } from 'element-plus'

const editFormRef = ref<FormInstance>()

const props = defineProps<{
  elements: CytoscapeElements;
  cy: cytoscape.Core;
  expandToNode: (targetId: string) => void;
  collapseNode: (targetId: string) => void;
  selectNode: (nodeID: string) => void;
  removeNode: (nodeID: string) => void;
}>()
const emit = defineEmits(['update:elements'])

// 状态管理
const graphStore = useGraphStore();

// 编辑和添加弹窗显示控制
const showEditDialog = ref(false);

const showAddChildDialog = ref(false);

// 编辑和添加表单数据
const editForm = ref({
  name: "",
  description: "",
  parentId: "",
  prerequisiteID: "",
  prerequisiteNodes: {} as Record<string, string>,
  resourceID: "",
  resourceNodes: {} as Record<string, string>,
});
const parentNodeList = ref<{ id: string; name: string }[]>([]);

// 递归收集所有子节点 id
function collectChildIds(nodeId: string, edges: CytoscapeElements["edges"]): string[] {
  const result: string[] = [];
  function dfs(id: string) {
    edges
      .filter((e) => e.data.source === id && e.data.relation === "包含")
      .forEach((e) => {
        result.push(e.data.target);
        dfs(e.data.target);
      });
  }
  dfs(nodeId);
  return result;
}

const collectAncestorIds = (nodeId: string, edges: CytoscapeElements["edges"]) => {
  const result: string[] = [];
  function dfs(id: string) {
    const parentEdge = edges.find(e => e.data.target === id && e.data.relation === "包含");
    if (parentEdge) {
      result.push(parentEdge.data.source);
      dfs(parentEdge.data.source);
    }
  }
  dfs(nodeId);
  return result;
};

function updateParentNodeList(selectedId: string) {
  // 找出所有以自身为前置节点的节点 id
  const nodesWithSelfAsPrerequisite = props.elements.edges
    .filter(e => e.data.source === selectedId && e.data.relation === "前置")
    .map(e => e.data.target);
  const childIds = collectChildIds(selectedId, props.elements.edges);
  parentNodeList.value = props.elements.nodes
    .filter(
      (n) =>
        n.data.id !== selectedId &&
        !childIds.includes(n.data.id) &&
        !nodesWithSelfAsPrerequisite.includes(n.data.id)
    )
    .map((n) => ({
      id: n.data.id,
      name: n.data.name,
    }));
}

const preNodeList = computed(() => {
  if (!graphStore.selectedNodeID) return [];
  const newParentId = editForm.value.parentId;
  const selectedNodeId = graphStore.selectedNodeID;
  const childIds = collectChildIds(selectedNodeId, props.elements.edges);
  const ancestorIds = collectAncestorIds(newParentId, props.elements.edges);

  // 找出所有以自身为前置节点的节点 id
  const nodesWithSelfAsPrerequisite = props.elements.edges
    .filter(e => e.data.source === selectedNodeId && e.data.relation === "前置")
    .map(e => e.data.target);

  const excludeIds = new Set([
    selectedNodeId,
    ...childIds,
    newParentId,
    ...ancestorIds,
    ...nodesWithSelfAsPrerequisite,
  ]);
  return props.elements.nodes
    .filter((n) => n.data.category === "Concept" && !excludeIds.has(n.data.id))
    .map((n) => ({
      id: n.data.id,
      name: n.data.name,
    }));
});

const filteredPrerequisiteNodes = computed(() => {
  const newParentId = editForm.value.parentId;
  const ancestorIds = collectAncestorIds(newParentId, props.elements.edges);
  const excludeIds = new Set([
    ...ancestorIds,
    newParentId,
  ]);
  const result: Record<string, string> = {};
  for (const [id, name] of Object.entries(editForm.value.prerequisiteNodes)) {
    if (!excludeIds.has(id)) {
      result[id] = name;
    }
  }
  return result;
});

const resNodeList = computed(() => {
  return graphStore.resources.map((r) => ({
    id: r.id,
    name: r.name,
  }));
});

const rules = {
  name: [{ required: true, message: "名称不能为空", trigger: "change" }],
  parentId: [{ required: true, message: "父节点不能为空", trigger: "change" }],
};

// 添加子节点相关
const addChildName = ref("");
const addChildDescription = ref("");
function addChildNode() {
  if (!graphStore.selectedNodeID) {
    ElMessage.warning("请先选中节点");
    return;
  }
  addChildName.value = "";
  addChildDescription.value = "";
  showAddChildDialog.value = true;
}
async function startEditChildNode() {
  if (!graphStore.selectedNodeID) {
    ElMessage.error("未选中父节点，无法添加子节点");
    return;
  }
  if (!addChildName.value) {
    ElMessage.warning("请填写子节点名称");
    return;
  }
  // 添加新节点
  const parentId = graphStore.selectedNodeID;
  const parentNode = props.elements.nodes.find(n => n.data.id === parentId);
  const newNodeId = `node_${Date.now()}`;
  const newNodeData: CytoscapeNode = {
    data: {
      id: newNodeId,
      name: addChildName.value,
      description: addChildDescription.value,
      category: "Concept",
      depth: parentNode!.data.depth + 1,
      expanded: true,
      img: "",
    },
  };
  props.elements.nodes.push(newNodeData);
  // 添加包含边
  const newEdgeData = {
    source: parentId,
    target: newNodeId,
    relation: "包含",
  };
  props.elements.edges.push({ data: newEdgeData });
  
  props.collapseNode(parentId);
  props.expandToNode(parentId);

  // 关闭添加子节点弹窗
  showAddChildDialog.value = false;
  emit('update:elements', props.elements);

  ElMessage.success("创建成功！请编辑新节点信息");
  props.selectNode(newNodeId);

  // 打开编辑弹窗
  startEdit();
}

function clearEditForm() {
  editForm.value.name = "";
  editForm.value.description = "";
  editForm.value.parentId = "";
  editForm.value.prerequisiteID = "";
  editForm.value.prerequisiteNodes = {};
  editForm.value.resourceID = "";
  editForm.value.resourceNodes = {};
}
function handleCancelEdit() {
  clearEditForm();
  showEditDialog.value = false;
}
function startEdit() {
  if (!graphStore.selectedNodeID) {
    ElMessage.warning("请先选中节点");
    return;
  }
  const selectedNode = props.elements.nodes.find(
    (n) => n.data.id === graphStore.selectedNodeID
  );  
  if (!selectedNode) {
    ElMessage.warning("请先选中节点");
    return;
  }
  if (selectedNode.data.category === "Course") {
    ElMessage.warning("课程节点不可编辑");
    return;
  }

  clearEditForm();

  // 名称和描述
  editForm.value.name = selectedNode.data.name;
  editForm.value.description = selectedNode.data.description || "";

  // 父节点
  updateParentNodeList(selectedNode.data.id);
  editForm.value.parentId = props.elements.edges.find(
    (l) => l.data.target === selectedNode.data.id && l.data.relation === "包含"
  )?.data.source || "";

  // 前置节点
  const preLinks = props.elements.edges.filter(
    (l) => l.data.target === selectedNode.data.id && l.data.relation === "前置"
  );
  preLinks.forEach((l) => {
    const preNode = props.elements.nodes.find(
      (n) => n.data.id === l.data.source
    );
    if (preNode) {
      editForm.value.prerequisiteNodes[preNode.data.id] = preNode.data.name;
    }
  });

  // 关联资源
  const resLinks = props.elements.edges.filter(
    (l) => l.data.source === selectedNode.data.id && l.data.relation === "关联"
  );
  resLinks.forEach((l) => {
    const resNode = graphStore.resources.find(
      (r) => r.id === l.data.target
    );
    if (resNode) {
      editForm.value.resourceNodes[resNode.id] = resNode.name;
    }
  });

  showEditDialog.value = true;
}

// 处理前置节点选择
function handlePrerequisiteSelect() {
  if (!editForm.value.prerequisiteID) return;
  const node = preNodeList.value.find(n => n.id === editForm.value.prerequisiteID);
  if (node && !editForm.value.prerequisiteNodes[node.id]) {
    editForm.value.prerequisiteNodes[node.id] = node.name;
  }
}
// 移除前置节点
function removePrerequisiteNode(id: string) {
  delete editForm.value.prerequisiteNodes[id];
}


// 处理关联资源选择
function handleResourceSelect() {
  if (!editForm.value.resourceID) return;
  const node = resNodeList.value.find(n => n.id === editForm.value.resourceID);
  if (node && !editForm.value.resourceNodes[node.id]) {
    editForm.value.resourceNodes[node.id] = node.name;
  }
}
// 移除关联资源
function removeResourceNode(id: string) {
  delete editForm.value.resourceNodes[id];
}



async function submitForm(formEl: FormInstance | undefined) {
  if (!formEl) return;
  await formEl.validate((valid) => {
    if (valid) {
      // 提交修改
      saveNodeEdits();
    } else {
      ElMessage.error("表单填写有误，请检查！");
    }
  });
}

// 递归更新 depth
function updateDepths(nodeId: string, parentDepth: number) {
  // 当前节点
  const node = props.elements.nodes.find(n => n.data.id === nodeId);
  if (node) {
    node.data.depth = parentDepth + 1;
    props.cy.getElementById(nodeId).data('depth', parentDepth + 1);
  }

  // 所有子节点
  props.elements.edges
    .filter(e => e.data.source === nodeId && e.data.relation === "包含")
    .forEach(e => {
      updateDepths(e.data.target, parentDepth + 1);
    });
}

async function saveNodeEdits() {
  if (!graphStore.selectedNodeID) {
    ElMessage.error("未选中节点，无法保存修改");
    return;
  }
  const selectedNode = props.cy.getElementById(graphStore.selectedNodeID!);
  if (!selectedNode) {
    ElMessage.error("未选中节点，无法保存修改");
    return;
  }
  const nodeId = selectedNode.id();

  // 更新 depth 字段
  const parentNode = props.elements.nodes.find(n => n.data.id === editForm.value.parentId);
  if (!parentNode) {
    ElMessage.error("父节点不存在，无法修改");
    return;
  }
  const parentDepth = parentNode.data.depth ?? 0;
  updateDepths(nodeId, parentDepth);

  // 修改节点基本信息，从 props.elements 中找到对应节点并修改，然后修改 props.cy 中对应节点的数据
  const node = props.elements.nodes.find((n) => n.data.id === nodeId);
  if (node) {
    node.data.name = editForm.value.name;
    node.data.description = editForm.value.description;
    selectedNode.data("name", editForm.value.name);
    selectedNode.data("description", editForm.value.description);
  }

  // 父节点关系（只允许一个父节点，“包含”关系）
  props.expandToNode(editForm.value.parentId);
  // 先移除原有父节点的“包含”边
  props.elements.edges = props.elements.edges.filter(
    (l) =>
      !(
        l.data.target === nodeId &&
        l.data.relation === "包含"
      )
  );
  props.cy.edges().filter(e => e.data('target') === nodeId && e.data('relation') === '包含').remove();

  // 添加新的父节点边
  const parentEdgeData = {
    source: editForm.value.parentId,
    target: nodeId,
    relation: "包含",
  };
  props.elements.edges.push({ data: parentEdgeData });
  props.cy.add({ group: 'edges', data: parentEdgeData });

  // 前置节点关系（全部替换为当前表单中的前置节点，“前置”关系）
  // 先移除原有的前置边
  props.elements.edges = props.elements.edges.filter(
    (l) =>
      !(
        l.data.target === nodeId &&
        l.data.relation === "前置"
      )
  );
  props.cy.edges().filter(
    e =>e.data('target') === nodeId && e.data('relation') === '前置'
  ).remove();
  // 添加新的前置边
  for (const preId of Object.keys(filteredPrerequisiteNodes.value)) {
    const preEdgeData = {
      source: preId,
      target: nodeId,
      relation: "前置",
    };
    props.elements.edges.push({ data: preEdgeData });
    if (props.cy.getElementById(preId).length) props.cy.add({ group: 'edges', data: preEdgeData });
  }

  // 关联资源关系（全部替换为当前表单中的资源，“关联”关系）
  // 先移除原有的关联边
  props.elements.edges = props.elements.edges.filter(
    (l) =>
      !(
        l.data.source === nodeId &&
        l.data.relation === "关联"
      )
  );
  // 添加新的关联边
  for (const resId of Object.keys(editForm.value.resourceNodes)) {
    props.elements.edges.push({
      data: {
        source: nodeId,
        target: resId,
        relation: "关联",
      },
    });
  };

  // 清空表单并关闭弹窗
  clearEditForm();
  showEditDialog.value = false;
  emit('update:elements', props.elements);

  ElMessage.success("修改成功");
  await nextTick();
  props.selectNode(graphStore.selectedNodeID!);
  await nextTick();
};

function deleteNode() {
  if (!graphStore.selectedNodeID) {
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
      const nodeId = graphStore.selectedNodeID!;
      const childIds = collectChildIds(nodeId, props.elements.edges);
      const idsToDelete = [nodeId, ...childIds];
      // 在 cytoscape 实例中删除节点和相关边
      idsToDelete.forEach((id) => {
        props.removeNode(id);
      });
      // 从元素中删除节点和相关边 
      props.elements.nodes = props.elements.nodes.filter(
        (n) => !idsToDelete.includes(n.data.id)
      );
      props.elements.edges = props.elements.edges.filter(
        (e) =>
          !idsToDelete.includes(e.data.source) &&
          !idsToDelete.includes(e.data.target)
      );
      emit('update:elements', props.elements);

      ElMessage.success("删除成功");
    })
    .catch(() => {
      // 用户取消，无操作
    });
}
</script>

<style scoped>
.edit-btn {
  position: absolute;
  right: 32px;
  top: 32px;
  z-index: 20;
}
</style>