#import uvicorn
from fastapi import FastAPI
import os
import numpy as np
import cv2
from flask import render_template
from tensorflow.keras.models import load_model

app_desc = """<h2>Try this app by uploading any image with `predict/image`</h2>
<h2>Try Covid symptom checker api - it is just a learning app demo</h2>
<br>by Aniket Maurya"""

#app = FastAPI(title='Tensorflow FastAPI Starter Pack', description=app_desc)

#@app.route('/finish', methods=['GET', 'POST'])
def api(folderpath: str):
    images = []
#    folderpath = "H:/GP/GP_PROJECT/frames"
    dim = (48, 48)
    for frame in os.listdir(folderpath):
        framepath = folderpath + '/' + frame
        img = cv2.imread(framepath, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, dim)
        images.append(img)
    npdata = np.array(images)
    fimages = npdata.reshape([npdata.shape[0], 48, 48, 1])
    fimages = fimages.astype('float32')

    model = load_model('C:/Users/adibw/Downloads/GP_PROJECT_final/GP_PROJECT/Model.23.hdf5')
    folderframe = "C:/Users/adibw/Downloads/GP_PROJECT_final/GP_PROJECT/frames"
    framecount = 0
    for frame in os.listdir(folderframe):
        framecount += 1




    # predict
    res = model.predict_classes(fimages)

    percent = 0.0
    total = res.size
    disframe = framecount - total
    total = framecount
    unique, counts = np.unique(res, return_counts=True)
    for level, count in zip(unique, counts):
        if level == 0:
            count += disframe
        percent += ((level + 1) * count) / total
    #return percent
    # data = {'Task': 'Hours per Day', 'engagement': 1, 'disengagement': 0}
    # return render_template('result.html', data=data)
    #return disframe
    if percent > 1.5:
        #data = {'Task': 'Hours per Day', 'engagement': 1}
        return 1
        #return render_template('result.html', data=data)
    else:
        return 0
        #data = {'Task': 'Hours per Day','disengagement': 1}
        #return render_template('result.html', data=data)

#if _name_ == "_main_":
#    uvicorn.run(app, debug=True)