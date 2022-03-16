import numpy as np
import cv2
import imutils
import masked_test_copy as mtc
import masked_test as mt

#original = cv2.imread("test.png")
#new = cv2.imread(".png")
#original = imultils.resize(original, height = 600)
#new = imultis.resize(new, height = 600)

#difference = cv2.subtract(original, new)
#b, g, r = cv2.split(difference)

def result():
    mean_single = mtc.single_image()
    #for i in range(1 , len(mean_single) + 1) :
     #   print ("Average Color : " + str(mean_single[i-1]))
    mean_test = mt.test_image()

    #print("color : " + str(mean_single[0]))

   # print("color 2 : " + str(mean_test))

    #a = mean_single[0][0]
    #b = mean_test[0]

    r_ph = []
    avg_ph = []
    for ph in range(16):
        r_box = []
        avg_box = []
        for box in range(4):
            r_rgb = []
            for rgb in range(3):
                r_rgb.append(abs(mean_test[box][rgb] - mean_single[ph][box][rgb]))
                 
            r_box.append(r_rgb)
            avg_box.append(sum(r_rgb) / len(r_rgb))
            
        r_ph.append(r_box)
        avg_ph.append(sum(avg_box) / len(avg_box))
        
    #            r[box][rgb].append(abs(mean_test[box][rgb] - mean_single[ph][box][rgb]))

    #print("a : " + str(a))
    #print("b : " + str(b))
    print("r : " + str(r_ph))
    print("avg : " + str(avg_ph))
    ph = avg_ph.index(min(avg_ph))
    if ph > 7:
        ph = ph - 1
                      
    return ph;
    

if __name__ == "__main__" :
    mean_single = mtc.single_image()
    #for i in range(1 , len(mean_single) + 1) :
     #   print ("Average Color : " + str(mean_single[i-1]))
    mean_test = mt.test_image()

    print("color : " + str(mean_single[0]))

    print("color 2 : " + str(mean_test))

    #a = mean_single[0][0]
    #b = mean_test[0]

    r_ph = []
    avg_ph = []
    for ph in range(16):
        r_box = []
        avg_box = []
        for box in range(4):
            r_rgb = []
            for rgb in range(3):
                r_rgb.append(abs(mean_test[box][rgb] - mean_single[ph][box][rgb]))
                 
            r_box.append(r_rgb)
            avg_box.append(sum(r_rgb) / len(r_rgb))
            
        r_ph.append(r_box)
        avg_ph.append(sum(avg_box) / len(avg_box))
        
    #            r[box][rgb].append(abs(mean_test[box][rgb] - mean_single[ph][box][rgb]))

    #print("a : " + str(a))
    #print("b : " + str(b))
    print("r : " + str(r_ph))
    print("avg : " + str(avg_ph))
    ph = avg_ph.index(min(avg_ph))
    if ph > 7:
        ph = ph - 1
                      
    print("ph : " + str(ph))

    #for i in range (len(r_ph)):
    #    if i <= 15:
    #        print("The pH strip has a value of [r_ph]")

    #if a == b:
    #    print ("Both inputs are equal")
    #else:
    #        print ("Input is not equal")

    #if cv2.countNonZero(b) <= 15 and cv2.countNonZero(g) <= 15 and cv2.countNonZero(r) <= 15:
    #    print("The color is equal")
    #    else:
    #        print("The color is different")
    #        cv2.imshow('Difference', different)
        
    #    cv2.waitKey(0)
    #    cv2.destroyAllWindows()]    