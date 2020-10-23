# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:38:12 2019

@author: Rafael de Carvalho Bueno
"""

import webbrowser

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
        
        data.write(str(piv_analyzer.get())+'\n')
        
        if int(piv_analyzer.get()) == 0:
            data.write(str(999)+'\n')
            data.write(str(999)+'\n')        
        else:
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
                piv_analyzer.set(0)
                piv_seltxt.config(state='disable')
                next(reader)
                piv_sel.config(state='disable')
                next(reader)                       
            else:
                piv_analyzer.set(1)
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
                Hsed.insert(END,float(reader.readline()))  
                upsed.config(state='normal')
                upsed.insert(END,float(reader.readline())) 
                downsed.config(state='normal')
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


                
def calibration_current():
    
    global iccur
    path_ic = askopenfilename(defaultextension='.mp4', filetypes=[('MP4 files','*.mp4')]) 
    pathout = filedialog.askdirectory()
    calibri.cal_current(path_ic,pathout)
    
    

    
def AboutCallBack():
   msg = messagebox.showinfo( "About", " Dyenamic - Beta Version \n Copyright (C) 2019 Rafael de Carvalho Bueno \n All rights reserved \n \n Developer: Rafael de Carvalho Bueno \n Supervisor: Tobias Bleninger \n Testers: Nathan Streisky da Silva\n André Diniz dos Santos \n \n \n Report problems and improvements to email adresss below \n rafael.bueno@ufpr.br\n \n for mor information, see: \n https://sites.google.com/view/rafaelbueno/programs \n ")    


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

        
    elif int(piv_analyzer.get()) == 1: 
        piv_sel.config(state='normal')
        piv_seltxt.config(state='normal')
          
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
window.iconbitmap("./dyenamic-icon.ico")

window.title("Dyenamic") 
window.geometry('800x800')

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
tabControl.add(tab2,text='Erodible bed')

tab3 = Frame(tabControl)
tabControl.add(tab3,text='Outputs and Run')


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
L.insert(END,40)
L.grid(row=8,column=1,pady=4)

info = Label(tab1, text="Water depth + sediment thickness (cm):      ").grid(row=9,column=0,pady=4,sticky='w')
H = Entry(tab1, bd =3)
H.insert(END,22)
H.grid(row=9,column=1,pady=4)

tka.Separator(tab1, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=10, padx=10, pady=10, sticky='we')
Label(tab1,anchor="w",font="Verdana 8 bold", text="Height of analysis:",width=50).grid(row=11,column=0,pady=8,sticky='w')


p1 = IntVar()
p2 = IntVar()
p3 = IntVar()

h1 = Checkbutton(tab1,text='Height 1 (cm)', variable=p1, onvalue=1, offvalue=0, command=selected_h1)
h2 = Checkbutton(tab1,text='Height 2 (cm)', variable=p2, onvalue=1, offvalue=0, command=selected_h2)
h3 = Checkbutton(tab1,text='Height 3 (cm)', variable=p3, onvalue=1, offvalue=0, command=selected_h3) 

h1.grid(row=12,column=0,pady=2,padx=100,sticky='w') 
h2.grid(row=13,column=0,pady=2,padx=100,sticky='w') 
h3.grid(row=14,column=0,pady=2,padx=100,sticky='w') 

ha = Entry(tab1, bd =3)
ha.grid(row=12,column=1)
ha.config(state='disable')

hb = Entry(tab1, bd =3)
hb.grid(row=13,column=1)
hb.config(state='disable')

hc = Entry(tab1, bd =3)
hc.grid(row=14,column=1)
hc.config(state='disable')

tka.Separator(tab1, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=15, padx=10, pady=10, sticky='we')
Label(tab1,anchor="w",font="Verdana 8 bold", text="Gravity current calibration parameters:",width=50).grid(row=16,column=0,pady=8,sticky='w')

Label(tab1, text="Minimum grayscale of current").grid(row=17,column=0,pady=4,sticky='w')
downcur = Entry(tab1, bd =3)
downcur.grid(row=17,column=1,pady=4)

Label(tab1, text="Maximum grayscale of current").grid(row=18,column=0,pady=4,sticky='w')
upcur = Entry(tab1, bd =3)
upcur.grid(row=18,column=1,pady=4)

piv_analyzer= IntVar()
Checkbutton(tab1,font="Verdana 8",text='PIV analyzer', variable=piv_analyzer, onvalue=1, offvalue=0, command=selected_piv).grid(row=21,column=0,pady=4,sticky='w') 
piv_analyzer.set(0)



# ------------------- Tab: Erodible Bed ---------------------------------------

sed_button= IntVar()
sed = Checkbutton(tab2,font="Verdana 8 bold",text='Erodible bed analysis', variable=sed_button, onvalue=1, offvalue=0, command=selected_sed).grid(row=1,column=0,pady=4,sticky='w') 
sed_button.set(0)

Label(tab2, text="Erodible bed thickness (cm):             ").grid(row=2,column=0,pady=4,sticky='w')
Hsed = Entry(tab2, bd =3, )
Hsed.grid(row=2,column=1,pady=4)
Hsed.config(state='disable')


tka.Separator(tab2, orient=HORIZONTAL).grid(column=0, columnspan= 4, row=3, padx=10, pady=10, sticky='we')
Label(tab2,anchor="w",font="Verdana 8 bold", text="Erodible bed calibration parameters:",width=50).grid(row=4,column=0,pady=8,sticky='w')


Label(tab2, text="Maximum grayscale for sediment particles").grid(row=5,column=0,pady=4,sticky='w')
upsed = Entry(tab2, bd =3)
upsed.grid(row=5,column=1,pady=4)
upsed.config(state='disable')

Label(tab2, text="Minimum grayscale for sediment particles").grid(row=6,column=0,pady=4,sticky='w')
downsed = Entry(tab2, bd =3)
downsed.grid(row=6,column=1,pady=4)
downsed.config(state='disable')

# ------------------- Tab: Output ---------------------------------------------

Label(tab3,anchor="w", text="Output folder:").grid(row=1,column=0,pady=4,sticky='w')
Button(tab3,text='Open File',command=output_folder).grid(row=1,column=1,pady=4,sticky='w')

Label(tab3,anchor="w",font="Verdana 8 bold", text="Images Outputs:",width=50).grid(row=3,column=0,pady=8,sticky='w')

png_frame= IntVar()
Checkbutton(tab3,font="Verdana 8 ",text='Video Frames', variable=png_frame, onvalue=1, offvalue=0).grid(row=4,column=0,pady=4,sticky='w') 
png_frame.set(0)

png_current= IntVar()
Checkbutton(tab3,font="Verdana 8 ",text='Gravity current', variable=png_current, onvalue=1, offvalue=0).grid(row=5,column=0,pady=4,sticky='w') 
png_current.set(0)

png_thorpe= IntVar()
Checkbutton(tab3,font="Verdana 8 ",text='Thorpe scale', variable=png_thorpe, onvalue=1, offvalue=0).grid(row=6,column=0,pady=4,sticky='w') 
png_thorpe.set(0)


png_varia= IntVar()
varia_sel = Checkbutton(tab3,font="Verdana 8 ",text='Sediment variation', variable=png_varia,  onvalue=1, offvalue=0)
varia_sel.grid(row=7,column=0,pady=4,sticky='w') 
varia_sel.config(state='disable')

png_motion= IntVar()
motion_sel = Checkbutton(tab3,font="Verdana 8",text='Sediment transport', variable=png_motion,  onvalue=1, offvalue=0)
motion_sel.grid(row=8,column=0,pady=4,sticky='w') 
motion_sel.config(state='disable')

png_piv= IntVar()
piv_sel = Checkbutton(tab3,font="Verdana 8 ",text='PIV', variable=png_piv,  onvalue=1, offvalue=0)
piv_sel.grid(row=9,column=0,pady=4,sticky='w') 
piv_sel.config(state='disable')

Label(tab3,anchor="w",font="Verdana 8 bold", text="Textfiles Outputs:",width=50).grid(row=10,column=0,pady=8,sticky='w')

txt_current= IntVar()
Checkbutton(tab3,font="Verdana 8 ",text='Gravity current', variable=txt_current, onvalue=1, offvalue=0).grid(row=11,column=0,pady=4,sticky='w') 
txt_current.set(0)

txt_thorpe= IntVar()
Checkbutton(tab3,font="Verdana 8 ",text='Thorpe scale', variable=txt_thorpe, onvalue=1, offvalue=0).grid(row=12,column=0,pady=4,sticky='w') 
txt_thorpe.set(0)


txt_varia= IntVar()
varia_seltxt = Checkbutton(tab3,font="Verdana 8 ",text='Sediment variation', variable=txt_varia,  onvalue=1, offvalue=0)
varia_seltxt.grid(row=13,column=0,pady=4,sticky='w') 
varia_seltxt.config(state='disable')

txt_motion= IntVar()
motion_seltxt = Checkbutton(tab3,font="Verdana 8",text='Sediment transport', variable=txt_motion,  onvalue=1, offvalue=0)
motion_seltxt.grid(row=14,column=0,pady=4,sticky='w') 
motion_seltxt.config(state='disable')

txt_piv= IntVar()
piv_seltxt = Checkbutton(tab3,font="Verdana 8 ",text='PIV', variable=txt_piv,  onvalue=1, offvalue=0)
piv_seltxt.grid(row=15,column=0,pady=4,sticky='w') 
piv_seltxt.config(state='disable')


Button(tab3,font="Verdana 10 bold",text='Run',command=export_data, height = 2, width = 20).grid(row=17,column=0,pady=8,sticky='w')



window.config(menu = menubar)
window.mainloop()