 # -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 17:16:51 2020

@author: rafae
"""
import matplotlib.pyplot as plt
import numpy as np
import warnings
import cv2
import os

warnings.filterwarnings('ignore')

from openpiv import tools, process, validation, filters, scaling, preprocess


def analyzer (frame_b, frame_a, text, plot, num_scene, pathout, scal, zre, xre, winsize, searchsize,overlap,intera,kernel,thold,maxVal,block,const, dt, fdpi):
    
    # winsize:     the size of the (square) interrogation window (pixels)
    # overlap:     the number of pixels by which two adjacent windows overlap.
    # searchsize:  the size of the (square) interrogation window from the second frame (pixels)
    # thold:       the signal to noise ratio threshold value  
    # intera:      the number of iterations
    # kernel:      the size of the kernel
    # scal:        the image scaling factor in pixels per meter
    
    block  = int(block)
    kernel = int(kernel)
    intera = int(intera)

    frame_a = np.invert(frame_a)
    frame_b = np.invert(frame_b)   
    
    if maxVal != 0:
        frame_a = cv2.adaptiveThreshold(frame_a,maxVal,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,block,const)
        frame_b = cv2.adaptiveThreshold(frame_b,maxVal,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,block,const)
 
 
    u0, v0, sig2noise = process.extended_search_area_piv( frame_a.astype(np.int32), frame_b.astype(np.int32), window_size=winsize, overlap=overlap, dt=dt, search_area_size=searchsize, sig2noise_method='peak2mean')
    x, y = process.get_coordinates( image_size=frame_a.shape, window_size=winsize, overlap=overlap )
    u1, v1, mask = validation.sig2noise_val( u0, v0, sig2noise, threshold = thold )
    u2, v2 = filters.replace_outliers( u1, v1, method='localmean', max_iter=intera, kernel_size=kernel)
    x, y, u3, v3 = scaling.uniform(x, y, u2, v2, scaling_factor = scal ) # scaling_factor (pixel per meter)

    # u3 = np.flip(u3,axis=0)
    # v3 = np.flip(v3,axis=0)

    xre = np.linspace(0,xre/10,len(x[0,:]))  
    zre = np.linspace(0,zre/10,len(x[:,0]))  

    if text == 1:
        tools.save(x, y, 100*u3, 100*v3, mask, pathout+'/piv'+str(num_scene)+'.txt' )
    
    if plot == 1:
        
        if text == 1:
            piv_plotting(xre, zre, u3,v3, num_scene, scal, pathout, fdpi)
            
        else:
            tools.save(x, y, 100*u3, 100*v3, mask, pathout+'/piv'+str(num_scene)+'.txt' )    
            piv_plotting(xre, zre, u3,v3, num_scene, scal, pathout, fdpi)
            os.remove(pathout+'/piv'+str(num_scene)+'.txt')
 
def piv_plotting(x,z, u3,v3, num_scene, scal, pathout, fdpi):
   

    fig, ax = plt.subplots(figsize=(8,8))
    tools.display_vector_field(pathout+'/piv'+str(num_scene)+'.txt', 
                           ax=ax, scaling_factor=scal, 
                           scale=100, # scale defines here the arrow length
                           width=0.0035, # width is the thickness of the arrow
                           on_img=True, # overlay on the image
                           image_name=str(num_scene)+'.png'); 
    
    plt.savefig(pathout+'/piv'+str(num_scene)+'.png' ,dpi=fdpi)
 