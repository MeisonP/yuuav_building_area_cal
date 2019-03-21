import json
import numpy as np
import cv2
import urllib2


def main(img_name, alpha):  # pass the image name from front-end, such as test.png
    print "cal_main: img_name={}".format(img_name)

    image = cv2.imread("./uploaded_images/{}".format(img_name))

    image = np.array(image)

    # extract the url/api data from url
    name = img_name
    url = "http://localhost:3000/api/json/%2F{}".format(name)
    data_str = urllib2.urlopen(url).read()
    load_dict = json.loads(data_str)
    obj_list = load_dict['objects']  # list

    for i in range(0, 2):
        if obj_list[i]['label'] == "Reference":
            ref_plg = obj_list[i]['polygon']
            ref_polygon_array = np.array(ref_plg)
            N_ref = ref_polygon_array.shape[0]

            ref_contours = np.empty((1, N_ref, 1, 2), dtype=np.int)

            for i in range(0, N_ref):
                ref_contours[0][i][0][0] = int(round(ref_polygon_array[i]['x']))
                ref_contours[0][i][0][1] = int(round(ref_polygon_array[i]['y']))
            ref_area_pixel = cv2.contourArea(ref_contours[0])

            # ########### Ref's area ######
            if alpha == "":
                ref_area = 1
            else:
                ref_area = float(alpha) # m*m
            # ##############

            coeff_area = ref_area / ref_area_pixel  # 1 square = (coeff_area * pixel_area)

            ref_cir_pixel = cv2.arcLength(ref_contours[0], True)
            ref_side = pow(ref_area, 0.5)  # m

            coeff_side = ref_side / ref_cir_pixel

            print "reference pixel: area={0}, cir={1}".format(ref_area_pixel, ref_cir_pixel)

            for i in range(0, 2):
                if obj_list[i]['label'] != "Reference":
                    obj_dict = obj_list[i]
                    plg = obj_dict['polygon']
                    polygon_array = np.array(plg)

                    N = polygon_array.shape[0]

                    contours = np.empty((1, N, 1, 2), dtype=np.int)

                    for i in range(0, N):
                        contours[0][i][0][0] = int(round(polygon_array[i]['x']))
                        contours[0][i][0][1] = int(round(polygon_array[i]['y']))
                    area_pixel = cv2.contourArea(contours[0])
                    cir_pixel = cv2.arcLength(contours[0], True)
                    print "building pixel: area={}, circumference={}".format(area_pixel, cir_pixel)

                    area = area_pixel * coeff_area
                    cir = cir_pixel * coeff_side
                    print "real value: {0} m2, {1} m".format(area, cir)

    return area, cir


