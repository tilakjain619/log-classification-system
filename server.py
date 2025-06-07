from fastapi import FastAPI, UploadFile, HTTPException, Request, File
from fastapi.responses import FileResponse, HTMLResponse
import pandas as pd
from fastapi.templating import Jinja2Templates

from classify import classify

app = FastAPI()

templates = Jinja2Templates(directory='templates')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html'
    )

@app.post("/api/classify")
async def classify_logs(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    try:
        df = pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")
        
        df['target_label'] = classify(list(zip(df['source'], df['log_message'])))

        output_file = "resources/output.csv"
        df.to_csv(output_file, index=False)

        return FileResponse(output_file, media_type='text/csv')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()