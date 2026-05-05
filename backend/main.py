import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import boto3
import uuid
from Controller.langgraph_controller import create_executor
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import shutil
from dotenv import load_dotenv

# Loading the environment
load_dotenv()
# Assiging the fastApi
app = FastAPI()

# Crediential 
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_S3_BUCKET")


# CORSM Middleware config
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# S3 config
s3 = boto3.client(
    "s3",
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key =  AWS_SECRET_KEY,
    region_name = AWS_REGION
)

@app.on_event("startup")
async def startup_event():
    global graph_executor
    graph_executor = create_executor() 

@app.post('/process/')
async def upload_file(file: Optional[UploadFile] = File(None),prompt: Optional[str] = Form(None)):
    file_path = None
    # Uplaoding the file in Amazon aws S3

    if file:
        # file_ext = file.filename.split(".")[-1]
        # s3_key = f"upload/{uuid.uuid4()}.{file_ext}" # Generate unique file name
        # try:
        #     s3.upload_fileobj(file.file, AWS_BUCKET, s3_key) # Upload to S3
        #     # file_path = f"https://{AWS_BUCKET}.s3.amazonaws.com/{s3_key}" # Generate url
        #     presigned_url = s3.generate_presigned_url(
        #     ClientMethod='get_object',
        #     Params={'Bucket': AWS_BUCKET, 'Key': s3_key},
        #     ExpiresIn=900  # 15 minutes
        # )
        #     file_path = presigned_url
        # except Exception as e:
        #     return JSONResponse({"status": "error", "detail": str(e)}, status_code=500)
        
        file_path = os.path.join("/Users/nareshjungshahi/Documents/Cloud_Computing/Data", file.filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        file.file.close() 

        
    # Input for Agents
    input_state = {
        "prompt": prompt,
        "file_path": file_path
    }

    print("DEBUG, Input state", input_state)

    # Calling the Agents
    response = graph_executor.invoke(input_state)

    print(type(response))
    print(response)


    return JSONResponse(
        {
            "status": "processed",
            "result": response
        }
    )

   