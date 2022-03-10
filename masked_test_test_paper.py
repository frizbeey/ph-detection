import numpy as np
import cv2
import imutils

def adding_color_label (image):

    space = 0
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    image = cv2.putText(image , "B" + "  | " + "G" + "   | " + "R" ,
                        (80, 25), font , 1, (0,0,0), 1, cv2.LINE_AA)

    for i , rgb in enumerate(mean):
        image = cv2.putText(image , str(int(rgb[0])) + " | " + str(int(rgb[1])) + " | " + str(int(rgb[2])),
                            (80, space + 50), font , 1, (0,0,0), 1, cv2.LINE_AA)

        space += 77

    return image

def arrangeing_coordinates (mean, center_coordinates):
    for i in range(len(mean) - 1):
        for j in range(len(mean) - 1):
            if center_coordinates[j][1] > center_coordinates[j+1][1]:
                x_temp = center_coordinates[j]
                mean_tmp = mean[j]

                center_coordinates[j] = center_coordinates[j+1]
                mean[j] = mean[j+1]

                center_coordinates[j+1] = x_temp
                mean[j+1] = mean_tmp

    return mean, center_coordinates

def color_mean (image, coordinate):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours (mask, [coordinate], -1, 255, -1)
    #cv2.imshow("masked", mask)
    #cv2.imshow("image2", image)
    return cv2.mean(image, mask=mask)

def color_mean_and_center_coordinates (contours, image):
    mean = []
    center_coordinates = []
    image_contour = []

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 3900 and area < 5000 :
            image_contour.append(contours[i])

    for i, cnt in enumerate(image_contour):
        M = cv2.moments(cnt)
        mean.append(color_mean(image , cnt))

        center_coordinates.append([int(M["m10"] / M["m00"]) , int(M["m01"] / M["m00"])] )
        cv2.circle (image, (int(M["m10"] / M["m00"]) , int(M["m01"] / M["m00"])), 5, (0, 0, 255), -1)

    mean, center_coordinates = arrangeing_coordinates(mean, center_coordinates)

    return mean, center_coordinates, image_contour

def removing_vertical_horizontal_line (BW_image):
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,25))
    detected_Vlines = cv2.morphologyEx(BW_image, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    #cv2.imshow("vertical kernels", detected_Vlines)

    Vcnts = cv2.findContours(detected_Vlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Vcnts = Vcnts[0] if len(Vcnts) == 2 else Vcnts[1]
    for c in Vcnts:
        cv2.drawContours(BW_image, [c], -1, (255,255,255), 2)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
    detected_Hlines = cv2.morphologyEx(BW_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    #cv2.imshow("horizontal kernels", detected_Hlines)
    #
    Hcnts = cv2.findContours(detected_Hlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Hcnts = Hcnts[0] if len(Hcnts) == 2 else Hcnts[1]
    for c in Hcnts:
        cv2.drawContours(BW_image, [c], -1, (255,255,255), 3)

    return BW_image

def otsu(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    BW_image = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]

    return removing_vertical_horizontal_line(BW_image)

def test_image():
    image = cv2.imread("test+background.jpg" , cv2.IMREAD_COLOR)

    BW_image = otsu(image);

    contours = cv2.findContours(BW_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    mean, center_coordinates, image_contour = color_mean_and_center_coordinates(contours, image)

#    image = adding_color_label(image)
    
    return mean

if __name__ == "__main__":
    image = cv2.imread("test+background.jpg" , cv2.IMREAD_COLOR)

#    row, col, num = image.shape

    BW_image = otsu(image);

    contours = cv2.findContours(BW_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    mean, center_coordinates, image_contour = color_mean_and_center_coordinates(contours, image)

    image = adding_color_label(image)
    
    print (" X , Y : " + str(center_coordinates))
    print (" ")
    print ("Average Color : " + str(mean))
    print("-------------------------------------")
        
    #print("mean : ", mean)
    #print("center", str(len(center_coordinates)))
    #print("contour", str(len(image_contour)))

    cv2.drawContours(image , image_contour, -1, (0, 255, 0), 2)

    cv2.imshow("image", image)
    #cv2.imshow("background ", background)
    #cv2.imshow("BW_image", BW_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
