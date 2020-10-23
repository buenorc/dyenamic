# -*- coding: utf-8 -*-
'''

Rafael de Carvalho Bueno (rafael.bueno@ufpr.br)
'''
import os 
import sys
import time
import numpy as np
from tkinter import *

import grase_packages as grapa
import grase_analyzer as grana


class StdoutRedirector(object):

    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, str):
        self.text_area.insert(END, str)
        self.text_area.see(END)

   

def main():

    old_stdout = sys.stdout
    start_time = time.time()
    
    root = Tk()
    root.configure(background='white')
    root.title("Dyenamic Running") 
    root.geometry('800x800')
    
    
    outputPanel = Text(root, wrap='word', height=30, width=100)
    outputPanel.grid(column=0, row=0, columnspan = 2, sticky='NSWE', padx=5, pady=5)

    sys.stdout = StdoutRedirector(outputPanel)
    

    print ("> Dyenamic is starting the data processing... ")
    root.update()
    print ("--------------------------------------------------------------------------------------")
    root.update()
    print ("> Dyenamic, version 1.00.1        September 2020")
    root.update()  
    print ("> ")
    root.update() 
    print ("--------------------------------------------------------------------------------------")
    root.update()
    print ("> ")
    root.update() 
    print ("> Part I       Reading information from GUI... ")
    root.update()

# -----------------------------------------------------------------------------
#                         INPUTS AND CONFIGURATIONS
# -----------------------------------------------------------------------------
#
# plot[variation, motion, frame, current, thorpe]
# text[variation, motion, None , current, thorpe]

    plot= np.zeros((7),int)
    text= np.zeros((7),int)
#    
    with open('temporary.txt') as reader:

        path_video = reader.readline()
        path_video = path_video.replace('\n','')
        
        pathout    = reader.readline()
        pathout    = pathout.replace('\n','')
        
        
        dt         = float(reader.readline())
        rhoa       = float(reader.readline())
        rhoc       = float(reader.readline())
        L          = float(reader.readline())
        H          = float(reader.readline())        
        ah1        = float(reader.readline())    # "999" used to swich off 
        ah2        = float(reader.readline())    # "999" used to swich off 
        ah3        = float(reader.readline())    # "999" used to swich off 
        maxcur     = float(reader.readline())
        mincur     = float(reader.readline())
        piv        = int(reader.readline())     # "1" activated / "0" do not activated
        text[6]    = int(reader.readline())
        plot[6]    = int(reader.readline())
        
        sedanal    = int(reader.readline())      # "1" activated / "0" do not activated
        Hsed       = float(reader.readline())    # "0" used to swich off 
        maxsed     = float(reader.readline())    # "999" used to swich off 
        minsed     = float(reader.readline())    # "999" used to swich off       
        plot[0]    = int(reader.readline())      # "1" activated / "0" do not activated
        plot[1]    = int(reader.readline())      # "1" activated / "0" do not activated
        text[0]      = int(reader.readline())      # "1" activated / "0" do not activated
        text[1]      = int(reader.readline())      # "1" activated / "0" do not activated
        
        plot[2]      = int(reader.readline())
        plot[3]      = int(reader.readline())
        plot[4]      = int(reader.readline())
        text[3]      = int(reader.readline())
        text[4]      = int(reader.readline())
            
    
    os.remove('temporary.txt')
    
    lenx   = L*100       # escala de comprimento do vídeo (mm)
    lenz   = H*100       # escala de altura do vídeo (mm)

    print ("> Part II      Defining frames from video and running PIV... ")
    root.update()          
    
    num_scene,bg,numr,numc,x,z,dt = grapa.vidtoframes(path_video, dt, mincur, maxcur,rhoa,rhoc,minsed,maxsed,lenx,lenz,sedanal,plot,text,pathout,piv,root)    
    
    print ("> ")
    root.update()
    print ("> Execution time for part I and II: ")
    root.update() 
    load_time = time.time()
    
    print ("> "+str(round(load_time-start_time,4))+' seconds')
    root.update() 
    print ('> ')   
    root.update() 
    print ("--------------------------------------------------------------------------------------")
    root.update()
    print('> ')
    root.update()
    print ("> Part III     Starting data processing...  ")
    root.update()  
  
    
    grana.load(pathout,num_scene,numr,numc,x,z,dt,rhoa,rhoc,Hsed,L,H,ah1,ah2,ah3,sedanal,plot,text,root)
    
    
    print ("> ")
    root.update()

    if sedanal == 0:
        print ("> Execution time for part III to V: ")
    else:
        print ("> Execution time for part III to VI: ")
    root.update() 
    
    new_time = time.time()
    print (">  "+str(round(new_time - load_time,4))+" seconds")
    root.update()  
    print ("> ")
    root.update()
    print ("> ")
    root.update()

    print ("--------------------------------------------------------------------------------------")
    root.update()
    print ("> ")
    root.update()

    print ("> FINISHED            Dyenamic ")
    root.update() 
    print ("> ")
    root.update()
    print ("> ")
    root.update()
    print ("> Check the following path for results:")
    root.update()
    print ("> "+pathout)
    root.update() 
    print ("> ")
    root.update()
    print ("> ")
    root.update()
    print ("> For additional information:")
    root.update()
    print ("> https://sites.google.com/view/rafaelbueno/programs")
    root.update()
    print ("> ")
    root.update()
    print ("> ")
    root.update()
    root.update()
    
    
    root.mainloop()
    sys.stdout = old_stdout