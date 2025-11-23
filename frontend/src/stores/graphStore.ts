import { defineStore } from "pinia";
import { graphAPI } from "../api";
import type { KnowledgeLink, KnowledgeNode, NodeDetail } from "../types";
import { isEmpty } from "element-plus/es/utils/types.mjs";

// 定义 Store 的类型
interface GraphState {
  nodes: KnowledgeNode[];
  links: KnowledgeLink[];
  selectedNode: KnowledgeNode | null;
  nodeDetail: NodeDetail | null;
  editMode: boolean;
  editNodes: KnowledgeNode | null;
  editLinks: KnowledgeLink | null;
  loading: boolean;
  error: string | null;
}

export const useGraphStore = defineStore("graph", {
  state: (): GraphState => ({
    nodes: [],
    links: [],
    selectedNode: null,
    nodeDetail: null,
    editMode: false,
    editNodes: null,
    editLinks: null,
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
        this.links = response.links;
      } catch (err: any) {
        this.error = err.message || "获取知识图谱失败"; 
      } finally {
        this.loading = false;
      }
    },
    async selectNode(nodeId: string) {
      this.selectedNode = this.nodes.find((n) => n.id === nodeId) || null;
      this.nodeDetail = null;
      if (this.selectedNode) {
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
      } else {
        this.error = "节点未找到";
      }
    },
    unSelectNode() {
      this.selectedNode = null;
      this.nodeDetail = null;
    },
    enterEditMode() {
      this.editMode = true;
      this.editNodes = JSON.parse(JSON.stringify(this.nodes));
      this.editLinks = JSON.parse(JSON.stringify(this.links));
    },
    exitEditMode(save = false) {
      if (save && this.editNodes && this.editLinks) {
        this.nodes = JSON.parse(JSON.stringify(this.editNodes));
        this.links = JSON.parse(JSON.stringify(this.editLinks));
      }
      this.editMode = false;
      this.editNodes = null;
      this.editLinks = null;
    }
  },
  getters: {
    getNodeById: (state) => {
      return (id: string) => state.nodes.find((n) => n.id === id) || null;
    },
    getSelectedNodeDetail: (state) => {
      if (state.selectedNode) {
        return state.nodeDetail;
      }
    },
    isEmpty: (state) => {
      return isEmpty(state.nodes) && isEmpty(state.links);
    },
    isLoading: (state) => {
      return state.loading;
    },
  },
});