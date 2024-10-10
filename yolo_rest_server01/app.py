from flask import Flask
from flask import request
import base64
import json
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('c:/ai_project01/sign_language_yolo_model.pt')

app = Flask(__name__)

#@app.route('/hello_rest_server', methods = ['POST'])
#def hello_world() :
#    return '안녕 난 rest server야'
#

@app.route("/image_test01", methods = ["POST"])
def image_send_test01() :
    image = request.get_json()
    print("image = ", image)
    return "스프링이 보낸 이미지 잘 받았습니다!!"

@app.route("/image_test02", methods = ["POST"])
def image_send_test02() :
    image = request.get_json()
    print("image = ", image)

    encoded_data = image.get("data")
    encoded_data = encoded_data.replace("image/jpeg;base64,","")
    decoded_data = base64.b64decode(encoded_data)

    with open('image.jpg', 'wb') as f :
        f.write(decoded_data)

    return "스프링이 보낸 이미지 잘 저장 했습니다!";

@app.route("/detect", methods = ["POST"])
def detect_yolo() :
    image = request.get_json()

    #print(" = " * 100)
    #print("image = ", image)
    #print(" = " * 100)

    encoded_data = image.get("data")
    encoded_data = encoded_data.replace("image/jpeg;base64,", "")
    decoded_data = base64.b64decode(encoded_data)
    #print(" = " * 100)
    #print("decoded_data = ", decoded_data)
    #print(" = " * 100)

    nparr = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #print("img = ", img)

    results = model.predict(img, imgsz = 640)
    #detect_img = results[0].plot()
    #cv2.imwrite('detect_result.jpg', detect_img)
    box_result = []
    for r in results :
        boxes = r.boxes
        for box in boxes :
            left, top, right, bottom = box.xyxy[0]
            cls = int(box.cls)
            cls_name = model.names[cls]
            conf = float(box.conf)
            if conf > 0.25 :
                box_result.append({
                    "left" : int(left), "top" : int(top), "right" : int(right),
                    "bottom" : int(bottom), "cls" : cls_name, "conf" : float(conf)
                })
    return json.dumps(box_result)

@app.route("/param_rest_server", methods = ['POST'])
def hello_rest2():
    param_name = request.form.get('name', '입력값 없음')
    print("param_name = ", param_name)
    return "그래 너의 이름은 " + param_name + " 이구아나!!"

if __name__ == '__main__' :
    app.run()
