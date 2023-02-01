import yaml
import os
import re
import fnmatch

filename = "2021-05-28_00-19-27.mp4"

filename, ext = filename.rsplit('.')

for filename in folder:
    if fnmatch.fnmatch(filename,"")