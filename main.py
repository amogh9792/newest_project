from source.utility.utility import generate_global_timestamp
from source.entity.config_entity import PipelineConfig
from source.logger import setup_logger
from source.logger import logging
from source.pipeline.pipeline import DataPipeline
from fastapi import FastAPI, Response
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from source.constant.constant import APP_PORT, APP_POST

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)
def run_pipeline(pipeline_type):

    try:
        global_timestamp = generate_global_timestamp()

        setup_logger(global_timestamp)

        pipeline_obj = DataPipeline(global_timestamp)

        logging.info(f"START: MODEL {pipeline_type.upper()}")

        if pipeline_type == 'training':
            pipeline_obj.run_train_pipeline()

        elif pipeline_type == "prediction":
            pipeline_obj.run_predict_pipeline()

        logging.info(f"END: MODEL {pipeline_type.upper()}")
        print(f"MODEL {pipeline_type} Completed")

        return f"Model {pipeline_type} Completed"

    except Exception as e:
        return f"ERROR OCCURRED {e}"

@app.get("/", tags = ['authentication'])
async def index():
    return RedirectResponse(url = '/docs')

@app.get("/train", tags = ['pipeline'])
async def train_route():
    main("training")
    return {"Message: Training pipeline start"}

@app.get('/predict', tags = ['pipeline'])
async def predict_route():
    main('prediction')
    return {"Message": "Prediction Pipeline Start"}

def main(pipeline_type):
    try:
        global_timestamp = generate_global_timestamp()
        setup_logger(global_timestamp)
        run_pipeline(pipeline_type)

    except Exception as e:
        print(e)
        logging.info(e)

if __name__ == '__main__':
    app_run(app, host = APP_POST, port = APP_PORT)

