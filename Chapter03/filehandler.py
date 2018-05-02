#!/usr/bin/python3
#filehandler.py
import os
import shutil
import photohandler as PH
from operator import itemgetter

FOLDERSONLY=True
DEBUG=True
defaultpath=""
NAME=0
DATE=1

class FileList:
  def __init__(self,folder):
    """Class constructor"""
    self.folder=folder
    self.listFileDates()

  def getPhotoNamedates(self):
    """returns the list of filenames and dates"""
    return self.photo_namedates

  def listFileDates(self):
    """Generate list of filenames and dates"""
    self.photo_namedates = list()
    if os.path.isdir(self.folder):
      for filename in os.listdir(self.folder):
        if filename.lower().endswith(".jpg"):
          aPhoto = PH.Photo(os.path.join(self.folder,filename))
          if aPhoto.filevalid:
            if (DEBUG):print("NameDate: %s %s"%
                             (filename,aPhoto.getDate()))
            self.photo_namedates.append((filename,
                                         aPhoto.getDate()))
            self.photo_namedates = sorted(self.photo_namedates,
                                    key=lambda date: date[DATE])

  def genFolders(self):
    """function to generate folders"""
    for i,namedate in enumerate(self.getPhotoNamedates()):
      #Remove the - from the date format
      new_folder=namedate[DATE].replace("-","")
      newpath = os.path.join(self.folder,new_folder)
      #If path does not exist create folder
      if not os.path.exists(newpath):
        if (DEBUG):print ("New Path: %s" % newpath)
        os.makedirs(newpath)
      if (DEBUG):print ("Found file: %s move to %s" %
                        (namedate[NAME],newpath))
      src_file = os.path.join(self.folder,namedate[NAME])
      dst_file = os.path.join(newpath,namedate[NAME])
      try:
        if (DEBUG):print ("File moved %s to %s" %
                          (src_file, dst_file))
        if (FOLDERSONLY==False):shutil.move(src_file, dst_file)
      except IOError:
        print ("Skipped: File not found")

def main():
  """called only when run directly, allowing module testing"""
  import tkinter as TK
  from tkinter import filedialog
  app = TK.Tk()
  app.withdraw()
  dirname = TK.filedialog.askdirectory(parent=app,
      initialdir=defaultpath,
      title='Select your pictures folder')
  if dirname != "":
    ourFileList=FileList(dirname)
    ourFileList.genFolders()

if __name__=="__main__":
  main()
#End
