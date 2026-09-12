from insightface.app import FaceAnalysis
import mediapipe as mp
from database import add_student,get_students,mark_attendance
import cv2
import numpy as np
app=FaceAnalysis(
    name="buffalo_l",
    # buffalo_l is a pretrained model for face detection and recognition
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=0,det_size=(640,640))
from camera import get_camera,get_frame

BaseOptions=mp.tasks.BaseOptions
FaceDetector=mp.tasks.vision.FaceDetector
FaceDetectorOptions=mp.tasks.vision.FaceDetectorOptions
VisionRunningMode=mp.tasks.vision.RunningMode

def create_detector():
    options=FaceDetectorOptions(
        base_options=BaseOptions(
            model_asset_path="models/blaze_face_short_range.tflite"
        ),
        running_mode=VisionRunningMode.IMAGE
    )
    return FaceDetector.create_from_options(options)
detector=create_detector()

def detect_faces(detector,frame):
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    image=mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )
    # converting rgb to bgr here because mediapipe take rgb as input
    result=detector.detect(image)
     # now converting it to mediapipe image format as rgb is still a numpy array and media pipe needs image format
    return result.detections

cap=get_camera()

while True:
    if not cap.isOpened():
        break
    frame=get_frame(cap)
    if frame is None:
        break
    detections=detect_faces(detector,frame)
   
    # detection contains the info about the detected face
    if detections:
        for detection in detections:
            bbox=detection.bounding_box
            x=bbox.origin_x
            y=bbox.origin_y
            width=bbox.width
            height=bbox.height
            face = frame[y:y+height, x:x+width]
            embedding=app.models["recognition"].get_feat(face)
            embedding=embedding[0]
            students=get_students()
            best_similarity=-1
            best_student=None
            for student in students:
                student_id,name,embedding_blob=student
                saved_embedding=np.frombuffer(embedding_blob,dtype="float32")
                similarity=np.dot(saved_embedding,embedding)/(
                    np.linalg.norm(saved_embedding)*np.linalg.norm(embedding)
                )
                if similarity>best_similarity:
                    best_similarity=similarity
                    best_student=(student_id,name)
            if best_student and best_similarity>0.6:
                print("Recognized Student:",best_student[1],best_similarity)
                mark_attendance(best_student[0])
            else:
                print("Unknown Student",best_similarity)
            key=cv2.waitKey(1) & 0xFF
            if key==ord('r'):
                    add_student("5001","Sahir",embedding)
                    print("Face registered")
            # print(embedding.shape)
            
            # similarity=np.dot(saved_embedding,embedding)/(
            #     np.linalg.norm(saved_embedding)*np.linalg.norm(embedding)
            # )
            # print(similarity)
            # if similarity>0.6:
            #     print("Face Matched")
            # else:
            #     print("Face Not Matched")

            # this code is for face recognition and getting the embedding of the detected face
            # if faces:
            #     embedding=faces[0].embedding
            #     if "saved_embedding" not in locals():
            #         saved_embedding=embedding
            #     similarity=np.dot(saved_embedding,embedding)/(
            #         np.linalg.norm(saved_embedding)*np.linalg.norm(embedding)
            #     )
            #     print(similarity)
            cv2.rectangle(
                frame,
                (x,y),
                (x+width,y+height),
                (0,255,0),
                2
            )
            # this is to show the rectangle around the detected face , the upper code
            cv2.imshow("Face",face)
    cv2.imshow("Camera",frame)
    
    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()