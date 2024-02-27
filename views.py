from flask import Blueprint, render_template, request, jsonify, redirect, url_for, Response
import random
import numpy as np
import cv2
import mediapipe as mp
import pickle
import pandas as pd
from socketio_instance import socketio
from flask_socketio import SocketIO, emit


#### SETUP THE BLUEPRINT AND HOME REDIRECTION
views = Blueprint(__name__, "views")

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@views.route('/') # return html
def home():
    return render_template('index.html', name = "Santiago", age= 20)

#### POSE CLASSIFICATION MODEL USING MEDIAPIPE AND FROM THE TRAINED DATA ON FILE body_language.pkl
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

with open('body_language.pkl', 'rb') as f:
    model = pickle.load(f)


@views.route('/video_feed') # return html
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') # return the response object


def gen_frames(): 
    camera = cv2.VideoCapture(0)  # Use 0 for web camera
    previous_class = None

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            success, frame = camera.read()  # Read the camera frame
            if not success:
                break
            else:
                # Recolor Feed
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False        

                # Make Detections
                results = holistic.process(image)

                # Recolor image back to BGR for rendering
                image.flags.writeable = True   
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Draw face landmarks
                mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                                        mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                        mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                        )

                # Right hand
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                        )

                # Left Hand
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                        )

                # Pose Detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                        )

                # Export coordinates
                try:
                    # Extract Pose landmarks
                    pose = results.pose_landmarks.landmark
                    pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                    
                    # Extract Face landmarks
                    face = results.face_landmarks.landmark
                    face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())
                    
                    # Concate rows
                    row = pose_row+face_row

                    # Make Detections
                    X = pd.DataFrame([row])
                    body_language_class = model.predict(X)[0]
                    body_language_prob = model.predict_proba(X)[0]

                    #new code for socket
                    print(f"Emitting pose classification: {body_language_class}")  # Add this line
                    socketio.emit('pose_classification', {'classification': body_language_class})
                    
                    # Grab ear coords
                    coords = tuple(np.multiply(
                                    np.array(
                                        (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x, 
                                         results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
                            , [640,480]).astype(int)) #640-480 are the dimensions of the camera
                    
                    cv2.rectangle(image, 
                                  (coords[0], coords[1]+5), 
                                  (coords[0]+len(body_language_class)*20, coords[1]-30), 
                                  (245, 117, 16), -1)
                    cv2.putText(image, body_language_class, coords, 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    
                    # Get status box
                    cv2.rectangle(image, (0,0), (250, 60), (245, 117, 16), -1)
                    
                    # Display Class
                    cv2.putText(image, 'CLASS'
                                , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class.split(' ')[0]
                                , (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    
                    # Display Probability
                    cv2.putText(image, 'PROB'
                                , (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)],2))
                                , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    
                except:
                    pass

                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    camera.release()


#### 3D OBJECTS GENERATION

@views.route('/objects3d', methods=["GET"])
def generate_objects(num_objects=1):
    objects = []
    for _ in range(num_objects):
        shape = np.random.choice(["sphere", "cube"])
        size = np.random.uniform(0.1, 1.0)
        x = np.random.uniform(-1.0, 1.0)
        y = np.random.uniform(-1.0, 1.0)
        z = np.random.uniform(-1.0, 1.0)
        color = np.random.rand(3) * 255
        rotation = np.random.rand(3) * 0.05  # Add rotation speed
        obj = {
            "shape": shape,
            "size": size,
            "x": x,
            "y": y,
            "z": z,
            "color": color.tolist(),
            "rotation": rotation.tolist()  # Add rotation speed to the object
        }
        objects.append(obj)
    return jsonify(objects)