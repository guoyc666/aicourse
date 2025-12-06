from fastapi import APIRouter
from fastapi import Depends
from utils.auth import get_current_active_user, verify_permission, check_role
from models import User
from database import get_db
from sqlalchemy.orm import Session
from schemas.graph import GraphDataOut, GraphNode, GraphEdge, GraphData, KnowledgeInfo, NodeDetail
from crud.graph import (
    batch_add_nodes_and_edges, delete_all_nodes_and_edges, get_all_knowledge_nodes, get_all_nodes_and_edges,get_node_detail,
    create_node,
    save_knowledge_graph, update_node, delete_node,
    create_edge, delete_edge
)

router = APIRouter()

@router.get("/graph", response_model=GraphDataOut)
def read_graph(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查权限
    #verify_permission(db, current_user.id, "graph:read")
    
    nodes, edges, resources = get_all_nodes_and_edges()
    return {"nodes": nodes, "edges": edges, "resources": resources}

@router.post("/graph")
def batch_add_nodes_edges(
    data: GraphData
):
    nodes = [n.model_dump() for n in data.nodes]
    edges = [l.model_dump() for l in data.edges]
    batch_add_nodes_and_edges(nodes, edges)
    return {"msg": "ok"}

@router.put("/graph")
def update_graph(
    data: GraphData,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    nodes = [n.model_dump() for n in data.nodes]
    edges = [l.model_dump() for l in data.edges]
    save_knowledge_graph(nodes, edges)
    return {"msg": "ok"}

@router.delete("/graph")
def delete_graph(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    verify_permission(db, current_user.id, "graph:update")
    delete_all_nodes_and_edges()
    return {"msg": "ok"}

@router.get("/node/detail/{node_id}", response_model=NodeDetail)
def get_node_detail_api(
    node_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_node_detail(db, node_id, current_user.id, check_role(db, current_user.id, "student"))

@router.get("/node/knowledge/all", response_model=list[KnowledgeInfo])
def get_all_nodes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    nodes= get_all_knowledge_nodes(db)   
    return nodes

@router.post("/node")
def add_node(
    node: GraphNode,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    create_node(node.model_dump())
    return {"msg": "ok"}

@router.put("/node/{node_id}")
def update_node(
    node: GraphNode,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    update_node(node.model_dump())
    return {"msg": "ok"}

@router.delete("/node/{node_id}")
def delete_node(
    node_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    delete_node(node_id)
    return {"msg": "ok"}

@router.post("/edge")
def add_edge(
    edge: GraphEdge,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    create_edge(edge.model_dump())
    return {"msg": "ok"}

@router.delete("/edge")
def delete_edge(
    source: str,
    target: str,
    relation: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    delete_edge(source, target, relation)
    return {"msg": "ok"}