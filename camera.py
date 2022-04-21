import cv2
import pickle
from imutils.video import WebcamVideoStream
#import face_recognition

class VideoCamera(object):

    count = 0
    skip = 120
    arrayOfFrames = []
    def __init__(self):

        
        self.stream = WebcamVideoStream(src=0).start()

    def end(self):
        self.stream.stop()
        return self.arrayOfFrames


    # def predict(self, frame, knn_clf, distance_threshold=0.4):
    #     # Find face locations
    #     X_face_locations = face_recognition.face_locations(frame)
    #     # print("X_face_locations",X_face_locations[0])
    #     # X_face_locations[0][0]: X_face_locations[0][1], X_face_locations[0][2]: X_face_locations[0][3]
    #     # try:
    #     #     print("here")
    #     #     cv2.imshow("fdgd",frame[57:304,242:118])
    #     #     cv2.waitKey(1)
    #     # except:
    #     #     pass
    #     # If no faces are found in the image, return an empty result.
    #     if len(X_face_locations) == 0:
    #         return []
    #
    #     # Find encodings for faces in the test iamge
    #     faces_encodings = face_recognition.face_encodings(frame, known_face_locations=X_face_locations)
    #
    #     # Use the KNN model to find the best matches for the test face
    #     closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    #     are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    #     for i in range(len(X_face_locations)):
    #         print("closest_distances")
    #         print(closest_distances[0][i][0])
    #
    #     # Predict classes and remove classifications that aren't within the threshold
    #     return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
    #             zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

    def imdet(self,image):
        cascade_classifier = cv2.CascadeClassifier('F:/OpenFace_2.2.0_win_x64/OpenFace_2.2.0_win_x64/classifiers/haarcascade_frontalface_default.xml')
        faces = cascade_classifier.detectMultiScale(
                image,
                scaleFactor=1.3,
                minNeighbors=5
            )
            #  None is we don't found an image
        if not len(faces) > 0:
            return None
        max_area_face = faces[0]
        for face in faces:
            if face[2] * face[3] > max_area_face[2] * max_area_face[3]:
                max_area_face = face
                # Chop image to face
        face = max_area_face
        image = image[face[1]:(face[1] + face[2]), face[0]:(face[0] + face[3])]
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return grayscale_image

    def get_frame(self):
        image = self.stream.read()
        #global skip
        self.count +=1
        self.skip -=1
        if (self.skip == 0):
            self.skip = 120
            li = []
            global person_name
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
    #        f = open("trainStatus.txt")
    #        for i in f:
    #            isTrained = int(i)
    #        if isTrained:  # change updated model file
                # load again
    #            with open("trained_knn_model.clf", 'rb') as f:
    #                self.knn_clf = pickle.load(f)
    #            file = open("trainStatus.txt", "w")
    #            file.write("0")
    #            file.close()
            cv2.imwrite('C:/Users/adibw/Downloads/GP_PROJECT_final/GP_PROJECT/frames/'+str(self.count)+'.jpg',image)
            predictions = self.imdet(image)

            name = ''
 #           for name, (top, right, bottom, left) in predictions:
 #               startX = int(left)
 #               startY = int(top)
 #               endX = int(right)
 #               endY = int(bottom)

#                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
    #            cv2.putText(image, name, (endX - 70, endY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            if type(predictions) is not None :
                #ret, jpeg = cv2.imencode('.jpg', predictions)
                #data = []
                #data.append(jpeg.tobytes())
        #        data.append(name)
                if predictions is not None:
                    predictions= cv2.resize(predictions,(48,48))
                    cv2.imwrite('C:/Users/adibw/Downloads/GP_PROJECT_final/GP_PROJECT/faces/'+str(self.count)+'.jpg',predictions)

                    self.arrayOfFrames.append(predictions)
