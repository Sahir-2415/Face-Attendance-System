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
FaceLandmarker=mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions=mp.tasks.vision.FaceLandmarkerOptions

# gives detailed points on the face

# function used to set up face landmarker - 468ish points on the face
def create_landmarker():
    options=FaceLandmarkerOptions(
        base_options=BaseOptions(
            model_asset_path="models/face_landmarker.task"
            # load the model
        ),
        running_mode=VisionRunningMode.IMAGE,
        # means i will give you images 1 at a time
        num_faces=1
        # only detect one face
    )
    return FaceLandmarker.create_from_options(options)
    # this is the actual landmarker
landmarker=create_landmarker()

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

    landmark_result=landmarker.detect(image)
    if landmark_result.face_landmarks:
        landmarks=landmark_result.face_landmarks[0]
        print("Landmarks detected:",len(landmarks))
    else:
        landmarks=None
    # converting rgb to bgr here because mediapipe take rgbqqqq as input
    result=detector.detect(image)
    print("Faces detected:", len(result.detections))
     # now converting it to mediapipe image format as rgb is still a numpy array and media pipe needs image format
    return result.detections,landmarks

cap=get_camera()
marked_students=set()

def align_face(frame,landmarks):
    h,w,_=frame.shape
    points=np.array([
        [landmarks[33].x*w,landmarks[33].y*h],
        [landmarks[263].x*w,landmarks[263].y*h],
        [landmarks[1].x*w,landmarks[1].y*h],
        [landmarks[61].x*w,landmarks[61].y*h],
        [landmarks[291].x*w,landmarks[291].y*h],
    ],dtype=np.float32)

    reference_points=np.array([
        [38.2946, 51.6963],
        [73.5318, 51.5014],
        [56.0252, 71.7366],
        [41.5493, 92.3655],
        [70.7299, 92.2041]
    ],dtype=np.float32)
    transform,_=cv2.estimateAffinePartial2D(
        points,reference_points
    )
    aligned_face=cv2.warpAffine(
        frame,transform,
        (112,112)
    )
    return aligned_face



while True:
    if not cap.isOpened():
        break
    frame=get_frame(cap)
    if frame is None:
        break
    detections,landmarks=detect_faces(detector,frame)
    print("landmarks:", landmarks is not None)
   
    # detection contains the info about the detected faceqqqqqqq
    if detections and landmarks:
        for detection in detections:
            bbox=detection.bounding_box
            x=bbox.origin_x
            y=bbox.origin_y
            width=bbox.width
            height=bbox.height
            # face = frame[y:y+height, x:x+width]
            aligned_face=align_face(frame,landmarks)
            embedding=app.models["recognition"].get_feat(aligned_face)
            embedding=embedding[0]
            students=get_students()
            print("Students in DB:", len(students))
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
            if best_student and best_similarity>0.5:
                student_id=best_student[0]
                name=best_student[1]
                print("Recognized Student:",best_student[1],best_similarity)
                if student_id not in marked_students:
                    mark_attendance(student_id)
                    marked_students.add(student_id)
                label=f"{name} - Present"
            else:
                label="Unknown"
            key=cv2.waitKey(1) & 0xFF
            if key==ord('r'):
                    student_id=input("Enter student id:")
                    name=input("Enter student name:")
                    add_student(student_id,name,embedding)
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
            cv2.putText(
                frame,label,
                (x,y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                2
            )
            # this is to show the rectangle around the detected face , the upper code
            cv2.imshow("Aligned face",aligned_face)
    cv2.imshow("Camera",frame)
    
    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()