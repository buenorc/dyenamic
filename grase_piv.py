 # -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 17:16:51 2020

@author: rafae
"""
import matplotlib.pyplot as plt
import numpy as np
import warnings
import cv2

warnings.filterwarnings('ignore')

from openpiv import tools, process, validation, filters, scaling, preprocess


def analyzer (frame_a, frame_b, text, plot, num_scene, pathout, scal, zre, xre, dt):
    
    winsize   = 16    # pixels
    searchsize = 32    # pixels, search in image b
    overlap    = 8    # pixels
    
    frame_a = cv2.adaptiveThreshold(frame_a,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,5)
    frame_b = cv2.adaptiveThreshold(frame_b,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,5)
    #frame_a = cv2.adaptiveThreshold(frame_a,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #frame_b = cv2.adaptiveThreshold(frame_b,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    
    plt.imshow(np.c_[frame_a,frame_b],cmap='gray')
    plt.savefig(pathout+'/filtered'+str(num_scene)+'.png',dpi=800)
    
    u0, v0, sig2noise = process.extended_search_area_piv( frame_a.astype(np.int32), frame_b.astype(np.int32), window_size=winsize, overlap=overlap, dt=dt, search_area_size=searchsize, sig2noise_method='peak2peak' )
    x, y = process.get_coordinates( image_size=frame_a.shape, window_size=winsize, overlap=overlap )
    u1, v1, mask = validation.sig2noise_val( u0, v0, sig2noise, threshold = 1.3 )
    u2, v2 = filters.replace_outliers( u1, v1, method='localmean', max_iter=10, kernel_size=2)
    x, y, u3, v3 = scaling.uniform(x, y, u2, v2, scaling_factor = scal ) # scaling_factor (pixel per meter)

    u3 = np.flip(u3,axis=0)
    v3 = np.flip(v3,axis=0)

    xre = np.linspace(0,xre/100,len(x[0,:]))  
    zre = np.linspace(0,zre/100,len(x[:,0]))  

    
    if plot == 1:
        piv_plotting(xre, zre, u3,v3, num_scene, pathout)

    if text == 0:
        tools.save(x, y, u3, v3, mask, pathout+'/piv'+str(num_scene)+'.txt' )
 
def piv_plotting(x,z, u3,v3, num_scene, pathout):
   

    xr,zr = np.meshgrid(x,z)


    fig, ax = plt.subplots()
    q = ax.quiver(xr, zr, u3,v3)
    ax.quiverkey(q, X=0.3, Y=1.1, U=1, label='field velocity (1 m/s)', labelpos='E')
    
    plt.savefig(pathout+'/piv'+str(num_scene)+'.png',dpi=800)
    plt.close()   

 