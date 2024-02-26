# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:38:12 2019

@author: Rafael de Carvalho Bueno
"""

import webbrowser

import platform
from tkinter import *
from tkinter import ttk
import tkinter.ttk as tka
from tkinter.filedialog import *
from tkinter import filedialog

import grase_calibration as calibri



def OpenUrl(url):
    webbrowser.open_new(url)



def save_settings(temporary):


    if temporary == 'temporary':
        data_file = 'temporary.txt' 
    else:   
        f = filedialog.asksaveasfile(defaultextension=".gcs")
        data_file = str(f.name)

    with open(data_file, 'w') as data:

        data.write(str(path_video)+'\n')
        data.write(str(folder_path)+'\n')
        data.write(str(dt.get())+'\n')
        data.write(str(rhoa.get())+'\n')
        data.write(str(rhoc.get())+'\n')
        data.write(str(L.get())+'\n')
        data.write(str(H.get())+'\n')
        data.write(str(Hc.get())+'\n')
        data.write(str(Lo.get())+'\n')
        data.write(str(zuser.get())+'\n')
        data.write(str(nu.get())+'\n')
        data.write(str(size.get())+'\n')
        
        if int(p1.get()) == 0:
            data.write(str(999)+'\n')
        else:
            data.write(str(ha.get())+'\n')

        if int(p2.get()) == 0:
            data.write(str(999)+'\n')
        else:
            data.write(str(hb.get())+'\n')

        if int(p3.get()) == 0:
            data.write(str(999)+'\n')
        else:
            data.write(str(hc.get())+'\n')
            
        data.write(str(upcur.get())+'\n')
        data.write(str(downcur.get())+'\n')
        
        data.write(str(model_number)+'\n')
        if model_number == 1:
            data.write(str(coefa.get())+'\n')
            data.write(str(coefb.get())+'\n')
            data.write(str(coefc.get())+'\n')

        if model_number == 0:
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            
        data.write(str(piv_analyzer.get())+'\n')


        if int(piv_analyzer.get()) == 0:
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')  
            data.write(str(999)+'\n')
            data.write(str(999)+'\n') 
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')  
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')        
        else:
            data.write(str(winsize.get())+'\n')
            data.write(str(searea.get())+'\n')
            data.write(str(overlap.get())+'\n')  
            data.write(str(intera.get())+'\n')
            data.write(str(kernel.get())+'\n') 
            data.write(str(thold.get())+'\n')
            data.write(str(maxVal.get())+'\n')  
            data.write(str(block.get())+'\n')
            data.write(str(const.get())+'\n')
            data.write(str(txt_piv.get())+'\n')
            data.write(str(png_piv.get())+'\n')
        
        data.write(str(sed_button.get())+'\n')
        
        if int(sed_button.get()) == 0:
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')
        else: 
            data.write(str(Hsed.get())+'\n')
            data.write(str(upsed.get())+'\n')
            data.write(str(downsed.get())+'\n')
            data.write(str(png_varia.get())+'\n')
            data.write(str(png_motion.get())+'\n')
            
            data.write(str(txt_varia.get())+'\n')
            data.write(str(txt_motion.get())+'\n')
        
        data.write(str(png_frame.get())+'\n')
        data.write(str(png_current.get())+'\n')
        data.write(str(png_thorpe.get())+'\n')
        
        data.write(str(txt_current.get())+'\n')
        data.write(str(txt_thorpe.get())+'\n')
        data.write(str(fdpi.get())+'\n')
            

def open_button():

    global path_video, folder_path 
    
    path_open = askopenfilename(defaultextension='.gcs', filetypes=[('GCS files','*.gcs')])
       
    if path_open:
        with open(str(path_open),'r') as reader:
            path_video = reader.readline()
            path_video = path_video.replace('\n','')

            folder_path = reader.readline()
            folder_path = folder_path.replace('\n','')
            
            dt.delete(0,'end')
            dt.insert(END,float(reader.readline()))           

            rhoa.delete(0,'end')
            rhoa.insert(END,float(reader.readline()))  
            
            rhoc.delete(0,'end')
            rhoc.insert(END,float(reader.readline()))  

            L.delete(0,'end')
            L.insert(END,float(reader.readline()))  

            H.delete(0,'end')
            H.insert(END,float(reader.readline()))  

            Hc.delete(0,'end')
            Hc.insert(END,float(reader.readline()))  

            Lo.delete(0,'end')
            Lo.insert(END,float(reader.readline()))  

            zuser.delete(0,'end')
            zuser.insert(END,float(reader.readline()))  
            
            nu.delete(0,'end')
            nu.insert(END,float(reader.readline()))  

            size.delete(0,'end')
            size.insert(END,float(reader.readline())) 

            ha.delete(0,'end')
            num = reader.readline().strip()  
            
            if num == '999':
                p1.set(0)
                ha.config(state='disable')
            else:
                p1.set(1)
                ha.config(state='normal') 
                ha.insert(END,float(num))                             
    
            hb.delete(0,'end')
            num = reader.readline().strip()  
            
            if num == '999':
                p2.set(0)
                hb.config(state='disable')
            else:
                p2.set(1)
                hb.config(state='normal') 
                hb.insert(END,float(num))   

            hc.delete(0,'end')
            num = reader.readline().strip()  
            
            if num == '999':
                p3.set(0)
                hc.config(state='disable')
            else:
                p3.set(1)
                hc.config(state='normal') 
                hc.insert(END,float(num))   

            upcur.delete(0,'end')
            upcur.insert(END,float(reader.readline())) 

            downcur.delete(0,'end')
            downcur.insert(END,float(reader.readline()))                 

            num = reader.readline().strip()  
            if num == '0':
                model.set(density_model[0])
                coefa.config(state='disable')
                next(reader)
                coefb.config(state='disable')
                next(reader)            
                coefc.config(state='disable')
                next(reader)   
                
            if num == '1':
                model.set(density_model[1])
                coefa.config(state='normal')
                coefa.delete(0,'end')
                coefa.insert(END,float(reader.readline())) 
                coefb.config(state='normal')
                coefb.delete(0,'end')
                coefb.insert(END,float(reader.readline())) 
                coefc.config(state='normal')
                coefc.delete(0,'end')
                coefc.insert(END,float(reader.readline())) 
                
            num = reader.readline().strip() 
        
            if num == '0':
                piv_analyzer.set(0)
                
                winsize.config(state='disable')
                next(reader)
                searea.config(state='disable')
                next(reader)                
                overlap.config(state='disable')
                next(reader)
                intera.config(state='disable')
                next(reader)
                kernel.config(state='disable')
                next(reader)
                thold.config(state='disable')
                next(reader)
                maxVal.config(state='disable')
                next(reader)
                block.config(state='disable')
                next(reader)
                const.config(state='disable')
                next(reader)                
                
                piv_seltxt.config(state='disable')
                next(reader)
                piv_sel.config(state='disable')
                next(reader)  
 
                  
            else:
                piv_analyzer.set(1)    

                winsize.config(state='normal')
                winsize.delete(0,'end')
                winsize.insert(END,float(reader.readline())) 

                searea.config(state='normal')
                searea.delete(0,'end')
                searea.insert(END,float(reader.readline())) 
                
                overlap.config(state='normal')
                overlap.delete(0,'end')
                overlap.insert(END,float(reader.readline())) 
                
                intera.config(state='normal')
                intera.delete(0,'end')
                intera.insert(END,float(reader.readline())) 
                
                kernel.config(state='normal')
                kernel.delete(0,'end')
                kernel.insert(END,float(reader.readline())) 
                
                thold.config(state='normal')
                thold.delete(0,'end')
                thold.insert(END,float(reader.readline())) 
                
                maxVal.config(state='normal')
                maxVal.delete(0,'end')
                maxVal.insert(END,float(reader.readline()))  
                
                block.config(state='normal')
                block.delete(0,'end')
                block.insert(END,float(reader.readline())) 
                
                const.config(state='normal')
                const.delete(0,'end')
                const.insert(END,float(reader.readline()))      

                piv_seltxt.config(state='normal')
                piv_sel.config(state='normal')
                txt_piv.set(int(reader.readline()))
                png_piv.set(int(reader.readline()))   
                
            num = reader.readline().strip()  
            
            if num == '0':

                sed_button.set(0)
                Hsed.config(state='disable')
                next(reader)
                upsed.config(state='disable')
                next(reader)
                downsed.config(state='disable')
                next(reader)
                                
                varia_sel.config(state='disable')
                next(reader)
                
                motion_sel.config(state='disable')
                next(reader)
                
                varia_seltxt.config(state='disable')
                next(reader)
                
                motion_seltxt.config(state='disable')
                next(reader)
                
            else:
                sed_button.set(1)
                Hsed.config(state='normal')
                Hsed.delete(0,'end')
                Hsed.insert(END,float(reader.readline()))  
                upsed.config(state='normal')
                upsed.delete(0,'end')
                upsed.insert(END,float(reader.readline())) 
                downsed.config(state='normal')
                downsed.delete(0,'end')
                downsed.insert(END,float(reader.readline())) 
                
                
                varia_sel.config(state='normal')
                motion_sel.config(state='normal')
                varia_seltxt.config(state='normal')
                motion_seltxt.config(state='normal')                       
                
                png_varia.set(int(reader.readline()))
                png_motion.set(int(reader.readline())) 
                txt_varia.set(int(reader.readline()))  
                txt_motion.set(int(reader.readline())) 
            
            png_frame.set(int(reader.readline()))
            png_current.set(int(reader.readline()))
            png_thorpe.set(int(reader.readline()))
            txt_current.set(int(reader.readline())) 
            txt_thorpe.set(int(reader.readline())) 

            fdpi.delete(0,'end')
            fdpi.insert(END,float(reader.readline()))  
                
def calibration_current():
    
    global iccur
    path_ic = askopenfilename(defaultextension='.mp4', filetypes=[('MP4 files','*.mp4')]) 
    pathout = filedialog.askdirectory()
    calibri.cal_current(path_ic,pathout)
    
    

    
def AboutCallBack():
   msg = messagebox.showinfo( "About", " Dyenamic - version 1.00.5 \n Copyright (C) 2021 Rafael de Carvalho Bueno \n All rights reserved \n \n Lead Developer and Project Manager: \n Rafael de Carvalho Bueno \n \n  Developers: \n  Nathan Streisky da Silva \n André Diniz dos Santos \n\n Quality Assurance: \n Tobias Bleninger  \n \n \n Report problems and improvements to email adresss below \n rafael.bueno.itt@gmail.com\n \n for mor information, see: \n https://sites.google.com/view/dyenamic/dyenamic \n ")    


# ------------ functions gravity current---------------------------------------
    
def video_input():
    global path_video
    path_video = askopenfilename(defaultextension='.mp4', filetypes=[('MP4 files','*.mp4')])
    

def selected_h1():
    global h1_type
    h1_type = int(p1.get())
    
    if int(p1.get()) == 0:
        ha.config(state='disable')
    elif int(p1.get()) ==1:
        ha.config(state='normal')
        
def selected_h2():
    global h2_type
    h2_type = int(p2.get())
    
    if int(p2.get()) == 0:
        hb.config(state='disable')
    elif int(p2.get()) ==1:
        hb.config(state='normal')

def selected_h3():
    global h3_type
    h3_type = int(p3.get())
    
    if int(p3.get()) == 0:
        hc.config(state='disable')
    elif int(p3.get()) ==1:
        hc.config(state='normal')
      
# ------------  functions calibration -----------------------------------------        

def coefficients(model_rho):
    
    global model_number
    
    if model_rho == 'Linear':
        model_number = 0
        coefa.config(state='disable')
        coefb.config(state='disable')
        coefc.config(state='disable')
        
    if model_rho == 'Potential':
        model_number = 1
        coefa.config(state='normal')
        coefb.config(state='normal')
        coefc.config(state='normal')

# ------------  functions sediment --------------------------------------------        


def selected_sed():
    global sed_type
    sed_type = int(sed_button.get())

    if int(sed_button.get())==0:
        Hsed.config(state='disable')
        upsed.config(state='disable')
        downsed.config(state='disable')
        varia_sel.config(state='disable')
        motion_sel.config(state='disable')
        varia_seltxt.config(state='disable')
        motion_seltxt.config(state='disable')
        
    elif int(sed_button.get())==1: 
        Hsed.config(state='normal')
        upsed.config(state='normal')
        downsed.config(state='normal')
        varia_sel.config(state='normal')
        motion_sel.config(state='normal')
        varia_seltxt.config(state='normal')
        motion_seltxt.config(state='normal')



# ------------  functions PIV     --------------------------------------------        

def selected_piv():
    global piv_type
    piv_type = int(piv_analyzer.get())



    if int(piv_analyzer.get()) == 0:
        piv_sel.config(state='disable')
        piv_seltxt.config(state='disable')
        
        winsize.config(state='disable')
        searea.config(state='disable')
        overlap.config(state='disable')
        intera.config(state='disable')
        kernel.config(state='disable')
        thold.config(state='disable')
        maxVal.config(state='disable')
        block.config(state='disable')
        const.config(state='disable')


    elif int(piv_analyzer.get()) == 1: 
        piv_sel.config(state='normal')
        piv_seltxt.config(state='normal')
        
        winsize.config(state='normal')
        searea.config(state='normal')
        overlap.config(state='normal')
        intera.config(state='normal')
        kernel.config(state='normal')
        thold.config(state='normal')
        maxVal.config(state='normal')
        block.config(state='normal')
        const.config(state='normal')
        
        winsize.delete(0,'end')
        winsize.insert(END,16)
        
        searea.delete(0,'end')
        searea.insert(END,32)
        
        overlap.delete(0,'end')
        overlap.insert(END,8)
        
        intera.delete(0,'end')
        intera.insert(END,10)
        
        kernel.delete(0,'end')
        kernel.insert(END,2)
        
        thold.delete(0,'end')
        thold.insert(END,1.3)
        
        maxVal.delete(0,'end')
        maxVal.insert(END,0)
        
        block.delete(0,'end')
        block.insert(END,5)
        
        const.delete(0,'end')
        const.insert(END,5)
        
          
# ------------  functions output and run --------------------------------------     

def output_folder():

    global folder_path
    folder_path = filedialog.askdirectory()

    

def export_data():
    
    import grase as grase
    save_settings('temporary')  
    grase.main()
        
# ---------------------- menu -------------------------------------------------        
window = Tk()

if platform.system() == 'Windows':
    window.iconbitmap("./dyenamic-icon.ico")

else:
    img = PhotoImage(file='./dyenamic-icon.png')
    window.tk.call('wm','iconphoto',window._w,img)


window.title("Dyenamic") 
window.geometry('800x860')

# ----------------------- initial menu ----------------------------------------

menubar = Menu(window)
filemenu = Menu(menubar, tearoff = 0)


menubar.add_cascade(label = "File", menu = filemenu)
editmenu = Menu(menubar, tearoff=0)

filemenu.add_command(label = "Open", command = open_button)
filemenu.add_command(label = "Save as...", command = lambda: save_settings(0))

filemenu.add_separator()
filemenu.add_command(label = "Exit", command = window.destroy)


calibramenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Calibration", menu = calibramenu)
calibramenu.add_command(label = "Gravity current", command = calibration_current)


helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Help", menu = helpmenu)
url = 'https://rafaelbuenoo.wixsite.com/researchbueno/dyenamic'
helpmenu.add_command(label = "Manual", command = lambda aurl=url:OpenUrl(aurl))
helpmenu.add_command(label = "About", command = AboutCallBack)



# ----------------------- Sub-menu --------------------------------------------

tabControl = ttk.Notebook(window)
tabControl.grid(row=1, column=0, columnspan=50, rowspan=15,sticky='NESW')

tab1 = Frame(tabControl)
tabControl.add(tab1,text='Gravity Current')

tab2 = Frame(tabControl)
tabControl.add(tab2,text='Calibration parameters')

tab3 = Frame(tabControl)
tabControl.add(tab3,text='Erodible bed')

tab4 = Frame(tabControl)
tabControl.add(tab4,text='Outputs and Run')


# ------------------- Tab: Gravity Current ------------------------------------

Label(tab1,anchor="w", text="Video (.mp4):").grid(row=2,column=0,pady=4,sticky='w')
Button(tab1,text='Open File',command=video_input).grid(row=2,column=1,pady=4,sticky='w')

Label(tab1, text="Temporal resolution (sec):    ").grid(row=3,column=0,pady=4,sticky='w')
dt = Entry(tab1, bd =3)
dt.insert(END,1)
dt.grid(row=3,column=1,pady=4)


tka.Separator(tab1, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=4, padx=10, pady=10, sticky='we')
Label(tab1,anchor="w",font="Verdana 8 bold", text="Experimental geometry and characteristic:",width=50).grid(row=5,column=0,pady=8,sticky='w')


Label(tab1, text="Ambient water density (kg/m³):             ").grid(row=6,column=0,pady=4,sticky='w')
rhoa = Entry(tab1, bd =3)
rhoa.insert(END,1000)
rhoa.grid(row=6,column=1,pady=4)

Label(tab1, text="Current water density (kg/m³):      ").grid(row=7,column=0,pady=4,sticky='w')
rhoc = Entry(tab1, bd =3)
rhoc.insert(END,1030)
rhoc.grid(row=7,column=1,pady=4)

Label(tab1, text="Horizontal length of the analyzed area (cm):      ").grid(row=8,column=0,pady=4,sticky='w')
L = Entry(tab1, bd =3)
L.insert(END,200)
L.grid(row=8,column=1,pady=4)

Label(tab1, text="Water depth + sediment thickness (cm):      ").grid(row=9,column=0,pady=4,sticky='w')
H = Entry(tab1, bd =3)
H.insert(END,20)
H.grid(row=9,column=1,pady=4)

Label(tab1, text="Initial current height (cm):      ").grid(row=10,column=0,pady=4,sticky='w')
Hc = Entry(tab1, bd =3)
Hc.insert(END,20)
Hc.grid(row=10,column=1,pady=4)

Label(tab1, text="Lock length (cm):      ").grid(row=11,column=0,pady=4,sticky='w')
Lo = Entry(tab1, bd =3)
Lo.insert(END,13)
Lo.grid(row=11,column=1,pady=4)

Label(tab1, text="Virtual length (cm):      ").grid(row=12,column=0,pady=4,sticky='w')
zuser = Entry(tab1, bd =3)
zuser.insert(END,0)
zuser.grid(row=12,column=1,pady=4)

Label(tab1, text="Kinematic viscosity of the denser fluid (m²/s):      ").grid(row=13,column=0,pady=4,sticky='w')
nu = Entry(tab1, bd =3)
nu.insert(END,0.00000115)
nu.grid(row=13,column=1,pady=4)

tka.Separator(tab1, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=14, padx=10, pady=10, sticky='we')
Label(tab1,anchor="w",font="Verdana 8 bold", text="Height of analysis:",width=50).grid(row=15,column=0,pady=8,sticky='w')


p1 = IntVar()
p2 = IntVar()
p3 = IntVar()

h1 = Checkbutton(tab1,text='Height 1 (cm)', variable=p1, onvalue=1, offvalue=0, command=selected_h1)
h2 = Checkbutton(tab1,text='Height 2 (cm)', variable=p2, onvalue=1, offvalue=0, command=selected_h2)
h3 = Checkbutton(tab1,text='Height 3 (cm)', variable=p3, onvalue=1, offvalue=0, command=selected_h3) 

h1.grid(row=16,column=0,pady=2,padx=100,sticky='w') 
h2.grid(row=17,column=0,pady=2,padx=100,sticky='w') 
h3.grid(row=18,column=0,pady=2,padx=100,sticky='w') 

ha = Entry(tab1, bd =3)
ha.grid(row=16,column=1)
ha.config(state='disable')

hb = Entry(tab1, bd =3)
hb.grid(row=17,column=1)
hb.config(state='disable')

hc = Entry(tab1, bd =3)
hc.grid(row=18,column=1)
hc.config(state='disable')

Label(tab1,anchor="w",font="Verdana 8 bold", text="Spectral analysis:",width=50).grid(row=19,column=0,pady=8,sticky='w')

Label(tab1, text="Window size (sec):      ").grid(row=20,column=0,pady=4,sticky='w')
size = Entry(tab1, bd =3)
size.insert(END,0)
size.grid(row=20,column=1,pady=4)

# ------------------- Tab: Calibration parameters -----------------------------

tka.Separator(tab2, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=0, padx=10, pady=10, sticky='we')
Label(tab2,anchor="w",font="Verdana 8 bold", text="Gravity current calibration parameters:",width=50).grid(row=1,column=0,pady=8,sticky='w')

Label(tab2, text="Minimum grayscale of current").grid(row=2,column=0,pady=4,sticky='w')
downcur = Entry(tab2, bd =3)
downcur.grid(row=2,column=1,pady=4)

Label(tab2, text="Maximum grayscale of current").grid(row=3,column=0,pady=4,sticky='w')
upcur = Entry(tab2, bd =3)
upcur.grid(row=3,column=1,pady=4)

Label(tab2, text="Density model:").grid(row=4,column=0,pady=4,padx=0,sticky='w')

density_model = ["Linear", "Potential"]
model = StringVar(tab2)
model.set(density_model[0])

model_options = OptionMenu(tab2,model,*density_model,command=coefficients)
model_options.grid(row=4,column=1,pady=4,sticky='w')

model_number = 0 # check if it is working

Label(tab2, text="Coefficeint A").grid(row=5,column=0,pady=4,sticky='w')
coefa = Entry(tab2, bd =3)
coefa.grid(row=5,column=1,pady=4)
coefa.config(state='disable')

Label(tab2, text="Coefficeint B").grid(row=6,column=0,pady=4,sticky='w')
coefb = Entry(tab2, bd =3)
coefb.grid(row=6,column=1,pady=4)
coefb.config(state='disable')

Label(tab2, text="Coefficeint C").grid(row=7,column=0,pady=4,sticky='w')
coefc = Entry(tab2, bd =3)
coefc.grid(row=7,column=1,pady=4)
coefc.config(state='disable')


tka.Separator(tab2, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=8, padx=10, pady=10, sticky='we')
Label(tab2,anchor="w",font="Verdana 8 bold", text="PIV calibration parameters:",width=50).grid(row=9,column=0,pady=8,sticky='w')

piv_analyzer= IntVar()
Checkbutton(tab2,font="Verdana 8",text='PIV measurements', variable=piv_analyzer, onvalue=1, offvalue=0, command=selected_piv).grid(row=10,column=0,pady=4,sticky='w') 
piv_analyzer.set(0)



Label(tab2, text="Window size (pixels)").grid(row=11,column=0,pady=4,sticky='w')
winsize = Entry(tab2, bd =3)
winsize.grid(row=11,column=1,pady=4)
winsize.config(state='disable')

Label(tab2, text="Search area (pixels)").grid(row=12,column=0,pady=4,sticky='w')
searea = Entry(tab2, bd =3)
searea.grid(row=12,column=1,pady=4)
searea.config(state='disable')


Label(tab2, text="Overlap (pixels)").grid(row=13,column=0,pady=4,sticky='w')
overlap = Entry(tab2, bd =3)
overlap.grid(row=13,column=1,pady=4)
overlap.config(state='disable')

Label(tab2, text="Noise ratio threshold").grid(row=14,column=0,pady=4,sticky='w')
thold = Entry(tab2, bd =3)
thold.grid(row=14,column=1,pady=4)
thold.config(state='disable')

Label(tab2, text="Number of iterations").grid(row=15,column=0,pady=4,sticky='w')
intera = Entry(tab2, bd =3)
intera.grid(row=15,column=1,pady=4)
intera.config(state='disable')

Label(tab2, text="Kernel size").grid(row=16,column=0,pady=4,sticky='w')
kernel = Entry(tab2, bd =3)
kernel.grid(row=16,column=1,pady=4)
kernel.config(state='disable')


Label(tab2, text="Maximum value").grid(row=17,column=0,pady=4,sticky='w')
maxVal = Entry(tab2, bd =3)
maxVal.grid(row=17,column=1,pady=4)
maxVal.config(state='disable')

Label(tab2, text="Block size").grid(row=18,column=0,pady=4,sticky='w')
block = Entry(tab2, bd =3)
block.grid(row=18,column=1,pady=4)
block.config(state='disable')

Label(tab2, text="Weighted average constant").grid(row=19,column=0,pady=4,sticky='w')
const = Entry(tab2, bd =3)
const.grid(row=19,column=1,pady=4)
const.config(state='disable')

# ------------------- Tab: Erodible Bed ---------------------------------------

sed_button= IntVar()
sed = Checkbutton(tab3,font="Verdana 8 bold",text='Erodible bed analysis', variable=sed_button, onvalue=1, offvalue=0, command=selected_sed).grid(row=1,column=0,pady=4,sticky='w') 
sed_button.set(0)

Label(tab3, text="Erodible bed thickness (cm):             ").grid(row=2,column=0,pady=4,sticky='w')
Hsed = Entry(tab3, bd =3)
Hsed.grid(row=2,column=1,pady=4)
Hsed.config(state='disable')


tka.Separator(tab3, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=3, padx=10, pady=10, sticky='we')
Label(tab3,anchor="w",font="Verdana 8 bold", text="Erodible bed calibration parameters:",width=50).grid(row=4,column=0,pady=8,sticky='w')


Label(tab3, text="Maximum grayscale for sediment particles").grid(row=5,column=0,pady=4,sticky='w')
upsed = Entry(tab3, bd =3)
upsed.grid(row=5,column=1,pady=4)
upsed.config(state='disable')

Label(tab3, text="Minimum grayscale for sediment particles").grid(row=6,column=0,pady=4,sticky='w')
downsed = Entry(tab3, bd =3)
downsed.grid(row=6,column=1,pady=4)
downsed.config(state='disable')

# ------------------- Tab: Output ---------------------------------------------

Label(tab4,anchor="w", text="Output folder:").grid(row=1,column=0,pady=4,sticky='w')
Button(tab4,text='Open File',command=output_folder).grid(row=1,column=1,pady=4,sticky='w')

Label(tab4,anchor="w",font="Verdana 8 bold", text="Images Outputs:",width=50).grid(row=3,column=0,pady=8,sticky='w')

png_frame= IntVar()
Checkbutton(tab4,font="Verdana 8 ",text='Video Frames', variable=png_frame, onvalue=1, offvalue=0).grid(row=4,column=0,pady=4,sticky='w') 
png_frame.set(0)

png_current= IntVar()
Checkbutton(tab4,font="Verdana 8 ",text='Gravity current', variable=png_current, onvalue=1, offvalue=0).grid(row=5,column=0,pady=4,sticky='w') 
png_current.set(0)

png_thorpe= IntVar()
Checkbutton(tab4,font="Verdana 8 ",text='Thorpe scale', variable=png_thorpe, onvalue=1, offvalue=0).grid(row=6,column=0,pady=4,sticky='w') 
png_thorpe.set(0)


png_varia= IntVar()
varia_sel = Checkbutton(tab4,font="Verdana 8 ",text='Sediment variation', variable=png_varia,  onvalue=1, offvalue=0)
varia_sel.grid(row=7,column=0,pady=4,sticky='w') 
varia_sel.config(state='disable')

png_motion= IntVar()
motion_sel = Checkbutton(tab4,font="Verdana 8",text='Sediment transport', variable=png_motion,  onvalue=1, offvalue=0)
motion_sel.grid(row=8,column=0,pady=4,sticky='w') 
motion_sel.config(state='disable')

png_piv= IntVar()
piv_sel = Checkbutton(tab4,font="Verdana 8 ",text='PIV', variable=png_piv,  onvalue=1, offvalue=0)
piv_sel.grid(row=9,column=0,pady=4,sticky='w') 
piv_sel.config(state='disable')

Label(tab4,anchor="w",font="Verdana 8 bold", text="Textfiles Outputs:",width=50).grid(row=10,column=0,pady=8,sticky='w')

txt_current= IntVar()
Checkbutton(tab4,font="Verdana 8 ",text='Gravity current', variable=txt_current, onvalue=1, offvalue=0).grid(row=11,column=0,pady=4,sticky='w') 
txt_current.set(0)

txt_thorpe= IntVar()
Checkbutton(tab4,font="Verdana 8 ",text='Thorpe scale', variable=txt_thorpe, onvalue=1, offvalue=0).grid(row=12,column=0,pady=4,sticky='w') 
txt_thorpe.set(0)


txt_varia= IntVar()
varia_seltxt = Checkbutton(tab4,font="Verdana 8 ",text='Sediment variation', variable=txt_varia,  onvalue=1, offvalue=0)
varia_seltxt.grid(row=13,column=0,pady=4,sticky='w') 
varia_seltxt.config(state='disable')

txt_motion= IntVar()
motion_seltxt = Checkbutton(tab4,font="Verdana 8",text='Sediment transport', variable=txt_motion,  onvalue=1, offvalue=0)
motion_seltxt.grid(row=14,column=0,pady=4,sticky='w') 
motion_seltxt.config(state='disable')

txt_piv= IntVar()
piv_seltxt = Checkbutton(tab4,font="Verdana 8 ",text='PIV', variable=txt_piv,  onvalue=1, offvalue=0)
piv_seltxt.grid(row=15,column=0,pady=4,sticky='w') 
piv_seltxt.config(state='disable')


Label(tab4, font="Verdana 8 bold", text="Figures quality (DPI)").grid(row=17,column=0,pady=4,sticky='w')
fdpi = Entry(tab4, bd =3)
fdpi.insert(END,100)
fdpi.grid(row=17,column=1,pady=4)




Button(tab4,font="Verdana 10 bold",text='Run',command=export_data, height = 2, width = 20).grid(row=19,column=0,pady=8,sticky='w')



window.config(menu = menubar)
window.mainloop()