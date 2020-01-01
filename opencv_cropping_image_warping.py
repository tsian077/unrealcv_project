#https://learnml.today/opencv-automatic-cropping-and-image-warping-2?fbclid=IwAR0ZB_bBbM1ItryW6HqmzXwU8WuchcLsGiy9jsfwWmYcYRG1u0JOuWEu9p0

import numpy as np
import cv2 
import math
from matplotlib import pyplot as plt

# depth0 = np.load('data_real2/depth/depth_0.npy')
# depth1 = np.load('data_real2/depth/depth_1.npy')
# rgb0 = cv2.imread('data_real2/lit/lit_0.png')
depth0 = cv2.imread('data_real2/lit/lit_0.png',0)
depth1 = cv2.imread('data_real2/lit/lit_1.png',0)
rgb0 = cv2.imread('data_real2/lit/lit_1.png')

print('depth0',depth0.shape)
print('depth1',depth1.shape)

#運用KAZE演算法來提取局部特徵
surf = cv2.KAZE_create()
kp1,des1 = surf.detectAndCompute(depth0,None)
kp2,des2 = surf.detectAndCompute(depth1,None)

#use KNN matcher to find similar on both depth images 
bf = cv2.BFMatcher()
print('des1',des1.shape)
print('des2',des2.shape)
matches = bf.knnMatch(des1,des2,k=2)


#將符合per Lowe's率的匹配存下來
good = []
for m,n in matches:
    # print('m',m.distance,'n',n.distance)
    if m.distance <0.7 * n.distance:
        good.append(m)

#如果匹配的點小於10的話，就是不一樣的影像或是扭曲太嚴重
MIN_MATCH_COUNT = 10
if len(good) > MIN_MATCH_COUNT:

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good
                            ]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good
                            ]).reshape(-1, 1, 2)

    kp1_matched=([ kp1[m.queryIdx] for m in good ])
    kp2_matched=([ kp2[m.trainIdx] for m in good ])   

    matches = cv2.drawMatches(depth0,kp1,rgb0,kp2, good,None, flags=2)
    # plt.figure(figsize=(10,10))
    # plt.axis('off')
    # plt.imshow(matches),plt.show()

 # Finds a perspective transformation between two planes. 
T, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

ss = T[0, 1]
sc = T[0, 0]
scaleRecovered = math.sqrt(ss * ss + sc * sc)
thetaRecovered = math.atan2(ss, sc) * 180 / math.pi
print("Calculated scale difference: %.2fCalculated rotation difference: %.2f" % (scaleRecovered, thetaRecovered))  

im_out = cv2.warpPerspective(
        depth1, 
        np.linalg.inv(T), 
        (depth1.shape[1], depth1.shape[0])
    )
print(im_out.shape)
cv2.imwrite('warping_image.png',im_out)