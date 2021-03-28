#anil gaikwad
#face detection and recognition
import dlib
import numpy as np
from cv2 import cv2
import pandas as pd
import os
import time
from PIL import Image, ImageDraw, ImageFont
from subprocess import call
import second1

# Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()
# Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
# Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

class Face_Recognizer:
    def __init__(self):
        self.feature_known_list = []  # Save the features of faces in the database
        self.name_known_list = []  # Save the name of faces in the database
        self.current_frame_feature_list = []  # Features of faces in current frame
        self.current_frame_name_position_list = []  # Positions of faces in current frame
        self.current_frame_name_list = []  # Names of faces in current frame
    # Get known faces from "features_all.csv"
    def get_face_database(self):
        if os.path.exists("data/features_all.csv"):
            path_features_known_csv = "data/features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                for j in range(0, 128):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.feature_known_list.append(features_someone_arr)
                self.name_known_list.append("Person_" + str(i + 1))
            return 1
        else:
            return 0
    # Compute the e-distance between two 128D features
    @staticmethod
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    def draw_note(self, img_rd):
        font = cv2.FONT_ITALIC
        cv2.putText(img_rd, "Face Recognizer", (20, 40), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_name(self, img_rd):
        # rectangle
        font = ImageFont.truetype("data/Hack-Regular.ttf", 30)
        img = Image.fromarray(cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        for i in range(self.current_frame_face_cnt):

            draw.text(xy=self.current_frame_name_position_list[i], text=self.current_frame_name_list[i], font=font)
            img_with_name = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_with_name
    def show_student_name(self):
        # Default  name: person_1,
        if self.current_frame_face_cnt >= 1:
            #data = pd.read_excel(r'data/excel/data.xlsx')
            #df = pd.DataFrame(data, columns=['Name'])
            self.name_known_list[0] = 'anil'.encode('utf-8').decode()
            #self.name_known_list = 'df'.encode('utf-8').decode()

    #  Face detection and recognition from input video stream
    def process(self, stream):
        #  Get faces known from "features.all.csv"
        if self.get_face_database():
            while stream.isOpened():
                flag, img_rd = stream.read()
                img_rd = cv2.flip(img_rd, 1) ##set Flip mode camera
                faces = detector(img_rd, 0)
                kk = cv2.waitKey(1)
                # Press 'q' to quit
                if kk == ord('q'):
                    #second1.Login()
                    break

                else:
                    self.draw_note(img_rd)
                    self.current_frame_feature_list = []
                    self.current_frame_face_cnt = 0
                    self.current_frame_name_position_list = []
                    self.current_frame_name_list = []
                    # Face detected in current frame
                    if len(faces) != 0:
                        # face descriptors for faces in current frame
                        for i in range(len(faces)):
                            shape = predictor(img_rd, faces[i])
                            self.current_frame_feature_list.append(
                                face_reco_model.compute_face_descriptor(img_rd, shape))
                        #  Traversal all the faces in the database
                        for k in range(len(faces)):
                            #  Set the default names of faces with "unknown"
                            self.current_frame_name_list.append("unknown")
                            # Positions of faces captured
                            self.current_frame_name_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                            #faces detected, compare the faces in the database
                            current_frame_e_distance_list = []
                            for i in range(len(self.feature_known_list)):

                                if str(self.feature_known_list[i][0]) != '0.0':
                                    e_distance_tmp = self.return_euclidean_distance(self.current_frame_feature_list[k],
                                                                                    self.feature_known_list[i])
                                    #print(e_distance_tmp)
                                    current_frame_e_distance_list.append(e_distance_tmp)
                                else:
                                    current_frame_e_distance_list.append(999999999)
                            # Find the one with minimum e distance
                            similar_person_num = current_frame_e_distance_list.index(min(current_frame_e_distance_list))
                            if min(current_frame_e_distance_list) < 0.4:
                                self.current_frame_name_list[k] = self.name_known_list[similar_person_num]
                            # Draw rectangle
                            for kk, d in enumerate(faces):
                                cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]),
                                              (0, 255, 255), 2)
                        self.current_frame_face_cnt = len(faces)

                        self.show_student_name()
                        img_with_name = self.draw_name(img_rd)

                    else:
                        img_with_name = img_rd
                cv2.imshow("Camera", img_with_name)

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 480)  # 640x480
        self.process(cap)

        cap.release()
        cv2.destroyAllWindows()

def main():
    Face_Recognizer_con = Face_Recognizer()
    Face_Recognizer_con.run()

if __name__ == '__main__':
    main()