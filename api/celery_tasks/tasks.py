from typing import List

from celery import shared_task

from classification.utils.dataset import local_conn
from inference.prediction import user_predict
from inference.train import main as start_train_model


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 1},
             name='seo-classification:predict')
def celery_user_predict(self, path_to_file: List[str]):
    y_preds = user_predict(path_to_file)
    return y_preds


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 1},
             name='seo-classification:train', acks_late=True)
def celery_start_train_model(self, id):
    with local_conn() as con:
        cursor = con.cursor()
        query = f"""UPDATE celery_training_status
                    SET task_id = '{self.AsyncResult(self.request.id)}', status = 'STARTED'
                    WHERE id = {id}"""
        cursor.execute(query)

    start_train_model()

    with local_conn() as con:
        cursor = con.cursor()
        query = f"DELETE FROM celery_training_status WHERE id = {id}"
        cursor.execute(query)

    return "Training completed"

