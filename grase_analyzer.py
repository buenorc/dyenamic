# -*- coding: utf-8 -*-
"""
Funções auxiliares 
Rafael de Carvalho Bueno (rafael.bueno@ufpr.br)

Para obter informações das relações px-distância real:
https://eleif.net/photo_measure.html

"""

import os
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import grase_spectral as psd


import matplotlib
matplotlib.use('Agg')

def test(plume,i,p1,p2,ah1,ah2,L,H,zmax):

    plume = np.rot90(plume, 3) # shift 1 place in horizontal axis
    plume = np.fliplr(plume)
    
    plt.figure(figsize=(10,4))
    plt.imshow(plume, extent=[0,L,0,H], cmap='gray')
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='Water density (kg/m³)')

    plt.scatter([zmax[i,p2]],[ah2],s=1,c='red')    
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig('Fig'+str(i)+'.png',dpi=800)
    plt.close()


def load(path,number,numrows,numcols,x,z,dt,size,rhoa,rhoc,nu,Hsed,L,H,Hini,Lo,zuser,ah1,ah2,ah3,sedanal,plot,text,root,fdpi):

    dz = H/numrows 
    t  = np.arange(0,number*dt,dt)
    if len(t) > number :
        t = t[:-1]
    
    xv = np.linspace(0,H,numrows)

    p1 = int((1-ah1/H)*numrows)
    p2 = int((1-ah2/H)*numrows)
    p3 = int((1-ah3/H)*numrows)
    
    
    glin  = 9.81*(rhoc-rhoa)/rhoc
    glina = 9.81*(rhoc-rhoa)/rhoa
    
    # vertical_var ~ [surface, ...      , bottom]  
    #                time    ,horizontal,  vertical
    
    c    = np.zeros((number  ,numcols,     numrows),float)
    tho  = np.zeros((number  ,numcols,     numrows),float)                          # thorpe scale
    mix  = np.zeros((number-1,numcols,     numrows),float)                          # mixing scale 
    
    zmax = np.zeros((number  ,numrows ),float)                                      # front evolution 
    c20  = np.zeros((number  ,numrows ),float)                                      # concentration x = 20 cm

    if sedanal == 1:
        s    = np.zeros((number  ,numcols,     numrows),float)                                                           # verify sedanal
        sco  = np.zeros((number  ,numcols,     numrows),float)                          # sediment background 
    else:
        Hsed = 0            
    
    print ("> Part IV      Calculating Thorpe scale... ")
    root.update()  
    
    jold = np.zeros((numrows),float)
    
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
            while c[i,j,k] > rhoa or j < jold[k]:
                j = j + 1
                if j == numcols-1:
                    break
            
            imax = j - 1               
            zmax[i,k] = z[imax]
        
            jold[k] = j 
        
        if i>0:
            mix[i-1,:,:] = c[i,:,:] - c[i-1,:,:]
            
        for j in range(numcols):
            tho[i,j,:]   = c[i,j,:] - np.sort(c[i,j,:])
        
 
    # 
    print ("> Part V       Computing velocity... ")
    root.update()  
    
    np.savetxt(path+'/zmax.txt',zmax,fmt='%.3f')
    np.savetxt(path+'/vertical_extend.txt',xv,fmt='%.3f')
    np.savetxt(path+'/horizontal_extend.txt',z,fmt='%.3f')

    # timeseries in different depths and velocity consistency

    rho_p1 = c[:,:,p1]
    rho_p2 = c[:,:,p2]
    rho_p3 = c[:,:,p3]

    if p1 != 999:
        density_heatmap(rho_p1,max(t),L,'p1',path, fdpi)
    if p2 != 999:
        density_heatmap(rho_p2,max(t),L,'p2',path, fdpi)
    if p3 != 999:
        density_heatmap(rho_p3,max(t),L,'p3',path, fdpi)

    zp1 = consistency_vel(zmax,p1,L,ah1)
    zp2 = consistency_vel(zmax,p2,L,ah2)
    zp3 = consistency_vel(zmax,p3,L,ah3)
 
    plot_evolution(t,number,numcols,numrows,x,zp1,zp2,zp3,ah1,ah2,ah3,path,glin,glina,c,H-Hsed,Hini,Lo,zuser,rhoa,nu,dz,Hsed,size,dt,fdpi,root)    
    count_current(t,dt,x,z,tho,mix,number,numrows,numcols,L,H,path,plot[4],text[4],fdpi)
        
    if sedanal == 1:
        
        print ("> Part VI      Analyzing erodible bed... ")
        root.update()  
        count_sediment(t,dt,x,z,s,sco,number,numrows,numcols,L,H,path,plot[0],text[0],fdpi)
    

def density_heatmap(rho,tlim,L,p,pathout,fdpi):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.flip(rho,axis=0), extent=[0,L,0,tlim], cmap=plt.get_cmap('plasma'), aspect='auto')
    plt.xlabel('x (cm)')
    plt.ylabel('time (sec)')
    plt.colorbar(orientation='vertical',label='water density (kg/m³)')
    
    np.savetxt(pathout+'/density_map_'+p+'.txt', np.flip(rho,axis=0), delimiter='\t', fmt='%.3f') 
    plt.savefig(pathout+'/density_map_'+p+'.png',dpi=fdpi)
    plt.close()            

   
def consistency_vel(zmax,p,L,ah):

    try: 
        z = zmax[:,p]
        number = len(z)

        z[0] = 0      # the first value is forced to be zero
              
        for i in range(1,number):
           
            if z[i]>=0.95*L:
                z[i] = None
            
            if  z[i]<np.nanmax(z[:i]):
                z[i] = None
            
    except IndexError:
        z = 999
    
    return z          
       
    
def count_current(t,dt,x,z,tho,mix,number,numrows,numcols,L,H,path,plot,text,fdpi):

    x6mix = np.zeros((number-1,numrows),float)
 
    max_scale = np.nanmax(tho)
    min_scale = np.nanmin(tho)    
    

    for  i in range(number):
        
        if text == 1:
            np.savetxt(path+'/thorpe'+str(i)+'.txt', np.transpose(tho[i,:,:]), delimiter='\t', fmt='%.3f')
        
        if plot == 1:
            plot_thorpe(tho[i,:,:],i,max_scale,min_scale,L,H,path,fdpi)
            
        if i >0:
            x6mix[i-1,:] = mix[i-1,int(numcols/2),:]
        
    current_heatmap(x6mix,max(t),dt,H,path,fdpi)

def plot_evolution(t,number,numcols,numrows,x,zp1,zp2,zp3,p1,p2,p3,pathout,glin,glina,c,H,Hini,Lo,zuser,rhoa,nu,dz,Hsed,size,dt,fdpi,root):


    vellin     = np.sqrt(glin*(Hini/2)*100)  # cm/s
    phi_tio    = Hini/H
    
    Frf        = 0.5*np.sqrt(phi_tio*(2-phi_tio))
    zeta       = ((27*Frf**2)/(12-2*Frf**2))**(1/3) 
 
    xs_slump = (0.5*vellin*(phi_tio*(2-phi_tio))*(t)-Lo)/(Lo)
    xs_simil = ((100*glina*Hini*Lo)**(1/3)*(t)**(2/3)-Lo)/Lo # zeta*((100*glina*Hini*Lo)**(1/3)*(t)**(2/3)-Lo)/Lo
    xs_visco = (((Hini*Lo)**(2/3))*((glin*(rhoa*glina/glin))**(1/3))*(t)**(1/5)-Lo)/Lo

    header = "time (sec)\thorizontal evolution (cm)\tconsidering y = "
    
    plt.figure(figsize=(10,6))

    if p1 != 999:
        plt.scatter(t,zp1,s=15,marker='^',color='red',label=r'$y=$'+str(round(p1,1))+' cm')
        np.savetxt(pathout+'/evolution'+str(round(p1,1))+'.txt',np.c_[t,zp1], header=header+str(round(p1,1))+' cm', delimiter='\t', fmt='%.3f')
        
    if p2 != 999:
        plt.scatter(t,zp2,s=15,marker='>',color='black',label=r'$y=$'+str(round(p2,1))+' cm')
        np.savetxt(pathout+'/evolution'+str(round(p2,1))+'.txt',np.c_[t,zp2], header=header+str(round(p2,1))+' cm', delimiter='\t', fmt='%.3f') 
    if p3 != 999:
        plt.scatter(t,zp3,s=15,marker='x',color='navy',label=r'$y=$'+str(round(p3,1))+' cm')
        np.savetxt(pathout+'/evolution'+str(round(p3,1))+'.txt',np.c_[t,zp3], header=header+str(round(p3,1))+' cm', delimiter='\t', fmt='%.3f')  

    plt.grid(axis='y',color='black',ls=":",lw=0.25)
    plt.grid(axis='x',color='black',ls=":",lw=0.25)
    
    plt.xlabel('time (sec)')
    plt.ylabel('x (cm)')
    
    plt.legend(loc='upper left',prop={'size': 8})
    
       
    plt.savefig(pathout+'/evolution.png',dpi=fdpi)
    plt.close()   



    plt.figure(figsize=(10,6))

    if p1 != 999:
        plt.scatter(t,(zp1+zuser-Lo)/Lo,s=15,marker='^',color='red',label=r'$y=$'+str(round(p1,1))+' cm')
        np.savetxt(pathout+'/evolution_dimensionless'+str(round(p1,1))+'.txt',np.c_[t,zp1], header=header+str(round(p1,1))+' cm', delimiter='\t', fmt='%.3f')
        
    if p2 != 999:
        plt.scatter(t,(zp2+zuser-Lo)/Lo,s=15,marker='>',color='black',label=r'$y=$'+str(round(p2,1))+' cm')
        np.savetxt(pathout+'/evolution_dimensionless'+str(round(p2,1))+'.txt',np.c_[t,zp2], header=header+str(round(p2,1))+' cm', delimiter='\t', fmt='%.3f') 
    if p3 != 999:
        plt.scatter(t,(zp3+zuser-Lo)/Lo,s=15,marker='x',color='navy',label=r'$y=$'+str(round(p3,1))+' cm')
        np.savetxt(pathout+'/evolution_dimensionless'+str(round(p3,1))+'.txt',np.c_[t,zp3], header=header+str(round(p3,1))+' cm', delimiter='\t', fmt='%.3f')  

    plt.plot(t,xs_slump,lw=0.5,ls='--',color='gray',label='slumping slope (Shin et al., 2004)')
    plt.plot(t,xs_simil,lw=0.5,ls='-' ,color='gray',label='self-similar slope')
    plt.plot(t,xs_visco,lw=0.5,ls=':' ,color='gray',label='viscous slope')

    plt.grid(axis='y',color='black',ls=":",lw=0.25)
    plt.grid(axis='x',color='black',ls=":",lw=0.25)
    
    plt.xlabel(r'$t (sec)$')
    plt.ylabel(r'$(x - \ell_o)/\ell_o$')
    
    plt.legend(loc='upper left',prop={'size': 8})
    
    plt.savefig(pathout+'/evolution_dimensionless.png',dpi=fdpi)
    plt.close()   



    plt.figure(figsize=(10,6))

    if p1 != 999:
        f, ff, fconf, conf = psd.welch_method(zp1, number, size, dt)
        plt.plot(f,ff,lw=1,ls='-',color='black',label=r'$y=$'+str(round(p1,1))+' cm')
        plt.plot(fconf,conf,lw=1,ls='--',color='black',alpha=0.5)
        np.savetxt(pathout+'/spectral_evolution'+str(round(p1,1))+'.txt',np.c_[f,ff,conf], header=header+str(round(p1,1))+' cm', delimiter='\t', fmt='%.3f')
        
    if p2 != 999:
        f, ff, fconf, conf = psd.welch_method(zp2, number, size, dt)
        plt.plot(f,ff,lw=1,ls='-',color='gray',label=r'$y=$'+str(round(p2,1))+' cm')
        plt.plot(fconf,conf,lw=1,ls='--',color='gray',alpha=0.5)
        np.savetxt(pathout+'/spectral_evolution'+str(round(p2,1))+'.txt',np.c_[f,ff,conf], header=header+str(round(p2,1))+' cm', delimiter='\t', fmt='%.3f')
    
    if p3 != 999:
        f, ff, fconf, conf = psd.welch_method(zp3, number, size, dt)
        plt.plot(f,ff,lw=1,ls='-',color='silver',label=r'$y=$'+str(round(p3,1))+' cm')
        plt.plot(fconf,conf,lw=1,ls='--',color='silver',alpha=0.5)
        np.savetxt(pathout+'/spectral_evolution'+str(round(p3,1))+'.txt',np.c_[f,ff,conf], header=header+str(round(p3,1))+' cm', delimiter='\t', fmt='%.3f')
  

    plt.grid(axis='y',color='black',ls=":",lw=0.25)
    plt.grid(axis='x',color='black',ls=":",lw=0.25)
    
    plt.xlabel('frequency (Hz)')
    plt.ylabel('PSD evolution (m²/Hz)')
    
    plt.legend(loc='upper left',prop={'size': 8})
    plt.xscale('log')
    plt.yscale('log')
       
    plt.savefig(pathout+'/evolution_spectral.png',dpi=fdpi)
    plt.close()   

    
    hf     = np.zeros(number  ,float)
    hf_ave = np.zeros(number  ,float)
    hf_try = np.zeros(numcols, float)
    
    hf_mid = np.zeros(number-1,float)
    hf_bar = np.zeros(number-1,float)
        
    interf = []
    for i in range(number):
        cfrozen = c[i,:,:]


        for j in range(numcols):
            
            zdiff = 0
            k     = numrows-1
            
            while cfrozen[j,k] > (0.005*rhoa+rhoa) and k>0:
                
                zdiff = zdiff + dz
                k     = k - 1 
                
            hf_try[j] = zdiff - Hsed

        interf.append(hf_try)
                
        hf[i]     = np.max(hf_try)
        hf_ave[i] = np.nanmean(hf_try[hf_try>0])


    for i in range(number-1):      
        hf_mid[i] = np.nanmean([hf[i],hf[i+1]])
        hf_bar[i] = np.nanmean([hf_ave[i],hf_ave[i+1]]) 
        
    np.savetxt(pathout+'/waveheight.txt', np.c_[t, hf, hf_ave], header= 'time(sec)\tmax height(cm)\tmean height(cm)', delimiter='\t', fmt='%.3f') 
    np.savetxt(pathout+'/interface.txt', np.array(interf), delimiter='\t', fmt='%.3f')
    
    v1_ck = [None, None]
    v2_ck = [None, None]
    v3_ck = [None, None]
    
    if p1 != 999:
        t1, v1 = current_velocity(t, zp1, p1, glin, Hini, nu, pathout,fdpi)
        current_froude(t1, v1, p1, glin, glina, hf_mid, hf_bar, H, Hini, pathout, fdpi)
        
        n  = np.count_nonzero(~np.isnan(v1))
        se = scipy.stats.sem(v1,nan_policy='omit')
        v1_ck = [np.nanmean(v1),se * scipy.stats.t.ppf(1.95/2., n-1)]
        
    if p2 != 999:
        t2, v2 = current_velocity(t, zp2, p2, glin, Hini, nu, pathout,fdpi)
        current_froude(t2, v2, p2, glin, glina, hf_mid, hf_bar, H, Hini, pathout, fdpi)

        n  = np.count_nonzero(~np.isnan(v2))
        se = scipy.stats.sem(v2,nan_policy='omit')
        v2_ck = [np.nanmean(v2),se * scipy.stats.t.ppf(1.95/2., n-1)]
        
    if p3 != 999:
        t3, v3 = current_velocity(t, zp3, p3, glin, Hini, nu, pathout,fdpi)
        current_froude(t3, v3, p3, glin, glina, hf_mid, hf_bar, H, Hini, pathout, fdpi)

        n  = np.count_nonzero(~np.isnan(v3))
        se = scipy.stats.sem(v3,nan_policy='omit')
        v3_ck = [np.nanmean(v3),se * scipy.stats.t.ppf(1.95/2., n-1)]  
        
    if v1_ck[0] != None and v2_ck[0] != None and v3_ck[0] != None:
        
        conf_ck = [v1_ck[1], v2_ck[1], v3_ck[1]]
        mean_ck = [v1_ck[0], v2_ck[0], v3_ck[0]] 
        
        imin = conf_ck.index(np.nanmin(conf_ck))
        
        v_ck = mean_ck[imin] 
        c_ck = conf_ck[imin]
        Nlim = 12                 # value obtained empirically 
        
        dt_limit = (x[1]-x[0])*Nlim/v_ck
        
    print ("> ")
    root.update() 
    print ("> Estimated averaged front velocity: "+str(round(v_ck,2))+" ± "+str(round(c_ck,2))+" cm/s")
    root.update() 
    print ("> \u0394t should be higher than " +str(round(dt_limit,2))+ " seconds")
    root.update()         
    print ("> ")
    root.update() 

    if dt < dt_limit:
         
        print ('> ')
        root.update() 
        print ('> Warning:     Increase the temporal resolution to improve performace')
        root.update() 
        print ('> ')
 


def current_froude( t, vel, p, glin, glina, hf_mid, hf_bar, H, Hini, pathout,fdpi):

    H      = H/100
    Hini   = Hini/100    
    
    hf_mid = hf_mid/100
    hf_bar = hf_bar/100
    
    hf_auto = Hini*np.ones((len(hf_mid)),float)/2
    
    phi_mid = hf_mid/H
    phi_bar = hf_bar/H
    phi_auto= hf_auto/H
    
    
    
    fr_max = vel/100/np.sqrt(glin*hf_mid)
    fr_ave = vel/100/np.sqrt(glin*hf_bar) 
    fr_auto= vel/100/np.sqrt(glin*hf_auto) 

    
    Ri_max = glina*hf_mid/(vel/100)**2
    Ri_ave = glina*hf_bar/(vel/100)**2
    Ri_auto= glina*hf_auto/(vel/100)**2
    
    fr_sim_mid = np.sqrt(phi_mid*(2-phi_mid)*(1-phi_mid)/(1+phi_mid))
    fr_sim_bar = np.sqrt(phi_bar*(2-phi_bar)*(1-phi_bar)/(1+phi_bar))
    fr_sim_auto= np.sqrt(phi_auto*(2-phi_auto)*(1-phi_auto)/(1+phi_auto))
    
    fr_shi     = 0.5*np.sqrt(2*hf_auto/H*(2-2*hf_auto/H))

    fig, ax = plt.subplots(2,1,figsize=(10,6))        
    ax[0].set_title('Maximum head height tracking | '+r'$y=$'+str(round(p,1))+' cm')

    ax[0].plot(t,hf_mid,lw=1,color='red', label='current height')    
    ax3 = ax[0].twinx()
    ax3.plot(t,Ri_max,lw=1,color='black', label='Richardson')
    ax3.set_ylabel(r'$Ri (t)$')
    
    
    ax[1].scatter(t,fr_max,s=15,marker='^',color='red',label='measured')
    ax[1].plot(t,fr_sim_mid,lw=1,color='navy',label='Benjamin (1968)')
    ax[1].plot(t,fr_shi,lw=1,color='blue',label='Shin et al. (2004)')
        
    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)

    ax[0].set_ylabel(r'$h_f (m)$')
    ax[1].set_xlabel('time (sec)')
    ax[1].set_ylabel(r'$Fr_f(t)$')
    
    ax[0].set_xlim([0,max(t)])
    ax[1].set_xlim([0,max(t)])
    
    np.savetxt(pathout+'/froude_max'+str(round(p,1))+'.txt', np.c_[t,hf_mid, fr_max, fr_sim_mid, fr_shi, Ri_max],  header= 'time(sec)\t maximum height (m)\t Fr measured\t Fr benjamin (1968)\t Fr Shin (2004)\t Ri', delimiter='\t', fmt='%.3f')
    
    ax[0].legend() 
    ax[1].legend() 

    plt.savefig(pathout+'/froude_max'+str(round(p,1))+'.png',dpi=fdpi)
    plt.close()       


    fig, ax = plt.subplots(2,1,figsize=(10,6))        
    ax[0].set_title('Averaged head height tracking | '+r'$y=$'+str(round(p,1))+' cm')

    ax[0].plot(t,hf_bar,lw=1,color='red', label='current height')
    ax3 = ax[0].twinx()
    ax3.plot(t,Ri_ave,lw=1,color='black', label='Richardson')
    ax3.set_ylabel(r'$Ri (t)$')    
    
    ax[1].scatter(t,fr_ave,s=15,marker='^',color='red',label='measured')
    ax[1].plot(t,fr_sim_bar,lw=1,color='navy',label='Benjamin (1968)')
    ax[1].plot(t,fr_shi,lw=1,color='blue',label='Shin et al. (2004)')
        
    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)

    ax[0].set_ylabel(r'$h_f (m)$')
    ax[1].set_xlabel('time (sec)')
    ax[1].set_ylabel(r'$Fr_f(t)$')
    
    ax[0].set_xlim([0,max(t)])
    ax[1].set_xlim([0,max(t)])
    
    np.savetxt(pathout+'/froude_averged'+str(round(p,1))+'.txt', np.c_[t,hf_bar, fr_ave, fr_sim_bar, fr_shi,Ri_ave],  header= 'time(sec)\t averaged height (m)\t Fr measured\t Fr benjamin (1968)\t Fr Shin (2004)\t Ri', delimiter='\t', fmt='%.3f')
    
    ax[0].legend() 
    ax[1].legend() 
    
    plt.savefig(pathout+'/froude_averged'+str(round(p,1))+'.png',dpi=fdpi)
    plt.close()    
 

    fig, ax = plt.subplots(2,1,figsize=(10,6))        
    ax[0].set_title('Automatic estimation | '+r'$y=$'+str(round(p,1))+' cm')

    ax[0].plot(t,hf_auto,lw=1,color='red', label='current height')
    ax3 = ax[0].twinx()
    ax3.plot(t,Ri_auto,lw=1,color='black', label='Richardson')
    ax3.set_ylabel(r'$Ri (t)$')    
    
    ax[1].scatter(t,fr_auto,s=15,marker='^',color='red',label='measured')
    ax[1].plot(t,fr_sim_auto,lw=1,color='navy',label='Benjamin (1968)')
    ax[1].plot(t,fr_shi,lw=1,color='blue',label='Shin et al. (2004)')
        
    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)

    ax[0].set_ylabel(r'$h_f (m)$')
    ax[1].set_xlabel('time (sec)')
    ax[1].set_ylabel(r'$Fr_f(t)$')
    
    ax[0].set_xlim([0,max(t)])
    ax[1].set_xlim([0,max(t)])
    
    np.savetxt(pathout+'/froude_auto'+str(round(p,1))+'.txt', np.c_[t,hf_bar, fr_auto, fr_sim_auto, fr_shi,Ri_auto],  header= 'time(sec)\t current height (m)\t Fr measured\t Fr benjamin (1968)\t Fr Shin (2004)\t Ri', delimiter='\t', fmt='%.3f')
    
    ax[0].legend() 
    ax[1].legend() 
    
    plt.savefig(pathout+'/froude_auto'+str(round(p,1))+'.png',dpi=fdpi)
    plt.close()       
 
def current_velocity(t, z, p, glin, Hini, nu, pathout,fdpi):
    
    lenew = len(t)-1
    tnew  = np.zeros((lenew),float)
    vel   = np.zeros((lenew),float)
    

    fig, ax = plt.subplots(2,1,figsize=(10,6)) 
    ax[0].set_title(r'$y=$'+str(round(p,1))+' cm')

    for i in range(lenew):
        tnew[i] = (t[i+1]+t[i])/2 
        vel[i]  = (z[i+1]-z[i])/(t[i+1]-t[i])

    fro = vel/100/np.sqrt(glin*Hini/100)
    Re  = vel*Hini/nu
    
    ax[0].scatter(tnew,vel,s=15,marker='^',color='red')   
    

    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)
    
    ax2 = ax[1].twinx()
    ax2.plot(tnew,Re,lw=0.8,ls='--',color='black',label='Froude number')
    ax[1].scatter(tnew,fro,s=15,marker='^',color='red', label='Reynolds number')
    
    ax[0].set_ylim([0,50])
    ax[0].set_ylabel(r'$u(t)$'+' (cm/s)')
    ax[1].set_ylabel(r'$Fr_{H}$')    
    ax2.set_ylabel(r'$Re_{H}$') 
    ax[1].set_xlabel('time (sec)')
    
    plt.legend()
    np.savetxt(pathout+'/velocity'+str(round(p,1))+'.txt', np.c_[tnew, vel, fro, Re], header= 'time(sec)\tfront velocity(cm/s)\tFroude initial (-)\t Reynolds number(-)', delimiter='\t', fmt='%.3f') 
    plt.savefig(pathout+'/velocity'+str(round(p,1))+'.png',dpi=fdpi)
    plt.close()           
    
    return tnew, vel
           
def current_heatmap(x6mix,tlim,dt,H,pathout,fdpi):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(x6mix), extent=[dt,tlim,0,H], cmap=plt.get_cmap('plasma'), aspect='auto')
    plt.xlabel('time (sec)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='density change(kg/m³)')
    
    np.savetxt(pathout+'/mixing_time.txt', np.transpose(x6mix), delimiter='\t', fmt='%.3f') 
    plt.savefig(pathout+'/mixing_time.png',dpi=fdpi)
    plt.close()            



def plot_thorpe(tho,num_scene,max_scale,min_scale,L,H,pathout,fdpi):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(tho), extent=[0,L,0,H], cmap=plt.get_cmap('plasma'))
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='overturn density displacement (kg/m³)')
    
    
    plt.gca().set_aspect('equal', adjustable='box')
     
    plt.savefig(pathout+'/thorpe'+str(num_scene)+'.png',dpi=fdpi)
    
    plt.clim(min_scale,max_scale)
    
    plt.close()

def count_sediment(t,dt,x,z,s,sco,number,numrows,numcols,L,H,path,plot,text,fdpi):
    
    total = np.zeros((number),float)
    tosco = np.zeros((number),float)
    x3tot = np.zeros((number),float)
    x4tot = np.zeros((number),float)
    x6tot = np.zeros((number),float)
    x8tot = np.zeros((number),float)
    x9tot = np.zeros((number),float)
    
    x6per = np.zeros((number,numrows),float)
    
    
    for i in range(number):
        
        
        total[i] = np.sum(s[i,:,:])  # area total
        tosco[i] = np.sum(sco[i,:,:]) # area total - initial total area
        
        x3tot[i] = np.sum(s[i,int(0.05*numcols),:]) 
        x4tot[i] = np.sum(s[i,int(0.25*numcols),:])
        x6tot[i] = np.sum(s[i,int(0.50*numcols),:])
        x8tot[i] = np.sum(s[i,int(0.75*numcols),:])
        x9tot[i] = np.sum(s[i,int(0.95*numcols),:])
        
        x6per[i][:] = s[i,int(numcols/2),:]
        
        if text == 1:
            np.savetxt(path+'/morchange'+str(i)+'.txt',np.transpose(sco[i,:,:]), delimiter='\t', fmt='%.3f')
            
        if plot == 1:
            plot_sedimen(sco[i,:,:],i,L,H,path,fdpi)
        
    sediment_heatmap(x6per,max(t),dt,H,path,fdpi)
    sediment_linearplot(t,total,tosco,x3tot,x4tot,x6tot,x8tot,x9tot,L,path,fdpi)

        

def sediment_linearplot(t,total,tosco,x3tot,x4tot,x6tot,x8tot,x9tot,L,path,fdpi):
    
    dim = [str(round(0.05*L,1)), str(round(0.25*L,1)), str(round(0.5*L,1)), str(round(0.75*L,1)), str(round(0.95*L,1))]
    
    fig, ax = plt.subplots(2,1,figsize=(10,6))

    tosco = tosco/10**2
    x3    = (x3tot-x3tot[0])
    x4    = (x4tot-x4tot[0])
    x6    = (x6tot-x6tot[0])
    x8    = (x8tot-x8tot[0])
    x9    = (x9tot-x9tot[0])
    
    ax[0].plot(t,tosco,lw=1,color='black')
    ax[1].plot(t,x3,lw=1,color='red' ,label=dim[0]+' cm')
    ax[1].plot(t,x4,lw=1,color='coral' ,label=dim[1]+' cm')
    ax[1].plot(t,x6,lw=1,color='black',label=dim[2]+' cm')
    ax[1].plot(t,x8,lw=1,color='royalblue' ,label=dim[3]+' cm')
    ax[1].plot(t,x9,lw=1,color='navy'  ,label=dim[4]+' cm')
        
    ax[0].set_title('Longitudinal bed elevation',loc='right', fontsize=10)
    
    ax[0].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[0].grid(axis='x',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='y',color='black',ls=":",lw=0.25)
    ax[1].grid(axis='x',color='black',ls=":",lw=0.25)

    ax[0].set_ylabel('area (cm²)')
    ax[1].set_ylabel('area at A (mm²)')
    
    ax[1].legend(loc='upper right',prop={'size': 8})
    
    plt.setp(ax[0].get_xticklabels(), visible=False)
    ax[1].set_xlabel('time (sec)')
    
    header_dye = 'time(sec)\tBed elevation(cm²)\t('+dim[0]+','+dim[1]+','+dim[2]+','+dim[3]+','+dim[4]+' mm) sediment variation (mm²)'
    np.savetxt(path+'/morchange_time.txt',np.c_[t,tosco,x3,x4,x6,x8,x9], header= header_dye, delimiter='\t', fmt='%.3f')
    plt.savefig(path+'/morchange_time.png',dpi=fdpi)
    

    
def plot_sedimen(sco,num_scene,L,H,pathout,fdpi):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(sco),extent=[0,L,0,H], cmap=plt.get_cmap('plasma'))
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.colorbar(orientation='horizontal',label='morphology changes')
    
    
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.savefig(pathout+'/morchange'+str(num_scene)+'.png',dpi=fdpi)
    
    
    plt.clim(-40,40)
    
    plt.close()
    
def sediment_heatmap(sedxfixed,tlim,dt,H,pathout,fdpi):
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.transpose(sedxfixed), extent=[dt,tlim,0,H], cmap=plt.get_cmap('plasma'), aspect='auto')
    plt.xlabel('time '+r'$(\Delta t)$')
    plt.ylabel('y (pixels)')
    plt.colorbar(orientation='horizontal',label='morphology changes')
    
    np.savetxt(pathout+'/sedxfixed.txt',np.transpose(sedxfixed), delimiter='\t', fmt='%.3f')
    plt.savefig(pathout+'/sediment-sumperfil.png',dpi=fdpi)
    plt.close()