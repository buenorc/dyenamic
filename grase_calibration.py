# -*- coding: utf-8 -*-
'''

Rafael de Carvalho Bueno (rafael.bueno@ufpr.br)
'''

import cv2
import openpiv as piv
import numpy as np


def cal_current(path_ic,pathout):

 
    vidcap = cv2.VideoCapture(path_ic)
    success,image = vidcap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    np.savetxt(pathout+'/initial-condition-current.txt', gray, delimiter='\t', fmt='%.3f')
    