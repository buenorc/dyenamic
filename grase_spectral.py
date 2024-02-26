# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:49:29 2020

@author: rafae
"""
import numpy as np
import scipy.special as sc
from scipy.stats.distributions import chi2
from scipy import signal

def chi2inv(p, nfft, nperseg, test=None):
#   
#   External Function: Statistical Analysis        
#   Function to estimate the inverse of cumulative distribution function (percentile)
#     
    if test == None:
        nw2=2*(2.5164*(nfft/nperseg))*1.2
        return chi2.ppf(p, df=nw2)/nw2
    else:
        nw2=(nfft/nperseg)
        return 2*sc.gammaincinv(nw2,p)/nw2  # Inverse incomplete gamma function

def stad_deviation(data):


    m = np.mean(data,axis=0)
    sd = np.std(data)
    
    return m, m-sd, m+sd
    

def conflevel(Ax,npr,dt,rho,wr,nfft,nperseg):
#   
#   External Function: Statistical Analysis        
#   Function to estimate the confidence levels based on the chi2 test (red noise)
# 
    facchi95=chi2inv(0.95, nfft, nperseg)   # Bernhardt and Kirillin (2013)
    
    fnyq=1/(2*dt)   # Nyquist frequency (half the sampling rate)


    theored=np.zeros((npr))
    for i in range(npr):
        theored[i]=(1-rho**2)/(1-(2*rho*np.cos(np.pi*wr[i]/fnyq))+rho**2)

    theoredun=theored[0];
    theored[0]=0;

    Art = np.mean(theored)
    theored[0]=theoredun
    theored=theored*(Ax/Art)    # Normalisation of the spectrum

    tabtchi=[]
    tabtchi[:]=theored*facchi95  # Chi-square confidence levels
     
    return tabtchi

def rhoAR1(datax):
#   
#   External Function: Statistical Analysis        
#   Function to calculate the lag-1 autocorrelation coefficient 
#   for an AR1 autocorrelation of data.
#
    nrho=len(datax)
    rho=0
    sommesup=0
    sommeinf=0

    moy=np.sum(datax)/nrho
    datam=datax-moy

    for i in range(1,nrho):
        j=i-1
        sommesup=sommesup+(datam[i]*datam[j])
        sommeinf=sommeinf+((datam[j])**2)
        
    rho=sommesup/sommeinf
    return rho

def Rednoise(nt,rho,nsim):
#   
#   External Function: Statistical Analysis        
#   Function to calculates AR1 autocorrelation (Monte-Carlo simulation)
#
    rzero=0
    
    redtab=np.zeros((nt,nsim))
    red=np.zeros(nt)
    i,j=1,1

    srho=np.sqrt(1-rho**2)

    for i in range(nsim):
        
        white=srho*np.random.randn(1)
        red[0]=rho*rzero+white
        
        for j in range(1,nt):
            white=srho*np.random.randn(1)
            red[j]=rho*red[j-1]+white

        redtab[:,i]=red

    return redtab

def RedConf(datax,dt,nsim,nperseg):
#   
#   External Function: Statistical Analysis        
#
    # calculation of the lag-1 autocorrelation coefficient
    rho=rhoAR1(datax)
    
    nt = len(datax)
    # calculation of nsim red noise models
    redtab = Rednoise(nt,rho,nsim)
    
    datan=[]
    i=1
    
    datan=datax-np.mean(datax)

    # spectral analysis of the data
    #nfft = max(256,2**np.ceil(np.log2(abs(len(datan)))))
    nfft = nperseg
    w,po   = signal.welch(datan[:], fs=1/dt, nperseg=nperseg)
    
    # calculation of the area of the data power spectrum
    Ax=np.mean(po)
    

    for i in range(nsim):  # spectral analysis of the nsim red noise signals
        
        red2n=redtab[:,i] -np.mean(redtab[:,i])
        wr,pr = signal.welch(red2n, fs=1/dt, nperseg=nperseg)
        
    npr=len(pr)
    tabtchi = conflevel(Ax,npr,dt,rho,wr,nfft,nperseg)
    
    return wr,tabtchi

def mask (serie):
#
#   External Function: Conditional Analysis
#   Function to filter not a number (NaN) values 
#    
    xi = np.arange(len(serie))
    
    m = np.isfinite(serie)
    xfiltered = np.interp(xi, xi[m], serie[m])
    
    return xfiltered

def welch_method(serie, number, size, dt):
#
   
    nsim = 10                    # number of Monte Carlo simulations;
    n    = int(size/dt)          # nperseg
    
    if n > len(serie) or size==0:  # Warning: the specified window size is larger than the time-serie
        n = len(serie)
    
    serie    = mask(serie)     
    freq, ff = signal.welch(serie, fs=1.0/dt, window='hamming', nperseg=n, detrend='linear', axis=-1)
    
    wr, conf = RedConf(serie,dt,nsim,n)
    
        
    return freq[1:], ff[1:], wr[1:], conf[1:]
    