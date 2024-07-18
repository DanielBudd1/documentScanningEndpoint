import cv2
import numpy as np
import pytesseract
from imutils import contours
import imutils
from pdf2image import convert_from_path
import pandas as pd


def convertPdfToImages(pdfPath):
    return convert_from_path(pdfPath)

def convertImagesToCv2Array(images):
    cv2Images = []
    for i in images:
        open_cv_image = np.array(i)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        cv2Images.append(open_cv_image)

    return cv2Images

def preprocessImage(image):
    image = imutils.resize(image, width=1653*2, height=2339*2)
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    return thresh


def flagKeyWords(image, keyWords):
    df = pytesseract.image_to_data(image, config='--psm 6',output_type='data.frame')
    keywordSearch = df[np.isin(df["text"].str.lower(), keyWords)]
    return not keywordSearch.empty


