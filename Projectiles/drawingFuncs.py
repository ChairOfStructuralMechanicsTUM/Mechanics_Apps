from scipy import ndimage
import os.path
import numpy as np
from math import ceil, floor, cos, sin
from bokeh.models import ColumnDataSource

cannon_orig_image = [[]]
cannon_size = []
base_data = ColumnDataSource(data = dict(image=[],xS=[],yS=[],h=[],w=[]))
cannon_data = ColumnDataSource(data = dict(image=[],xS=[],yS=[],h=[],w=[]))
monkey_data = ColumnDataSource(data = dict(image=[],xS=[],yS=[],h=[],w=[]))
banana_data = ColumnDataSource(data = dict(image=[],xS=[],yS=[],h=[],w=[]))
height = 0

# transform saved image to a bokeh readable format
def convertForBokeh(img):
    # bokeh reads a 2D array. If we have a 3D array
    # (usually the case {1st dim = x, 2nd dim = y, 3rd dim  = rgba})
    # then reorganise it so bokeh can read it
    if img.ndim > 2:
        if img.shape[2] == 3:
            # if the 3rd dimension only contains 3 elements (rgb),
            # then add opacity (assumed to be fully opaque)
            # dstack adds values at deepest levels in img
            # Values added are 255*matrix(with necessary size)
            img = np.dstack([img, np.ones(img.shape[:2], np.uint8) * 255])
        # view transforms 4 8bit integers into 1 32bit integer (8*4=32)
        # i.e. 4 2bit integers to 1 8bit integer would be:
        # [0 1 2 3] == [00 01 10 11] => [00011011] = [27]
        # squeeze removes 1D arrays, i.e. : 
        # [[1], [2], [3], [4]] becomes [1, 2, 3, 4]
        img = np.squeeze(img.view(np.uint32))
    # thus we have a 2D array in bokeh readable format which can be returned
    return img

## Drawing functions
# all are very similar but must be distinct to define column data sources
def drawBase(p):
    # find path to file
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "Images/base.png")
    # upload file
    img = ndimage.imread(filename)
    # convert file to bokeh readable image
    img = convertForBokeh(img)
    # save information to ColumnDataSource
    global base_data
    # bokeh reads in the opposite direction to scipy so -1 corrects this
    base_data.data=dict(image=[img[::-1,:]], xS=[0],yS=[0],w=[10],h=[10])
    # render image
    p.image_rgba(image='image', x='xS', y='yS',dw='w',dh='h',source=base_data,level='annotation')
    
def drawBranch(p):
    # find path to file
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "Images/branch.png")
    # upload file
    img = ndimage.imread(filename)
    # convert file to bokeh readable image
    img = convertForBokeh(img)
    # render image
    # bokeh reads in the opposite direction to scipy so -1 corrects this
    p.image_rgba(image=[img[::-1,:]], x=[150], y=[70],dw=[50],dh=[25],level='annotation')

def drawBanana(p):
    # find path to file
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "Images/banana.png")
    # upload file
    img = ndimage.imread(filename)
    # convert file to bokeh readable image
    img = convertForBokeh(img)
    # save information to ColumnDataSource
    global banana_data
    # bokeh reads in the opposite direction to scipy so -1 corrects this
    banana_data.data=dict(image=[img[::-1,:]], xS=[8],yS=[10],w=[5],h=[5])
    # render image
    p.image_rgba(image='image', x='xS', y='yS',dw='w',dh='h',source=banana_data,level='annotation')

def drawMonkey(p):
    # find path to file
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "Images/monkey.png")
    # upload file
    img = ndimage.imread(filename)
    # convert file to bokeh readable image
    img = convertForBokeh(img)
    # save information to ColumnDataSource
    global monkey_data
    # bokeh reads in the opposite direction to scipy so -1 corrects this
    monkey_data.data=dict(image=[img[::-1,:]], xS=[180],yS=[70],w=[20],h=[20])
    # render image
    p.image_rgba(image='image', x='xS', y='yS',dw='w',dh='h',source=monkey_data,level='annotation')

def drawCannon(p):
    # find path to file
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "Images/cannon.png")
    # upload file
    img = ndimage.imread(filename)
    # convert file to bokeh readable image
    img = convertForBokeh(img)
    # pad image so rotation can occur within frame
    size=img.shape
    size=[int(ceil(size[0]/4.0)),int(ceil(size[1]/4.0))]
    img = np.lib.pad(img,((size[0],size[0]),(size[1],size[1])),'constant',constant_values=(0))
    # save information to ColumnDataSource and other variables for rotation later
    global cannon_data, cannon_orig_image, cannon_size
    cannon_orig_image = img
    cannon_size = img.shape
    # bokeh reads in the opposite direction to scipy so -1 corrects this
    cannon_data.data=dict(image = [img[::-1,:]], xS=[0.3], yS=[0.5],h=[15],w=[15])
    # render image
    p.image_rgba(image='image', x='xS', y='yS',dh='h',dw='w',source=cannon_data,level='annotation')

## image modifying functions to give monkey that holds onto branch or not and lives in space or not
# draw monkey not holding onto branch
def monkeyLetGo(space = False):
    global monkey_data
    # find path to file
    dir = os.path.dirname(__file__)
    if (space):
        filename = os.path.join(dir, "Images/spaceMonkeyLetGo.png")
    else:
        filename = os.path.join(dir, "Images/monkeyLetGo.png")
    # upload file
    img = ndimage.imread(filename)
    # convert file to bokeh readable image
    img = convertForBokeh(img)
    # update ColumnDataSource
    monkey_data.data=dict(image=[img[::-1,:]],xS=[180],yS=[70],w=[20],h=[20])

def monkeyGrab(space = False):
    global monkey_data
    # find path to file
    dir = os.path.dirname(__file__)
    if (space):
        filename = os.path.join(dir, "Images/spaceMonkey.png")
    else:
        filename = os.path.join(dir, "Images/monkey.png")
    # upload file
    img = ndimage.imread(filename)
    # convert file to bokeh readable image
    img = convertForBokeh(img)
    # update ColumnDataSource
    monkey_data.data=dict(image=[img[::-1,:]],xS=[180],yS=[70],w=[20],h=[20])

## rotation of cannon
def rotateCannon(angle):
    global cannon_orig_image, cannon_size
    # find points (in image coordinates) about which the image is rotated
    aboutX=4.7*cannon_size[0]/15.0
    aboutY=7.5*cannon_size[1]/15.0
    # rearrange 2D matrix into 3D matrix by splitting each 32bit int into 4 8bit ints
    # this makes it easier to access values
    img = cannon_orig_image.view(np.uint8).reshape(cannon_size[0],cannon_size[1],4)
    # create new blank image
    new_img = np.zeros(img.shape,dtype=np.uint8)
    # cos(theta) and sin(theta) do not vary over loop so they are calculated in advance
    cosTheta=cos(angle)
    sinTheta=sin(angle)
    # fill new_img with rotated img
    for i in range(0,cannon_size[0]):
        Y=i-aboutY
        for j in range(0,cannon_size[1]):
            X=j-aboutX
            if (img[i,j,3]!=0):
                # find new coordinates
                Xcoord = aboutY+X*sinTheta+Y*cosTheta
                Ycoord = aboutX+X*cosTheta-Y*sinTheta
                # not all pixels are necessarily covered so filling 2 pixels prevents holes
                # appearing in the image (up to theta=65)
                if (new_img[int(floor(Xcoord)),int(floor(Ycoord)),3]==0):
                    new_img[int(floor(Xcoord)),int(floor(Ycoord)),:]=img[i,j,:]
                if (new_img[int(ceil(Xcoord)),int(ceil(Ycoord)),3]==0):
                    new_img[int(ceil(Xcoord)),int(ceil(Ycoord)),:]=img[i,j,:]
    # convert new_img into bokeh readable format
    new_img=np.squeeze(new_img.view(np.uint32))
    # update ColumnDataSource
    cannon_data.data=dict(image = [new_img[::-1,:]], xS=[0.3], yS=[0.5+height],h=[15],w=[15])

## functions which move objects
def moveBanana((x,y) = (0,0)):
    # default values are in cannon
    if ((x,y)==(0,0)):
        (x,y)=(8,10+height)
    global banana_data
    # modify the position
    newData=dict(banana_data.data)
    newData['xS']=[x]
    newData['yS']=[y]
    # update ColumnDataSource
    banana_data.data=newData
    return (x,y)

def moveMonkey(y = 0):
    global monkey_data
    # modify the position
    newData=dict(monkey_data.data)
    newData['yS']=[70+y]
    # update ColumnDataSource
    monkey_data.data=newData
    return (180,70+y)

def modifyHeight(h):
    global height, base_data, cannon_data
    height=h
    # modify the position of the cannon base
    newData=dict(base_data.data)
    newData['yS']=[h]
    base_data.data=newData
    # modify the position of the cannon
    newData=dict(cannon_data.data)
    newData['yS']=[h+0.5]
    cannon_data.data=newData
    # modify the position of the banana
    moveBanana((8,10+height))
