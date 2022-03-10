import numpy as np
import cv2
import imutils

def removing_vertical_horizontal_line (black_white_image):

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,25))
    detected_Vlines = cv2.morphologyEx(black_white_image, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    Vcnts = cv2.findContours(detected_Vlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Vcnts = Vcnts[0] if len(Vcnts) == 2 else Vcnts[1]
    for c in Vcnts:
        cv2.drawContours(black_white_image, [c], -1, (255,255,255), 2)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
    detected_Hlines = cv2.morphologyEx(black_white_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    Hcnts = cv2.findContours(detected_Hlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Hcnts = Hcnts[0] if len(Hcnts) == 2 else Hcnts[1]
    for c in Hcnts:
        cv2.drawContours(black_white_image, [c], -1, (255,255,255), 3)

    return black_white_image

def otsu(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_white_image = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]

    return removing_vertical_horizontal_line (black_white_image)

def color_mean(image, coordinate):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours (mask , [coordinate], -1, 255, -1)
    return cv2.mean(image, mask=mask)[:3]

if __name__  == "__main__":
    image = cv2.imread('indicator.png', cv2.IMREAD_COLOR)
    test_image = cv2.imread('test.png')

    black_white_image = otsu(image)

    contours = cv2.findContours(black_white_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    mean = []
    center_coordinates = []
    image_contour = []

    for i, cnt in enumerate(contours) :
        area = cv2.contourArea(cnt)
        if area > 3900 and area < 5000 :
            image_contour.append(contours[i])
    # remove too small and too big contour
    for i, cnt in enumerate(image_contour) :
        M = cv2.moments(cnt)
        area = cv2.contourArea(cnt)

        if area > 3900 and area < 5000 :
            mean.append(color_mean(image, cnt))
            center_coordinates.append([int(M["m10"] / M["m00"]) , int(M["m01"] / M["m00"])] )
            cv2.circle (image, (int(M["m10"] / M["m00"]) , int(M["m01"] / M["m00"])), 7, (0, 0, 255), -1)

    del contours[0]


    print ("mean" + str(len(mean)))
    print ("center " + str(len(center_coordinates)))
    print ("contour : " + str(len(image_contour)))

    cv2.drawContours(image, image_contour, -1, (0, 255, 0), 2)


    print("after")
    ## arrangeing the mean

    for j in range (len(mean) - 1) :
        for i in range (len(mean) - 1) :
            ## rearrange the x axis
            if center_coordinates[i][0] > center_coordinates[i+1][0] :
                x_tmp = center_coordinates [i]
                mean_tmp = mean[i]

                center_coordinates[i] = center_coordinates [i+1]
                mean[i] = mean [i+1]

                center_coordinates[i+1] = x_tmp
                mean[i+1] = mean_tmp


    for i in range(8):
        for j in range(8):
            for k in range(7):
                var = ((i*7)+i)+k
                if center_coordinates[var][1] > center_coordinates[var+1][1] :
                    y_tmp = center_coordinates [var]
                    mean_tmp = mean[var]

                    center_coordinates[var] = center_coordinates [var+1]
                    mean[var] = mean[var+1]

                    center_coordinates[var+1] = y_tmp
                    mean[var+1] = mean_tmp

    ph_table = []
    avg_color_table = []

    for i in range(16):

        ph_group = []
        color_group = []

        for j in range(i*4, i*4+4):
            ph_group.append(center_coordinates[j])
            color_group.append(mean[j])

        ph_table.append(ph_group)
        avg_color_table.append(color_group)
        #ph_table.append(ph_group[i+8])
        #avg_color_table.append(color_group[i+8])
#
    ph_table_2 = [16]
    avg_color_table2 = [16]

    for i in range (8):
        ph_table_2.append(ph_table[i*2])
        avg_color_table2.append(avg_color_table[i*2])
#
    for i in range (1, 16, 2):
        ph_table_2.append(ph_table[i])
        avg_color_table2.append(avg_color_table[i])
#

    for i in range(1 , len(avg_color_table2) + 1) :
        print (" X , Y : " + str(ph_table_2[i-1]))
        print (" ")
        print ("Average Color : " + str(avg_color_table2[i-1]))
        print("-------------------------------------")

    cv2.imshow('image', image)
    cv2.imshow('b & w', black_white_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
