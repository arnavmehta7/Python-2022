from fastapi import FastAPI, File, UploadFile
from PIL import Image
import uvicorn
from io import BytesIO
import numpy as np
import os,cv2



app = FastAPI(title='IRIS RECOGNITION')

# Cascades
eye_cascade = cv2.CascadeClassifier('aarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('aarcascade_frontalface_default.xml')

# Take Image and find if in data
def get_eye_filtered_from_face(imag):
    # img = cv2.imread(img_path)
    img = imag
    img = cv2.resize(img,(300,300))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # if faces:
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray).tolist()
    #     print(eyes[0].tolist())
    #     for (ex,ey,ew,eh) in eyes[0].tolist():
    #          cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        ex,ey,ew,eh = eyes[0]
    #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        crop_img = roi_color[ey: ey + eh, ex: ex + ew]
    # crop_img = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    crop_img = cv2.resize(crop_img,(300,300))
    crop_img = cv2.GaussianBlur(crop_img, (7, 7), 1)
    crop_img = cv2.Canny(crop_img, 20, 70, apertureSize=3)
        # plt.imshow(crop_img)
    # if not faces:
        # crop_img = cv2.resize(gray,(300,300))
        # crop_img = cv2.GaussianBlur(crop_img, (7, 7), 1)
        # crop_img = cv2.Canny(crop_img, 20, 70, apertureSize=3)
    return crop_img

def gaus_canny(imag):
    # image_test2 = cv2.imread(imag, cv2.IMREAD_GRAYSCALE)
    image_test2 = cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
    image_test2 = cv2.resize(image_test2,(300,300))

    image_test2 = cv2.GaussianBlur(image_test2, (7, 7), 1)
    image_test2 = cv2.Canny(image_test2, 20, 70, apertureSize=3)
    return image_test2




img_list = sorted(os.listdir('./Data'))

# Initiate Algo
sift = cv2.SIFT_create()
index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)
names = []
kp_desc_stored = []

for i in img_list:
    pathImg = './Data/'+i
    read_img = gaus_canny(cv2.imread(pathImg))
    kp_new, desc_new = sift.detectAndCompute(read_img, None)
    kp_desc_stored.append([kp_new,desc_new])

    names.append(i[:-5])
print(names,'Names')
print("Data Loaded Cool")


def process(img):
    good_points_list = []

    kp_1, desc_1 = sift.detectAndCompute(gaus_canny(img), None)
    for i in range(len(img_list)):
        matches = flann.knnMatch(desc_1,kp_desc_stored[i][1],k=2)
        good_points= []
        for m, n in matches:
            if m.distance < 0.6*n.distance:
                good_points.append(m)
        good_points_list.append(good_points)
    stored_only_points = []
    for i in good_points_list:
        stored_only_points.append(len(i))
        print(len(i))
    pos = np.argmax(stored_only_points)
    print(pos,'Max Arg')
    print('Names',names)
    print('len',len(names))
    if pos<=len(names):
        return names[np.argmax(stored_only_points)]    
    else:
        return "NONE"





@app.get('/')
async def hello_world():
    return "hello Humans"


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    return image

@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    result = process(image)
    return {'Val':str(result)}

if __name__ == "__main__":
    uvicorn.run(app, debug=True)