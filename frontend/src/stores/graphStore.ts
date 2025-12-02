import { defineStore } from "pinia";
import { graphAPI } from "../api";
import type { KnowledgeEdge, KnowledgeNode, NodeDetail } from "../types";
import { isEmpty } from "element-plus/es/utils/types.mjs";

// 定义 Store 的类型
interface GraphState {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  resources: Array<{
    id: string;
    name: string;
  }>;
  editMode: boolean;

  selectedNodeID: string | null;
  nodeDetail: NodeDetail | null;
  
  updating: boolean;
  loading: boolean;
  error: string | null;
}

export const useGraphStore = defineStore("graph", {
  state: (): GraphState => ({
    nodes: [],
    edges: [],
    resources: [],
    editMode: false,

    selectedNodeID: null,
    nodeDetail: null,

    updating: false,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchGraph() {
      this.loading = true;
      this.error = null;
      try {
        const response = await graphAPI.fetchKnowledgeGraph();
        this.nodes = response.nodes;
        this.edges = response.edges;
        this.resources = response.resources;
        //console.log("知识图谱数据：", response);
      } catch (err: any) {
        this.error = err.message || "获取知识图谱失败"; 
      } finally {
        this.loading = false;
      }
    },
    async postGraph() {
      this.loading = true;
      this.error = null;
      try {
        await graphAPI.updateKnowledgeGraph(this.nodes,this.edges);
      } catch (err: any) {
        this.error = err.message || "更新知识图谱失败"; 
      } finally {
        this.loading = false;
      }
    },
    async selectNode(nodeId: string) {
      this.selectedNodeID = nodeId;
      this.nodeDetail = null;
      if (!this.editMode) {
        this.loading = true;
        try {
          const detail = await graphAPI.fetchNodeDetail(nodeId);
          //console.log("节点详情：", detail);
          this.nodeDetail = detail;
        } catch (err: any) {
          this.error = err.message || "获取节点详情失败";
        } finally {
          this.loading = false;
        }
      }
    },
    unSelectNode() {
      this.selectedNodeID = null;
      this.nodeDetail = null;
    },
    enterEditMode() {
      this.unSelectNode();
      this.editMode = true;
      this.updating = false;
    },
    exitEditMode(save = false) {
      this.unSelectNode();
      this.editMode = false;
      this.updating = save;
    },
  },
  getters: {
    getNodeById: (state) => {
      return (id: string) => state.nodes.find((n) => n.id === id) || null;
    },
    getSelectedNodeDetail: (state) => {
      if (state.selectedNodeID) {
        return state.nodeDetail;
      }
    },
    isEmpty: (state) => {
      return isEmpty(state.nodes) && isEmpty(state.edges);
    },
    isLoading: (state) => {
      return state.loading;
    },
  },
});