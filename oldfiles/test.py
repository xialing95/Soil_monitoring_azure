import os
import json

log_f = open('static/log.json', 'r+')
ImageList = log_f.readline()
print(ImageList)
log_f.seek(0)
log_f.truncate()
log_f.writelines(ImageList[1:])
log_f.close()
