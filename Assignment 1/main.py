import cv2
import numpy as np
from glob import glob
import math

def overhead_using_video(points, sx, sy, x, y):  # x = 500, y = 100
    #pointsUp = [[x, y], [x + sx, y], [x + sx, y + sy], [x, y + sy]]
    pointsUp = [[x, y + sy], [x + sx, y + sy], [x + sx, y], [x,y]]

    points = np.array(points)
    pointsUp = np.array(pointsUp)

    H, mask = cv2.findHomography(points, pointsUp)

    return H

def get_transformed_image(img, H, show=0):
    try:
        r, c, co = img.shape
    except:
        r, c = img.shape

    out = cv2.warpPerspective(img, H, (c, r))
    crop_img = out[0:300, 0:210]

    if show == 1:
        crop_img = cv2.flip(crop_img, 1)
        cv2.imshow("Output", crop_img)
        cv2.waitKey(0)
        cv2.destroyWindow("Output")
    return crop_img

def max_distance(points):
    length = len(points)
    max_len = 0
    i_m = 0
    j_m = 0
    for i in range(length):
        for j in range(length):
            dist = math.sqrt((points[i][0][1]-points[j][0][1])**2+ (points[i][0][0]-points[j][0][0])**2)
            if dist > max_len:
                max_len = dist
                i_m = i
                j_m = j
    return max_len,points[i_m],points[j_m]

def best_four(points):
    length = len(points)
    max_arr = 0
    for i in range(length):
        for j in range(length):
            for k in range(length):
                for l in range(length):
                    arr = [points[i],points[j],points[k],points[l]]
                    arr = np.array(arr)
                    area = cv2.contourArea(arr)
                    if area > max_arr:
                        max_arr = area
                        best = arr
    return best

def calculate_real_length(dist):
    scale_factor = 29.7/300.0       # Scale 29.7 c.m is equivalent to 300 px
    dist = scale_factor * dist
    return dist

def main(debug = 0):

    img_mask = 'data/*.jpg'
    img_names = glob(img_mask)


    for fn in img_names:

        image = cv2.imread(fn, 0)           # Black and white image
        diffimage = cv2.imread(fn)          # Color image

        #image = cv2.undistort(image, np.load('cal_Mat.npy'), np.load('dist_Mat.npy'), None, np.load('cam_Mat.npy'))
        #diffimage = cv2.undistort(diffimage, np.load('cal_Mat.npy'), np.load('dist_Mat.npy'), None, np.load('cam_Mat.npy'))

        image = cv2.resize(image, (312, 416))
        diffimage = cv2.resize(diffimage, (312, 416))

        image = cv2.blur(image, (5, 5))
        _,image = cv2.threshold(image,100,255,cv2.THRESH_BINARY)


        cv2.imshow("Input image", diffimage)
        cv2.waitKey(30)

        edges = cv2.Canny(image, 50, 150, apertureSize=3)       # finding canny edges of image for segmentation

        corners = cv2.goodFeaturesToTrack(edges, 25, 0.01, 10)  # now finding corners

        hull = cv2.convexHull(corners)                          # Finding convex hull of the corner points

        if debug:
            print "Hull points : ", len(hull)

        hull = best_four(hull)                                     # choosing best four points of proposed rectangle

        H = overhead_using_video(hull,210,300,0,0)                 # Calculating homography
        diffimage = get_transformed_image(diffimage,H,debug)            # transforming both images (color and b/w)
        image = get_transformed_image(image, H, 0)

        img = cv2.blur(diffimage,(3,3))                             #   Sharpening the image
        diffimage = cv2.add(cv2.absdiff(diffimage,img),diffimage)

        edges_roi = cv2.Canny(diffimage, 50, 500, apertureSize=3)       # finding canny edges of image for segmentation

                                                                        # Creating the region of interest to remove the edge features
        edges = edges_roi[10:290, 10:200]
        diffimage = diffimage[10:290, 10:200]

        corners = cv2.goodFeaturesToTrack(edges, 25, 0.01, 10)          #  After removing edge irregularities, finding corners

        if debug:
            # for visualizing the corner points
            for i in corners:
                x, y = i.ravel()
                cv2.circle(diffimage, (x, y), 3, (255, 255, 255), 2)
            cv2.imshow('result', image)

        dist,i,j = max_distance(corners)
        cv2.line(diffimage,(i[0][0],i[0][1]),(j[0][0],j[0][1]),(0,0,255),2)

        print "Size of the pen/object : ", calculate_real_length(dist), "c.m."
        diffimage = cv2.flip(diffimage, 1)

        cv2.imshow('edges', edges)
        cv2.imshow("Image", diffimage)
        cv2.waitKey(0)

main(1)
