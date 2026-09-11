import mediapipe as mp
import cv2
BaseOptions=mp.tasks.BaseOptions
FaceDetector=mp.tasks.vision.FaceDetector
FaceDetectorOptions=mp.tasks.vision.FaceDetectorOptions
VisionRunningMode=mp.tasks.vision.RunningMode
options=FaceDetectorOptions(
    base_options=BaseOptions(
        model_asset_path="models/blaze_face_short_range.tflite"
    ),
    running_mode=VisionRunningMode.IMAGE
)
detector=FaceDetector.create_from_options(options)

cap=cv2.VideoCapture(0)

ret,frame=cap.read()
rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
# converting rgb to bgr here because mediapipe take rgb as input

# now converting it to mediapipe image format as rgb is still a numpy array and media pipe needs image format

image=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb)

result=detector.detect(image)

# detection contains the info about the detected face
if result.detections:
    for detection in result.detections:
        bbox=detection.bounding_box
        x=bbox.origin_x
        y=bbox.origin_y
        width=bbox.width
        height=bbox.height
        print(x,y,width,height)
        face=frame[y:y+height,x:x+width]
        cv2.imshow("Face",face)
        cv2.waitKey(0)
        # this is basically to wait for a key press to close the window

print(len(result.detections))