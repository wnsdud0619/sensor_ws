#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import rospy
import argparse
import scipy.misc
import numpy as np
import message_filters
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from autoware_perception_msgs.msg import *


def parse_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--legacy', action='store_true', help='Use existing topic name')
    args = parser.parse_args(rospy.myargv()[1:])
    return args

class TL_ROI_publisher:
    def __init__(self, use_legacy=False):
        TL_IMAGE_TOPIC         = "/sensing/camera/traffic_light/image_raw"
        TL_ROI_TOPIC        = '/traffic_light_recognition/rois'
        TL_ROI_IMG_TOPIC    = TL_IMAGE_TOPIC + "/rois"
        if use_legacy:
            TL_ROI_TOPIC    = '/perception/traffic_light_recognition/rois'
        sub_img = message_filters.Subscriber(TL_IMAGE_TOPIC, Image, queue_size=2)
        sub_roi = message_filters.Subscriber(TL_ROI_TOPIC, TrafficLightRoiArray, queue_size=2)

        self.br = CvBridge()
        self.pub = rospy.Publisher(TL_ROI_IMG_TOPIC, Image, queue_size=2)
        self.timesync_sub = message_filters.TimeSynchronizer([sub_img, sub_roi], 2)
        self.timesync_sub.registerCallback(self.callback)

        print("=" * 80)
        print("Use legacy topic name = %s" % use_legacy)
        print("[Input] TL Image topic = %s" % TL_IMAGE_TOPIC)
        print("[Input] TL RoIs topic = %s" % TL_ROI_TOPIC)
        print("[Output] TL_RoI Image topic = %s" % TL_ROI_IMG_TOPIC)
        print("=" * 80)
        print("Running...")

    def callback(self, img_msg, roi_msg):
        if not roi_msg.rois:  # RoI가 없는 경우에도 TL states topic이 나오도록 빈 이미지를 송신
            msg = self.br.cv2_to_imgmsg(np.zeros((128, 256, 3), dtype=np.uint8), encoding=img_msg.encoding)
            msg.header = img_msg.header
            self.pub.publish(msg)
            return

        np_img = np.fromstring(img_msg.data, np.uint8).reshape(img_msg.height, img_msg.width, 3)

        # ROI 추출
        roi_imgs = []
        for roi in roi_msg.rois:
            xx = roi.roi.x_offset
            yy = roi.roi.y_offset
            width = roi.roi.width
            height = roi.roi.height
            roi_img = np_img[yy:yy + height, xx:xx + width]      
            roi_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2RGB)
            roi_img = scipy.misc.imresize(roi_img, (128, 256), interp='cubic')
            roi_imgs.append(roi_img)

        # 하나의 이미지로 ROI를 결합한 뒤, Publish
        roi_imgs = np.concatenate(roi_imgs, axis=1)
        msg = self.br.cv2_to_imgmsg(np.array(roi_imgs), encoding=img_msg.encoding)
        msg.header = img_msg.header
        self.pub.publish(msg)


if __name__ == '__main__':
    rospy.init_node('tl_roi_img_pub', anonymous=True)
    args = parse_config()
    TL_pub = TL_ROI_publisher(args.legacy)
    rospy.spin()