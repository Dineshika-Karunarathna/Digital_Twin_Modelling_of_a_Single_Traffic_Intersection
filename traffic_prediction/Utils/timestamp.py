import cv2

vidcap = cv2.VideoCapture('C:\\Users\\janit\\Desktop\\day.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)
success,image = vidcap.read()
count = 0
success = True

while success:
    success,frame = vidcap.read()
    count+=1
    print("time stamp current frame:",count/fps)