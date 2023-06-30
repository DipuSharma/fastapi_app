from fastapi import APIRouter
from celery.result import AsyncResult
from starlette.responses import JSONResponse
from src.routers.Auth.tasks import operation_task
from src.routers.Auth.schema import CeleryTest

router = APIRouter(prefix='/api', tags=[f'Auth'], responses={404: {"description": "Not found"}})

@router.post("/operation")
async def get_mathmetic_result(form: CeleryTest):
    if form:
        x = form.num1
        y = form.num2
        o = form.Operation
    task = operation_task.apply_async(args=(x, y, o))
    
    return JSONResponse({"task_id": task.id})


@router.get("/result/{task_id}")
async def result(task_id: str):
    task = AsyncResult(task_id)

    # Task Not Ready
    if not task.ready():
        return {"status": task.status}

    # Task done: return the value
    task_result= task.get()
    return JSONResponse({"task_id": str(task_id),
            "status": task.status,
            "result": task_result
            })