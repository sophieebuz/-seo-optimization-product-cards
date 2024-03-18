import os
from pathlib import Path

from fastapi import APIRouter, File, Request, UploadFile
from fastapi.templating import Jinja2Templates
from PIL import Image

from api.celery_config.celery_utils import get_task_info
from api.celery_tasks.tasks import (celery_start_train_model,
                                    celery_user_predict)
from classification.utils.dataset import local_conn
from inference.prediction import user_predict
from inference.train import main as start_train_model

templates = Jinja2Templates(directory=f"{Path.cwd() / 'api' / 'templates'}")
router = APIRouter(prefix='/seo-classification', tags=['seo optimization product card'])


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse('main_page.html',
                                      {"request": request})


@router.post("/prediction")
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

        # pred = celery_user_predict.apply_async(args=[[str(img_name)]], ignore_result=False)
        #
        # while pred.ready() is not True:
        #     continue
        # os.remove(img_name)

        # task_result =  AsyncResult("fdf00e40-64e5-40d9-bcc8-c2b3d99df2c0")
        # print(task_result.result)

    # return {"prediction is": pred.get()}
    return {"prediction is": pred}


@router.get("/training")
async def start_training_model(request: Request):
    with local_conn() as con:
        cursor = con.cursor()
        try:
            cursor.execute(f"SELECT task_id FROM celery_taskmeta")
            query = cursor.fetchall()
            tasks_info = [get_task_info(id) for id in query]
        except:
            con.rollback()
            tasks_info = []

        cursor.execute(f"SELECT * FROM celery_training_status")
        train_info = cursor.fetchall()

    return templates.TemplateResponse('training_model.html',
                                      {"request": request,
                                       "tasks_info": tasks_info,
                                       "train_info": train_info,
                                       "id": None})

@router.post("/training")
async def start_training_model(request: Request):
    with local_conn() as con:
        cursor = con.cursor()
        try:
            cursor.execute(f"SELECT task_id FROM celery_taskmeta")
            query = cursor.fetchall()
            tasks_info = [get_task_info(id) for id in query]
        except:
            con.rollback()
            tasks_info = []

        cursor.execute(f"SELECT nextval('celery_seq')")
        id = cursor.fetchall()[0][0]
        query = f"INSERT INTO celery_training_status (id, status) VALUES ({id}, 'PENDING')"
        cursor.execute(query)

        cursor.execute(f"SELECT * FROM celery_training_status")
        train_info = cursor.fetchall()

    celery_start_train_model.apply_async(args=[id])

    return templates.TemplateResponse('training_model.html',
                                      {"request": request,
                                       "tasks_info": tasks_info,
                                       "train_info": train_info,
                                       "id": {"mark": True, "id": id}})