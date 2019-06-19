import numpy as np
import matplotlib.pyplot as plt
import imageio as iio
from scipy.signal import convolve
from math import *
import cv2
import math
import cv2

def main():
    file = str(input("File location:")).rstrip()
    image = iio.imread(file)
    plt.figure("Original image")
    plt.imshow(image,cmap="gray")
    image1 = Luminance(image)
    plt.figure("Gray level image")
    plt.imshow(image1,cmap="gray")
    image2 = convolve(image1,gaussian_filter(5),'valid')
    plt.figure("Removing noise")
    plt.imshow(image2,cmap="gray")
    image3 = Sobel(image2)
    image3 = normalize(image3,255,image3.max(),image3.min())
    plt.figure("Edges")
    plt.imshow(image3,cmap="gray")
    image4 = findEdges(image3,128)
    plt.figure("Threshhold filter")
    plt.imshow(image4,cmap="gray")
    image5 = HoughTransform(image4,70.0,110.0)
    image6 = HoughTransform(image4,-20.0,20.0)
    image7 = image5+image6
    # edges = getQuadrangle(image7)
    plt.figure("Hough Transform")
    plt.imshow(np.where(image7!=0,255,0),cmap="gray")
    plt.figure("Distortion Correction")
    image8 = distortionCorrection(image,np.array(((102,128),(532,110),(553,428),(100,404))))
    plt.imshow(image8)
    plt.show()
def Luminance(image):
    return 0.299*image[:,:,0]+0.587*image[:,:,1]+0.114*image[:,:,2]
def findEdges(image,tH=15):
    image = np.where(image >= tH, 1,0)
    return image
def gaussian_filter(k=3,sigma=1.0):
    arx = np.arange((-k//2)+1.0,(k//2)+1.0)
    x,y = np.meshgrid(arx,arx)
    filt = np.exp(-(1/2)*(np.square(x)+np.square(y))/np.square(sigma))
    return filt/np.sum(filt)
def Sobel(image):
    vertical = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    horizontal = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    diagonal1 = np.array([[0,1,2],[-1,0,1],[-2,-1,0]])
    diagonal2 = np.array([[-2,-1,0],[-1,0,1],[0,1,2]])
    return convolve(image,vertical,'valid')+convolve(image,horizontal,'valid')#+convolve(image,diagonal1,'valid')+convolve(image,diagonal2,'valid')
def HoughTransform(img,minAngle=-90.0,maxAngle=90.0):
    M,N =  img.shape
    dist_max = ceil(sqrt(M*M+N*N))
    theta = np.deg2rad(np.arange(minAngle,maxAngle))
    # dists = np.linspace(-dist_max,dist_max,dist_max*2)
    hough = np.zeros((dist_max*2,len(theta)))
    x,y = np.nonzero(img)
    points = [[list()] * len(theta) for i in range(dist_max*2)]
    newImage = np.zeros((img.shape))

    c = np.cos(theta)
    s = np.sin(theta)
    aa = dist_max*2
    for i in range(len(x)):
        xa = x[i]
        ya = y[i]
        for t in range(len(theta)):
            rho = int(round(xa*c[t] + ya*s[t]))+dist_max
            if(rho < aa):
                hough[rho,t] += 1
                points[rho][t].append((xa,ya))
    max = maxPoints(hough)
    for x in range(dist_max*2):
        for y in range(len(theta)):
            if(hough[x][y] in max):
                for z in points[x][y]:
                    newImage[z[0]][z[1]] = 255
    return newImage
def maxPoints(hough, n=5):
    flat = hough.flatten()
    flat = np.flip(np.sort(flat))

    max = []
    for i in range(n):
        max.append(flat[0])
        idx = np.argwhere(flat==flat[0])
        flat = np.delete(flat, idx)

    return max
def getQuadrangle(img):
    img = np.where(img > 0, 1, 0).astype('uint8')
    img, contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
def distortionCorrection(img,corners):
    M,N,_ = img.shape
    aux,b = cv2.findHomography(corners,np.array(((0,0),(N,0),(N,M),(0,M))))
    return cv2.warpPerspective(img,aux,(N,M))
def normalize(img,newMax,max,min=0):
    return newMax*((img-min)/(max-min))
if(__name__=="__main__"):
    main()
