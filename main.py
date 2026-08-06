import os
from blacklist_checker import generate_audit_report, generate_pdf_report
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

# 1. إنشاء تطبيق FastAPI
app = FastAPI(
    title="BlacklistMail Radar API",
    description="Enterprise Domain Intelligence & Blacklist Audit API",
    version="1.0.0",
)

# 2. إنشاء مجلد مؤقت لحفظ تقارير PDF
PDF_DIR = "./generated_reports"
os.makedirs(PDF_DIR, exist_ok=True)


# 3. مسار عرض واجهة الـ Dashboard الرسمية
@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """عرض لوحة التحكم الرئيسية من ملف dashboard.html"""
    html_file_path = "dashboard.html"
    if not os.path.exists(html_file_path):
        raise HTTPException(
            status_code=404,
            detail="dashboard.html file not found. Please place it in the same directory.",
        )

    with open(html_file_path, "r", encoding="utf-8") as f:
        return f.read()


# 4. API endpoint لإرجاع نتائج الفحص كـ JSON
@app.get("/api/v1/audit/{domain}")
def audit_domain(domain: str):
    """إرجاع بيانات الفحص الشاملة للدومين بتنسيق JSON"""
    try:
        clean_domain = (
            domain.strip()
            .lower()
            .replace("http://", "")
            .replace("https://", "")
            .split("/")[0]
        )
        report_data = generate_audit_report(clean_domain)
        return {"success": True, "data": report_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 5. API endpoint لتوليد وتحميل ملف الـ PDF
@app.get("/api/v1/download-pdf/{domain}")
def download_pdf_report(domain: str, background_tasks: BackgroundTasks):
    """توليد تقرير PDF احترافي وتحميله مباشرة مع مسحه تلقائياً بعد الإرسال"""
    clean_domain = (
        domain.strip()
        .lower()
        .replace("http://", "")
        .replace("https://", "")
        .split("/")[0]
    )
    pdf_filename = f"report_{clean_domain}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)

    try:
        # جلب البيانات وتوليد ملف PDF
        report_data = generate_audit_report(clean_domain)
        generate_pdf_report(report_data, pdf_path)

        # إضافة مهمة خلفية لمسح الملف بعد تنزيله لعدم استهلاك مساحة الخادم
        background_tasks.add_task(os.remove, pdf_path)

        return FileResponse(
            path=pdf_path,
            filename=f"BlacklistMail_Radar_{clean_domain}.pdf",
            media_type="application/pdf",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate PDF: {str(e)}"
        )


# 6. التشغيل المباشر عند استدعاء الملف
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)