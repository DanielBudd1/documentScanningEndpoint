from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
from utility import convertPdfToImages, convertImagesToCv2Array, preprocessImage, flagKeyWords

app = FastAPI()

origins = ["*"]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)


app.get("/home")
def helloWorld():
    return "HelloWorld"

@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    keyWords = ['amex','american','express','capital','tap','hsbc']
    flaggedFiles = []
    for file in files:
        if file.content_type != "application/pdf":
            return {"error": f"File {file.filename} is not a PDF"}

        images = convertPdfToImages(file)
        images = convertImagesToCv2Array(images)
        
        for i in images:
            preprocessImage = preprocessImage(i)
            containsKeyWords = flagKeyWords(i)
            if containsKeyWords:
                flaggedFiles.append(file) 
                break

    if flaggedFiles:
        return {"filenames": [file.filename for file in flaggedFiles]}
    else:
        return {"No files of relevance"}
