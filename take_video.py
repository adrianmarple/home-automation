import ctypes
import cv2
import numpy as np
import time
import threading
import ctypes

import clapper
import send_keys

MAX_VIDEO_LENGTH = 30  # seconds
TEMP_VIDEO_PATH = 'temp.avi'
FPS_TEST_LENGTH = 10
FPS = 10
FRAME_DURATION_MS = 1000 / FPS
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)


def crop_to_ratio(img, w, h, ratio=float(SCREEN_WIDTH) / SCREEN_HEIGHT):
    if h * ratio > w:
        new_h = w / ratio
        y0 = (h - new_h) / 2
        y1 = y0 + new_h
        x0 = 0
        x1 = w
    else:
        new_w = h * ratio
        x0 = (w - new_w) / 2
        x1 = x0 + new_w
        y0 = 0
        y1 = h
    return img[y0:y1, x0:x1]


while True:
    cap = cv2.VideoCapture(0)
    start = time.time()
    for i in xrange(FPS_TEST_LENGTH):
        ret, frame = cap.read()
        cv2.waitKey(1)
    end = time.time()
    FRAME_DURATION_MS = int(1000 * (end - start) / FPS_TEST_LENGTH)
    FPS = 1000.0 / FRAME_DURATION_MS
    print 'FRAME_DURATION_MS:', FRAME_DURATION_MS, 'FPS:', FPS

    clapper.wait_for_claps(2)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        'frame', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

    w = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
    h = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
    fourcc = cv2.cv.CV_FOURCC('M', 'S', 'V', 'C')
    out = cv2.VideoWriter(TEMP_VIDEO_PATH, fourcc, FPS, (w, h))
    start = time.time()
    clap_listener = clapper.ClapListener(1, timeout=MAX_VIDEO_LENGTH)
    while True:
        ret, frame = cap.read()
        out.write(frame)
        frame = crop_to_ratio(frame, w, h)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        if (MAX_VIDEO_LENGTH and time.time() - start > MAX_VIDEO_LENGTH) \
                or not clap_listener.isAlive():
            break
    cap.release()
    out.release()

    clapper.wait_for_claps(1)

    cap = cv2.VideoCapture(TEMP_VIDEO_PATH)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        frame = crop_to_ratio(frame, w, h)
        cv2.imshow('frame', frame)
        if cv2.waitKey(FRAME_DURATION_MS) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
