export interface BaseNode {
  id: string;
  category: string;
  name: string;
  description?: string;
}

export interface CourseNode extends BaseNode {
  category: "Course"; // 课程节点
  depth: number;
}

export interface ConceptNode extends BaseNode {
  category: "Concept"; // 概念节点
  depth: number;
  difficulty?: number;
  importance?: number;
  mastery?: number;
  progress?: number;
}

export type ResourceNode =
  | (BaseNode & {
      category: "Resource";
      type: "video" | "audio";
      size?: string;
      duration?: string;
    })
  | (BaseNode & {
      category: "Resource";
      type: "ppt" | "pdf";
      size?: string;
      pageCount?: number;
    })
  | (BaseNode & {
      category: "Resource";
      type: "doc";
      size?: string;
      wordCount?: number;
    });

// 联合类型
export type KnowledgeNode = CourseNode | ConceptNode | ResourceNode;

export type KnowledgeLink = {
  source: string;
  target: string;
  relation: string;
};

export type LearningRecord = {
  id?: number;
  student_id: number;
  resource_id: string;
  status: number; // 0: 未完成, 1: 已完成
  total_time: number; // 总学习时长，单位为秒
  page_times: number[]; // 每页学习时长数组，单位为秒
  timestamp: string; // 学习记录的时间戳
};

export type DailyEvent = {
  id: number;
  resource_id: string;
  resource_name: string;
  time: string; // "HH:MM" 格式的时间字符串
  duration: number; // 学习时长，单位为秒
}

export type NodeDetail = {
  id: string;                    // 节点ID
  name: string;                  // 节点名称
  description?: string;           // 节点描述
  total_time: number;            // 学习总时长（单位：分钟）
  average_time: number;         // 平均学习时长（单位：分钟）
  resources: Array<{
    id: string;
    name: string;
    type: string;                // 资源类型，如视频、文档、PPT等
    is_child: boolean;          // 是否来自子节点
  }>;
  prerequisites: Array<{
    id: string;
    name: string;
  }>;                            // 前置知识点
  successors: Array<{
    id: string;
    name: string;
  }>;                            // 后续知识点
}