from sqlalchemy import Column, Integer, String, Float, Date, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True, unique=True)
    transaction_type = Column(String)
    payment_type = Column(String)
    net_amount = Column(Float)
    invoice_amount = Column(Float)
    order_date = Column(Date)
    payment_date = Column(Date)
    p_description = Column(String)
    shipment_invoice_amount = Column(Float)
    payment_net_amount = Column(Float)
    status = Column(Enum('Previous Month Order', 'Order & Payment Received',
                         'Payment Pending', 'Return', 'Negative Payout',
                         'Removal Order IDs', 'Order Not Applicable but Payment Received'))

class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True, index=True)
    p_description = Column(String)
    sum_of_net_amount = Column(Float)

class DashboardMetrics(Base):
    __tablename__ = "dashboard_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String)
    metric_value = Column(Integer)