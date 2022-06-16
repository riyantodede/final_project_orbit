from flask import Flask,render_template,Response, url_for
from flask import request
import cv2
import time
import os

faceCasecade = faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eyesCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
mouthCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

app=Flask(__name__)
video_capture = cv2.VideoCapture(0)

def generate_frames():
    Terbangun = False
    while True:
        success,frame=video_capture.read()
        if not success:
            break
        else:
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            wajah = faceCascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in wajah:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                if Terbangun:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.putText(frame,'Mengantuk', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),5)
                    os.system('emergency-alert-alarm.wav')
                    time.sleep(1)
                else :
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    cv2.putText(frame,'Terjaga', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0),5)

                mata = eyesCascade.detectMultiScale(roi_gray, 1.18, 35)
                for (sx, sy, sw, sh) in mata :
                    cv2.rectangle(roi_color, (sh, sy), (sx+sw, sy+sh), (255, 0, 0), 2)
                    cv2.putText(frame, 'Mata', (x + sx, y + sy), 1, 1, (0, 255, 0), 1)

                if len(mata)>0:
                    Terbangun = False
                else :
                    time.sleep(5)
                    Terbangun = True

                mulut = mouthCascade.detectMultiScale(roi_gray, 1.18, 35)
                for (sx, sy, sw, sh) in mulut :
                    cv2.rectangle(roi_color, (sh, sy), (sx+sw, sy+sh), (255, 0, 0), 2)
                    cv2.putText(frame, 'Mulut', (x + sx,y + y), 1, 1, (0, 255, 0), 1)

                if len(mulut)>0:
                    Terbangun = False
                else :
                    time.sleep(5)
                    Terbangun = True

            
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)