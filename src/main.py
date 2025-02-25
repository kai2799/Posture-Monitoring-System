from PyQt5 import QtWidgets, uic, sip
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox, QLabel, QTableWidgetItem,QVBoxLayout,QWidget
from PyQt5.QtCore import QTimer, QDate, QTime, Qt, pyqtSignal
from PyQt5.QtMultimedia import QSound
import sys
import mysql.connector as mycon
import cv2
import datetime
import os
import numpy as np
import mediapipe as mp


class Main_UI(QtWidgets.QMainWindow):
    def __init__(self, login_app):
        self.log_App = login_app
        self.log_App.show()


class login_UI(QtWidgets.QWidget):    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("login.ui", self)
        # Set the window's icon
        self.setWindowIcon(QIcon("C:/Users/gawoo/F/UI/logo.jpg"))  # Replace with the path to  icon file
        
        # Set the window's title
        self.setWindowTitle("ErgoPosture- Sitting Posture Monitoring Application")

        # Flag to control capturing mode (0: No capture, 1: Waiting for capture, 2: Capturing)
        self.capture_mode = 0

        # Counter for naming captured images
        self.image_counter = 1

        # Flag to control capturing
        self.capture_flag = 1  

        # Initialize improper sitting posture count
        self.improper_sitting_count = 0  


        self.label_26.setText("Off")

        self.toolButton_8.clicked.connect(self.onClicked)
        self.capture_button_text = "START"

        self.toolButton_9.clicked.connect(self.CaptureClicked)
        self.toolButton_9.setEnabled(False)  # Disable capture button initially
        self.toolButton_10.clicked.connect(self.history_btn_clicked) 
        self.toolButton_11.clicked.connect(self.update_button_clicked)
        self.pushButton.clicked.connect(self.ProfileClicked)
        self.pushButton_2.clicked.connect(self.onChangeProfilePicClicked)

        

        # Load and display default image
        self.displayDefaultImage()

        # Initialize variables for posture detection
        self.base_posture = None
        self.algorithm_version = 1 # Set the desired algorithm version (1 or 2)

        # Setup mediapipe instance
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)  # Initialize pose instance

        # Initialize improper sitting time
        self.improper_sitting_time = 0  

        # Start a timer to update the time and date every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)  # Update every 1000 ms (1 second)

        # Initial call to update time and date
        self.updateDateTime()


        self.toolButton.clicked.connect(lambda: self.login_Def())
        self.toolButton_2.clicked.connect(lambda: self.signup_Def())
        self.toolButton_7.clicked.connect(lambda: self.forgot_Def())
        self.toolButton_6.clicked.connect(lambda: self.Background.setCurrentIndex(0))
        self.toolButton_3.clicked.connect(lambda: self.Background.setCurrentIndex(1))
        self.toolButton_4.clicked.connect(lambda: self.Background.setCurrentIndex(0))
        self.toolButton_5.clicked.connect(lambda: self.Background.setCurrentIndex(2))
        self.toolButton_12.clicked.connect(lambda: self.Background.setCurrentIndex(3))
        self.toolButton_13.clicked.connect(lambda: self.Background.setCurrentIndex(3))
        
        
    def login_Def(self):
        try:
            self.msg = QtWidgets.QMessageBox()
            username = self.lineEdit.text()
            password = self.lineEdit_2.text()
            mydb = mycon.connect(host="localhost", user="root", password="",database="fyp_db")
            mycursor = mydb.cursor()

            # Use placeholders in the query to prevent SQL injection
            query = "SELECT * FROM `log_db` WHERE `Username` = %s AND `Password` = %s"
            mycursor.execute(query, (username, password))

            #mycursor.execute("SELECT * FROM `log_db` WHERE `Username=`"+ username + "` and Password=`"+ password +"`")
            result = mycursor.fetchone()

            if not username or not password:
                self.msg.setText("Please fill in all fields!")
                self.msg.exec_()
                return
            
            if result:
                #self.close()
                username = result[0]  # Assuming username is the first column
                # Store the username in an instance variable to access it in other methods
                self.curent_user = username
                # Load and display the user's profile picture
                self.load_profile_picture(self.curent_user)
                # Switch to the desired page after a successful login
                self.label_8.setText(self.curent_user)                
                self.Background.setCurrentIndex(3)

            else:
                self.msg.setText("Incorrect Username or Password")
                self.msg.exec_()

        except mycon.Error as e:
            print("Localhost Not Connected")


    def signup_Def(self):
        try:
            new_username = self.lineEdit_3.text()
            new_password = self.lineEdit_4.text()
            new_confirm_password = self.lineEdit_5.text()
            new_birthday = self.lineEdit_6.text()
            default_profile_pic = "C:/Users/gawoo/F/UI/Profile.png"  # Default profile picture path

            self.msg = QtWidgets.QMessageBox()

            # Check if all fields are filled
            if not new_username or not new_password or not new_confirm_password or not new_birthday:
                self.msg.setText("Please fill in all fields!")
                self.msg.exec_()
                return

            if new_password == new_confirm_password:
                mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
                mycursor = mydb.cursor()

                # Check if the username already exists
                mycursor.execute("SELECT * FROM `log_db` WHERE `Username`=%s", (new_username,))
                result = mycursor.fetchone()

                if result:
                    self.msg.setText("Username already exists!")
                    self.msg.exec_()
                else:
                    # Insert new user into the database including the default profile picture path
                    mycursor.execute("INSERT INTO `log_db` (`Username`, `Password`, `Birthday`, `profile_pic`) VALUES (%s, %s, %s, %s)",
                                 (new_username, new_password, new_birthday, default_profile_pic))
                    mydb.commit()
                    self.msg.setText("Registration successful!")
                    self.msg.exec_()

                    # Clear textboxes after successful sign-up
                    self.lineEdit_3.clear()
                    self.lineEdit_4.clear()
                    self.lineEdit_5.clear()
                    self.lineEdit_6.clear()

            else:
                
                self.msg.setText("Passwords do not match!")
                self.msg.exec_()
                # Clear textboxes after successful sign-up
                self.lineEdit_3.clear()
                self.lineEdit_4.clear()
                self.lineEdit_5.clear()
                self.lineEdit_6.clear()

        except mycon.Error as e:
            print("Localhost Not Connected")
    
    def forgot_Def(self):
        try:
            self.msg = QtWidgets.QMessageBox()
            forgot_username = self.lineEdit_7.text()
            forgot_birthday = self.lineEdit_8.text()
            mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
            mycursor = mydb.cursor()

            # Use placeholders in the query to prevent SQL injection
            query = "SELECT * FROM `log_db` WHERE `Username` = %s AND `Birthday` = %s"
            mycursor.execute(query, (forgot_username, forgot_birthday))
            result = mycursor.fetchone()

            if not forgot_username or not forgot_birthday:
                self.msg.setText("Please fill in all fields!")
                self.msg.exec_()
                return
            
            if result:
                # Display retrieved username and password
                retrieved_username = result[0]  # Assuming the username is in the first column
                retrieved_password = result[1]  # Assuming the password is in the second column

                # Display a message with the retrieved username and password
                message = f"Username: {retrieved_username}\nPassword: {retrieved_password}"
                self.msg.setText(message)
                self.msg.exec_()

                # Clear textboxes after successful sign-up
                self.lineEdit_7.clear()
                self.lineEdit_8.clear()

            else:
                # No records found in the database
                self.msg.setText("No records found in the database.")
                self.msg.exec_()

        except mycon.Error as e:
            print("Localhost Not Connected")
    
    def onClicked(self):
        if self.capture_button_text == "START":
            self.startCapturing()
        else:
            self.stopCapturing()

    def convert_cv_qt(cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)
    
    def startCapturing(self):
        self.label_26.setText("In monitoring...")
        self.capture_button_text = "Stop"
        self.capture_flag = 1
        self.toolButton_9.setEnabled(True)  # Enable capture button when capturing starts

        cap = cv2.VideoCapture(0)
        while cap.isOpened() and self.capture_flag:
            ret, frame = cap.read()
            if ret:
                print('Camera opened')
                # Perform posture detection
                posture_frame = self.detect_posture(frame)
                qimg = QImage(posture_frame.data, posture_frame.shape[1], posture_frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                self.displayImproperImage(qimg)

                if self.capture_mode == 2:
                    self.image_counter += 1
                    cv2.imwrite(f'C:/Users/gawoo/Downloads/{self.image_counter}.jpg', frame)
                    self.capture_mode = 1

                cv2.waitKey(1)
            else:
                print('return not found')

        cap.release()
        cv2.destroyAllWindows()
        self.capture_button_text = "START"
        self.toolButton_8.setText(self.capture_button_text)
        self.toolButton_9.setEnabled(False)  # Disable capture button when capturing stops

    def stopCapturing(self):
        self.capture_flag = 0
        self.displayDefaultImage()
        self.label_26.setText("Off")
        self.base_posture = None  # Clear the extracted landmarks
        # Insert detection session information into the database
        self.insertDetectionSession(self.improper_sitting_count)
        self.improper_sitting_count = 0  # Reset the counter here

    def displayImproperImage(self, qimg, window=1):
        # Since QImage does not have a 'shape' attribute, we directly set the QPixmap.
        self.label_17.setPixmap(QPixmap.fromImage(qimg))
        self.label_17.setAlignment(Qt.AlignCenter)
        self.toolButton_8.setText(self.capture_button_text)

    def insertDetectionSession(self, improper_sitting_count):
        try:
            current_user = self.curent_user
            # Connect to the database
            mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
            mycursor = mydb.cursor()

            # Determine the next record_id
            mycursor.execute("SELECT MAX(Record_ID) FROM record_db")
            max_id_result = mycursor.fetchone()
            next_record_id = 1 if max_id_result[0] is None else int(max_id_result[0]) + 1  # Ensure max_id_result[0] is treated as an integer

            # Prepare date and time
            current_date = datetime.date.today().isoformat()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")

            insert_query = "INSERT INTO record_db (Record_ID, Username, Record_Date, Record_Time, Improper_Count) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(insert_query, (next_record_id, current_user, current_date, current_time, improper_sitting_count))

            # Commit the transaction
            mydb.commit()
            
        except mycon.Error as e:
            print("Error saving detection session to database: ", e)

    def stopCaptureClicked(self):
        if self.capture_button_text == "STOP":
            self.stopCapturing()

    def CaptureClicked(self):
        self.capture_mode = 2

    """def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        self.label_17.setPixmap(QPixmap.fromImage(img))
        self.label_17.setAlignment(Qt.AlignCenter)
        self.toolButton_8.setText(self.capture_button_text)"""

    def displayDefaultImage(self):
        # default image path
        default_image = QImage('C:/Users/gawoo/F/UI/ErgoPostureGuide (2).png')
        pixmap = QPixmap.fromImage(default_image)
        self.label_17.setPixmap(pixmap)
        self.label_17.setAlignment(Qt.AlignCenter)
    
    def detect_posture(self, frame):
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888).rgbSwapped()
        image.flags.writeable = False

        # Make detection
        results = self.pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Set base posture at the beginning (if not set before)
            if self.base_posture is None:
                self.base_posture = BasePosture(
                    [landmarks[self.mp_pose.PoseLandmark.NOSE].x, landmarks[self.mp_pose.PoseLandmark.NOSE].y],
                    [landmarks[self.mp_pose.PoseLandmark.LEFT_EAR].x, landmarks[self.mp_pose.PoseLandmark.LEFT_EAR].y],
                    [landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR].y],
                    [landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].x, landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].y],
                    [landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].x, landmarks[self.mp_pose.PoseLandmark.LEFT_EYE].y],
                    [landmarks[self.mp_pose.PoseLandmark.MOUTH_LEFT].x, landmarks[self.mp_pose.PoseLandmark.MOUTH_LEFT].y],
                    [landmarks[self.mp_pose.PoseLandmark.MOUTH_RIGHT].x, landmarks[self.mp_pose.PoseLandmark.MOUTH_RIGHT].y],
                    [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y],
                    [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
                )

            # Calculate deviation
            deviation = self.base_posture.calculate_deviation(landmarks, self.algorithm_version)
            print(f"Calculated Deviation: {deviation}")
            
            # Check if deviation is greater than 10
            if deviation > 10:
                # Increment improper sitting time
                self.improper_sitting_time += 1


                # Check if improper sitting time exceeds 5 seconds
                if self.improper_sitting_time >= 500: 

                     # Increment improper sitting count
                    self.improper_sitting_count += 1  # Increment the counter here

                    # Pop up message box
                    self.showMessageBox("Improper Sitting Alert", "Please adjust your sitting position!", qimage)

                    # Reset improper sitting time
                    self.improper_sitting_time = 0

            else:
                # Reset improper sitting time if deviation is less than or equal to 10
                self.improper_sitting_time = 0

            l_mouth=[landmarks[self.mp_pose.PoseLandmark.MOUTH_LEFT].x, landmarks[self.mp_pose.PoseLandmark.MOUTH_LEFT].y]

            # Visualize deviation
            #cv2.putText(image, str(deviation), 
                        #tuple(np.multiply(l_mouth, [640, 480]).astype(int)), 
                       # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        except Exception as e:
            print(f'Error 3: {e}')

        # Render detections
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                  self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        return image
    
    def updateDeviationLabel(self, text):
        # This method will update the label text; it's connected to the signal
        print(f"Updating label with: {text}")
        self.label_22.setText(text)
    
    def showMessageBox(self, title, message, image=None):
        # Play sound notification
        sound = QSound("C:/Users/gawoo/F/UI/notify.wav")
        sound.play()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.NoIcon)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        # Set the window flags to ensure it stays on top
        msgBox.setWindowFlags(msgBox.windowFlags() | Qt.WindowStaysOnTopHint)

        # Create a custom widget to hold the layout
        custom_widget = QWidget()
        layout = QVBoxLayout(custom_widget)  # Vertical layout

        # Add an image if provided
        if image is not None:
            # Create a QLabel to hold the image
            image_label = QLabel()
            pixmap = QPixmap.fromImage(image)
            image_label.setPixmap(pixmap.scaled(320, 240, Qt.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)  # Add image label to the layout first

        # Add the main text of the message box to the layout
        text_label = QLabel(message)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)  # Add text label to the layout after the image

        # Set the custom widget with the layout to the message box
        msgBox.layout().addWidget(custom_widget, 0, 0, 1, msgBox.layout().columnCount())

        # Execute the message box
        msgBox.exec_()

    def updateDateTime(self):
        # Get current date and time
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()

        # Format date and time
        date_str = current_date.toString(Qt.ISODate)
        time_str = current_time.toString(Qt.DefaultLocaleLongDate)

        # Update QLabel text
        self.label_24.setText(f"{time_str}")
        self.label_11.setText(f"{date_str}")

    def ProfileClicked(self):
        try:
            # Connect to the database
            mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
            mycursor = mydb.cursor()

            # Query to retrieve account information based on the username
            query = "SELECT * FROM `log_db` WHERE `Username` = %s"
            mycursor.execute(query, (self.curent_user,))
            account_info = mycursor.fetchone()

            if account_info:
                # Assuming account_info is a tuple with columns 
                # update your profile page with the retrieved information
                username = account_info[0]
                password = account_info[1]
                confirm_password = account_info[1]
                birthday = account_info[2]
                # Extract other information as needed

                # Update the profile page with the retrieved information
                self.lineEdit_9.setText(username)
                self.lineEdit_10.setText(password)
                self.lineEdit_11.setText(confirm_password)
                self.lineEdit_12.setText(birthday)
                # Update other widgets with their respective values

            else:
                # Handle case where account information is not found
                # For example, clear the profile page fields
                self.lineEdit_username.setText("")
                self.lineEdit_email.setText("")
                # Clear other widgets or show a message indicating no information found
            
            self.Background.setCurrentIndex(4)
        except mycon.Error as e:
            print("Error: ", e)

    def update_button_clicked(self):
        username =self.lineEdit_9.text()
        password = self.lineEdit_10.text()
        confirm_password = self.lineEdit_11.text()
        birthday = self.lineEdit_12.text()  # Assuming you have a QLineEdit for birthday

        if not password or not confirm_password or not birthday:
            self.msg.setText("Please fill out all fields!")
            self.msg.exec_()
        elif password != confirm_password:
            self.msg.setText("Password and Confirm Password do not match!")
            self.msg.exec_()
        else:
            # Call method to update user profile if passwords match
            result = self.update_profile(password, birthday, username)
            if result:
                self.msg.setText("Profile updated successfully!")
                self.msg.exec_()
            else:
                self.msg.setText("Error 303: Update Failed")
                self.msg.exec_()
    
    def update_profile(self, password, birthday,current_user):
        try:
            # Connect to the database
            mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
            mycursor = mydb.cursor()

            # Perform the update operation here
            query = "UPDATE `log_db` SET `Password` = %s, `Birthday` = %s WHERE `Username` = %s"
            mycursor.execute(query, (password, birthday, current_user))
            mydb.commit()

            return True  # Return True if update successful

        except mycon.Error as e:
            print("Error3 : ", e) 
            return False  # Return False if update failed
    
    def history_btn_clicked(self):
        try:
            current_user = self.label_8.text()
            print(current_user)
            # Connect to database
            mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
            # Modify the cursor to return rows as dictionaries
            viewHistory = mydb.cursor(dictionary=True)
            # Perform the retrieve operation here
            query = "SELECT * FROM `record_db` WHERE `Username` = %s "
            viewHistory.execute(query, (current_user,))
            result = viewHistory.fetchall()

            if result:
                self.tableWidget.setRowCount(len(result))

                for row, item in enumerate(result):
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(str(item['Record_ID'])))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(item['Record_Date']))
                    self.tableWidget.setItem(row, 2, QTableWidgetItem(item['Record_Time']))
                    self.tableWidget.setItem(row, 3, QTableWidgetItem(str(item['Improper_Count'])))

                self.Background.setCurrentIndex(5)

            else:
                # Show some message if no data got from db
                QMessageBox.information(self, 'Warning', 'No data got from database, please try again')
                return

        except mycon.Error as e:
            print("Error:2 ", e) 
            return False  # Return False if update failed
    
    def onChangeProfilePicClicked(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Profile Picture', '', 'Image files (*.jpg *.jpeg *.png *.gif)')
        if fname:
            # Create a QPixmap object with the image file
            pixmap = QPixmap(fname)

            # Optionally, scale the QPixmap to fit the pushButton's current size (or to a specific size)
            scaled_pixmap = pixmap.scaled(self.pushButton.width(), self.pushButton.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Set the pushButton's icon to the QPixmap
            self.pushButton.setIcon(QIcon(scaled_pixmap))

            # Optionally, adjust the pushButton's icon size to ensure the image fits well
            self.pushButton.setIconSize(scaled_pixmap.size())

            # Save the profile picture path to the database
            self.update_profile_picture_path(self.curent_user, fname)

    def update_profile_picture_path(self, username, path):
        try:
            mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
            mycursor = mydb.cursor()
            query = "UPDATE log_db SET profile_pic = %s WHERE Username = %s"
            mycursor.execute(query, (path, username))
            mydb.commit()
        except mycon.Error as e:
            print("Error updating profile picture in database: ", e)

    def load_profile_picture(self, username):
        try:
            mydb = mycon.connect(host="localhost", user="root", password="", database="fyp_db")
            mycursor = mydb.cursor()
            query = "SELECT profile_pic FROM log_db WHERE Username = %s"
            mycursor.execute(query, (username,))
            result = mycursor.fetchone()
            if result and result[0]:
                pixmap = QPixmap(result[0])
                scaled_pixmap = pixmap.scaled(self.pushButton.width(), self.pushButton.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.pushButton.setIcon(QIcon(scaled_pixmap))
                self.pushButton.setIconSize(scaled_pixmap.size())
        except mycon.Error as e:
            print("Error loading profile picture from database: ", e)

class BasePosture:
    def __init__(self, nose, left_ear, right_ear, left_eye, right_eye, left_mouth, right_mouth, left_shoulder, right_shoulder):
        self.nose = nose
        self.left_ear = left_ear
        self.right_ear = right_ear
        self.left_eye = left_eye
        self.right_eye = right_eye
        self.left_mouth = left_mouth
        self.right_mouth = right_mouth
        self.left_shoulder = left_shoulder
        self.right_shoulder = right_shoulder

    def calculate_deviation(self, landmarks, algorithm_version):
        # Extract coordinates for relevant landmarks
        nose = [landmarks[mp.solutions.pose.PoseLandmark.NOSE].x, landmarks[mp.solutions.pose.PoseLandmark.NOSE].y]
        left_ear = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR].y]
        right_ear = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR].y]
        left_eye = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE].y]
        right_eye = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_EYE].y]
        left_mouth = [landmarks[mp.solutions.pose.PoseLandmark.MOUTH_LEFT].x, landmarks[mp.solutions.pose.PoseLandmark.MOUTH_LEFT].y]
        right_mouth = [landmarks[mp.solutions.pose.PoseLandmark.MOUTH_RIGHT].x, landmarks[mp.solutions.pose.PoseLandmark.MOUTH_RIGHT].y]
        left_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y]
        right_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y]

        if algorithm_version == 1:
            # Algorithm: Utilizes shoulders in addition to the face to track posture
            l_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y]
            r_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y]

            # Calculate deviation
            deviation = int(
                ((nose[0] + left_ear[0] + right_ear[0] + left_eye[0] + right_eye[0] + left_mouth[0] + right_mouth[0] + l_shoulder[0] + r_shoulder[0]) /
                 (self.nose[0] + self.left_ear[0] + self.right_ear[0] + self.left_eye[0] + self.right_eye[0] + self.left_mouth[0] + self.right_mouth[0] + self.left_shoulder[0] + self.right_shoulder[0]) * 100)
            )

        elif algorithm_version == 2:
            # Algorithm 2: Utilizes only the face to track posture
            # Calculate deviation
            deviation = int(
                ((nose[0] + left_mouth[0] + right_mouth[0]) /
                 (self.nose[0] + self.left_mouth[0] + self.right_mouth[0]) * 100)
            )

        #calc_deviation = deviation
        #adjusted_deviation = 100 if deviation >= 100 else int(deviation)
        #adjusted_deviation = 100 - adjusted_deviation
        # Modify adjusted_deviation
        if deviation < 100:
            adjusted_deviation = 100 - deviation
        else:
            adjusted_deviation = deviation - 100
            
        return adjusted_deviation #calc_deviation 
    


#if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    mainWin = Main_UI()
#    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_app = login_UI()
    mainWin = Main_UI(login_app)
    sys.exit(app.exec_())