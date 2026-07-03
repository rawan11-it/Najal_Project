"""
najal_backend/main.py
----------------------
نقطة الدخول الرئيسية للـ Backend (FastAPI).

Good Practice المتبعة هنا:
1. فصل الـ Schemas (Pydantic models) عن منطق الـ Endpoints.
2. تسمية واضحة لكل route بما يعكس وظيفتها.
3. استخدام async def لأن الاتصال بـ APIs خارجية (NASA / الأرصاد) عملية I/O.
4. تعليقات توضح "الخطوة القادمة" لكل عضو يكمل عليها لاحقاً.
5. بيانات mock مؤقتة بدل قاعدة بيانات حقيقية، حتى يقدر الفريق يشتغل بالتوازي
   بدون انتظار جاهزية قاعدة البيانات.

طريقة التشغيل:
    pip install fastapi uvicorn pydantic
    uvicorn main:app --reload
    ثم افتح: http://127.0.0.1:8000/docs  (توثيق تلقائي تفاعلي)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Najal API", version="0.1.0")

# السماح لواجهة React بالاتصال بالـ Backend أثناء التطوير
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقاً: حدد النطاق الحقيقي بدل *
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ Schemas (شكل البيانات المتفق عليه مع Frontend) ============

class HeatPoint(BaseModel):
    neighborhood: str
    lat: float
    lng: float
    temperature_c: float
    tree_priority: str  # "high" | "medium" | "low"


class TreeReport(BaseModel):
    citizen_name: str
    lat: float
    lng: float
    description: str
    photo_url: Optional[str] = None


class TreeRecommendation(BaseModel):
    lat: float
    lng: float
    soil_type: str


class IrrigationDay(BaseModel):
    day: date
    should_water: bool
    reason: str


# ============ بيانات مؤقتة (تُستبدل لاحقاً بقاعدة بيانات حقيقية) ============
# ملاحظة لمسؤول البيانات: عبّي هذي القائمة ببيانات حقيقية/واقعية عن أحياء القصيم
MOCK_HEATMAP: List[HeatPoint] = [
    HeatPoint(neighborhood="الصفراء", lat=26.35, lng=43.98, temperature_c=44.5, tree_priority="high"),
    HeatPoint(neighborhood="النهضة", lat=26.33, lng=43.96, temperature_c=41.2, tree_priority="medium"),
]

REPORTS_DB: List[TreeReport] = []  # لاحقاً: تُستبدل بجدول حقيقي في قاعدة البيانات


# ============ واجهة البلدية ============

@app.get("/api/municipality/heatmap", response_model=List[HeatPoint])
async def get_heatmap():
    """يرجع بيانات الخريطة الحرارية لكل الأحياء.
    TODO (Backend): استبدال MOCK_HEATMAP باستدعاء حقيقي لـ NASA Earthdata API.
    """
    return MOCK_HEATMAP


@app.post("/api/municipality/reports", status_code=201)
async def submit_tree_report(report: TreeReport):
    """يستقبل بلاغ عن شجرة مريضة من مواطن."""
    REPORTS_DB.append(report)
    return {"message": "تم استلام البلاغ بنجاح", "total_reports": len(REPORTS_DB)}


@app.get("/api/municipality/reports", response_model=List[TreeReport])
async def list_tree_reports():
    """يرجع كل البلاغات (لعرضها في لوحة البلدية)."""
    return REPORTS_DB


# ============ واجهة المزارع / المواطن (توصية الأشجار) ============

@app.post("/api/recommend-tree")
async def recommend_tree(payload: TreeRecommendation):
    """محرك توصية مبسط (Rule-Based) لنوع الشجرة المناسب.
    TODO (AI/ML): استبدال هذا المنطق البسيط بمنطق أذكى يعتمد على بيانات
    التربة والمناخ الحقيقية.
    """
    if payload.soil_type == "sandy":
        tree = "السدر"
    elif payload.soil_type == "clay":
        tree = "الأثل"
    else:
        tree = "النخيل"

    return {"recommended_tree": tree, "reason": f"مناسب لتربة {payload.soil_type}"}


# ============ جدول الري الذكي ============

@app.get("/api/irrigation-schedule", response_model=List[IrrigationDay])
async def get_irrigation_schedule():
    """يرجع جدول ري مقترح لـ 7 أيام قادمة.
    TODO (Backend): ربطها ببيانات المركز الوطني للأرصاد الحقيقية.
    """
    # بيانات مؤقتة للتجربة
    from datetime import timedelta
    today = date.today()
    schedule = [
        IrrigationDay(day=today + timedelta(days=i),
                      should_water=(i % 2 == 0),
                      reason="حرارة مرتفعة ورطوبة منخفضة" if i % 2 == 0 else "تمت التغطية أمس")
        for i in range(7)
    ]
    return schedule


@app.get("/")
async def root():
    return {"status": "ok", "project": "نَجَلَ"}
