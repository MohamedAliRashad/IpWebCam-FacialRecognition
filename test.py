import requests
import cv2
import numpy as np
import time

web = "http://192.168.43.1:8080/shot.jpg"

start_time = time.time()
counter = 0

while True:

	page = requests.get(web)
	
	imgN = np.array(bytearray(page.content), dtype = np.uint8)

	img = cv2.imdecode(imgN, -1)

	cv2.imshow('Frame', img)

	counter += 1

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print("Time elapsed: {}".format(time.time() - start_time))
print("Approx. fps: {}".format(counter/(time.time()-start_time)))
cv2.destroyAllWindows()
