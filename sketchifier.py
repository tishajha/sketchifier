import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('500x500')
top.title('Sketchify Your Image !')
top.configure(background='skyblue')
label=Label(top,background='black', font=('arial',20,'bold'))

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)

def dodgev2(x,y):
    return cv2.divide(x,255-y,scale=256)

def cartoonify(ImagePath):
    # read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized0 = cv2.resize(originalmage, (960, 540))
    #plt.imshow(ReSized1, cmap='gray')


    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized1 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')


    #applying median blur to smoothen an image
    img_invert = cv2.bitwise_not(grayScaleImage)#cv2.medianBlur(grayScaleImage, 5)
    ReSized2 = cv2.resize(img_invert, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    smoothGrayScale = cv2.GaussianBlur(img_invert,(21,21),sigmaX=0,sigmaY=0);

    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized4, cmap='gray')

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    finalImage = dodgev2(grayScaleImage,smoothGrayScale)
    ReSized4 = cv2.resize(finalImage, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')


    # Plotting the whole transition
    images=[ReSized1, ReSized2, ReSized3, ReSized4,ReSized0,ReSized4]

    fig, axes = plt.subplots(3,2, figsize=(10,10), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save sketch image",command=lambda: save(ReSized4, ImagePath),padx=40,pady=10)
    save1.configure(background='orange', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
    
def save(ReSized4, ImagePath):
    #saving an image using imwrite()
    newName="sketchified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized4, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(top,text="Sketchify an Image",command=upload,padx=10,pady=15)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=70)

top.mainloop()



