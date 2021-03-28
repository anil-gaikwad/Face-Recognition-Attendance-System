#anil gaikwad
import dlib
import numpy as np
import cv2
import os
import shutil
import time

#database()
# Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()
class Face_Register:
    def __init__(self):
        self.path_photos_from_camera = "data/face_images/"
        self.font = cv2.FONT_ITALIC
        self.ss_cnt = 0                  #  cnt for screen shots

        self.existing_faces_cnt = 0
        self.save_flag = 1               #  The flag to control if save
        self.press_n_flag = 0            # The flag to check if press 'n' before 's'

    #  Make dir for saving photos and csv
    def pre_work_mkdir(self):
        #  Create folders
        if os.path.isdir(self.path_photos_from_camera):
            pass
        else:
            os.mkdir(self.path_photos_from_camera)

    #  Delete the old data of faces
    def pre_work_del_old_face_folders(self):
        folders_rd = os.listdir(self.path_photos_from_camera)
        for i in range(len(folders_rd)):
            shutil.rmtree(self.path_photos_from_camera+folders_rd[i])
        if os.path.isfile("data/features_all.csv"):
            os.remove("data/features_all.csv")
    #  Start from person_x+1
    def check_existing_faces_cnt(self):
        if os.listdir("data/face_images/"):
            #  Get the order of latest person
            person_list = os.listdir("data/face_images/")
            person_num_list = []
            for person in person_list:
                person_num_list.append(int(person.split('_')[-1]))
    # note on camera
    def draw_note(self, img_rd):
        cv2.putText(img_rd, "welcome ", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "press N & S", (20, 400), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    #  Main process of face detection and saving
    def process(self, stream):
        self.pre_work_mkdir()
        # checking images in folder
        self.check_existing_faces_cnt()

        while stream.isOpened():
            flag, img_rd = stream.read()  # get camera video stream
            img_rd = cv2.flip(img_rd, 1)
            kk = cv2.waitKey(1)
            faces = detector(img_rd, 0)   # Using Dlib face detector

            #   Press 'n' to create the folders for saving faces
            if kk == ord('n'):
                self.existing_faces_cnt += 1
                current_face_dir = self.path_photos_from_camera + "person_" + str(self.existing_faces_cnt)
                os.makedirs(current_face_dir)
                print("Create folders: ", current_face_dir)

                self.ss_cnt = 0          # Clear the cnt of screen shots
                self.press_n_flag = 1    #  Pressed 'n' already

            #  Face detected
            if len(faces) != 0:
                #  Show the ROI of faces
                for k, d in enumerate(faces):
                    #  Compute size of rectangle box
                    height = (d.bottom() - d.top())
                    width = (d.right() - d.left())
                    hh = int(height/2)
                    ww = int(width/2)

                    #  size of ROI > 480x640
                    if (d.right()+ww) > 640 or (d.bottom()+hh > 480) or (d.left()-ww < 0) or (d.top()-hh < 0):
                        cv2.putText(img_rd, "OUT OF RANGE", (20, 300), self.font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                        color_rectangle = (0, 0, 255)
                        save_flag = 0
                    else:
                        color_rectangle = (255, 255, 255)
                        save_flag = 1

                    cv2.rectangle(img_rd,
                                  tuple([d.left() - ww, d.top() - hh]),
                                  tuple([d.right() + ww, d.bottom() + hh]),
                                  color_rectangle, 3)
                    # Create blank image according to the size of face detected
                    img_blank = np.zeros((int(height*2), width*2, 3), np.uint8)
                    if save_flag:
                        #  Press 's' to save faces
                        if kk == ord('s'):
                            # Check if you have pressed 'n'
                            if self.press_n_flag:
                                self.ss_cnt += 1
                                for ii in range(height*2):
                                    for jj in range(width*2):
                                        img_blank[ii][jj] = img_rd[d.top()-hh + ii][d.left()-ww + jj]
                                cv2.imwrite(current_face_dir + "/image" + str(self.ss_cnt) + ".jpg", img_blank)
                                print("Save ", str(current_face_dir) + "/image" + str(self.ss_cnt) + ".jpg")

            self.draw_note(img_rd)
            #  exits
            if kk == ord('q'):
                break

            cv2.namedWindow("camera", 1)
            cv2.imshow("camera", img_rd)

    def run(self):
        cap = cv2.VideoCapture(0)
        self.process(cap)

        cap.release()
        cv2.destroyAllWindows()

def main():
    Face_Register_con = Face_Register()
    Face_Register_con.run()


if __name__ == '__main__':

    main()