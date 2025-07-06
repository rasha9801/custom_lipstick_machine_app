from flask import Flask,render_template,Response, request
from portion import getColorsPortion
import faceBlendCommon as face
from threading import Thread
from PIL import Image
import numpy as np
import requests
import base64
import dlib
import json
import cv2
import io

url              = "http://-.-.-.-:8080/shot.jpg"
app              = Flask(__name__)
PREDICTOR_PATH   = "Haarcascades/shape_predictor_68_face_landmarks.dat"
faceDetector     = dlib.get_frontal_face_detector()
landmarkDetector = dlib.shape_predictor(PREDICTOR_PATH)
camera           = cv2.VideoCapture(0)
red              = 255
green            = 255
blue             = 255
image            = None
mask             = []
lips             = []
pixels           = []
justLips         = []
justFace         = []
inverseMask      = []

def getImagepixels():
    global image, pixels
    pixels  = image.astype(float)/255

def getRouge():
    global image, lips, pixels, red, green, blue
    rouge = np.ones(image.shape)
    rouge = rouge * [blue/255, green/255, red/255]
    while len(pixels) == 0:
        i = 0
    lips  = cv2.multiply(rouge, pixels)
    
def initLips():
    global justLips, mask, lips
    while len(lips) == 0:
        i = 0
    justLips = cv2.multiply(mask, lips)
    
def initFace():
    global justFace, inverseMask, pixels
    while len(pixels) == 0:
        i = 0
    justFace = cv2.multiply(inverseMask, pixels)
    
def apply_mask(im):
    try:
        landmarks   = face.getLandmarks(faceDetector, landmarkDetector, im)
        if len( landmarks ) == 0:
            return im
        global mask, inverseMask, justLips, justFace
        lipsPoints  = landmarks[48:60]
        teethPoints = landmarks[60:68]
        mask        = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.int32(lipsPoints), (1, 1, 1))
        cv2.fillConvexPoly(mask, np.int32(teethPoints), (0, 0, 0))
        mask        = 255*np.uint8(mask)
        mask        = cv2.GaussianBlur(mask,(15,15),cv2.BORDER_DEFAULT)
        inverseMask = cv2.bitwise_not(mask)
        mask        = mask.astype(float)/255
        inverseMask = inverseMask.astype(float)/255  
        Thread(target = initLips).start()
        Thread(target = initFace).start()
        while len( justLips) == 0 or len( justFace ) == 0:
            i = 0
        result      = justFace + justLips
        return result * 255
    except:
        return im

def gen_frames():  
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            global image
            image         = frame
            Thread(target = getImagepixels).start()
            Thread(target = getRouge).start()
            frame = apply_mask(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def cameraphone():
    global url
    global red, green, blue
    while True:
        frame             = requests.get(url).content
        if not (red == 255 and green == 255 and blue == 255 ):
            global image
            frame         = Image.open(io.BytesIO(frame))
            frame         = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
            image         = frame
            Thread(target = getImagepixels).start()
            Thread(target = getRouge).start()
            frame         = apply_mask(frame)
            ret, buffer   = cv2.imencode('.jpg', frame)
            frame         = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    global red, green, blue
    red   = 255
    green = 255
    blue  = 255
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    global red, green, blue
    getColorsPortion( red, green, blue )
    return ( '' , 200) 

@app.route('/processing/file', methods=['POST'])
def processFile():
    file        = request.files['img'].read()
    file_bytes = np.frombuffer(file, np.uint8)
    img        = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
    im_rgb     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    color      = im_rgb[0][0]
    return ( '('+ str(color[0]) + ', ' + str(color[1]) + ', ' + str(color[2]) + ')' , 200) 


@app.route('/processing/img', methods=['POST'])
def processImg():
    data    = json.loads(request.data)
    imgdata = base64.b64decode(data)
    image   = Image.open(io.BytesIO(imgdata))
    im_rgb  = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    color   = im_rgb[0][0]
    cv2.imwrite('image.jpeg', im_rgb)
    return ( '('+ str(color[0]) + ', ' + str(color[1]) + ', ' + str(color[2]) + ')' , 200) 

@app.route('/divinfo', methods=['POST'])
def get_divinfo():
    divinfo = request.form['yourdiv']
    str     = divinfo.split()
    global red, green, blue
    red     = int(str[0])
    green   = int(str[1])
    blue    = int(str[2])
    return ('', 200)

@app.route('/video_feed')
def video_feed():
    ip_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if ip_add != "" and ip_add != "127.0.0.1":
        return Response(cameraphone() , mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)