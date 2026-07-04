"""
najal_backend/main.py
----------------------
نقطة الدخول الرئيسية للـ Backend (FastAPI) — نسخة متصلة بقاعدة بيانات حقيقية.

طريقة التشغيل:
    pip install fastapi uvicorn pydantic sqlalchemy
    uvicorn main:app --reload
    ثم افتح: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta

from database import engine, get_db
from models import Base, User, Neighborhood, TreeReport, PlantedTree

# ينشئ كل الجداول تلقائياً أول مرة يشتغل السيرفر (لو مو موجودة)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Najal API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Schemas (شكل البيانات بين Frontend و Backend) ============

class HeatPointOut(BaseModel):
    id: int
    neighborhood: str = None
    lat: float
    lng: float
    temperature_c: float = None
    tree_priority: str = None

    class Config:
        from_attributes = True


class TreeReportIn(BaseModel):
    citizen_id: int
    lat: float
    lng: float
    description: str
    photo_url: Optional[str] = None


class TreeReportOut(BaseModel):
    id: int
    citizen_id: int
    lat: float
    lng: float
    description: str
    status: str

    class Config:
        from_attributes = True


class PlantedTreeIn(BaseModel):
    user_id: int
    tree_type: str
    lat: float
    lng: float


class TreeRecommendation(BaseModel):
    lat: float
    lng: float
    soil_type: str


# ============ تهيئة بيانات أولية (Seed) لو الجدول فاضي ============

@app.on_event("startup")
def seed_neighborhoods():
    db = next(get_db())
    if db.query(Neighborhood).count() == 0:
        db.add_all([
            Neighborhood(name="الصفراء", city="بريدة", lat=26.35, lng=43.98,
                         avg_temperature_c=44.5, soil_type="sandy", tree_priority="high"),
            Neighborhood(name="النهضة", city="بريدة", lat=26.33, lng=43.96,
                         avg_temperature_c=41.2, soil_type="clay", tree_priority="medium"),
        ])
        db.commit()
    db.close()


# ============ واجهة البلدية ============

@app.get("/api/municipality/heatmap", response_model=List[HeatPointOut])
def get_heatmap(db: Session = Depends(get_db)):
    """يرجع بيانات الخريطة الحرارية من قاعدة البيانات الحقيقية."""
    neighborhoods = db.query(Neighborhood).all()
    return [
        HeatPointOut(
            id=n.id, neighborhood=n.name, lat=n.lat, lng=n.lng,
            temperature_c=n.avg_temperature_c, tree_priority=n.tree_priority,
        )
        for n in neighborhoods
    ]


@app.post("/api/municipality/reports", response_model=TreeReportOut, status_code=201)
def submit_tree_report(report: TreeReportIn, db: Session = Depends(get_db)):
    """يستقبل بلاغ عن شجرة مريضة ويخزنه فعلياً بقاعدة البيانات."""
    user = db.query(User).filter(User.id == report.citizen_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")

    new_report = TreeReport(**report.model_dump())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


@app.get("/api/municipality/reports", response_model=List[TreeReportOut])
def list_tree_reports(db: Session = Depends(get_db)):
    """يرجع كل البلاغات المخزّنة فعلياً (تبقى بعد إعادة تشغيل السيرفر)."""
    return db.query(TreeReport).all()


# ============ واجهة المواطن — الزراعة والنقاط ============

@app.post("/api/citizen/plant-tree", status_code=201)
def plant_tree(payload: PlantedTreeIn, db: Session = Depends(get_db)):
    """يسجّل شجرة جديدة مزروعة، ويضيف نقاط فعلية لحساب المستخدم."""
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")

    new_tree = PlantedTree(**payload.model_dump())
    db.add(new_tree)

    user.points += new_tree.points_earned  # تحديث نقاط المستخدم فعلياً
    db.commit()

    return {"message": "تم تسجيل الشجرة", "total_points": user.points}


@app.get("/api/citizen/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """يرجع أعلى المساهمين نقاطاً (لعرضها على الخريطة الحية)."""
    top_users = db.query(User).order_by(User.points.desc()).limit(10).all()
    return [{"name": u.name, "points": u.points} for u in top_users]


# ============ توصية الأشجار وجدول الري (بدون تغيير — ما تحتاج قاعدة بيانات) ============

@app.post("/api/recommend-tree")
def recommend_tree(payload: TreeRecommendation):
    if payload.soil_type == "sandy":
        tree = "السدر"
    elif payload.soil_type == "clay":
        tree = "الأثل"
    else:
        tree = "النخيل"
    return {"recommended_tree": tree, "reason": f"مناسب لتربة {payload.soil_type}"}


@app.get("/api/irrigation-schedule")
def get_irrigation_schedule():
    today = date.today()
    return [
        {
            "day": str(today + timedelta(days=i)),
            "should_water": i % 2 == 0,
            "reason": "حرارة مرتفعة ورطوبة منخفضة" if i % 2 == 0 else "تمت التغطية أمس",
        }
        for i in range(7)
    ]


@app.get("/")
def root():
    return {"status": "ok", "project": "نَجَلَ"}