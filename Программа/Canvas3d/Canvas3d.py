# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 09:49:24 2020

@author: dgregoriev

This is a UI module meant to handle transforms to display
geometry content on the Canvas widget

"""
 
try:
    #if python 2.7 is used this will work
    import Tkinter as tk
except ModuleNotFoundError:
    #this means its a 3.x interpreter
    import tkinter as tk
    import tkinter.ttk as ttk

from . import Point as pt
import math
from . import Matrix3d as m3
from . import Coord as cord
from . import Curve as curv


class ViewingPlane():
    '''
    This is a model coordinate system object that represents the
    model coordinate system plane to which the model location data
    will be projected for a view
    '''
    def __init__(self):
        '''
        model coord0
        view rotation
        view translate (move)
        view scale (zoom)
        view center offset (centerpt)
        '''
        self.vcord0 = cord.Coord.coordsDepot.objDict[0]
        self.vtranslate = cord.CoordRect(id=None,base=self.vcord0,parent=self.vcord0)
        self.vrotate = cord.CoordRect(id=None,base=self.vtranslate,parent=self.vtranslate)
        self.vscale = cord.CoordRect(id=None,base=self.vrotate,parent=self.vrotate)
        self.vieweroff = cord.CoordRect(id=None,base=self.vscale,parent=self.vscale)
        self.vscale.scale_coordsys(2)
            
    def screenresized(screenw, screenh):
        '''
        This takes the width and height of the screen and adjusts
        the vieweroff to center the 0,0 point
        '''
        pass

class UIpoint():
    '''
    This class represents the UI point that's drawn to the screen
    
    '''
    def __init__(self,pointtomirror,canvasobj):
    
        #.create_oval(10, 10, 80, 80, outline="#f11",
        #                   fill="#1f1", width=2)
        self.canvasobj = canvasobj
        self.view = self.canvasobj.viewer
        self.refpoint = pointtomirror
        self.style = pointtomirror.style
        #create a second point that is a screen projected version
        self.scrnpt = self.refpoint.in_coordsys(targetcoord = self.view.vieweroff)
        self.visible = True
        self.refresh()
        
    def refresh(self):
        '''
        This function forces the screenpoint to refresh
        '''
        #get the proper size of the pt
        ptscrnsize = m3.Vector3d(self.style.globradius,0,0)
        print(ptscrnsize)
        ptscrnsize = self.view.vscale.getTransToGlob().inv()*ptscrnsize
        ptscrnsize = self.view.vrotate.getTransToGlob()*ptscrnsize
        print(ptscrnsize)
        ptscrnsize = math.sqrt((ptscrnsize.T()*ptscrnsize).matrix[0][0]-1)
        print(ptscrnsize)
        self.scrnpt = self.refpoint.in_coordsys(self.view.vieweroff)
        
        leftedge = self.scrnpt.matrix[0][0]-ptscrnsize
        topedge = self.scrnpt.matrix[1][0]-ptscrnsize
        rightedge = self.scrnpt.matrix[0][0]+ptscrnsize
        bottomedge = self.scrnpt.matrix[1][0]+ptscrnsize
        #print(str(leftedge)+' '+str(topedge)+' '+str(rightedge)+' '+str(bottomedge))
        self.canvasobj.create_oval(leftedge, topedge, rightedge, bottomedge, 
                           outline=self.style.outline, fill=self.style.fill, 
                           width=self.style.outlinethkness)

class UIline():
    '''
    This class represents the UI line that's drawn to the screen
    '''
    def __init__(self,linetomirror,canvasobj):
        #.create_oval(10, 10, 80, 80, outline="#f11",
        #                   fill="#1f1", width=2)
        self.canvasobj = canvasobj
        self.view = self.canvasobj.viewer
        self.refline = linetomirror
        self.style = linetomirror.style
        #create a second line that is a screen projected version
        self.scrnline = self.refline.in_coordsys(targetcoord = self.view.vieweroff)
        self.visible = True
        self.refresh()
        
    def refresh(self):
        '''
        This function forces the screenline to refresh
        '''
        pt0 = self.scrnline.pts[0]
        pt0xy = (pt0.matrix[0][0],pt0.matrix[1][0])
        pt1 = self.scrnline.pts[1]
        pt1xy = (pt1.matrix[0][0],pt1.matrix[1][0])
        self.canvasobj.create_line(pt0xy[0],pt0xy[1],pt1xy[0],pt1xy[1], 
                                   width=self.style.width, fill=self.style.fill
                                   , capstyle=self.style.capstyle)
        

class Canvas3d(tk.Canvas):
    '''
    This class is meant to be able to receive global data and
    convert that to canvas data able to be viewed on the screen.
    The goal is that any needed conversion to display is hidden
    '''
    def __init__(self,parent,**kwargs):
        
        
        #first extract the canvas width and height from the arguments
        self.width = 200
        self.height = 200
        super().__init__(master=parent,**kwargs)
        

        self.uipointlist = []
                
        
        self.pointlist = []
        
        self.viewer = ViewingPlane()
        
        self.centerview()
        #self.viewer.vtranslate.translate_coordsys(0,-100,-1)
        self.viewer.vrotate.rotate_k_coordsys(math.pi/4)
        self.viewer.vrotate.rotate_i_coordsys(math.pi/4)
        #self.viewer.vscale.scale_coordsys(3)
        
        
        topleft = pt.Point(0,0,0)
        topright = pt.Point(50,0,0)
        bottomright = pt.Point(50,-50,0)
        bottomleft = pt.Point(0,-50,0)
        
        
        line0 = curv.Line(topleft,topright)
        scrnline0 = UIline(line0,self)
        line1 = curv.Line(topright,bottomright)
        scrnline1 = UIline(line1,self)
        line2 = curv.Line(bottomright,bottomleft)
        scrnline2 = UIline(line2,self)
        line3 = curv.Line(bottomleft,topleft)
        scrnline3 = UIline(line3,self)
        
        
        scrnpt0 = UIpoint(topleft,self)
        '''
        scrnpt1 = UIpoint(topright,self)
        scrnpt2 = UIpoint(bottomright,self)
        scrnpt3 = UIpoint(bottomleft,self)
        '''
        
        
        
    def redraw(self):
        '''
        This function dumps the view and redraws the full screen
        
        '''
        pass
        
    def centerview(self):
        '''
        This centers the view on the 0,0,0 point, resetting the viewer offset
        '''
        self.update()
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        #reset any camera moves
        self.viewer.vtranslate.own_exp_to_coord0list = []
        #since screen coords have +y facing down, we spin the coord sys
        self.viewer.vtranslate.rotate_i_coordsys(math.pi)#spin the coord sys
        xtranslate = self.width/2
        ytranslate = self.height/2
        self.viewer.vtranslate.translate_coordsys(xtranslate,ytranslate,0)
        
    def canvasResized(self, event):
        '''
        capture the new dimensions of the canvas
        '''
        pass
    

if __name__ == "__main__":
    root = tk.Tk()
    inputpanel = Canvas3d(root)
    #root.update()
    inputpanel.centerview()
    inputpanel.grid(row=0, sticky='S')
    root.mainloop()