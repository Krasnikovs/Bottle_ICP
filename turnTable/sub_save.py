#!/usr/bin/env python
import serial
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import numpy
import pyrealsense2 as rs2

pipeline = rs2.pipeline()
config = rs2.config()
bridge = CvBridge()
img_counter = 0
board = serial.Serial('/dev/ttyACM0')
save_img_path = '/home/goodchair/prakse/images'
config.enable_stream(rs2.stream.depth, 120, 720, rs2.format.bgr8, 30)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    image_topic = "/camera/color/image_raw"
    spin_amount = 360/int(data.data.encode())
    #rospy.Subscriber(image_topic, Image, callback_img)
    for x in range(spin_amount):
        board.write(data.data.encode())
        rospy.loginfo(board.readline())
        #while True:
            #rospy.Subscriber(image_topic, Image, callback_img)
            #break
        #callback_img()
        #save_img(image_topic)
	global sub_once
        sub_once = rospy.Subscriber(image_topic, Image, callback_img)


def take_img():
    global save_img_paths
    global pipepline
    global config
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    align_to = rs2.stream.color
    align = rs2.align(align_to)

    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)
    aligned_depth_frames = aligned_frames.get_depth_frames()
    color_frame = aligned_frames.get_color_frame()

    depth_image = numpy.asanyarry(aligned_depth_frame.get_date())
    color_image = np.asanyarray(color_frame.get_data())

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    images = np.hstack((False, depth_colormap))
    cv2.namedWindow('Align Exaple', cv2.WINDOW_AUTOSIZE)

    imageName1 = 'testimg.jpg'
    imageName2 = 'testdepth.jpg'

    cv2.imwrite(os.path.join(save_img_path, imageName1), color_image)
    cv2.imwrite(os.path.join(save_img_path, imageName2), images)
    print("Received an image!")
    key = cv2.waitKay(1)

    pipleline.stop()

def save_img(msg):
    global img_counter
    global save_img_paths
    #cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    img_counter = img_counter + 1
    cv2.imwrite(os.path.join(save_img_path, 'camera_image_' + str(img_counter) + '.jpeg'), msg)
    print("Received an image!")

def callback_img(msg):
    global img_counter
    global save_img_paths
    print("Received an image!")
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        img_counter = img_counter + 1
        cv2.imwrite(os.path.join(save_img_path, 'camera_image_' + str(img_counter) + '.jpeg'), cv2_img)
    rospy.sleep(1)
    sub_once.unregister()
    #rospy.on_shutdown(img_received)

def listener():
    rospy.init_node('listener', anonymous=True)

    image_topic = "/camera/color/image_raw"
 
    rospy.Subscriber("chatter", String, callback)
    #rospy.Subscriber(image_topic, Image, callback_img)
 
    rospy.spin()
 
if __name__ == '__main__':
    listener()
