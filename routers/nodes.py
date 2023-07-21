from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Node, Audit
from database import SessionLocal
from security import authenticate
from database import get_db

router = APIRouter()


@router.post("/node/")
def create_node(name: str, parent_id: int = None, user = Depends(authenticate)):
    db: Session = SessionLocal()
    try:
        node = Node(name=name, parent_id=parent_id)
        db.add(node)
        db.commit()
        audit = Audit(node_id=node.id, action=f"Node {name} created by {user.username}")
        db.add(audit)
        db.commit()
        db.refresh(node)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return node


@router.get("/node/{node_id}")
def read_node(node_id: int, user = Depends(authenticate)):
    db: Session = SessionLocal()
    node = db.query(Node).get(node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    db.close()
    return node


@router.put("/node/{node_id}/approve")
def approve_node(node_id: int, user = Depends(authenticate)):
    db: Session = SessionLocal()
    try:
        node = db.query(Node).get(node_id)
        if node is None:
            raise HTTPException(status_code=404, detail="Node not found")
        node.is_approved = True
        db.commit()
        audit = Audit(node_id=node.id, action=f"Node {node.name} approved by {user.username}")
        db.add(audit)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
    return node


@router.get("/nodes")
def get_nodes(db: Session = Depends(get_db)):
    nodes = db.query(Node).all()
    return nodes
