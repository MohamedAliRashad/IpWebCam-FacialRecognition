import cv2
import numpy as np
import os
import argparse
import face_recognition
import time 

# Some Argments For The project to be cooler :)
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ip', help = "ip address of the ip webcam app", required=True)
parser.add_argument('-p', '--path', help = "path to the training images", default="Training_images")
args = parser.parse_args()


# The URL to the javascript web page
url = "http://" + args.ip + "/video"

# Declaring some variables
known_faces = []
known_names = []


# Looping over the images in the training image path and extracting information from them
for image in os.listdir(args.path):
	image_loaded = face_recognition.load_image_file(args.path + '/' + image)
	face_encoding = face_recognition.face_encodings(image_loaded)[0]
	known_faces.append(face_encoding)
	known_names.append(image.split('.')[0])

# Declaring some other variables
face_locations = []
face_encodings = []
face_names = []
font = cv2.FONT_HERSHEY_DUPLEX
process_this_image = True
start_time = time.time()
counter = 0

# The Fastest way i found
cap = cv2.VideoCapture(url)

while True:
	
	# Read From Video object directly
	ret, frame = cap.read()
	
	# Resizing the frame to 1/4 the size for a faster recognition
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

	# Convert the image from BGR to RGB
	rgb_small_frame = small_frame[:, :, ::-1]

	# For a clean list
	face_names = []

	# Only process every other image in the video to save time
	if process_this_image:
		
		# Processing frames
		face_locations = face_recognition.face_locations(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

		for face_encoding in face_encodings:
			
			# Comparing faces
			match = face_recognition.compare_faces(np.array(known_faces), face_encoding)
			name = "Unknown"

			for i in range(len(match)):
				
				# Finding a match
				if match[i]:
					name = known_names[i]
					break
			
			face_names.append(name)
		
	process_this_image = not process_this_image

	# Display The Results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
	
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4
		
		# Drawing a box around the face  
		cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
		
		# Draw a label with the name inside it
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0,0,255), cv2.FILLED)
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255,255,255), 1)

	counter += 1

	# Displaying Video
	cv2.imshow("Video", frame)

	# Hit 'q' to exit
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

# Printing The elapsed time & approximated fps
print("Elapsed Time: {}".format(time.time() - start_time))
print("Approx. FPS: {}".format(counter/(time.time() - start_time)))

# Cleaning up
cv2.destroyAllWindows()
