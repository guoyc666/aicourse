from fastapi import APIRouter
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from schemas_.graph import GraphNode, GraphLink, GraphData, NodeDetail
from crud.graph import (
    batch_add_nodes_and_links, get_all_nodes_and_links,get_node_detail,
    create_node,
    save_knowledge_graph, update_node, delete_node,
    create_link, delete_link
)

router = APIRouter()

@router.get("/graph", response_model=GraphData)
def read_graph():
    nodes, links = get_all_nodes_and_links()
    return {"nodes": nodes, "links": links}

@router.post("/graph")
def batch_add_nodes_links(data: GraphData):
    nodes = [n.model_dump() for n in data.nodes]
    links = [l.model_dump() for l in data.links]
    batch_add_nodes_and_links(nodes, links)
    return {"msg": "ok"}

@router.put("/graph")
def update_graph(data: GraphData):
    nodes = [n.model_dump() for n in data.nodes]
    links = [l.model_dump() for l in data.links]
    save_knowledge_graph(nodes, links)
    return {"msg": "ok"}

@router.get("/node/detail/{node_id}/{student_id}", response_model=NodeDetail)
def get_node_detail_api(
    node_id: str,
    student_id: int = 1,
    db: Session = Depends(get_db)
):
    return get_node_detail(node_id, student_id, db)

@router.post("/node")
def add_node(node: GraphNode):
    create_node(node.model_dump())
    return {"msg": "ok"}

@router.put("/node/{node_id}")
def update_node_api(node_id: str, node: GraphNode):
    update_node(node_id, node.model_dump())
    return {"msg": "ok"}

@router.delete("/node/{node_id}")
def delete_node_api(node_id: str):
    delete_node(node_id)
    return {"msg": "ok"}

@router.post("/link")
def add_link(link: GraphLink):
    create_link(link.model_dump())
    return {"msg": "ok"}

@router.delete("/link")
def delete_link_api(source: str, target: str, relation: str):
    delete_link(source, target, relation)
    return {"msg": "ok"}