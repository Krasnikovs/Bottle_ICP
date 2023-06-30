import roslaunch
import rospy


uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
launch = roslaunch.scriptapi.ROSLaunch()
launch.parent = roslaunch.parent.ROSLaunchParent(uuid, "/opt/ros/melodic/share/realsense2_camera/launch/rs_camera.launch")
launch.start()

try:
    launch.spin()
finally:
    launch.shutdown()
