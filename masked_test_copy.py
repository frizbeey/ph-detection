import numpy as np
import cv2
import imutils
import random

def adding_color_label (image, mean):

    spacev = 0
    spaceh = 0
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    image = cv2.putText(image , "B" + "  | " + "G" + "   | " + "R" ,
                        (80, 25), font , 1, (0,0,0), 1, cv2.LINE_AA)
    print("mean : ", mean)

    for i , rgb in enumerate(mean):
        if i%4 == 0 and i!=0:
            spaceh += 200
            spacev = 0
        for j, colors in enumerate(rgb):
            print ("rgb :" + str(colors))
            image = cv2.putText(image , str(int(colors[0])) + " | " + str(int(colors[1])) + " | " + str(int(colors[2])),
                            (spaceh + 50, spacev + 50), font , 1, (0,0,0), 1, cv2.LINE_AA)
            spacev += 40
        
        image = cv2.putText(image , "--------", (spaceh + 50, spacev + 50), font , 1, (0,0,0), 1, cv2.LINE_AA)
        spacev+=40
        
        
    return image

def arrangeing_coordinates (mean, center_coordinates):
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

    ph_table_2 = []
    avg_color_table2 = []

    for i in range (8):
        ph_table_2.append(ph_table[i*2])
        avg_color_table2.append(avg_color_table[i*2])
#
    for i in range (1, 16, 2):
        ph_table_2.append(ph_table[i])
        avg_color_table2.append(avg_color_table[i])

    return avg_color_table2, ph_table_2

def color_mean (image, coordinate):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours (mask, [coordinate], -1, 255, -1)
    #cv2.imshow("masked" + str(random.randint(1, 100)), mask)
    #cv2.imshow("image2", image)
    return cv2.mean(image, mask=mask)

def color_mean_and_center_coordinates (contours, image):
    mean = []
    center_coordinates = []
    image_contour = []
    
    print("len :" + str(len(contours)))

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        print ("area : ", area)
        
        if area > 3400 and area < 4500 :
            image_contour.append(contours[i])
    
    print("len2 :" + str(len(image_contour)))

    for i, cnt in enumerate(image_contour):
        M = cv2.moments(cnt)
        
        mean.append(color_mean(image , cnt))
#
        center_coordinates.append([int(M["m10"] / M["m00"]) , int(M["m01"] / M["m00"])] )
        
        cv2.circle (image, (int(M["m10"] / M["m00"]) , int(M["m01"] / M["m00"])), 5, (0, 0, 255), -1)
        
   # for i in center_coordinates:
        
    #    print("center coordinates : ", i)
        
    #print("size : ", len(center_coordinates))

    mean, center_coordinates = arrangeing_coordinates(mean, center_coordinates)
    
    #for i in center_coordinates:
        
        #print("center coordinates : ", i)
        
    #return image_contour

    return mean, center_coordinates, image_contour

def removing_vertical_horizontal_line (BW_image):
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,15))
    detected_Vlines = cv2.morphologyEx(BW_image, cv2.MORPH_OPEN, vertical_kernel, iterations=5)

   # cv2.imshow("vertical kernels", detected_Vlines)

    Vcnts = cv2.findContours(detected_Vlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    Vcnts = Vcnts[0] if len(Vcnts) == 2 else Vcnts[1]
    for c in Vcnts:
        cv2.drawContours(BW_image, [c], -1, (255,255,255), 2)
        
    #cv2.imshow("vertical kernels", BW_image)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
    detected_Hlines = cv2.morphologyEx(BW_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    #cv2.imshow("horizontal kernels", detected_Hlines)
    #
    Hcnts = cv2.findContours(detected_Hlines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Hcnts = Hcnts[0] if len(Hcnts) == 2 else Hcnts[1]
    for c in Hcnts:
        cv2.drawContours(BW_image, [c], -1, (255,255,255), 3)
   # cv2.imshow("horizontal kernels2", BW_image)

    return BW_image

def otsu(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("bw_image2", gray)
    BW_image = cv2.threshold(gray, 140, 250, cv2.THRESH_BINARY)[1]
    #cv2.imshow("bw_image", BW_image)
    final = removing_vertical_horizontal_line(BW_image)
    return final
    #return BW_image

def single_image():
    image = cv2.imread("ph_library.png" , cv2.IMREAD_COLOR)

    BW_image = otsu(image);

    contours = cv2.findContours(BW_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    mean, center_coordinates, image_contour = color_mean_and_center_coordinates(contours, image)

#    image = adding_color_label(image)
    
    return mean

if __name__ == "__main__":
    image = cv2.imread("ph_library.png" , cv2.IMREAD_COLOR)
    text = cv2.imread("background.png" , cv2.IMREAD_COLOR)
    text = cv2.resize(text, (1000, 1000), interpolation= cv2.INTER_LINEAR)
    
    row, col, num = image.shape

    BW_image = otsu(image);

    contours = cv2.findContours(BW_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    mean, center_coordinates, image_contour = color_mean_and_center_coordinates(contours, image)
    #image_contour = color_mean_and_center_coordinates(contours)

    for i in range(1 , len(mean) + 1) :
        print (" X , Y : " + str(center_coordinates[i-1]))
        print (" ")
        print ("Average Color : " + str(mean[i-1]))
        print("-------------------------------------")

    text = adding_color_label(text, mean)

    print("mean : ", mean)
    print("center", str(len(center_coordinates)))
    print("contour", str(len(image_contour)))

    cv2.drawContours(image, image_contour, -1, (255, 255, 0), 2)
    #cv2.drawContours(image, contours, -1, (255, 255, 0), 2)

    cv2.imshow("image", image)
    #cv2.imshow("image", image_contour)
  #  cv2.imshow("values", text)
    #cv2.imshow("background ", background)
    #cv2.imshow("BW_image", BW_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
