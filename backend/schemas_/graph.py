from pydantic import BaseModel
from typing import Optional, List, Literal, Union


# neo4j节点基础模型
class BaseNode(BaseModel):
    id: str
    category: str
    name: str

class CourseNode(BaseNode):
    category: Literal["Course"]
    description: Optional[str] = None
    depth: Optional[int] = None

class ConceptNode(BaseNode):
    category: Literal["Concept"]
    description: Optional[str] = None
    depth: Optional[int] = None
    difficulty: Optional[int] = None
    importance: Optional[int] = None

class ResourceNode(BaseNode):
    category: Literal["Resource"]
    type: str

GraphNode = Union[CourseNode, ConceptNode, ResourceNode]

class GraphLink(BaseModel):
    source: str
    target: str
    relation: str

class GraphData(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]

class ResourceInfo(BaseModel):
    id: str
    name: str
    type: str
    is_child: bool = False

class NodeRef(BaseModel):
    id: str
    name: str

class NodeDetail(BaseModel):
    id: str
    name: str
    description: Optional[str]
    total_time: int
    average_time: int
    resources: List[ResourceInfo]
    prerequisites: List[NodeRef]
    successors: List[NodeRef]