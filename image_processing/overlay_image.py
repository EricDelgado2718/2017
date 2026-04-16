import numpy as np
import cv2
from cv2_enumerate_cameras import enumerate_cameras
from pupil_apriltags import Detector

CAMERA_PARAMS = (1710.4, 1707.8, 919.6875, 523.0886)  # fx, fy, cx, cy
TAG_SIZE = 0.165  # meters

K = np.array([[CAMERA_PARAMS[0], 0, CAMERA_PARAMS[2]],
              [0, CAMERA_PARAMS[1], CAMERA_PARAMS[3]],
              [0, 0, 1]], dtype=np.float64)
DIST = np.zeros(5)

def detect_apriltags(frame, detector, feed = True):
    if not feed:
        image = cv2.imread("./ID5.png")
    else:
        image = frame

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    results = detector.detect(gray, estimate_tag_pose=True,
                              camera_params=CAMERA_PARAMS, tag_size=TAG_SIZE)

    for r in results:
        rvec, _ = cv2.Rodrigues(r.pose_R)
        tvec = r.pose_t
        cv2.drawFrameAxes(image, K, DIST, rvec, tvec, TAG_SIZE * 0.5, 3)

        distance = float(np.linalg.norm(tvec))

        ptA = r.corners[0]
        cv2.putText(image, f"ID {r.tag_id}", (int(ptA[0]), int(ptA[1]) - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(image, f"d={distance:.2f}m", (int(ptA[0]), int(ptA[1]) - 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

def detect_buoys(image):
    def draw_bounding_box(image, mask, color, kernel_size = 5, iterations = 3):
        kernel = np.ones((kernel_size,kernel_size), np.uint8)

        erosion = cv2.erode(mask, kernel, iterations=3)
        dilation = cv2.dilate(erosion, kernel, iterations=3)
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 4)

    # convert image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    light_lower_red = np.array([0, 50, 50])
    light_upper_red = np.array([10, 255, 255])

    dark_lower_red = np.array([160, 50, 50])
    dark_upper_red = np.array([180, 255, 255])

    light_red_mask = cv2.inRange(hsv_image, light_lower_red, light_upper_red)
    dark_red_mask = cv2.inRange(hsv_image, dark_lower_red, dark_upper_red)
    red_mask = cv2.bitwise_or(light_red_mask, dark_red_mask)

    draw_bounding_box(image, green_mask, (0, 255, 0))
    draw_bounding_box(image, red_mask, (0, 0, 255))

def get_camera_position(tag1, tag2,intertag_dist = 1):
    angle = np.acos((intertag_dist**2 + tag1**2 + tag2**2 )/ (2 * tag1 * tag2))
    # Herons Formula
    s = 1/2 * (intertag_dist + tag1 + tag2)
    area = np.sqrt(s*(s-a)*(s-b)*(s-c))
    perpendicular_distance = 2 * area / intertag_dist


def main():
    # set up camera
    cap = False
    for cam_info in enumerate_cameras():
        if "EMEET" in cam_info.name:
            cap = cv2.VideoCapture(cam_info.index)
            print("EMEET CAMERA FOUND")
            break

    if not cap:
        raise Error("EMEET Camera not found")

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    image_family = "tag36h11"
    detector = Detector(image_family)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        detect_apriltags(frame, detector)
        detect_buoys(frame)
        cv2.imshow("Result", frame)
        if cv2.waitKey(1) & 0xFF == ord('1'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
