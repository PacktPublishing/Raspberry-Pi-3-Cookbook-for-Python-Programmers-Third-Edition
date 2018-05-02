#!/usr/bin/python3
#photohandler.py
from PIL import Image
from PIL import ExifTags
import datetime
import os

#set module values
previewsize=240,240
defaultimagepreview="./preview.ppm"
filedate_to_use="Exif DateTime"
#Define expected inputs
ARG_IMAGEFILE=1
ARG_LENGTH=2
    
class Photo:
    def __init__(self,filename):
        """Class constructor"""
        self.filename=filename
        self.filevalid=False
        self.exifvalid=False
        img=self.initImage()
        if self.filevalid==True:
            self.initExif(img)
            self.initDates()
    
    def initImage(self):
        """opens the image and confirms if valid, returns Image"""
        try:
            img=Image.open(self.filename)
            self.filevalid=True
        except IOError:
            print ("Target image not found/valid %s" %
                   (self.filename))
            img=None
            self.filevalid=False
        return img
        
    def initExif(self,image):
        """gets any Exif data from the photo"""
        try:
            self.exif_info={
                ExifTags.TAGS[x]:y
                for x,y in image._getexif().items()
                if x in ExifTags.TAGS
            }
            self.exifvalid=True
        except AttributeError:
            print ("Image has no Exif Tags")
            self.exifvalid=False

            
    def initDates(self):
        """determines the date the photo was taken"""
        #Gather all the times available into YYYY-MM-DD format
        self.filedates={}
        if self.exifvalid:
            #Get the date info from Exif info
            exif_ids=["DateTime","DateTimeOriginal",
                      "DateTimeDigitized"]
            for id in exif_ids:
                dateraw=self.exif_info[id]
                self.filedates["Exif "+id]=\
                                dateraw[:10].replace(":","-")
        modtimeraw = os.path.getmtime(self.filename)
        self.filedates["File ModTime"]="%s" %\
            datetime.datetime.fromtimestamp(modtimeraw).date()
        createtimeraw = os.path.getctime(self.filename)
        self.filedates["File CreateTime"]="%s" %\
            datetime.datetime.fromtimestamp(createtimeraw).date()

    def getDate(self):
        """returns the date the image was taken"""
        try:
            date = self.filedates[filedate_to_use]
        except KeyError:
            print ("Exif Date not found")
            date = self.filedates["File ModTime"]
        return date
        
    def previewPhoto(self):
        """creates a thumbnail image suitable for tk to display"""
        imageview=self.initImage()
        imageview=imageview.convert('RGB')
        imageview.thumbnail(previewsize,Image.ANTIALIAS)
        imageview.save(defaultimagepreview,format='ppm')
        return defaultimagepreview

#Module test code
def dispPreview(aPhoto):
    """Create a test GUI"""
    import tkinter as TK

    #Define the app window
    app = TK.Tk()
    app.title("Photo View Demo")
   
    #Define TK objects
    # create an empty canvas object the same size as the image
    canvas = TK.Canvas(app, width=previewsize[0],
                       height=previewsize[1])
    canvas.grid(row=0,rowspan=2)
    # Add list box to display the photo data
    #(including xyscroll bars)
    photoInfo=TK.Variable()
    lbPhotoInfo=TK.Listbox(app,listvariable=photoInfo,
                           height=18,width=45,
                           font=("monospace",10))
    yscroll=TK.Scrollbar(command=lbPhotoInfo.yview,
                         orient=TK.VERTICAL)
    xscroll=TK.Scrollbar(command=lbPhotoInfo.xview,
                         orient=TK.HORIZONTAL)
    lbPhotoInfo.configure(xscrollcommand=xscroll.set,
                          yscrollcommand=yscroll.set)
    lbPhotoInfo.grid(row=0,column=1,sticky=TK.N+TK.S)
    yscroll.grid(row=0,column=2,sticky=TK.N+TK.S)
    xscroll.grid(row=1,column=1,sticky=TK.N+TK.E+TK.W)
    
    # Generate the preview image
    preview_filename = aPhoto.previewPhoto()
    photoImg = TK.PhotoImage(file=preview_filename)
    # anchor image to NW corner
    canvas.create_image(0,0, anchor=TK.NW, image=photoImg) 
    
    # Populate infoList with dates and exif data
    infoList=[]
    for key,value in aPhoto.filedates.items():
        infoList.append(key.ljust(25) + value)
    if aPhoto.exifvalid:
        for key,value in aPhoto.exif_info.items():
           infoList.append(key.ljust(25) + str(value))
    # Set listvariable with the infoList
    photoInfo.set(tuple(infoList))

    app.mainloop()

def main():
    """called only when run directly, allowing module testing"""
    import sys
    #Check the arguments
    if len(sys.argv) == ARG_LENGTH:
        print ("Command: %s" %(sys.argv))
        #Create an instance of the Photo class
        viewPhoto = Photo(sys.argv[ARG_IMAGEFILE])
        #Test the module by running a GUI
        if viewPhoto.filevalid==True:
            dispPreview(viewPhoto)
    else:
        print ("Usage: photohandler.py imagefile")

if __name__=='__main__':
  main()
#End 

