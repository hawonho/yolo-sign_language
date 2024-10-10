import cv2
import matplotlib.pyplot as plt
import mediapipe as mp

from ultralytics import YOLO

model = YOLO("c:/ai_project01/sign_language_yolo_model.pt")

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:

    while cap.isOpened()==True:
        success, image = cap.read()

        if success==False:
            continue

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks != None:

            #cv2.putText(
            #    image,
            #    text="Detect Hand!!!",
            #    org=(300, 50),
            #    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            #    fontScale=1,
            #    color=(0, 0, 255),
            #    thickness=2
            #)
            #print("손 찾았음!!!!!!!")
            results = model.predict(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), imgsz=800)

            for r in results:
                boxes = r.boxes

                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]

                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)

                    cv2.rectangle(image,
                                  (x1, y1),
                                  (x2, y2),
                                  (0, 255, 0),
                                  3
                    )
                    print("box.cls=", box.cls)
                    cls = int(box.cls[0])
                    print("model.names=", model.names)
                    cls_name = model.names[cls]
                    print("box.conf[0]=", box.conf[0])

                    conf_score = float(box.conf[0])
                    confidence = round(conf_score, 2)
                    yolo_text = cls_name + ":" + str(confidence)

                    cv2.putText(
                        image,
                        text=yolo_text,
                        org=(x1, y1),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(0, 255, 0),
                        thickness=2
                    )

        cv2.imshow('webcam_window01', image)

        if cv2.waitKey(1) == ord('q'):
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #plt.imsave("cam_img.jpg", image)
            break

cap.release()