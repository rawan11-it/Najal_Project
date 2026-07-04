from fastapi import FastAPI

app = FastAPI(title="منصة نَجَلَ للتشجير")

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "مرحباً بكم في منصة نَجَلَ لذكاء التشجير الاصطناعي بالقصيم"
    }

"""
hi

"""