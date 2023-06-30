#!/usr/bin/env python
import serial
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import datetime

date_now = datetime.datetime.now()
bridge = CvBridge()
img_counter = 0
board = serial.Serial('/dev/ttyACM0')
save_img_path = '/home/goodchair/prakse/images'

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " I heard %s", data.data)
    image_topic = "/camera/color/image_raw"
    spin_amount = 360.0/float(data.data.encode())
    spin_amount_int = int(round(spin_amount))
    for x in range(spin_amount_int):
        board.write(data.data.encode())
        rospy.loginfo(board.readline())
	global sub_once
	rospy.sleep(1)
        sub_once = rospy.Subscriber(image_topic, Image, callback_img)

def callback_img(msg):
    global date_now
    global img_counter
    global save_img_paths
    print("Received an image!")
    date_str = str(date_now.strftime("%Y") + "-" + date_now.strftime("%m") + "-" + date_now.strftime("%d") + "_" + date_now.strftime("%H") + ":" + date_now.strftime("%M"))
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        img_counter = img_counter + 1
        cv2.imwrite(os.path.join(save_img_path, 'camera_image_' + str(img_counter) + "_" + date_str + '.jpeg'), cv2_img)
    rospy.sleep(1)
    sub_once.unregister()

def listener():
    rospy.init_node('listener', anonymous=True)

    image_topic = "/camera/color/image_raw"

    rospy.Subscriber("chatter", String, callback)
    rospy.spin()
 
if __name__ == '__main__':
    listener()
