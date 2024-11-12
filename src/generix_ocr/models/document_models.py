from pydantic import BaseModel
from typing import List

class OCRClassification(BaseModel):
    """Classification of the OCR result"""
    document_type: str

class OCRevaluation(BaseModel):
    """Evaluation of the OCR result"""
    evaluation: str
    
class InvoiceItem(BaseModel):
    """Item in the invoice"""
    description: str
    quantity: int
    unit_price: float
    total_price: float

class InvoiceData(BaseModel):
    """Data of the invoice"""
    invoice_number: str
    invoice_date: str
    seller_info: str
    buyer_info: str
    items: List[InvoiceItem]
    subtotal: float
    tax_amount: float
    total_amount: float

class DeliveryNoteItem(BaseModel):
    """Item in the delivery note"""
    description: str
    quantity: int

class DeliveryNoteData(BaseModel):
    """Data of the delivery note"""
    delivery_note_number: str
    delivery_date: str
    sender_info: str
    recipient_info: str
    items: List[DeliveryNoteItem]

class ReceptionNoteItem(BaseModel):
    """Item in the reception note"""
    description: str
    quantity_received: int
    quantity_ordered: int
    
class ReceptionNoteData(BaseModel):
    """Data of the reception note"""
    reception_note_number: str
    reception_date: str
    supplier_info: str
    receiver_info: str
    items: List[ReceptionNoteItem]
    received_by: str

class PurchaseOrderItem(BaseModel):
    """Item in the purchase order"""
    description: str
    quantity: int
    unit_price: float
    total_price: float

class PurchaseOrderData(BaseModel):
    """Data of the purchase order"""
    po_number: str
    order_date: str
    vendor_info: str
    billing_info: str
    shipping_info: str
    items: List[PurchaseOrderItem]
    subtotal: float
    tax_amount: float
    total_amount: float