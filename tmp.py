import cv2, os, time
import numpy as np

def c(d, e):
    a = np.zeros((d,e), dtype=np.int)
    b = cv2.merge((a,a,a))
    cv2.imwrite("asdf.jpg", a)
    return os.path.getsize("asdf.jpg")

S = 336
cnt = 1
while True:
    q = c(1,cnt)
    if q > S:
        break
    cnt += 1
    time.sleep(0.02)
print(cnt)
print(q)

# 9, 16, 32,
