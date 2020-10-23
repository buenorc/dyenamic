# -*- coding: utf-8 -*-
"""
Funções auxiliares 
Rafael de Carvalho Bueno (rafael.bueno@ufpr.br)

Para obter informações das relações px-distância real:
https://eleif.net/photo_measure.html

"""

import os
import numpy as np
import matplotlib.pyplot as plt


import matplotlib
matplotlib.use('Agg')



def load(path,number,numrows,numcols,x,z,dt,rhoa,rhoc,Hsed,L,H,ah1,ah2,ah3,sedanal,plot,text,root):

    dz = H/numrows 
    t  = np.arange(0,number*dt,dt)
    if len(t) > number :
        t = t[:-1]
    
    xv = x*dz

    p1 = int((1-ah1/H)*numrows)
    p2 = int((1-ah2/H)*numrows)
    p3 = int((1-ah3/H)*numrows)
    
    
    glin = 9.81*(rhoc-rhoa)/np.mean([rhoa,rhoc])
    
    # vertical_var ~ [surface, ...      , bottom]  
    #                time    ,horizontal,  vertical
    
    c    = np.zeros((number  ,numcols,     numrows),float)
    tho  = np.zeros((number  ,numcols,     numrows),float)                          # thorpe scale
    mix  = np.zeros((number-1,numcols,     numrows),float)                          # mixing scale 
    
    zmax = np.zeros((number  ,numrows ),float)                                      # front evolution 
    c20  = np.zeros((number  ,numrows ),float)                                      # concentration x = 20 cm

    if sedanal == 1:
        s    = np.zeros((number  ,numcols,     numrows),float)                                                           # verify sedanal
        sco  = np.zeros((number  ,numcols,     numrows),float)                          # sediment background              verify sedanal
    
    print ("> Part IV      Calculating Thorpe scale... ")
    root.update()  
    
    for i in range(number):
        
        
        c[i,:,:]   = np.loadtxt(path+'/current'+str(i)+'.txt',delimiter=' ',unpack=True)
        if text[3] == 0:
            os.remove(path+'/current'+str(i)+'.txt')
        
        c20[i,:] = c[i,int(numcols/2),:]
        
        if sedanal == 1:
            s[i,:,:]   = np.loadtxt(path+'/sediment'+str(i)+'.txt',delimiter=' ',unpack=True)                              # verify sedanal      
            sco[i,:,:] = s[i,:,:] - s[0,:,:]                                                                              # verify sedanal     
            
            if text[1] == 0:
                os.remove(path+'/sediment'+str(i)+'.txt')
        
        for k in range(numrows):
            
            j=0
            while c[i,j,k] != rhoa:
                j = j + 1
                if j == numcols-1:
                    break
            
            imax = j - 1               
            zmax[i,k] = z[imax]
        
        if i>0:
            mix[i-1,:,:] = c[i,:,:] - c[i-1,:,:]
            
        for j in range(numcols):
            tho[i,j,:] = c[i,j,:] - np.sort(c[i,j,:])
            
    # 
    print ("> Part V       Computing velocity... ")
    root.update()  
    
    np.savetxt(path+'/zmax.txt',zmax,fmt='%.3f')
    np.savetxt(path+'/vertical_extend.txt',xv,fmt='%.3f')
    np.savetxt(path+'/horizontal_extend.txt',z,fmt='%.3f')

    # timeseries in different depths and velocity consistency


    zp1 = consistency_vel(zmax,p1,L,ah1)
    zp2 = consistency_vel(zmax,p2,L,ah2)
    zp3 = consistency_vel(zmax,p3,L,ah3)
    

    

    plot_evolution(t,number,numcols,numrows,x,zp1,zp2,zp3,ah1,ah2,ah3,path,glin,c,H,rhoa,dz,Hsed)    
    count_current(t,dt,x,z,s,tho,mix,number,numrows,numcols,L,H,path,plot[4],text[4])
    
    
    if sedanal == 1:
        
        print ("> Part VI      Analyzing erodible bed... ")
        root.update()  
        count_sediment(t,dt,x,z,s,sco,number,numrows,numcols,L,H,path,plot[0],text[0])
    

   
def consistency_vel(zmax,p,L,ah):

    try: 
        z = zmax[:,p]
        
        
        number = len(z)
        for i in range(1,number-1):
            if  z[i]>=0.95*L or z[i+1]<z[i] or z[i-1]==None:
                z[i] = None
        
            z[0]      = None   # the first value is discarted
            z[number-1] = None   # the last value is discarted
    
    except IndexError:
        z = 999

    
    return z         
    
def count_current(t,dt,x,z,s,tho,mix,number,numrows,numcols,L,H,path,plot,text):

    x6mix = np.zeros((number-1,numrows),float)
 
    max_scale = np.nanmax(tho)
    min_scale = np.nanmin(tho)    
    

    for  i in range(number):
        
        if text == 1:
            np.savetxt(path+'/thorpe'+str(i)+'.txt', np.transpose(tho[i,:,:]), delimiter='\t', fmt='%.3f')
        
        if plot == 1:
            plot_thorpe(tho[i,:,:],i,max_scale,min_scale,L,H,path)
            
        if i >0:
            x6mix[i-1,:] = mix[i-1,int(numcols/2),:]
        
    current_heatmap(x6mix,max(t),dt,H,path)

def plot_evolution(t,number,numcols,numrows,x,zp1,zp2,zp3,p1,p2,p3,pathout,glin,c,H,rhoa,dz,Hsed):

    header = "time (sec)\thorizontal evolution (cm)\tconsidering y = "
    
    plt.figure(figsize=(10,6))

    if p1 != 999:
        plt.scatter(t,zp1,s=15,marker='^',label=r'$y=$'+str(round(p1,1))+' cm')
        np.savetxt(pathout+'/evolution'+str(round(p1,1))+'.txt',np.c_[t,zp1], header=header+str(round(p1,1))+' cm', delimiter='\t', fmt='%.3f')
    if p2 != 999:
        plt.scatter(t,zp2,s=15,marker='>',label=r'$y=$'+str(round(p2,1))+' cm')
        np.savetxt(pathout+'/evolution'+str(round(p2,1))+'.txt',np.c_[t,zp2], header=header+str(round(p2,1))+' cm', delimiter='\t', fmt='%.3f') 
    if p3 != 999:
        plt.scatter(t,zp3,s=15,marker='x',label=r'$y=$'+str(round(p3,1))+' cm')
        np.savetxt(pathout+'/evolution'+str(round(p3,1))+'.txt',np.c_[t,zp3], header=header+str(round(p3,1))+' cm', delimiter='\t', fmt='%.3f')  

    plt.grid(axis='y',color='black',ls=":",lw=0.25)
    plt.grid(axis='x',color='black',ls=":",lw=0.25)
    
    plt.xlabel('time (sec)')
    plt.ylabel('x (cm)')
    
    plt.legend(loc='upper left',prop={'size': 8})
    
       
    plt.savefig(pathout+'/evolution.png',dpi=800)
    plt.close()   
    
    hf     = np.zeros(number  ,float)
    hf_mid = np.zeros(number-1,float)
    hf_try = np.zeros(numcols, float)
    
    for i in range(number):
        cfrozen = c[i,:,:]


        for j in range(numcols):
            
            zdiff = 0
            k     = numrows-1
            
            while cfrozen[j,k] != rhoa and k>0:
                
                zdiff = zdiff + dz
                k     = k - 1 
                
            hf_try[j] = zdiff - Hsed
                
        hf[i] = np.max(hf_try)
    
    for i in range(number-1):      
        hf_mid[i] = np.mean([hf[i],hf[i+1]])
        
    np.savetxt(pathout+'/waveheight.txt', np.c_[t, hf], header= 'time(sec)\tfront height(cm)', delimiter='\t', fmt='%.3f') 
    
    
    if p1 != 999:
        t1, v1 = current_velocity(t, zp1, p1, glin, H-Hsed, pathout)
        current_froude(t1, v1, p1, glin, hf_mid, H,Hsed, pathout)
    if p2 != 999:
        t2, v2 = current_velocity(t, zp2, p2, glin, H-Hsed, pathout)
        current_froude(t2, v2, p2, glin, hf_mid, H,Hsed, pathout)
    if p3 != 999:
        t3, v3 = current_velocity(t, zp3, p3, glin, H-Hsed, pathout)
        current_froude(t3, v3, p3, glin, hf_mid, H,Hsed, pathout)
        

def current_froude( t, vel, p, glin, hf_mid, H, Hsed, pathout):
    
    fr = vel/100/np.sqrt(glin*hf_mid)

    fig, ax = plt.subplots(2,1,figsize=(10,6))        
    ax[0].set_title(r'$y=$'+str(round(p,1))+' cm')

    ax[0].plot(t,hf_mid)
    ax[1].scatter(t,fr,s=15,marker='^')

        
    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)

    ax[0].set_ylabel(r'$h_f (cm)$')
    ax[1].set_xlabel('time (sec)')
    ax[1].set_ylabel(r'$Fr_f(t)$')
    
    ax[0].set_xlim([0,max(t)])
    ax[1].set_xlim([0,max(t)])
    
    np.savetxt(pathout+'/froude'+str(round(p,1))+'.txt', np.c_[t,hf_mid, fr],  header= 'time(sec)\tFront height (cm)\tFroude front(-)', delimiter='\t', fmt='%.3f')
    plt.savefig(pathout+'/froude'+str(round(p,1))+'.png',dpi=800)
    plt.close()       

def current_velocity(t, z, p, glin,H, pathout):
    
    lenew = len(t)-1
    tnew  = np.zeros((lenew),float)
    vel   = np.zeros((lenew),float)
    

    fig, ax = plt.subplots(2,1,figsize=(10,6)) 
    ax[0].set_title(r'$y=$'+str(round(p,1))+' cm')

    for i in range(lenew):
        tnew[i] = (t[i+1]+t[i])/2 
        vel[i]  = (z[i+1]-z[i])/(t[i+1]-t[i])

    fro = vel/100/np.sqrt(glin*H/100)
    
    ax[0].scatter(tnew,vel,s=15,marker='^')   
    ax[1].scatter(tnew,fro,s=15,marker='^')

    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)
    
    ax[0].set_ylim([0,50])
    ax[0].set_ylabel(r'$u(t)$'+' (cm/s)')
    ax[1].set_ylabel(r'$Fr_{H}$')    
    ax[1].set_xlabel('time (sec)')
    
    np.savetxt(pathout+'/velocity'+str(round(p,1))+'.txt', np.c_[tnew, vel, fro], header= 'time(sec)\tfront velocity(cm/s)\tFroude initial (-)', delimiter='\t', fmt='%.3f') 
    plt.savefig(pathout+'/velocity'+str(round(p,1))+'.png',dpi=800)
    plt.close()           
    
    return tnew, vel
           
def current_heatmap(x6mix,tlim,dt,H,pathout):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(x6mix), extent=[dt,tlim,0,H], cmap=plt.get_cmap('plasma'), aspect='auto')
    plt.xlabel('time (sec)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='density change(kg/m³)')
    
    np.savetxt(pathout+'/mixing_time.txt', np.transpose(x6mix), delimiter='\t', fmt='%.3f') 
    plt.savefig(pathout+'/mixing_time.png',dpi=800)
    plt.close()            



def plot_thorpe(tho,num_scene,max_scale,min_scale,L,H,pathout):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(tho), extent=[0,L,0,H], cmap=plt.get_cmap('plasma'))
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='Thorpe scale (kg/m³)')
    
    
    plt.gca().set_aspect('equal', adjustable='box')
     
    plt.savefig(pathout+'/thorpe'+str(num_scene)+'.png',dpi=800)
    
    plt.clim(min_scale,max_scale)
    
    plt.close()

def count_sediment(t,dt,x,z,s,sco,number,numrows,numcols,L,H,path,plot,text):
    
    total = np.zeros((number),float)
    tosco = np.zeros((number),float)
    x6tot = np.zeros((number),float)
    x6per = np.zeros((number,numrows),float)
    
    
    for i in range(number):
        
        
        total[i] = np.sum(s[i,:,:])  # area total
        tosco[i] = np.sum(sco[i,:,:]) # area total - initial total area
        x6tot[i] = np.sum(s[i,int(numcols/2),:])
        x6per[i][:] = s[i,int(numcols/2),:]
        
        if text == 1:
            np.savetxt(path+'/morchange'+str(i)+'.txt',np.transpose(sco[i,:,:]), delimiter='\t', fmt='%.3f')
            
        if plot == 1:
            plot_sedimen(sco[i,:,:],i,L,H,path)
        
    sediment_heatmap(x6per,max(t),dt,H,path)
    sediment_linearplot(t,total,tosco,x6tot,path)

        

def sediment_linearplot(t,total,tosco,x6tot,path):
    
    fig, ax = plt.subplots(2,1,figsize=(10,6))

    tosco = tosco*10**-2 
    x6    = (x6tot-x6tot[0])*10**-2
    
    ax[0].plot(t,tosco) 
    ax[1].plot(t,x6) 
        
    ax[0].set_title('Longitudinal bed elevation',loc='right', fontsize=10)
    ax[1].set_title('A: x=20 cm',loc='right', fontsize=10)

    
    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)

    ax[1].set_title('section x = 20 cm',loc='right', fontsize=10)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)

    ax[0].set_ylabel('area (cm²)')
    ax[1].set_ylabel('area at A (cm²)')
    
    plt.setp(ax[0].get_xticklabels(), visible=False)
    ax[1].set_xlabel('time (sec)')
    
    
    np.savetxt(path+'/morchange_time.txt',np.c_[t,tosco,x6], header= 'time(sec)\tBed elevation(cm²)\tsediment variation (cm²)', delimiter='\t', fmt='%.3f')
    plt.savefig(path+'/morchange_time.png',dpi=800)
    

    
def plot_sedimen(sco,num_scene,L,H,pathout):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(sco),extent=[0,L,0,H], cmap=plt.get_cmap('plasma'))
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='morphology changes')
    
    
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.savefig(pathout+'/morchange'+str(num_scene)+'.png',dpi=800)
    
    
    plt.clim(-40,40)
    
    plt.close()
    
def sediment_heatmap(sedxfixed,tlim,dt,H,pathout):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(sedxfixed), extent=[dt,tlim,0,H], cmap=plt.get_cmap('plasma'), aspect='auto')
    plt.xlabel('time '+r'$(\Delta t)$')
    plt.ylabel('y (pixels)')
    plt.colorbar(orientation='horizontal',label='morphology changes')
    
    np.savetxt(pathout+'/sedxfixed.txt',np.transpose(sedxfixed), delimiter='\t', fmt='%.3f')
    plt.savefig(pathout+'/sediment-sumperfil.png',dpi=800)
    plt.close()