"""
najal_data/mock_data.py
-------------------------
كل البيانات الوهمية (Mock/Fallback) المستخدمة في المشروع في مكان واحد.

Good Practice المتبعة هنا:
1. فصل البيانات عن منطق الكود بالكامل — أي عضو يعدّل بيانات بدون
   المساس بمنطق الـ Backend أو الـ AI.
2. كل قائمة بيانات موثّقة بمصدرها الحقيقي (حتى لو مؤقتة الآن).
3. تنسيق موحّد (dict/list بسيطة) يسهل تحويله مباشرة لـ JSON للـ API.

طريقة الاستخدام:
    from mock_data import QASSIM_NEIGHBORHOODS, TREE_TYPES
"""

# ============ أحياء القصيم (بيانات تقريبية لأغراض العرض) ============
# TODO (مسؤول البيانات): استبدال الإحداثيات بإحداثيات حقيقية دقيقة،
# ومصدر الحرارة الحقيقي من NASA Earthdata API لاحقاً.

QASSIM_NEIGHBORHOODS = [
    {
        "name": "الصفراء",
        "city": "بريدة",
        "lat": 26.3510,
        "lng": 43.9800,
        "avg_temperature_c": 44.5,
        "tree_priority": "high",
        "soil_type": "sandy",
    },
    {
        "name": "النهضة",
        "city": "بريدة",
        "lat": 26.3300,
        "lng": 43.9600,
        "avg_temperature_c": 41.2,
        "tree_priority": "medium",
        "soil_type": "clay",
    },
    {
        "name": "الفيصلية",
        "city": "عنيزة",
        "lat": 26.0900,
        "lng": 43.9950,
        "avg_temperature_c": 42.8,
        "tree_priority": "high",
        "soil_type": "sandy",
    },
]


# ============ أنواع الأشجار/النباتات المناسبة لمناخ القصيم ============
# المصدر: بحث سريع عن نباتات ملائمة للمناخ الصحراوي الحار وقليل الأمطار

TREE_TYPES = [
    {"name": "السدر", "soil": "sandy", "water_need": "low", "heat_tolerance": "high"},
    {"name": "الأثل", "soil": "clay", "water_need": "low", "heat_tolerance": "high"},
    {"name": "النخيل", "soil": "any", "water_need": "medium", "heat_tolerance": "high"},
    {"name": "الغاف", "soil": "sandy", "water_need": "very_low", "heat_tolerance": "very_high"},
]


# ============ أمراض نباتات شائعة (لاختبار نموذج Computer Vision) ============

PLANT_DISEASES = [
    {
        "id": "leaf_spot",
        "name_ar": "تبقع الأوراق",
        "treatment": "استخدم مبيد فطري نحاسي كل 7 أيام، وتجنب الري على الأوراق مباشرة.",
    },
    {
        "id": "powdery_mildew",
        "name_ar": "البياض الدقيقي",
        "treatment": "رش كبريت زراعي، وزيادة التهوية بين النباتات.",
    },
    {
        "id": "healthy",
        "name_ar": "سليم",
        "treatment": "لا يوجد مرض، استمر بنفس نظام الري والتسميد الحالي.",
    },
]


# ============ إعدادات عامة للمشروع ============

CONFIG = {
    "project_name": "نَجَلَ",
    "region": "منطقة القصيم",
    "points_per_tree_planted": 10,
    "points_per_report_submitted": 5,
}
