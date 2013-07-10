#!/usr/bin/python

import os, subprocess
import urllib, codecs

from IPython import embed

from difflib import unified_diff
from html.parser import HTMLParser

class MaintainerParser(HTMLParser):
    def __init__(self, strict):
      self.counter = -1
      HTMLParser.__init__(self, strict=strict)
    def handle_data(self, data):
      #print(data)
      self.counter -= 1
      if "Maintainer:" in data:
        #print ("start maintainer", data)
        self.counter = 2
      elif self.counter == 0:
        #print ("Found maintainer", data)
        self.maintainer = data

class OutOfDateParser(HTMLParser):
    def __init__(self, strict):
      self.outOfDate = False
      HTMLParser.__init__(self, strict=strict)
    def handle_data(self, data):
      if "Flagged out-of-date" in data:
        self.outOfDate = True

class Package:
  def __init__(self, name):
    self.name = name
    
    if self.isGit():
      url = "https://aur.archlinux.org/packages/%s" % self.name
      response = urllib.request.urlopen(url)
      self.aurHTML = response.read().decode('UTF-8')
  
  def isGit(self):
    if "git" in self.name:
      return True
    return False

  def isPacman4(self):
    if subprocess.call(["grep", "pkgver()", self.name+"/PKGBUILD"], stdout=subprocess.PIPE):
      return False
    return True
  
  def aurDiff(self):
    if not self.isGit():
      return ""

    url = "https://aur.archlinux.org/packages/%s/%s/PKGBUILD" % (self.name[0:2], self.name)
    response = urllib.request.urlopen(url)
      
    aurPKG = response.read().decode('ISO-8859-1')
    locPKG = codecs.open(self.name+"/PKGBUILD", 'r',encoding='ISO-8859-1').read()
      
    diff = unified_diff(aurPKG.splitlines(1), locPKG.splitlines(1))
    thediff = ''.join(diff)
    return len(thediff)

  def maintainer(self):
    if not self.isGit():
      return ""
    parser = MaintainerParser(strict=False)
    parser.feed(self.aurHTML)
    return parser.maintainer

  def outOfDate(self):
    if not self.isGit():
      return ""
    parser = OutOfDateParser(strict=False)
    parser.feed(self.aurHTML)
    if parser.outOfDate:
      return "out of date"
    else:
      return ""
      
  def prettyPrint(self, space):
    print (self.name, space, "|", 
       " X " if self.isGit() else "   ", "|", 
       " X " if self.isPacman4() else "   ", "|", 
       self.aurDiff(), "\t",
       self.maintainer(),
       self.outOfDate())
               
class PackageManager:
  def __init__(self):
    self.packages = []
    self.longestName = 0

  def getSpaceString(self, name):
    string = ""
    for i in range(0, (self.longestName - len(name))):
      string += " "
    return string
    
  def list(self):
    for file in os.listdir("."):
      if os.path.isdir(file):
        if not ".git" in file:
          self.packages.append(file)
          if len(file) > self.longestName:
            self.longestName = len(file)

    self.packages.sort()
    
    print ("", self.getSpaceString(""), "|", "Git", "|", "PM4", "|", "diff", "|", "maintainer")
          
    for package in self.packages:
      pkg = Package(package)
      pkg.prettyPrint(self.getSpaceString(package))

      
pm = PackageManager()
pm.list()
