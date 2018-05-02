#!/usr/bin/env python3
#xivelylog.py
import xively
import time
import datetime
import requests
from random import randint
import data_local as dataDevice

# Set the FEED_ID and API_KEY from your account
FEED_ID = 399948883
API_KEY = "CcRxJbP5TuHp1PiOGVrN2kTGeXVsb6QZRJU236v6PjOdtzze"
api = xively.XivelyAPIClient(API_KEY) # initialize api client
DEBUG=True

myData = dataDevice.device()
myDataNames=myData.getName()

def get_datastream(feed,name,tags):
  try:
    datastream = feed.datastreams.get(name)
    if DEBUG:print ("Found existing datastream")
    return datastream
  except:
    if DEBUG:print ("Creating new datastream")
    datastream = feed.datastreams.create(name, tags=tags)
    return datastream

def run():
  print ("Connecting to Xively")
  feed = api.feeds.get(FEED_ID)
  if DEBUG:print ("Got feed" + str(feed))
  datastreams=[]
  for dataName in myDataNames:
    dstream = get_datastream(feed,dataName,dataName)
    #dstream.max_value = None
    #dstream.min_value = None
    if DEBUG:print ("Got %s datastream:%s"%(dataName,dstream))
    datastreams.append(dstream)

  while True:
    data=myData.getNew()
    for idx,dataValue in enumerate(data):
      if DEBUG:
        print ("Updating %s: %s" % (dataName,dataValue))
      datastreams[idx].current_value = dataValue
      datastreams[idx].at = datetime.datetime.utcnow()
    try:
      for ds in datastreams:
        ds.update()
    except requests.HTTPError as e:
      print ("HTTPError({0}): {1}".format(e.errno, e.strerror))
    time.sleep(60)

run()
#End
