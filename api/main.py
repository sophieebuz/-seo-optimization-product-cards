import os
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.templating import Jinja2Templates
from PIL import Image

from inference.prediction import user_predict

app = FastAPI()
templates = Jinja2Templates(directory=f"{Path.cwd() / 'api' / 'templates'}")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse('main_page.html',
                                      {"request": request})


@app.post("/prediction")
async def create_pred(request: Request,
                      uploaded_file: UploadFile = File(...)):
    img_name = uploaded_file.filename
    with Image.open(uploaded_file.file) as img:
        if img.mode == "RGBA":
            img = img.convert("RGB")

        path_to_save = Path.cwd() / "data" / "users_images"
        img_name = path_to_save / img_name
        img.save(fp=img_name, format='PNG')

        pred = user_predict([img_name])
        os.remove(img_name)

    return {"prediction is": pred}