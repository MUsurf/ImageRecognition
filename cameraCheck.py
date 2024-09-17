import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not accessible or not found")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    cv.imshow('Camera Test', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


