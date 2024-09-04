from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine
from models import Base, Order, Summary, DashboardMetrics
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/Dashboard")
def dashboard_summary(db: Session = Depends(get_db)):
    metrics = db.query(DashboardMetrics).all()
    return {metric.metric_name: metric.metric_value for metric in metrics}

# @app.get("/orders/{status}")
# def get_orders_by_status(status: str, db: Session = Depends(get_db)):
#     orders = db.query(Order).filter(Order.status == status).all()
#     return orders

# @app.get("/summary")
# def get_summary(db: Session = Depends(get_db)):
#     return db.query(Summary).all()

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.get("/removal_order_ids")
def get_removal_order_ids(db: Session = Depends(get_db)):
    return db.query(Order).filter(func.length(Order.order_id) == 10).all()

@app.get("/order_not_applicable_but_payment_received")
def get_order_not_applicable_but_payment_received(db: Session = Depends(get_db)):
    return db.query(Order).filter(
        Order.order_id.isnot(None),
        Order.payment_net_amount.isnot(None),
        Order.shipment_invoice_amount.is_(None)
    ).all()