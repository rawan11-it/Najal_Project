/**
 * najal_frontend/App.jsx
 * ------------------------
 * نقطة الدخول الرئيسية للواجهة (React).
 *
 * Good Practice المتبعة هنا:
 * 1. تقسيم الواجهة إلى 3 مكونات (Components) مستقلة حسب نوع المستخدم،
 *    كل مكون بإمكان عضو مختلف تطويره لاحقاً دون تعارض في الكود (Git).
 * 2. فصل منطق الاتصال بالـ API في دالة واحدة قابلة لإعادة الاستخدام.
 * 3. استخدام useState/useEffect بشكل بسيط وواضح (بدون تعقيد زائد).
 * 4. تسمية المتغيرات بالإنجليزية (معيار عالمي) مع تعليقات عربية للتوضيح.
 *
 * طريقة التشغيل:
 *   npx create-react-app najal-frontend
 *   انسخ هذا الملف داخل src/App.jsx
 *   npm start
 */

import React, { useState, useEffect } from "react";

const API_BASE = "http://127.0.0.1:8000/api";

// ============ دالة موحّدة لكل نداءات الـ API ============
async function apiGet(endpoint) {
  const res = await fetch(`${API_BASE}${endpoint}`);
  if (!res.ok) throw new Error(`فشل الاتصال بـ ${endpoint}`);
  return res.json();
}

// ============ مكوّن واجهة البلدية ============
function MunicipalityView() {
  const [heatmap, setHeatmap] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiGet("/municipality/heatmap")
      .then(setHeatmap)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>جاري تحميل الخريطة الحرارية...</p>;

  return (
    <div>
      <h2>خريطة الحرارة الحية</h2>
      <ul>
        {heatmap.map((point) => (
          <li key={point.neighborhood}>
            {point.neighborhood} — {point.temperature_c}° — أولوية التشجير:{" "}
            {point.tree_priority}
          </li>
        ))}
      </ul>
      {/* TODO (Frontend): استبدال هذي القائمة بخريطة تفاعلية حقيقية (Leaflet/Mapbox) */}
    </div>
  );
}

// ============ مكوّن واجهة المزارع ============
function FarmerView() {
  const [diagnosis, setDiagnosis] = useState(null);

  function handleImageUpload(event) {
    // TODO (Frontend + AI/ML): إرسال الصورة فعلياً لـ /api/diagnose-plant
    // هذا مثال مبدئي يوضح شكل التدفق فقط
    setDiagnosis({ disease: "قيد التحليل...", confidence: null });
  }

  return (
    <div>
      <h2>تشخيص أمراض النباتات</h2>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      {diagnosis && <p>النتيجة: {diagnosis.disease}</p>}
    </div>
  );
}

// ============ مكوّن واجهة المواطن ============
function CitizenView() {
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    apiGet("/irrigation-schedule").then(setSchedule).catch(console.error);
  }, []);

  return (
    <div>
      <h2>جدول الري الذكي</h2>
      <ul>
        {schedule.map((day) => (
          <li key={day.day}>
            {day.day} — {day.should_water ? "🟢 اسقِ اليوم" : "🔴 لا حاجة للري"} (
            {day.reason})
          </li>
        ))}
      </ul>
    </div>
  );
}

// ============ المكوّن الرئيسي ============
export default function App() {
  const [activeTab, setActiveTab] = useState("citizen");

  const tabs = {
    municipality: <MunicipalityView />,
    farmer: <FarmerView />,
    citizen: <CitizenView />,
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: "20px", direction: "rtl" }}>
      <h1>نَجَلَ 🌳</h1>

      <nav style={{ marginBottom: "20px" }}>
        <button onClick={() => setActiveTab("municipality")}>البلدية</button>
        <button onClick={() => setActiveTab("farmer")}>المزارع</button>
        <button onClick={() => setActiveTab("citizen")}>المواطن</button>
      </nav>

      {tabs[activeTab]}
    </div>
  );
}
