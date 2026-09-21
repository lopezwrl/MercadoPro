from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return {
        "sales_today": 0,
        "sales_month": 0,
        "sales_count": 0,
        "average_ticket": 0,
        "products_sold": 0,
        "low_stock": 0,
        "near_expiry": 0,
        "payables": 0,
        "receivables": 0,
        "cash": 0,
        "estimated_profit": 0,
        "demo": True
    }
