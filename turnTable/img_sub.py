import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import os

# Instantiate CvBridge
bridge = CvBridge()
img_counter = 0
save_img_path = '/home/goodchair/prakse/images'

def image_callback(msg):
    global img_counter
    global save_img_paths
    print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
	img_counter = img_counter + 1
        cv2.imwrite(os.path.join(save_img_path, 'camera_image_' + str(img_counter) + '.jpeg'), cv2_img)

def main():
    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/camera/color/image_raw"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    # Spin until ctrl + c
    rospy.spin()

if __name__ == '__main__':
    main()
