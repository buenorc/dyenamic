# -*- coding: utf-8 -*-
"""
Funções auxiliares 
Rafael de Carvalho Bueno (rafael.bueno@ufpr.br)

Para obter informações das relações px-distância real:
https://eleif.net/photo_measure.html

"""

import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt


import matplotlib
matplotlib.use('Agg')

from tkinter import *


def pixel_length(img,lenx,lenz):
    
    height = img.shape[0]
    length  = img.shape[1]  
    
    area = (lenx/length)*(lenz/height)
    
    return area     # same unit of lexx and lenz (preferably in mm)

def vidtoframes(videoFile, dt, mincur, maxcur,rhoa,rhoc,minsed,maxsed,lenx,lenz,model,eq,sedanal,plot,text,pathout,piv,winsize, searchsize,overlap,intera,kernel,thold,maxVal,block,const,root,fdpi):

    vidcap = cv2.VideoCapture(videoFile)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    nfr = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = nfr/fps
       
    bg = 0
  
    # verify fps
    if fps<1/dt:
        
        dt = 1/fps
        
        print ('> ')
        root.update() 
        print ('> Warning:     The defined temporal resolution dt is smaller than')
        root.update() 
        print ('>              the camera temporal resolution')
        root.update() 
        print ('> ')
        root.update() 
        print ('>              The temporal resolution will be automatically')
        root.update()         
        print ('>              altered to '+str(round(dt,5))+' seconds')
        root.update()  

    start_time = time.time()
    
    old = None    
    save = 0
    success,image = vidcap.read()
    

    N   = int(dur/dt)
    
    while success:        
        

        cv2.imwrite("./%d.png" % save, image)     
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(save*dt*1000))


        bg,numrows,numcols,x,z,old = frame_analyzer(save,mincur,maxcur,rhoa,rhoc,minsed,maxsed,lenx,lenz,bg,sedanal,plot,text,pathout,piv,dt,old,model,eq,winsize, searchsize,overlap,intera,kernel,thold,maxVal,block,const,root,fdpi)
           
        if save == 1:
            print ('> ')
            root.update()  
            spend_time = time.time() - start_time
            estimated  = round((N)*spend_time,0)
            hour_comp  = time.localtime(time.time()+estimated)
            form_comp  = time.strftime('%d %b, %H:%M %S', hour_comp)
                    
            print ('> Run info:    This may take few minutes ')
            root.update()                
            print ('>              Estimated time: '+str(estimated)+' seconds')    
            root.update() 
            print ('>              Should be completed on '+ form_comp)      
            root.update()             
        
        success,image = vidcap.read()
        save = save + 1 
        
    vidcap.release()
              
    return save,bg,numrows,numcols,x,z,dt


def frame_analyzer(number,mincur,maxcur,rhoa,rhoc,minsed,maxsed,lenx,lenz, background, sedanal,plot,text,pathout,piv,dt,old,model,eq,winsize, searchsize,overlap,intera,kernel,thold,maxVal,block,const,root,fdpi):
    img = cv2.imread("./%d.png" %number, cv2.IMREAD_GRAYSCALE)
    pixar = pixel_length(img,lenx,lenz) # mm²

    numrows = len(img)  
    numcols = len(img[0])

    
    if number > 0 and piv==1:

        scalz  = (img.shape[0]*1000/lenz) # pixel/m
        scalx  = (img.shape[1]*1000/lenx) # pixel/m
        
        if number == 1:
            ratio_scaling = scalx/scalz

            print ('> ')
            root.update() 
            print ('> Warning:     The scaling ratio is '+str(round(ratio_scaling,2)))
            root.update() 
            print ('>              The ideal value is 1')
            root.update() 
            print ('>              See the user manual to improve this parameter')
            root.update()         
            print ('> ')             
            root.update()  

        import grase_piv as pivel 
        pivel.analyzer(img, old, text[6], plot[6], number, pathout, scalx, lenz, lenx, winsize, searchsize,overlap,intera,kernel,thold,maxVal,block,const, dt,fdpi)

    old = img    
    if plot[2] == 0:
        os.remove("./%d.png"  %(number))
        
    curre = np.empty((numrows,numcols,))
    sedim = np.zeros((numrows,numcols),float)       

    
    x = np.linspace(0,lenz/10,numrows)  
    z = np.linspace(0,lenx/10,numcols)  
    

    for i in range(numrows):
        for j in range(numcols):

            if (img [i][j]<mincur):                                     
                curre [i][j] = None
                if sedanal == 1:
                    if (img [i][j] >= minsed and img[i][j] <= maxsed):

                        sedim [i][j] = pixar  # mm²
                    
            else:
                if(img [i][j]>maxcur):
                    curre [i][j] = rhoa
                else:
                    curre [i][j] = concentration(mincur,maxcur,img[i][j],rhoa,rhoc,model,eq)
    
    # consistência dos dados para retirar imperfeições e sombras nas images
    if number == 0:
        background = curre

    for i in range(numrows):
        for j in range(numcols):
            
            if curre[i][j] >= 0.995*background[i][j] and curre[i][j] <= 1.005*background[i][j]:
                curre[i][j] = rhoa
    
    if plot[3] == 1:            
        plot_current(x,z,curre,number,pathout,rhoa,rhoc,lenx,lenz, fdpi)
    
    write_current(curre,number,pathout)
    
    if sedanal == 1:
        if plot[1] == 1:
            plot_sedimen(x,z,sedim,number,pathout,lenx,lenz, fdpi)
            
        write_sedimen(sedim,number,pathout)
    
    return background,numrows,numcols,x,z,old
    
def concentration(mincur,maxcur,value, rhoa, rhoc, model, eq): 

    if model == 1:  # potential (user defined)
        y = eq[0]*value**eq[1] + eq[2] 

    if model == 0:  # linear
        a = (rhoc-rhoa)/(mincur-maxcur)
        b = rhoc - a*mincur
        y = a*value+b
    
    return y

def write_current(plume, num,pathout):
    np.savetxt(pathout+'/current'+str(num)+'.txt',plume,fmt='%.3f')

def plot_current(x,y,plume,num_scene,pathout,rhoa,rhoc,lenx,lenz,fdpi):
    
    plt.figure(figsize=(10,6))
    plt.imshow(plume, extent=[0,lenx/10,0,lenz/10], cmap=plt.get_cmap('plasma'))
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='Water density (kg/m³)')
    plt.clim(rhoa,rhoc)
    
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(pathout+'/current'+str(num_scene)+'.png',dpi=fdpi)
    plt.close()
     
def write_sedimen(plume, num,pathout):
    np.savetxt(pathout+'/sediment'+str(num)+'.txt',plume,fmt='%.3f')

def plot_sedimen(x,y,plume,num_scene,pathout,lenx,lenz,fdpi):
    
    plt.figure(figsize=(10,6))
    plt.imshow(plume, extent=[0,lenx/10,0,lenz/10], cmap=plt.get_cmap('plasma'))
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='occupied area')
    #plt.clim(0,100)
    
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(pathout+'/sediment'+str(num_scene)+'.png',dpi=fdpi)
    plt.close()