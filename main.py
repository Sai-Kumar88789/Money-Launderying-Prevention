# from aml.pipelines.training_pipeline import TrainPipeline

# train = TrainPipeline()
# train.run_pipeline()

from aml.configuration.mongodb_connection import MongodbClient
from aml.exception import AMLException
import os,sys
from aml.logger import logging
from aml.pipelines import training_pipeline
from aml.pipelines.training_pipeline import TrainPipeline
import os
from aml.utils.main_utils import read_yaml_file
from aml.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, File, UploadFile,Request
from aml.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse,FileResponse
from uvicorn import run as app_run
from fastapi.responses import Response , StreamingResponse,HTMLResponse
from aml.ml.model.estimator import ModelResolver,TargetValueMapping
from aml.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import pandas as pd
import io


env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGODB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGODB_URL']=env_config['MONGODB_URL']


app = FastAPI()
origins = ["*"]
app.mount(
    "/templates",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "templates"),
    name="templates",
)
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request, "title": "Home", "body": "Welcome to my website!"}
    return templates.TemplateResponse("index.html", context=context)
@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        #get data from user csv file
        #conver csv file to dataframe
        #df = pd.read_csv(file.file)
        content_file = await file.read()

        print(file.filename)
        print(content_file)
    
        df = pd.read_csv(io.StringIO(file.file.read().decode("utf-8")))

        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exist():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        #return df.to_html()
        #decide how to return file to user.
        results_csv = df.to_csv(index=False)
        return Response(content=results_csv, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=results.csv"})
    
        
    except Exception as e:
        return {"error": str(e)}

# def main():
#     try:
#         set_env_variable(env_file_path)
#         training_pipeline = TrainPipeline()
#         training_pipeline.run_pipeline()
#     except Exception as e:
#         print(e)
#         logging.exception(e)


if __name__=="__main__":
    #main()
    #set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)