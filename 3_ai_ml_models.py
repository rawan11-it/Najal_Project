"""
najal_ai_ml/models.py
-----------------------
كل نماذج الذكاء الاصطناعي الخاصة بمشروع نَجَلَ في مكان واحد منظّم.

Good Practice المتبعة هنا:
1. كل نموذج/وظيفة في دالة منفصلة بـ docstring واضح (input/output).
2. فصل "منطق النموذج" عن "طريقة استدعائه" حتى يسهل استبدال Mock بنموذج حقيقي لاحقاً.
3. Type hints على كل دالة (best practice في بايثون الحديث).
4. TODOs واضحة توجّه أي عضو يكمل هذا الملف لاحقاً.

طريقة التشغيل (تجربة مبدئية):
    pip install torch torchvision pillow
    python models.py
"""

from typing import Dict, Optional
from dataclasses import dataclass


# ============ 1. تشخيص أمراض النباتات (Computer Vision) ============

@dataclass
class DiagnosisResult:
    disease_name: str
    confidence: float
    treatment_plan: str


# قاعدة معرفة بسيطة: كل مرض له خطة علاج جاهزة
TREATMENT_PLANS: Dict[str, str] = {
    "leaf_spot": "استخدم مبيد فطري نحاسي كل 7 أيام، وتجنب الري على الأوراق مباشرة.",
    "powdery_mildew": "رش كبريت زراعي، وزيادة التهوية بين النباتات.",
    "healthy": "لا يوجد مرض، استمر بنفس نظام الري والتسميد الحالي.",
}


def diagnose_plant_image(image_path: str) -> DiagnosisResult:
    """
    يشخّص صورة نبات ويرجع اسم المرض + نسبة الثقة + خطة العلاج.

    TODO (AI/ML): استبدال هذا الجزء بنموذج حقيقي:
        1. حمّل نموذج مُدرّب مسبقاً (مثلاً MobileNetV2) عبر torchvision.models
        2. درّبه (Fine-tune) على بيانات PlantVillage dataset
        3. استبدل القيم الوهمية أدناه بنتيجة النموذج الفعلي

    حالياً: نتيجة Mock ثابتة لأغراض بناء بقية النظام والتجربة.
    """
    # مثال Mock — استبدله بالتنبؤ الحقيقي
    predicted_class = "leaf_spot"
    confidence = 0.87

    return DiagnosisResult(
        disease_name=predicted_class,
        confidence=confidence,
        treatment_plan=TREATMENT_PLANS.get(predicted_class, "استشر مختص زراعي."),
    )


# ============ 2. محرك التوصية بنوع الشجرة/النبتة (Rule-Based) ============

def recommend_tree(soil_type: str, avg_temperature: float, area_m2: float) -> str:
    """
    يقترح نوع شجرة/نبتة مناسب بناءً على التربة، متوسط الحرارة، ومساحة الموقع.

    هذا نموذج Rule-Based بسيط ومقصود أن يكون كذلك (سريع وموثوق لبناء الـ MVP).
    TODO (AI/ML لاحقاً): يمكن تطويره لنموذج تصنيف حقيقي إذا توفرت بيانات كافية.
    """
    if area_m2 < 5:
        return "نباتات أصص صغيرة (صبار / ريحان)"

    if soil_type == "sandy" and avg_temperature > 40:
        return "السدر (يتحمل الحرارة والتربة الرملية)"
    elif soil_type == "clay":
        return "الأثل"
    else:
        return "النخيل"


# ============ 3. التنبؤ بصحة المحصول لـ 14 يوم ============

def predict_crop_health(current_health: float, temperature_trend: list) -> list:
    """
    يتوقع صحة المحصول (كنسبة من 0 إلى 100) لكل يوم من 14 يوم قادمة.

    current_health: الصحة الحالية للمحصول (0-100)
    temperature_trend: قائمة بدرجات الحرارة المتوقعة لـ 14 يوم

    TODO (AI/ML): استبدال هذا الحساب المبسط بنموذج Time-Series حقيقي
    (مثل Prophet أو LSTM) بعد توفر بيانات تاريخية حقيقية.
    """
    predictions = []
    health = current_health

    for day, temp in enumerate(temperature_trend[:14], start=1):
        # منطق مبسط: كل درجة فوق 42 تقلل الصحة بنسبة بسيطة
        if temp > 42:
            health -= 1.5
        else:
            health += 0.3
        health = max(0, min(100, health))
        predictions.append({"day": day, "predicted_health": round(health, 1)})

    return predictions


# ============ تجربة سريعة عند تشغيل الملف مباشرة ============
if __name__ == "__main__":
    result = diagnose_plant_image("sample.jpg")
    print("التشخيص:", result)

    tree = recommend_tree(soil_type="sandy", avg_temperature=44, area_m2=20)
    print("الشجرة المقترحة:", tree)

    health_forecast = predict_crop_health(80, [41, 43, 45, 40, 39, 44, 46] * 2)
    print("توقعات الصحة:", health_forecast)
