################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob, zipfile
import shutil
import errno
import urllib2,urllib
import re
import downloader
import extract
import uservar
import skinSwitch
import time
from datetime import date, datetime, timedelta
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from string import digits

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = xbmcaddon.Addon(ADDON_ID)
VERSION        = ADDON.getAddonInfo('version')
USER_AGENT     = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
LOG            = xbmc.translatePath('special://logpath/')
PROFILE        = xbmc.translatePath('special://profile/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDOND         = os.path.join(USERDATA,  'addon_data')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED       = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES        = os.path.join(USERDATA,  'sources.xml')
GUISETTINGS    = os.path.join(USERDATA,  'guisettings.xml')
FAVOURITES     = os.path.join(USERDATA,  'favourites.xml')
PROFILES       = os.path.join(USERDATA,  'profiles.xml')
THUMBS         = os.path.join(USERDATA,  'Thumbnails')
DATABASE       = os.path.join(USERDATA,  'Database')
FANART         = os.path.join(PLUGIN,    'fanart.jpg')
ICON           = os.path.join(PLUGIN,    'icon.png')
ART            = os.path.join(PLUGIN,    'resources', 'art')
WIZLOG         = os.path.join(ADDONDATA, 'wizard.log')
SKIN           = xbmc.getSkinDir()
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
TWODAYS        = TODAY + timedelta(days=2)
THREEDAYS      = TODAY + timedelta(days=3)
ONEWEEK        = TODAY + timedelta(days=7)
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
EXCLUDES       = uservar.EXCLUDES
BUILDFILE      = uservar.BUILDFILE
APKFILE        = uservar.APKFILE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
AUTOINSTALL    = uservar.AUTOINSTALL
REPOADDONXML   = uservar.REPOADDONXML
REPOZIPURL     = uservar.REPOZIPURL
CONTACT        = uservar.CONTACT
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
INCLUDEVIDEO   = ADDON.getSetting('includevideo')
INCLUDEALL     = ADDON.getSetting('includeall')
INCLUDEBOB     = ADDON.getSetting('includebob')
INCLUDEPHOENIX = ADDON.getSetting('includephoenix')
INCLUDESPECTO  = ADDON.getSetting('includespecto')
INCLUDEGENESIS = ADDON.getSetting('includegenesis')
INCLUDEEXODUS  = ADDON.getSetting('includeexodus')
INCLUDEONECHAN = ADDON.getSetting('includeonechan')
INCLUDESALTS   = ADDON.getSetting('includesalts')
INCLUDESALTSHD = ADDON.getSetting('includesaltslite')
SHOWADULT      = ADDON.getSetting('adult')
WIZDEBUGGING   = ADDON.getSetting('addon_debug')
DEBUGLEVEL     = ADDON.getSetting('debuglevel')
ENABLEWIZLOG   = ADDON.getSetting('wizardlog')
CLEANWIZLOG    = ADDON.getSetting('autocleanwiz')
CLEANWIZLOGBY  = ADDON.getSetting('wizlogcleanby')
CLEANDAYS      = ADDON.getSetting('wizlogcleandays')
CLEANSIZE      = ADDON.getSetting('wizlogcleansize')
CLEANLINES     = ADDON.getSetting('wizlogcleanlines')
BACKUPLOCATION = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
MYBUILDS       = os.path.join(BACKUPLOCATION, 'My_Builds', '')
LOGFILES       = ['log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'tvmc.old.log']
MAXWIZSIZE     = [100, 200, 300, 400, 500, 1000]
MAXWIZLINES    = [100, 200, 300, 400, 500]
MAXWIZDATES    = [1, 2, 3, 7]


###########################
###### Settings Items #####
###########################

def getS(name):
	try: return ADDON.getSetting(name)
	except: return False

def setS(name, value):
	try: ADDON.setSetting(name, value)
	except: return False

def openS(name=""):
	ADDON.openSettings()

def clearS(type):
	build    = {'buildname':'', 'buildversion':'', 'buildtheme':'', 'latestversion':'', 'lastbuildcheck':'2016-01-01'}
	install  = {'installed':'false', 'extract':'', 'errors':''}
	default  = {'defaultskinignore':'false', 'defaultskin':'', 'defaultskinname':''}
	lookfeel = ['default.enablerssfeeds', 'default.font', 'default.rssedit', 'default.skincolors', 'default.skintheme', 'default.skinzoom', 'default.soundskin', 'default.startupwindow', 'default.stereostrength']
	if type == 'build':
		for set in build:
			setS(set, build[set])
		for set in install:
			setS(set, install[set])
		for set in default:
			setS(set, default[set])
		for set in lookfeel:
			setS(set, '')
	elif type == 'default':
		for set in default:
			setS(set, default[set])
		for set in lookfeel:
			setS(set, '')
	elif type == 'install':
		for set in install:
			setS(set, install[set])
	elif type == 'lookfeel':
		for set in lookfeel:
			setS(set, '')

###########################
###### Display Items ######
###########################

def TextBoxes(heading,announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			ebi("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		xbmc.sleep(500)

def LogNotify(title,message,times=2000,icon=ICON):
	ebi('XBMC.Notification(%s, %s, %s, %s)' % (title, message, times, icon))

def percentage(part, whole):
	return 100 * float(part)/float(whole)

###########################
###### Build Info #########
###########################

def checkBuild(name, ret):
	if not workingURL(BUILDFILE) == True: return False
	link = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
	match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for version, url, gui, kodi, theme, icon, fanart, adult, description in match:
			if ret   == 'version':       return version
			elif ret == 'url':           return url
			elif ret == 'gui':           return gui
			elif ret == 'kodi':          return kodi
			elif ret == 'theme':         return theme
			elif ret == 'icon':          return icon
			elif ret == 'fanart':        return fanart
			elif ret == 'adult':         return adult
			elif ret == 'description':   return description
			elif ret == 'all':           return name, version, url, gui, kodi, theme, icon, fanart, adult, description
	else: return False

def checkTheme(name, theme, ret):
	themeurl = checkBuild(name, 'theme')
	if not workingURL(themeurl) == True: return False
	link = openURL(themeurl).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"' % theme).findall(link)
	if len(match) > 0:
		for url, icon, fanart, description in match:
			if ret   == 'url':           return url
			elif ret == 'icon':          return icon
			elif ret == 'fanart':        return fanart
			elif ret == 'description':   return description
			elif ret == 'all':           return name, theme, url, icon, fanart, description
	else: return False

def checkApk(name, ret):
	if not workingURL(APKFILE) == True: return False
	link = openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for url, icon, fanart, adult, description in match:
			if   ret == 'url':           return url
			elif ret == 'icon':          return icon
			elif ret == 'fanart':        return fanart
			elif ret == 'adult':         return adult
			elif ret == 'description':   return description
			elif ret == 'all':           return name, url, icon, fanart, adult, description
	else: return False

def checkAddon(name, ret):
	if not workingURL(APKFILE) == True: return False
	link = openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(%s)".+?lugin="(.+?)".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for plugin, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
			if   ret == 'plugin':        return plugin
			elif ret == 'url':           return url
			elif ret == 'repository':    return repository
			elif ret == 'repositoryxml': return repositoryxml
			elif ret == 'repositoryurl': return repositoryurl
			elif ret == 'icon':          return icon
			elif ret == 'fanart':        return fanart
			elif ret == 'adult':         return adult
			elif ret == 'description':   return description
			elif ret == 'all':           return name, plugin, url, repository, repositoryurl, icon, fanart, adult, description
	else: return False

def checkTutorial(name, ret):
	if not workingURL(APKFILE) == True: return False
	link = openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for url, icon, fanart, description in match:
			if   ret == 'url':           return url
			elif ret == 'icon':          return icon
			elif ret == 'fanart':        return fanart
			elif ret == 'description':   return description
			elif ret == 'all':           return name, url, icon, fanart, description
	else: return False

def checkWizard(ret):
	if not workingURL(WIZARDFILE) == True: return False
	link = openURL(WIZARDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('id="%s".+?ersion="(.+?)".+?ip="(.+?)"' % ADDON_ID).findall(link)
	if len(match) > 0:
		for version, zip in match:
			if ret   == 'version':       return version
			elif ret == 'zip':           return zip
			elif ret == 'all':           return ADDON_ID, version, zip
	else: return False

def buildCount(ver=None):
	link = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?odi="(.+?)".+?dult="(.+?)"').findall(link)
	count = 0
	if len(match) > 0:
		for name, kodi, adult in match:
			if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
			kodi = int(float(kodi))
			if ver == None: count += 1
			elif int(ver) == 17 and kodi == 17: count += 1
			elif int(ver) == 16 and kodi == 16: count += 1
			elif int(ver) == 15 and kodi <= 15: count += 1
	return count

def themeCount(name, count=True):
	themefile = checkBuild(name, 'theme')
	if themefile == 'http://': return False
	link = openURL(themefile).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)"').findall(link)
	if len(match) == 0: return False
	if count == True: return len(match)
	else: 
		themes = []
		for item in match:
			themes.append(item)
		return themes

###########################
###### URL Checks #########
###########################
 
def workingURL(url):
	if url == 'http://': return False
	try: 
		req = urllib2.Request(url)
		req.add_header('User-Agent', USER_AGENT)
		response = urllib2.urlopen(req)
		response.close()
	except Exception, e:
		return e
	return True
 
def openURL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', USER_AGENT)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

###########################
###### Misc Functions #####
###########################

def getKeyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if keyboard.isConfirmed():
		return unicode( keyboard.getText(), "utf-8" )
	return default

def getSize(path, total=0):
	for dirpath, dirnames, filenames in os.walk(path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total += os.path.getsize(fp)
	return total

def convertSize(num, suffix='B'):
	for unit in ['', 'K', 'M', 'G']:
		if abs(num) < 1024.0:
			return "%3.02f %s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.02f %s%s" % (num, 'G', suffix)

def getCacheSize():
	PROFILEADDONDATA = os.path.join(PROFILE,'addon_data')
	dbfiles   = [
		(os.path.join(ADDONDATA, 'plugin.video.phstreams', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.bob', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.specto', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.genesis', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.exodus', 'cache.db')),
		(os.path.join(DATABASE,  'onechannelcache.db')),
		(os.path.join(DATABASE,  'saltscache.db')),
		(os.path.join(DATABASE,  'saltshd.lite.db'))]
	cachelist = [
		(PROFILEADDONDATA),
		(ADDONDATA),
		(os.path.join(HOME,'cache')),
		(os.path.join(HOME,'temp')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
		(os.path.join(ADDONDATA,'script.module.simple.downloader')),
		(os.path.join(ADDONDATA,'plugin.video.itv','Images')),
		(os.path.join(PROFILEADDONDATA,'script.module.simple.downloader')),
		(os.path.join(PROFILEADDONDATA,'plugin.video.itv','Images'))]
		
	totalsize = 0

	for item in cachelist:
		if os.path.exists(item) and not item in [ADDONDATA, PROFILEADDONDATA]:
			totalsize = getSize(item, totalsize)
		else:
			for root, dirs, files in os.walk(item):
				for d in dirs:
					if 'cache' in d.lower(): totalsize = getSize(os.path.join(root, d), totalsize)
	
	if INCLUDEVIDEO == 'true':
		files = []
		if INCLUDEALL == 'true': files = dbfiles
		else:
			if INCLUDEBOB == 'true':     files.append(os.path.join(ADDONDATA, 'plugin.video.bob', 'cache.db'))
			if INCLUDEPHOENIX == 'true': files.append(os.path.join(ADDONDATA, 'plugin.video.phstreams', 'cache.db'))
			if INCLUDESPECTO == 'true':  files.append(os.path.join(ADDONDATA, 'plugin.video.specto', 'cache.db'))
			if INCLUDEGENESIS == 'true': files.append(os.path.join(ADDONDATA, 'plugin.video.genesis', 'cache.db'))
			if INCLUDEEXODUS == 'true':  files.append(os.path.join(ADDONDATA, 'plugin.video.exodus', 'cache.db'))
			if INCLUDEONECHAN == 'true': files.append(os.path.join(DATABASE,  'onechannelcache.db'))
			if INCLUDESALTS == 'true':   files.append(os.path.join(DATABASE,  'saltscache.db'))
			if INCLUDESALTSHD == 'true': files.append(os.path.join(DATABASE,  'saltshd.lite.db'))
		if len(files) > 0:
			for item in files: totalsize = getSize(item, totalsize)
		else: log("Clear Cache: Clear Video Cache Not Enabled", xbmc.LOGNOTICE)
	return totalsize

def copyAnything(src, dst):
	try:
		shutil.copytree(src, dst)
	except Exception, e:
		try:
			log("shutil.copytree: %s" % str(e), xbmc.LOGERROR)
			shutil.copy(src, dst)
		except Exception, e:
			log("shutil.copy: %s" % str(e), xbmc.LOGERROR)

import os
from shutil import *
def copytree(src, dst, symlinks=False, ignore=None):
	names = os.listdir(src)
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()
	if not os.path.isdir(dst):
		os.makedirs(dst)
	errors = []
	for name in names:
		if name in ignored_names:
			continue
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if symlinks and os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			elif os.path.isdir(srcname):
				copytree(srcname, dstname, symlinks, ignore)
			else:
				copy2(srcname, dstname)
		except Error, err:
			errors.extend(err.args[0])
		except EnvironmentError, why:
			errors.append((srcname, dstname, str(why)))
	try:
		copystat(src, dst)
	except OSError, why:
		errors.extend((src, dst, str(why)))
	if errors:
		raise Error, errors

def getInfo(label):
	try: return xbmc.getInfoLabel(label)
	except: return False

def removeFolder(path):
	log("Deleting Folder: %s" % path, xbmc.LOGNOTICE)
	try: shutil.rmtree(path,ignore_errors=True, onerror=None)
	except: return False
	
def currSkin():
	return xbmc.getSkinDir()

def removeFile(path):
	log("Deleting File: %s" % path, xbmc.LOGNOTICE)
	try:    os.remove(path)
	except: return False

def cleanHouse(folder, ignore=False):
	total_files = 0; total_folds = 0
	for root, dirs, files in os.walk(folder):
		if ignore == False: dirs[:] = [d for d in dirs if d not in EXCLUDES]
		file_count = 0
		file_count += len(files)
		if file_count >= 0:
			for f in files:
				try: 
					os.unlink(os.path.join(root, f))
					total_files += 1
				except: 
					try:
						shutil.rmtree(os.path.join(root, f))
					except:
						log("Error Deleting %s" % f, xbmc.LOGERROR)
			for d in dirs:
				total_folds += 1
				try: 
					shutil.rmtree(os.path.join(root, d))
					total_folds += 1
				except: 
					log("Error Deleting %s" % d, xbmc.LOGERROR)
	return total_files, total_folds

def emptyfolder(folder):
	total = 0
	for root, dirs, files in os.walk(folder, topdown=True):
		dirs[:] = [d for d in dirs if d not in EXCLUDES]
		file_count = 0
		file_count += len(files) + len(dirs)
		if file_count == 0:
			shutil.rmtree(os.path.join(root))
			total += 1
			log("Empty Folder: %s" % root, xbmc.LOGNOTICE)
	return total

def log(msg, level=xbmc.LOGDEBUG):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(WIZLOG): f = open(WIZLOG, 'w'); f.close()
	if WIZDEBUGGING == 'false': return False
	if DEBUGLEVEL == '0': return False
	if DEBUGLEVEL == '1' and not level in [xbmc.LOGNOTICE, xbmc.LOGERROR, xbmc.LOGSEVERE, xbmc.LOGFATAL]: return False
	if DEBUGLEVEL == '2': level = xbmc.LOGNOTICE
	try:
		if isinstance(msg, unicode):
			msg = '%s' % (msg.encode('utf-8'))
		xbmc.log('%s: %s' % (ADDONTITLE, msg), level)
	except Exception as e:
		try: xbmc.log('Logging Failure: %s' % (e), level)
		except: pass
	if ENABLEWIZLOG == 'true':
		lastcheck = getS('nextcleandate') if not getS('nextcleandate') == '' else str(TODAY)
		if CLEANWIZLOG == 'true' and lastcheck <= str(TODAY): checkLog()
		with open(WIZLOG, 'a') as f:
			line = "[%s %s] %s" % (datetime.now().date(), str(datetime.now().time())[:8], msg)
			f.write(line.rstrip('\r\n')+'\n')

def checkLog():
	nextclean = getS('nextcleandate')
	next = TOMORROW
	if CLEANWIZLOGBY == '0':
		keep = TODAY - timedelta(days=MAXWIZDATES[int(float(CLEANDAYS))])
		x    = 0
		f    = open(WIZLOG); a = f.read(); f.close(); lines = a.split('\n')
		for line in lines:
			if str(line[1:11]) >= str(keep):
				break
			x += 1
		newfile = lines[x:]
		writing = '\n'.join(newfile)
		f = open(WIZLOG, 'w'); f.write(writing); f.close()
	elif CLEANWIZLOGBY == '1':
		maxsize = MAXWIZSIZE[int(float(CLEANSIZE))]*1024
		f    = open(WIZLOG); a = f.read(); f.close(); lines = a.split('\n')
		if os.path.getsize(WIZLOG) >= maxsize:
			start = len(lines)/2
			newfile = lines[start:]
			writing = '\n'.join(newfile)
			f = open(WIZLOG, 'w'); f.write(writing); f.close()
	elif CLEANWIZLOGBY == '2':
		f      = open(WIZLOG); a = f.read(); f.close(); lines = a.split('\n')
		maxlines = MAXWIZLINES[int(float(CLEANLINES))]
		if len(lines) > maxlines:
			start = len(lines) - int(maxlines/2)
			newfile = lines[start:]
			writing = '\n'.join(newfile)
			f = open(WIZLOG, 'w'); f.write(writing); f.close()
	setS('nextcleandate', str(next))

def latestDB(DB):
	if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
		match = glob.glob(os.path.join(DATABASE,'%s*.db' % DB))
		comp = '%s(.+?).db' % DB[1:]
		highest = 0
		for file in match :
			try: check = int(re.compile(comp).findall(file)[0])
			except: check = 0
			if highest < check :
				highest = check
		return '%s%s.db' % (DB, highest)
	else: return False

def addonId(add):
	try: 
		return xbmcaddon.Addon(id=add)
	except:
		return False

def kodi17Fix():
	#skinSwitch.swapUS()
	addonlist = glob.glob(os.path.join(ADDONS, '*/'))
	DP.create(ADDONTITLE,'[COLOR %s]Enabling All Addons ' % COLOR2,'', 'Please Wait[/COLOR]')
	xbmc.sleep(400)
	x = 0
	for folder in sorted(addonlist, key = lambda x: x):
		addonxml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addonxml):
			x += 1
			perc   = int(percentage(x, len(addonlist)))
			fold   = folder.replace(ADDONS, '')[1:-1]
			f      = open(addonxml)
			a      = f.read().replace('\n','').replace('\r','').replace('\t','')
			match  = re.compile('<addo.+?id="(.+?)".+?>').findall(a)
			match2 = re.compile('<addo.+? name="(.+?)".+?>').findall(a)
			icon   = os.path.join(folder, 'icon.png')
			f.close()
			try:
				add    = xbmcaddon.Addon(id=match[0])
				log("%s was enabled" % match[0], xbmc.LOGDEBUG)
				DP.update(perc,"", "Skipping [COLOR %s]%s[/COLOR]: Already Enabled!" % (COLOR1, fold))
			except:
				try:
					DP.update(perc,"", "Enabling [COLOR %s]%s[/COLOR]" % (COLOR1, fold))
					log("%s was disabled" % match[0], xbmc.LOGDEBUG)
					toggleAddon(fold, 'true')
				except:
					try:
						log("2nd Attempt to Enable: %s" % match[0], xbmc.LOGDEBUG)
						toggleAddon(fold, 'true')
					except:
						if len(match) == 0: log("Unabled to enable: %s(Cannot Determine Addon ID)" % match2[0], xbmc.LOGERROR)
						elif len(match2) == 0: log("Unabled to enable: %s(Cannot Determine Addon Name)" % match2[0], xbmc.LOGERROR)
						else: log("Unabled to enable: %s" % match2[0], xbmc.LOGERROR)
			if DP.iscanceled(): break
		xbmc.sleep(100)
	if DP.iscanceled(): 
		DP.close()
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Enabling Addons Cancelled![/COLOR]" % COLOR2)
		sys.exit()
	DP.close()
	forceUpdate()

def toggleDependency(name, DP=None):
	dep=os.path.join(ADDONS, name, 'addon.xml')
	if os.path.exists(dep):
		source=open(dep,mode='r'); link=source.read(); source.close(); 
		match=re.compile('import addon="(.+?)"').findall(link)
		for depends in match:
			if not 'xbmc.python' in depends:
				dependspath=os.path.join(ADDONS, depends)
				if not DP == None: 
					DP.update("","Checking Dependency [COLOR yellow]%s[/COLOR] for [COLOR yellow]%s[/COLOR]" % (depends, name),"")
				if os.path.exists(dependspath):
					toggleAddon(name, 'true')
			xbmc.sleep(100)

def disableProblematic(title=''):
	try: DP.update(0, '', '[COLOR %s]Disabling Problematic Addons![/COLOR]' % COLOR2)
	except: DP.create(ADDONTITLE, '', '[COLOR %s]Disabling Problematic Addons![/COLOR]' % COLOR2)
	x = 0; goback = []; gobackscript = []
	addons = ['plugin.video.1channel',
			  'plugin.video.salts',
			  'plugin.video.saltshd.lite',
			  'script.trakt',
			  'script.module.dudehere.routines',
			  'script.module.metahandler']
			  
	files  = [[os.path.join(DATABASE, 'onechannelcache.db')],
			  [os.path.join(DATABASE, 'saltscache.db'), os.path.join(DATABASE, 'saltscache.db-shm'), os.path.join(DATABASE, 'saltscache.db-wal')],
			  [os.path.join(DATABASE, 'saltshd.lite.db'), os.path.join(DATABASE, 'saltshd.lite.db-shm'), os.path.join(DATABASE, 'saltshd.lite.db-wal')],
			  [os.path.join(ADDOND, 'script.trakt', 'queue.db')],
			  [os.path.join(ADDOND, 'script.module.dudehere.routines', 'access.log'),os.path.join(ADDOND, 'script.module.dudehere.routines', 'trakt.db')],
			  [os.path.join(ADDOND, 'script.module.metahandler', 'meta_cache', 'video_cache.db')]]

	addonlist = glob.glob(os.path.join(ADDONS, '*/'))
	for folder in sorted(addonlist, key = lambda x: x):
		fold   = folder.replace(ADDONS, '')[1:-1]
		if fold in EXCLUDES: continue
		addonxml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addonxml):
			f      = open(addonxml)
			b      = f.read()
			a      = b.replace('\n','').replace('\r','').replace('\t','')
			if not str(a).find('script.common.plugin.cache') == -1 and not fold == 'script.common.plugin.cache':
				addons.append('%s' % fold)
				files.append([''])
	addons.append('script.common.plugin.cache')
	files.append([os.path.join(HOME, 'cache', 'commoncache.db')])
	x = 0
	for item in addons:
		x += 1
		addon = os.path.join(ADDONS, item)
		if os.path.exists(os.path.join(addon, 'addon.xml')):
			f = open(os.path.join(addon, 'addon.xml'))
			a      = f.read().replace('\r','').replace('\t','')
			match  = re.compile('<extension.+?oint="xbmc.service".+?ibrary="(.+?)".+?>').findall(a)
			match2  = re.compile('<extension.+?ibrary="(.+?)".+?oint="xbmc.service".+?>').findall(a)
			if len(match) > 0 or len(match2) > 0:
				file = match[0] if len(match) > 0 else match2[0]
				gobackscript.append(os.path.join(addon, file))
				f.close()
				cleanHouse(addon)
				perc  = int(percentage(x, len(addons)))
				DP.update(perc, "", "[COLOR %s]Deleting[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, item))
				goback.append(item)
			else:
				gobackscript.append('')
				goback.append(item)
	if len(goback) < 1:
		return
	xbmc.sleep(400)
	x = 0
	for script in goback:
		x += 1
		addon = os.path.join(ADDONS, script)
		perc  = int(percentage(x, len(goback)))
		scriptfile = gobackscript[goback.index(script)]
		DP.update(perc, "", "[COLOR %s]Disabling[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, script))
		if not scriptfile == '': ebi('StopScript(%s)' % scriptfile)
		ebi('StopScript(%s)' % addon)
		ebi('StopScript(%s)' % script)
		xbmc.sleep(500)
		if not scriptfile == '': ebi('StopScript(%s)' % scriptfile)
		ebi('StopScript(%s)' % addon)
		ebi('StopScript(%s)' % script)
		query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":false}, "id":1}' % script
		response = xbmc.executeJSONRPC(query)
		xbmc.sleep(400)
		for item in files[x-1]:
			try: os.remove(item)
			except Exception, e: 
				pass

def disableAll():
	addonlist = glob.glob(os.path.join(ADDONS, '*/'))
	DP.create(ADDONTITLE,'[COLOR %s]Disabling All Addons ' % COLOR2,'', 'Please Wait[/COLOR]')
	returnto = []; scriptto = []
	xbmc.sleep(400)
	x = 0
	for folder in sorted(addonlist, key = lambda x: x):
		fold   = folder.replace(ADDONS, '')[1:-1]
		if fold in EXCLUDES: continue
		addonxml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addonxml):
			x += 1
			perc   = int(percentage(x, len(addonlist)))
			f      = open(addonxml)
			b      = f.read()
			a      = b.replace('\n','').replace('\r','').replace('\t','')
			match  = re.compile('<addo.+?id="(.+?)".+?>').findall(a)
			match2 = re.compile('<addo.+? name="(.+?)".+?>').findall(a)
			match3  = re.compile('<extension.+?oint="xbmc.service".+?ibrary="(.+?)".+?>').findall(a)
			match4  = re.compile('<extension.+?ibrary="(.+?)".+?oint="xbmc.service".+?>').findall(a)
			match5  = re.compile('<extension.+?oint="xbmc.service".+?ibrary="(.+?)".+?>').findall(b)
			match6  = re.compile('<extension.+?ibrary="(.+?)".+?oint="xbmc.service".+?>').findall(b)
			icon   = os.path.join(folder, 'icon.png')
			f.close()
			DP.update(perc,"", "Disabling [COLOR %s]%s[/COLOR]" % (COLOR1, fold))
			try:
				addonid = match[0] if len(match) > 0 else fold
				add     = xbmcaddon.Addon(id=addonid)
				if len(match3) > 0 or len(match4) > 0 or len(match5) > 0 or len(match6) > 0:
					if   len(match3) > 0: script = match3[0]
					elif len(match4) > 0: script = match4[0]
					elif len(match5) > 0: script = match5[0]
					elif len(match6) > 0: script = match6[0]
					log("%s / %s" % (addonid, script), xbmc.LOGDEBUG)
					DP.update(perc,"", "Stopping Script [COLOR %s]%s[/COLOR]" % (COLOR1, addonid))
					ebi('StopScript(%s)' % os.path.join(ADDONS, addonid))
					ebi('StopScript(%s)' % os.path.join(addonid))
					ebi('StopScript(%s)' % os.path.join(ADDONS, addonid, script))
					returnto.append(addonid)
					scriptto.append(os.path.join(ADDONS, addonid, script))
				else:
					DP.update(perc,"", "Disabling [COLOR %s]%s[/COLOR]" % (COLOR1, addonid))
					query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":false}, "id":1}' % addonid
					response = xbmc.executeJSONRPC(query)
				xbmc.sleep(100)
			except Exception, e:
				log("Error disabling: %s (%s)" % (fold, str(e)), xbmc.LOGERROR)
			if DP.iscanceled(): 
				DP.close()
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Disabling Addons Cancelled[/COLOR]" % COLOR2)
				sys.exit()
	if len(returnto) > 0:
		DP.update(0, "", "Giving Kodi time to StopScript on %s Addons" % len(returnto))
		xbmc.sleep(500)
		x = 0
		for addon in returnto:
			x += 1
			perc   = int(percentage(x, len(returnto)))
			DP.update(perc,"", "Disabling [COLOR %s]%s[/COLOR]" % (COLOR1, addon))
			try:
				log("%s / %s" % (addon, scriptto[returnto.index(addon)]), xbmc.LOGDEBUG)
				ebi('StopScript(%s)' % addon)
				ebi('StopScript(%s)' % os.path.join(ADDONS, addon))
				ebi('StopScript(%s)' % os.path.join(ADDONS, addon, scriptto[returnto.index(addon)]))
				xbmc.sleep(500)
				query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":false}, "id":1}' % addon
				response = xbmc.executeJSONRPC(query)
			except Exception, e:
				log("Error disabling: %s (%s)" % (addon, str(e)), xbmc.LOGERROR)
			if DP.iscanceled(): 
				DP.close()
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Disabling Addons Cancelled[/COLOR]" % COLOR2)
				sys.exit()
	DP.close()

def toggleAdult():
	do = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Enable[/COLOR] or [COLOR %s]Disable[/COLOR] all Adult addons?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B]Enable[/B]", nolabel="[B]Disable[/B]")
	state = 'true' if do == 1 else 'false'
	goto = 'Enabling' if do == 1 else 'Disabling'
	link = openURL('http://noobsandnerds.com/TI/AddonPortal/adult.php').replace('\n','').replace('\r','').replace('\t','')
	list = re.compile('i="(.+?)"').findall(link)
	count = 0
	for item in list:
		fold = os.path.join(ADDONS, item)
		if os.path.exists(fold):
			count += 1
			toggleAddon(item, state, True)
			log("[Toggle Adult] %s %s" % (goto, item), xbmc.LOGNOTICE)
	if count > 0: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s][COLOR %s]%d[/COLOR] Adult Addons %s[/COLOR]" % (COLOR2, COLOR1, count, goto.replace('ing', 'ed'))); forceUpdate(True)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Adult Addons Found[/COLOR]" % COLOR2)

def toggleAddon(id, value, over=None):
	addonxml = os.path.join(ADDONS, id, 'addon.xml')
	if os.path.exists(addonxml):
		f      = open(addonxml)
		b      = f.read()
		a      = b.replace('\n','').replace('\r','').replace('\t','')
		match  = re.compile('<addo.+?id="(.+?)".+?>').findall(a)
		match2 = re.compile('<addo.+? name="(.+?)".+?>').findall(a)
		match3  = re.compile('<extension.+?oint="xbmc.service".+?ibrary="(.+?)".+?>').findall(a)
		match4  = re.compile('<extension.+?ibrary="(.+?)".+?oint="xbmc.service".+?>').findall(a)
		match5  = re.compile('<extension.+?oint="xbmc.service".+?ibrary="(.+?)".+?>').findall(b)
		match6  = re.compile('<extension.+?ibrary="(.+?)".+?oint="xbmc.service".+?>').findall(b)
		addonid = match[0] if len(match) > 0 else id
		if len(match3) > 0 or len(match4) > 0 or len(match5) > 0 or len(match6) > 0:
			if   len(match3) > 0: script = match3[0]
			elif len(match4) > 0: script = match4[0]
			elif len(match5) > 0: script = match5[0]
			elif len(match6) > 0: script = match6[0]
			log("We got a live one, stopping script: %s" % match[0], xbmc.LOGDEBUG)
			ebi('StopScript(%s)' % os.path.join(ADDONS, addonid))
			ebi('StopScript(%s)' % addonid)
			ebi('StopScript(%s)' % os.path.join(ADDONS, addonid, script))
			xbmc.sleep(500)
	query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":%s}, "id":1}' % (addonid, value)
	response = xbmc.executeJSONRPC(query)
	if 'error' in response and over == None:
		v = 'Enabling' if value == 'true' else 'Disabling'
		DIALOG.ok(ADDON_NAME, "[COLOR %s]Error %s [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, v, id), "Check to make sure the addon list is upto date and try again.[/COLOR]")
		forceUpdate()

def percentage(part, whole):
	return 100 * float(part)/float(whole)

def addonInfo(add, info):
	addon = addonId(add)
	if addon: return addon.getAddonInfo(info)
	else: return False

def whileWindow(window, active=False, count=0, counter=15):
	windowopen = getCond('Window.IsActive(%s)' % window)
	log("%s is %s" % (window, windowopen), xbmc.LOGDEBUG)
	while not windowopen and count < counter:
		log("%s is %s(%s)" % (window, windowopen, count))
		windowopen = getCond('Window.IsActive(%s)' % window)
		count += 1 
		xbmc.sleep(500)
		
	while windowopen:
		active = True
		log("%s is %s" % (window, windowopen), xbmc.LOGDEBUG)
		windowopen = getCond('Window.IsActive(%s)' % window)
		xbmc.sleep(250)
	return active

def cleanupBackup():
	if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to clean up your 'My_Builds' folder?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, MYBUILDS), yeslabel="[B]Clean Up[/B]", nolabel="[B]No Cancel[/B]"):
		cleanHouse(xbmc.translatePath(MYBUILDS))
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Backup Location: Cleared![/COLOR]" % COLOR2)
	else:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Clean Up Cancelled![/COLOR]" % COLOR2)

def getCond(type):
	return xbmc.getCondVisibility(type)

def ebi(proc):
	xbmc.executebuiltin(proc)

def refresh():
	ebi('Container.Refresh()')

def forceUpdate(silent=False):
	ebi('UpdateAddonRepos()')
	ebi('UpdateLocalAddons()')
	if silent == False: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Forcing Addon Updates[/COLOR]' % COLOR2)

def convertSpecial(url, over=False):
	total = fileCount(url); start = 0
	DP.create(ADDONTITLE, "[COLOR %s]Changing Physical Paths To Special" % COLOR2, "", "Please Wait[/COLOR]")
	for root, dirs, files in os.walk(url):
		for file in files:
			start += 1
			perc = int(percentage(start, total))
			if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
				DP.update(perc, "[COLOR %s]Scanning: [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, root.replace(HOME, '')), "[COLOR %s]%s[/COLOR]" % (COLOR1, file), "Please Wait[/COLOR]")
				a = open((os.path.join(root, file))).read()
				encodedpath  = urllib.quote(HOME)
				encodedpath2  = urllib.quote(HOME).replace('%3A','%3a').replace('%5C','%5c')
				b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
				f = open((os.path.join(root, file)), mode='w')
				f.write(str(b))
				f.close()
	DP.close()
	log("[Convert Paths to Special] Complete", xbmc.LOGNOTICE)
	if over == False: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Convert Paths to Special: Complete![/COLOR]" % COLOR2)

def latestApk(apk):
	if apk == "kodi":
		kodi  = "https://kodi.tv/download/"
		link  = openURL(kodi).replace('\n','').replace('\r','').replace('\t','')
		match = re.compile("<h2>Current release:.+?odi v(.+?) &#8220;(.+?)&#8221;</h2>").findall(link)
		if len(match) == 1:
			ver    = match[0][0]
			title  = match[0][1]
			apkurl = "http://mirrors.kodi.tv/releases/android/arm/kodi-%s-%s-armeabi-v7a.apk" % (ver, title)
			return ver, apkurl, "Latest Official Version of Kodi v%s" % ver
		else: return False
	elif apk == "spmc":
		spmc  = 'https://github.com/koying/SPMC/releases/latest/'
		link  = openURL(spmc).replace('\n','').replace('\r','').replace('\t','')
		match = re.compile(".+?class=\"release-title\">(.+?)</h1>.+?").findall(link)
		ver   = re.sub('<[^<]+?>', '', match[0]).replace(' ', '')
		apkurl = 'https://github.com/koying/SPMC/releases/download/%s-spmc/SPMC-armeabi-v7a_%s.apk' % (ver, ver)
		return ver, apkurl, "Latest Official Version of SPMC v%s" % ver

def clearCrash():  
	files = []
	for file in glob.glob(os.path.join(LOG, 'xbmc_crashlog*.*')):
		files.append(file)
	if len(files) > 0:
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to delete the Crash logs?' % COLOR2, '[COLOR %s]%s[/COLOR] Files Found[/COLOR]' % (COLOR1, len(files))):
			for f in files:
				os.remove(f)
			LogNotify('[COLOR %s]Clear Crash Logs[/COLOR]' % COLOR1, '[COLOR %s]%s Crash Logs Removed' % (COLOR2, len(files)))
		else: LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Crash Logs Cancelled[/COLOR]' % COLOR2)
	else: LogNotify('[COLOR %s]Clear Crash Logs[/COLOR]' % COLOR1, '[COLOR %s]No Crash Logs Found[/COLOR]' % COLOR2)

def hidePassword():
	if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]hide[/COLOR] all passwords when typing in the add-on settings menus?[/COLOR]" % COLOR2):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = re.compile('<setting.+?id=(.+?).+?>').findall(f)
				for line in match:
					if 'pass' in line:
						if not 'option="hidden"' in line:
							try:
								change = line.replace('/', 'option="hidden" /')
								f.replace(line, change)
								count += 1
								log("[Hide Passwords] found in %s on %s" % (sett.replace(HOME, ''), line), xbmc.LOGDEBUG)
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("[COLOR %s]Hide Passwords[/COLOR]" % COLOR1, "[COLOR %s]%s items changed[/COLOR]" % (COLOR2, count))
		log("[Hide Passwords] %s items changed" % count, xbmc.LOGNOTICE)
	else: log("[Hide Passwords] Cancelled", xbmc.LOGNOTICE)

def unhidePassword():
	if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]unhide[/COLOR] all passwords when typing in the add-on settings menus?[/COLOR]" % (COLOR2, COLOR1)):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = re.compile('<setting.+?id=(.+?).+?>').findall(f)
				for line in match:
					if 'pass' in line:
						if 'option="hidden"' in line:
							try:
								change = line.replace('option="hidden"', '')
								f.replace(line, change)
								count += 1
								log("[Unhide Passwords] found in %s on %s" % (sett.replace(HOME, ''), line), xbmc.LOGDEBUG)
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("[COLOR %s]Unhide Passwords[/COLOR]" % COLOR1, "[COLOR %s]%s items changed[/COLOR]" % (COLOR2, count))
		log("[Unhide Passwords] %s items changed" % count, xbmc.LOGNOTICE)
	else: log("[Unhide Passwords] Cancelled", xbmc.LOGNOTICE)

def wizardUpdate(startup=None):
	if workingURL(WIZARDFILE):
		ver = checkWizard('version')
		zip = checkWizard('zip')
		if ver > VERSION:
			yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]There is a new version of the [COLOR %s]%s[/COLOR]!' % (COLOR2, COLOR1, ADDONTITLE), 'Would you like to download [COLOR %s]v%s[/COLOR]?[/COLOR]' % (COLOR1, ver), nolabel='[B]Remind Me Later[/B]', yeslabel="[B]Update Wizard[/B]")
			if yes:
				log("[Auto Update Wizard] Installing wizard v%s" % ver, xbmc.LOGNOTICE)
				DP.create(ADDONTITLE,'[COLOR %s]Downloading Update...' % COLOR2,'', 'Please Wait[/COLOR]')
				lib=os.path.join(PACKAGES, '%s-%s.zip' % (ADDON_ID, ver))
				try: os.remove(lib)
				except: pass
				downloader.download(zip, lib, DP)
				xbmc.sleep(2000)
				DP.update(0,"", "Installing %s update" % ADDONTITLE)
				percent, errors, error = extract.all(lib, ADDONS, DP, True)
				DP.close()
				xbmc.sleep(1000)
				ebi('UpdateAddonRepos()')
				ebi('UpdateLocalAddons()')
				xbmc.sleep(1000)
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Add-on updated[/COLOR]' % COLOR2)
				log("[Auto Update Wizard] Wizard updated to v%s" % ver, xbmc.LOGNOTICE)
				ebi('RunScript("%s/startup.py")' % os.path.join(ADDONS, ADDON_ID))
			else: log("[Auto Update Wizard] Install New Wizard Ignored: %s" % ver, xbmc.LOGNOTICE)
		else: 
			if not startup: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No New Version of Wizard[/COLOR]" % COLOR2)
			log("[Auto Update Wizard] No New Version v%s" % ver, xbmc.LOGNOTICE)
	else: log("[Auto Update Wizard] Url for wizard file not valid: %s" % WIZARDFILE, xbmc.LOGNOTICE)

def convertText(type):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if type == "builds":
		working = workingURL(BUILDFILE)
		if BUILDFILE == 'http://':
			DIALOG.ok(ADDONTITLE, "[COLOR %s]Error converting Text File:[/COLOR]" % COLOR2, "[COLOR %s]Build File set to 'http://' in uservar.py[/COLOR]" % COLOR1)
			return
		if not working == True:
			DIALOG.ok(ADDONTITLE, "[COLOR %s]Error converting Text File:[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, working))
			return
		filename = os.path.join(ADDONDATA, 'builds.txt')
		writing = ''
		a = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
		match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(a)
		for name, version, url, gui, kodi, theme, icon, fanart in match:
			if not writing == '': writing += '\n'
			writing += 'name="%s"\n' % name
			writing += 'version="%s"\n' % version
			writing += 'url="%s"\n' % url
			writing += 'gui="%s"\n' % gui
			writing += 'kodi="%s"\n' % kodi
			writing += 'theme="%s"\n' % theme
			writing += 'icon="%s"\n' % icon
			writing += 'fanart="%s"\n' % fanart
			writing += 'adult="no"\n'
			writing += 'description="Download %s from %s"\n' % (name, ADDONTITLE)
	elif type == "apks":
		working = workingURL(APKFILE)
		if APKFILE == 'http://':
			DIALOG.ok(ADDONTITLE, "[COLOR %s]Error converting Text File:[/COLOR]" % COLOR2, "[COLOR %s]APK File set to 'http://' in uservar.py[/COLOR]" % COLOR1)
			return
		if not working == True:
			DIALOG.ok(ADDONTITLE, "[COLOR %s]Error converting Text File:[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, working))
			return
		filename = os.path.join(ADDONDATA, 'apk.txt')
		writing = ''
		a = openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(a)
		for name, url, icon, fanart in match:
			if not writing == '': writing += '\n'
			writing += 'name="%s"\n' % name
			writing += 'url="%s"\n' % url
			writing += 'icon="%s"\n' % icon
			writing += 'fanart="%s"\n' % fanart
			writing += 'adult="no"\n'
			writing += 'description="Download %s from %s"\n\n' % (name, ADDONTITLE)
	f = open(filename, 'w'); f.write(writing); f.close()
	DIALOG.ok(ADDONTITLE, "[COLOR %s]The text file for [COLOR %s]%s[/COLOR] has been written to support v0.1.6 of Aftermath Wizard." % (COLOR2, COLOR1, type.title()), "Path: [/COLOR][COLOR %s]%s[/COLOR]" % (COLOR1, filename.replace(USERDATA, '')))

def chunks(s, n):
	for start in range(0, len(s), n):
		yield s[start:start+n]

def asciiCheck(use=None, over=False):
	if use == None:
		source   = DIALOG.browse(3, '[COLOR %s]Select the folder you want to scan[/COLOR]' % COLOR2, 'files', HOME, False, False)
		if over == True:
			yes = 1
		else:
			yes      = DIALOG.yesno(ADDONTITLE,'[COLOR %s]Do you want to [COLOR %s]delete[/COLOR] all filenames with special characters or would you rather just [COLOR %s]scan and view[/COLOR] the results in the log?[/COLOR]' % (COLOR2, COLOR1, COLOR1), yeslabel='[B]Delete[/B]', nolabel='[B]Scan[/B]')
	else: 
		source   = use
		if over == True:
			yes = 1
		else:
			yes      = DIALOG.yesno(ADDONTITLE,'[COLOR %s]Would you like to [COLOR %s]Scan[/COLOR] for Non-Ascii File Names and [COLOR %s]Remove[/COLOR] Them?[/COLOR]' % (COLOR2, COLOR1, COLOR1), yeslabel='[B]Delete Files[/B]', nolabel='[B]Skip Scan[/B]')
		if not yes: return

	if source == "":
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: Cancelled[/COLOR]" % COLOR2)
		return
	
	files_found  = os.path.join(ADDONDATA, 'asciifiles.txt')
	files_fails  = os.path.join(ADDONDATA, 'asciifails.txt')
	afiles       = open(files_found, mode='w+')
	afails       = open(files_fails, mode='w+')
	f1           = 0; f2           = 0
	items        = fileCount(source)
	msg          = ''
	prog         = []
	log("Source file: (%s)" % str(source), xbmc.LOGNOTICE)
	
	DP.create(ADDONTITLE, 'Please wait...')
	for base, dirs, files in os.walk(source):
		dirs[:] = [d for d in dirs]
		files[:] = [f for f in files]
		for file in files:
			prog.append(file) 
			prog2 = int(len(prog) / float(items) * 100)
			DP.update(prog2,"[COLOR %s]Checking for non ASCII files" % COLOR2,'[COLOR %s]%s[/COLOR]' % (COLOR1, d), 'Please Wait[/COLOR]')
			try:
				file.encode('ascii')
			except UnicodeDecodeError:
				badfile = os.path.join(base, file)
				if yes:
					try: 
						os.remove(badfile)
						for chunk in chunks(badfile, 75):
							afiles.write(chunk+'\n')
						afiles.write('\n')
						f1 += 1
						log("[ASCII Check] File Removed: %s " % badfile, xbmc.LOGERROR)
					except:
						for chunk in chunks(badfile, 75):
							afails.write(chunk+'\n')
						afails.write('\n')
						f2 += 1
						log("[ASCII Check] File Failed: %s " % badfile, xbmc.LOGERROR)
				else:
					for chunk in chunks(badfile, 75):
						afiles.write(chunk+'\n')
					afiles.write('\n')
					f1 += 1
					log("[ASCII Check] File Found: %s " % badfile, xbmc.LOGERROR)
				pass
	DP.close(); afiles.close(); afails.close()
	total = int(f1) + int(f2)
	if total > 0:
		if os.path.exists(files_found): afiles = open(files_found, mode='r'); msg = afiles.read(); afiles.close()
		if os.path.exists(files_fails): afails = open(files_fails, mode='r'); msg2 = afails.read(); afails.close()
		if yes:
			if use:
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: %s Removed / %s Failed.[/COLOR]" % (COLOR2, f1, f2))
			else:
				TextBoxes(ADDONTITLE, "[COLOR yellow][B]%s Files Removed:[/B][/COLOR]\n %s\n\n[COLOR yellow][B]%s Files Failed:[B][/COLOR]\n %s" % (f1, msg, f2, msg2))
		else: 
			TextBoxes(ADDONTITLE, "[COLOR yellow][B]%s Files Found:[/B][/COLOR]\n %s" % (f1, msg))
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: None Found.[/COLOR]" % COLOR2)

def fileCount(home, excludes=True):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'packages', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'library', 'keymaps']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	item = []
	for base, dirs, files in os.walk(home):
		if excludes:
			dirs[:] = [d for d in dirs if d not in exclude_dirs]
			files[:] = [f for f in files if f not in exclude_files]
		for file in files:
			item.append(file)
	return len(item)

def defaultSkin():
	log("[Default Skin Check]", xbmc.LOGNOTICE)
	tempgui = os.path.join(USERDATA, 'guitemp.xml')
	gui = tempgui if os.path.exists(tempgui) else GUISETTINGS
	if not os.path.exists(gui): return False
	log("Reading gui file: %s" % gui, xbmc.LOGNOTICE)
	guif = open(gui, 'r+')
	msg = guif.read().replace('\n','').replace('\r','').replace('\t','').replace('    ',''); guif.close()
	log("Opening gui settings", xbmc.LOGNOTICE)
	match = re.compile('<lookandfeel>.+?<ski.+?>(.+?)</skin>.+?</lookandfeel>').findall(msg)
	log("Matches: %s" % str(match), xbmc.LOGNOTICE)
	if len(match) > 0:
		skinid = match[0]
		addonxml = os.path.join(ADDONS, match[0], 'addon.xml')
		if os.path.exists(addonxml):
			addf = open(addonxml, 'r+')
			msg2 = addf.read().replace('\n','').replace('\r','').replace('\t',''); addf.close()
			match2 = re.compile('<addon.+?ame="(.+?)".+?>').findall(msg2)
			if len(match2) > 0: skinname = match2[0]
			else: skinname = 'no match'
		else: skinname = 'no file'
		log("[Default Skin Check] Skin name: %s" % skinname, xbmc.LOGNOTICE)
		log("[Default Skin Check] Skin id: %s" % skinid, xbmc.LOGNOTICE)
		setS('defaultskin', skinid)
		setS('defaultskinname', skinname)
		setS('defaultskinignore', 'false')
	if os.path.exists(tempgui):
		log("Deleting Temp Gui File.", xbmc.LOGNOTICE)
		os.remove(tempgui)
	log("[Default Skin Check] End", xbmc.LOGNOTICE)

def lookandFeelData(do='save'):
	scan = ['lookandfeel.enablerssfeeds', 'lookandfeel.font', 'lookandfeel.rssedit', 'lookandfeel.skincolors', 'lookandfeel.skintheme', 'lookandfeel.skinzoom', 'lookandfeel.soundskin', 'lookandfeel.startupwindow', 'lookandfeel.stereostrength']
	if do == 'save':
		for item in scan:
			query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"%s"}, "id":1}' % (item)
			response = xbmc.executeJSONRPC(query)
			if not 'error' in response:
				match = re.compile('{"value":(.+?)}').findall(str(response))
				setS(item.replace('lookandfeel', 'default'), match[0])
				log("%s saved to %s" % (item, match[0]), xbmc.LOGNOTICE)
	else:
		for item in scan:
			value = getS(item.replace('lookandfeel', 'default'))
			query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"%s","value":%s}, "id":1}' % (item, value)
			response = xbmc.executeJSONRPC(query)
			log("%s restored to %s" % (item, value), xbmc.LOGNOTICE)

def sep(middle=''):
	char = uservar.SPACER
	ret = char * 40
	if not middle == '': 
		middle = '[ %s ]' % middle
		fluff = int((40 - len(middle))/2)
		ret = "%s%s%s" % (ret[:fluff], middle, ret[:fluff+2])
	return ret[:40]

##########################
###BACK UP/RESTORE #######
##########################
def backUpOptions(type, name=""):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'library', 'keymaps']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	bad_files     = [os.path.join(DATABASE, 'onechannelcache.db'),
					 os.path.join(DATABASE, 'saltscache.db'), 
					 os.path.join(DATABASE, 'saltscache.db-shm'), 
					 os.path.join(DATABASE, 'saltscache.db-wal'),
					 os.path.join(DATABASE, 'saltshd.lite.db'),
					 os.path.join(DATABASE, 'saltshd.lite.db-shm'), 
					 os.path.join(DATABASE, 'saltshd.lite.db-wal'),
					 os.path.join(ADDOND, 'script.trakt', 'queue.db'),
					 os.path.join(HOME, 'cache', 'commoncache.db'),
					 os.path.join(ADDOND, 'script.module.dudehere.routines', 'access.log'),
					 os.path.join(ADDOND, 'script.module.dudehere.routines', 'trakt.db'),
					 os.path.join(ADDOND, 'script.module.metahandler', 'meta_cache', 'video_cache.db')]
	
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	if not os.path.exists(backup): os.makedirs(backup)
	if not os.path.exists(mybuilds): os.makedirs(mybuilds)
	if type == "build":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Are you sure you wish to backup the current build?[/COLOR]" % COLOR2, nolabel="[B]Cancel Backup[/B]", yeslabel="[B]Backup Build[/B]"):
			if name == "":
				name = getKeyboard("","Please enter a name for the %s zip" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			zipname       = os.path.join(mybuilds, '%s.zip' % name)
			for_progress  = 0
			ITEM          = []
			if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you want to include your addon_data folder?" % COLOR2, 'This contains [COLOR %s]ALL[/COLOR] addon settings including passwords but may also contain important information such as skin shortcuts. We recommend [COLOR %s]MANUALLY[/COLOR] removing the addon_data folders that aren\'t required.' % (COLOR1, COLOR1), '[COLOR %s]%s[/COLOR] addon_data is ignored[/COLOR]' % (COLOR1, ADDON_ID), yeslabel='[B]Include data[/B]',nolabel='[B]Don\'t Include[/B]'):
				exclude_dirs.append('addon_data')
			convertSpecial(HOME, True)
			asciiCheck(HOME, True)
			zipf = zipfile.ZipFile(zipname , 'w')
			DP.create("%s: Creating Zip" % ADDONTITLE, "Creating back up zip", "", "Please Wait...")
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM) 
						DP.update(int(progress), 'Creating back up zip: %s / %s' % (for_progress, N_ITEM), '[COLOR yellow]%s[/COLOR]'% file, 'Please Wait')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
								if not file == latestDB(temp):  log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
						except Exception, e:
							log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
							log("%s / %s" % (Exception, e))
					except Exception, e:
						log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
						log("Build Backup Error: %s" % str(e), xbmc.LOGNOTICE)
			zipf.close()
			xbmc.sleep(1000)
			DP.update(100, "Creating %s_guisettings.zip" % name, "", "")
			backUpOptions('guifix', name)
			DP.close()
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]backup successful:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "guifix":
		if name == "":
			guiname = getKeyboard("","Please enter a name for the %s zip" % type)
			if not guiname: return False
		else: guiname = name
		guiname = urllib.quote_plus(guiname)
		guizipname = os.path.join(mybuilds, '%s_guisettings.zip' % guiname)
		if os.path.exists(GUISETTINGS):
			zipf = zipfile.ZipFile(guizipname, mode='w')
			try:
				zipf.write(GUISETTINGS, 'guisettings.xml', zipfile.ZIP_DEFLATED)
				zipf.write(PROFILES,    'profiles.xml',    zipfile.ZIP_DEFLATED)
				match = glob.glob(os.path.join(ADDOND,'skin.*'))
				for fold in match:
					fd = fold[len(ADDOND)+1:]
					if not fd in ['skin.confluence', 'skin.estuary']:
						if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to add the following skin folder to the GuiFix Zip File?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, fd), yeslabel="[B]Add Skin[/B]", nolabel="[B]Skip Skin[/B]"):
							for base, dirs, files in os.walk(os.path.join(ADDOND,fold)):
								files[:] = [f for f in files if f not in exclude_files]
								for file in files:
									fn = os.path.join(base, file)
									zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
						else: log("[Back Up] Type = '%s': %s ignored" % (type, fold), xbmc.LOGNOTICE)
			except Exception, e:
				log("[Back Up] Type = '%s': %s" % (type, e), xbmc.LOGNOTICE)
				pass
			zipf.close()
		else: log("[Back Up] Type = '%s': guisettings.xml not found" % type, xbmc.LOGNOTICE)
		if name == "":
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]GuiFix Zip Created![/COLOR]" % COLOR2)
	elif type == "theme":
		if not DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to create a theme backup?[/COLOR]" % COLOR2): LogNotify("Theme Backup", "Cancelled!"); return False
		if name == "":
			themename = getKeyboard("","Please enter a name for the %s zip" % type)
			if not themename: return False
		else: themename = name
		themename = urllib.quote_plus(themename)
		zipname = os.path.join(mybuilds, '%s.zip' % themename)
		zipf = zipfile.ZipFile(zipname, mode='w')
		try:
			if not SKIN == 'skin.confluence':
				skinfold = os.path.join(ADDONS, SKIN, 'media')
				match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
				if len(match2) > 1:
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to go through the Texture Files for?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, SKIN), yeslabel="[B]Add Textures[/B]", nolabel="[B]Skip Textures[/B]"):
						skinfold = os.path.join(ADDONS, SKIN, 'media')
						match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
						for xbt in match2:
							if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to add the Texture File [COLOR %s]%s[/COLOR]?" % (COLOR1, COLOR2, xbt.replace(skinfold, "")[1:]), "from [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, SKIN), yeslabel="[B]Add Textures[/B]", nolabel="[B]Skip Textures[/B]"):
								fn  = xbt
								fn2 = fn.replace(HOME, "")
								zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				else:
					for xbt in match2:
						if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to add the Texture File [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, xbt.replace(skinfold, "")[1:]), "from [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, SKIN), yeslabel="[B]Add Textures[/B]", nolabel="[B]Skip Textures[/B]"):
							fn  = xbt
							fn2 = fn.replace(HOME, "")
							zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				ad_skin = os.path.join(ADDOND, SKIN, 'settings.xml')
				if os.path.exists(ad_skin):
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to go add the [COLOR %s]settings.xml[/COLOR] in [COLOR %s]/addon_data/[/COLOR] for?" % (COLOR2, COLOR1, COLOR1), "[COLOR %s]%s[/COLOR]"  % (COLOR1, SKIN), yeslabel="[B]Add Settings[/B]", nolabel="[B]Skip Settings[/B]"):
						skinfold = os.path.join(ADDOND, SKIN)
						zipf.write(ad_skin, ad_skin.replace(HOME, ""), zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to include a [COLOR %s]Backgrounds[/COLOR] folder?[/COLOR]" % (COLOR2, COLOR1)):
				fn = DIALOG.browse(0, 'Select location of backgrounds', 'files', '', True, False, HOME, False)
				if not fn == HOME:
					for base, dirs, files in os.walk(fn):
						dirs[:] = [d for d in dirs if d not in exclude_dirs]
						files[:] = [f for f in files if f not in exclude_files]
						for file in files:
							try:
								fn2 = os.path.join(base, file)
								zipf.write(fn2, fn2[len(HOME):], zipfile.ZIP_DEFLATED)
							except Exception, e:
								log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
								log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
				text = latestDB('Textures')
				if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to include the [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, text)):
					zipf.write(os.path.join(DATABASE, text), '/userdata/Database/%s' % text, zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, COLOR2, ADDONTITLE), "[COLOR %s]Would you like to include the [COLOR %s]guisettings.xml[/COLOR]?[/COLOR]" % (COLOR2, COLOR1)):
				zipf.write(GUISETTINGS, '/userdata/guisettings.xml', zipfile.ZIP_DEFLATED)
		except Exception, e:
			log("[Back Up] Type = '%s': %s" % (type, str(e)), xbmc.LOGNOTICE)
			pass
		zipf.close()
		DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] theme zip successful:[/COLOR]" % (COLOR1, COLOR2, themename), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "addondata":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Are you sure you wish to backup the current addon_data?[/COLOR]" % COLOR2, nolabel="[B]Cancel Backup[/B]", yeslabel="[B]Backup Addon_Data[/B]"):
			if name == "":
				name = getKeyboard("","Please enter a name for the %s zip" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			name = '%s_addondata.zip' % name
			zipname       = os.path.join(mybuilds, name)
			
			for_progress  = 0
			ITEM          = []
			convertSpecial(ADDOND, True)
			asciiCheck(ADDOND, True)
			zipf = zipfile.ZipFile(zipname , 'w')
			DP.create("%s: Creating Zip" % ADDONTITLE, "[COLOR %s]Creating back up addon_data zip" % COLOR2, "", "Please Wait...[/COLOR]")
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM) 
						DP.update(int(progress), 'Creating back up zip: %s / %s' % (for_progress, N_ITEM), '[COLOR yellow]%s[/COLOR]'% file, 'Please Wait')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
								if not file == latestDB(temp):  log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(ADDOND):], zipfile.ZIP_DEFLATED)
						except Exception, e:
							log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
							log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
					except Exception, e:
						log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
						log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
			zipf.close()
			xbmc.sleep(500)
			DP.close()
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]backup successful:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))

def restoreLocal(type):
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	file = DIALOG.browse(1, '[COLOR %s]Select the backup file you want to restore[/COLOR]' % COLOR2, 'files', '.zip', False, False, mybuilds)
	log("[RESTORE BACKUP %s] File: %s " % (type.upper(), file), xbmc.LOGNOTICE)
	if file == "" or not file.endswith('.zip'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Local Restore: Cancelled[/COLOR]" % COLOR2)
		return
	DP.create(ADDONTITLE,'[COLOR %s]Installing Local Backup' % COLOR2,'', 'Please Wait[/COLOR]')
	if not os.path.exists(USERDATA): os.makedirs(USERDATA)
	if not os.path.exists(ADDOND): os.makedirs(ADDOND)
	if type == "gui": loc = USERDATA
	elif type == "addondata": 
		loc = ADDOND
	else : loc = HOME
	log("Restoring to %s" % loc, xbmc.LOGNOTICE)
	display = file.replace('\\', '/').split('/')
	DP.update(0,'Installing Local Backup','', 'Please Wait')
	percent, errors, error = extract.all(file,loc,DP)
	clearS('build')
	DP.close()
	defaultSkin()
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, display[-1]), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B]No Thanks[/B]',yeslabel='[B]View Errors[/B]')
		if yes:
			if isinstance(errors, unicode):
				error = error.encode('utf-8')
			TextBoxes(ADDONTITLE, error.replace('\t',''))
	killxbmc()

def restoreExternal(type):
	source = DIALOG.browse(1, '[COLOR %s]Select the backup file you want to restore[/COLOR]' % COLOR2, 'files', '.zip', False, False)
	if source == "" or not source.endswith('.zip'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore: Cancelled[/COLOR]" % COLOR2)
		return
	try: 
		work = workingURL(source)
	except:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore: Error Valid URL[/COLOR]" % COLOR2)
		log("Not a working url, if source was local then use local restore option", xbmc.LOGNOTICE)
		log("External Source: %s" % source, xbmc.LOGNOTICE)
		return

	log("[RESTORE EXT BACKUP %s] File: %s " % (type.upper(), source), xbmc.LOGNOTICE)
	zipit = str(source).replace('\\', '/').split('/'); zname = zipit[-1]
	DP.create(ADDONTITLE,'[COLOR %s]Downloading Zip file' % COLOR2,'', 'Please Wait[/COLOR]')
	if type == "gui": loc = USERDATA
	elif type == "addondata": loc = ADDOND
	else : loc = HOME
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	if not os.path.exists(USERDATA): os.makedirs(USERDATA)
	if not os.path.exists(ADDOND): os.makedirs(ADDOND)
	if not os.path.exists(backup): os.makedirs(backup)
	if not os.path.exists(mybuilds): os.makedirs(mybuilds)
	file = os.path.join(mybuilds, zname)
	downloader.download(source, file, DP)
	
	DP.update(0,'Installing Local Backup','', 'Please Wait')
	percent, errors, error = extract.all(file,loc,DP)
	clearS('build')
	DP.close()
	defaultSkin()
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, zname), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B]No Thanks[/B]',yeslabel='[B]View Errors[/B]')
		if yes:
			TextBoxes(ADDONTITLE, error.replace('\t',''))
	killxbmc()

##########################
###DETERMINE PLATFORM#####
##########################

def platform():
	if xbmc.getCondVisibility('system.platform.android'):             return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):             return 'linux'
	elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'): return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):           return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):               return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):              return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):               return 'ios'
	elif xbmc.getCondVisibility('system.platform.darwin'):            return 'ios'

def Grab_Log(file=False, old=False):
	finalfile   = 0
	logfilepath = os.listdir(LOG)
	logsfound   = []

	for item in logfilepath:
		if old == True and item.endswith('.old.log'): logsfound.append(os.path.join(LOG, item))
		elif old == False and item.endswith('.log') and not item.endswith('.old.log'): logsfound.append(os.path.join(LOG, item))

	if len(logsfound) > 0:
		logsfound.sort(key=lambda f: os.path.getmtime(f))
		if file == True: return logsfound[-1]
		else:
			filename    = open(logsfound[-1], 'r')
			logtext     = filename.read()
			filename.close()
			return logtext
	else: 
		return False

def clearPackages(over=None):
	if os.path.exists(PACKAGES):
		try:
			for root, dirs, files in os.walk(PACKAGES):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					size = convertSize(getSize(PACKAGES))
					if over: yes=1
					else: yes=DIALOG.yesno("[COLOR %s]Delete Package Files" % COLOR2, "[COLOR %s]%s[/COLOR] files found / [COLOR %s]%s[/COLOR] in size." % (COLOR1, str(file_count), COLOR1, size), "Do you want to delete them?[/COLOR]", nolabel='[B]Don\'t Clear[/B]',yeslabel='[B]Clear Packages[/B]')
					if yes:
						for f in files: os.unlink(os.path.join(root, f))
						for d in dirs: shutil.rmtree(os.path.join(root, d))
						LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Clear Packages: Success![/COLOR]' % COLOR2)
				else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Clear Packages: None Found![/COLOR]' % COLOR2)
		except Exception, e:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Clear Packages: Error![/COLOR]' % COLOR2)
			log("Clear Packages Error: %s" % str(e), xbmc.LOGERROR)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Clear Packages: None Found![/COLOR]' % COLOR2)

def clearPackagesStartup():
	start = datetime.utcnow() - timedelta(minutes=5)
	file_count = 0; cleanupsize = 0
	if os.path.exists(PACKAGES):
		pack = os.listdir(PACKAGES)
		pack.sort(key=lambda f: os.path.getmtime(os.path.join(PACKAGES, f)))
		try:
			for item in pack:
				file = os.path.join(PACKAGES, item)
				lastedit = datetime.utcfromtimestamp(os.path.getmtime(file))
				if lastedit <= start:
					if os.path.isfile(file):
						file_count += 1
						cleanupsize += os.path.getsize(file)
						os.unlink(file)
					elif os.path.isdir(file): 
						cleanupsize += getSize(file)
						cleanfiles, cleanfold = cleanHouse(file)
						file_count += cleanfiles + cleanfold
						try:
							shutil.rmtree(file)
						except Exception, e:
							log("Failed to remove %s: %s" % (file, str(e), xbmc.LOGERROR))
			if file_count > 0: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Packages: Success: %s[/COLOR]' % (COLOR2, convertSize(cleanupsize)))
			else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Packages: None Found![/COLOR]' % COLOR2)
		except Exception, e:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Packages: Error![/COLOR]' % COLOR2)
			log("Clear Packages Error: %s" % str(e), xbmc.LOGERROR)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Packages: None Found![/COLOR]' % COLOR2)

def clearCache(over=None):
	PROFILEADDONDATA = os.path.join(PROFILE,'addon_data')
	dbfiles   = [
		(os.path.join(ADDONDATA, 'plugin.video.phstreams', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.bob', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.specto', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.genesis', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.exodus', 'cache.db')),
		(os.path.join(DATABASE,  'onechannelcache.db')),
		(os.path.join(DATABASE,  'saltscache.db')),
		(os.path.join(DATABASE,  'saltshd.lite.db'))]
		
	cachelist = [
		(PROFILEADDONDATA),
		(ADDONDATA),
		(os.path.join(HOME,'cache')),
		(os.path.join(HOME,'temp')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
		(os.path.join(ADDONDATA,'script.module.simple.downloader')),
		(os.path.join(ADDONDATA,'plugin.video.itv','Images')),
		(os.path.join(PROFILEADDONDATA,'script.module.simple.downloader')),
		(os.path.join(PROFILEADDONDATA,'plugin.video.itv','Images'))]
		
	delfiles = 0
	
	for item in cachelist:
		if os.path.exists(item) and not item in [ADDONDATA, PROFILEADDONDATA]:
			for root, dirs, files in os.walk(item):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					for f in files:
						if not f in LOGFILES:
							try:
								os.unlink(os.path.join(root, f))
								delfiles += 1
							except:
								pass
						else: log('Ignore Log File: %s' % f, xbmc.LOGNOTICE)
					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[Success] cleared %s files from %s" % (str(file_count), os.path.join(item,d)), xbmc.LOGNOTICE)
						except:
							log("[Failed] to wipe cache in: %s" % os.path.join(item,d), xbmc.LOGNOTICE)
		else:
			for root, dirs, files in os.walk(item):
				for d in dirs:
					if 'cache' in d.lower():
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[Success] wiped %s " % os.path.join(item,d), xbmc.LOGNOTICE)
						except:
							log("[Failed] to wipe cache in: %s" % os.path.join(item,d), xbmc.LOGNOTICE)
	if INCLUDEVIDEO == 'true':
		files = []
		if INCLUDEALL == 'true': files = dbfiles
		else:
			if INCLUDEBOB == 'true':     files.append(os.path.join(ADDONDATA, 'plugin.video.bob', 'cache.db'))
			if INCLUDEPHOENIX == 'true': files.append(os.path.join(ADDONDATA, 'plugin.video.phstreams', 'cache.db'))
			if INCLUDESPECTO == 'true':  files.append(os.path.join(ADDONDATA, 'plugin.video.specto', 'cache.db'))
			if INCLUDEGENESIS == 'true': files.append(os.path.join(ADDONDATA, 'plugin.video.genesis', 'cache.db'))
			if INCLUDEEXODUS == 'true':  files.append(os.path.join(ADDONDATA, 'plugin.video.exodus', 'cache.db'))
			if INCLUDEONECHAN == 'true': files.append(os.path.join(DATABASE,  'onechannelcache.db'))
			if INCLUDESALTS == 'true':   files.append(os.path.join(DATABASE,  'saltscache.db'))
			if INCLUDESALTSHD == 'true': files.append(os.path.join(DATABASE,  'saltshd.lite.db'))
		if len(files) > 0:
			for item in files:
				if os.path.exists(item):
					delfiles += 1
					try:
						textdb = database.connect(item)
						textexe = textdb.cursor()
					except Exception, e:
						log("DB Connection error: %s" % str(e), xbmc.LOGERROR)
						continue
					if 'Database' in item:
						try:
							textexe.execute("DELETE FROM url_cache")
							textexe.execute("VACUUM")
							textdb.commit()
							textexe.close()
							log("[Success] wiped %s" % item, xbmc.LOGNOTICE)
						except Exception, e:
							log("[Failed] wiped %s: %s" % (item, str(e)), xbmc.LOGNOTICE)
					else:
						textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
						for table in textexe.fetchall():
							try:
								textexe.execute("DELETE FROM %s" % table[0])
								textexe.execute("VACUUM")
								textdb.commit()
								log("[Success] wiped %s in %s" % (table, item), xbmc.LOGNOTICE)
							except Exception, e:
								log("[Failed] wiped %s in %s: %s" % (table, item, str(e)), xbmc.LOGNOTICE)
						textexe.close()
		else: log("Clear Cache: Clear Video Cache Not Enabled", xbmc.LOGNOTICE)
	LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Cache: Removed %s Files[/COLOR]' % (COLOR2, delfiles))

def checkSources():
	if not os.path.exists(SOURCES):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Sources.xml File Found![/COLOR]" % COLOR2)
		return False
	x      = 0
	bad    = []
	remove = []
	f      = open(SOURCES)
	a      = f.read()
	temp   = a.replace('\r','').replace('\n','').replace('\t','')
	match  = re.compile('<files>.+?</files>').findall(temp)
	f.close()
	if len(match) > 0:
		match2  = re.compile('<source>.+?<name>(.+?)</name>.+?<path pathversion="1">(.+?)</path>.+?<allowsharing>(.+?)</allowsharing>.+?</source>').findall(match[0])
		DP.create(ADDONTITLE, "[COLOR %s]Scanning Sources for Broken links[/COLOR]" % COLOR2)
		for name, path, sharing in match2:
			x     += 1
			perc   = int(percentage(x, len(match2)))
			DP.update(perc, '', "[COLOR %s]Checking [COLOR %s]%s[/COLOR]:[/COLOR]" % (COLOR2, COLOR1, name), "[COLOR %s]%s[/COLOR]" % (COLOR1, path))
			if 'http' in path:
				working = workingURL(path)
				if not working == True:
					bad.append([name, path, sharing, working])

		log("Bad Sources: %s" % len(bad), xbmc.LOGNOTICE)
		if len(bad) > 0:
			choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] Source(s) have been found Broken" % (COLOR1, len(bad), COLOR2),"Would you like to Remove all or choose one by one?[/COLOR]", yeslabel="[B]Remove All[/B]", nolabel="[B]Choose to Delete[/B]")
			if choice == 1:
				remove = bad
			else:
				for name, path, sharing, working in bad: 
					log("%s sources: %s, %s" % (name, path, working), xbmc.LOGNOTICE)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] was reported as non working" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, path), "[COLOR %s]%s[/COLOR]" % (COLOR1, working), yeslabel="[B]Remove Source[/B]", nolabel="[B]Keep Source[/B]"):
						remove.append([name, path, sharing, working])
						log("Removing Source %s" % name, xbmc.LOGNOTICE)
					else: log("Source %s was not removed" % name, xbmc.LOGNOTICE)
			if len(remove) > 0:
				for name, path, sharing, working in remove: 
					a = a.replace('\n        <source>\n            <name>%s</name>\n            <path pathversion="1">%s</path>\n            <allowsharing>%s</allowsharing>\n        </source>' % (name, path, sharing), '')
					log("Removing Source %s" % name, xbmc.LOGNOTICE)
				
				f = open(SOURCES, mode='w')
				f.write(str(a))
				f.close()
				alive = len(match) - len(bad)
				kept = len(bad) - len(remove)
				removed = len(remove)
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Checking sources for broken paths has been completed" % COLOR2, "Working: [COLOR %s]%s[/COLOR] | Kept: [COLOR %s]%s[/COLOR] | Removed: [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR2, COLOR1, alive, COLOR1, kept, COLOR1, removed))
			else: log("No Bad Sources to be removed.", xbmc.LOGNOTICE)
		else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]All Sources Are Working[/COLOR]" % COLOR2)
	else: log("No Sources Found", xbmc.LOGNOTICE)

def checkRepos():
	DP.create(ADDONTITLE, '[COLOR %s]Checking Repositories...[/COLOR]' % COLOR2)
	badrepos = []
	ebi('UpdateAddonRepos')
	repolist = glob.glob(os.path.join(ADDONS,'repo*'))
	if len(repolist) == 0:
		DP.close()
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Repositories Found![/COLOR]" % COLOR2)
		return
	sleeptime = len(repolist); start = 0;
	while start < sleeptime:
		start += 1
		if DP.iscanceled(): break
		perc = int(percentage(start, sleeptime))
		DP.update(perc, '', '[COLOR %s]Checking: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, repolist[start-1].replace(ADDONS, '')[1:]))
		xbmc.sleep(1000)
	if DP.iscanceled(): 
		DP.close()
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Enabling Addons Cancelled[/COLOR]" % COLOR2)
		sys.exit()
	DP.close()
	logfile = Grab_Log(False)
	fails = re.compile('CRepositoryUpdateJob(.+?)failed').findall(logfile)
	for item in fails:
		log("Bad Repository: %s " % item, xbmc.LOGNOTICE)
		brokenrepo = item.replace('[','').replace(']','').replace(' ','').replace('/','').replace('\\','')
		if not brokenrepo in badrepos:
			badrepos.append(brokenrepo)
	if len(badrepos) > 0:
		msg  = "[COLOR %s]Below is a list of Repositories that did not resolve.  This does not mean that they are Depreciated, sometimes hosts go down for a short period of time.  Please do serveral scans of your repository list before removing a repository just to make sure it is broken.[/COLOR][CR][CR][COLOR %s]" % (COLOR2, COLOR1)
		msg += '[CR]'.join(badrepos)
		msg += '[/COLOR]'
		TextBoxes("%s: Bad Repositories" % ADDONTITLE, msg)
	else: 
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]All Repositories Working![/COLOR]" % COLOR2)

#############################
####KILL XBMC ###############
#####THANKS GUYS @ TI########

def killxbmc(over=None):
	if over: choice = 1
	else: choice = DIALOG.yesno('Force Close Kodi', '[COLOR %s]You are about to close Kodi' % COLOR2, 'Would you like to continue?[/COLOR]', nolabel='[B]Cancel[/B]',yeslabel='[B]Force Close Kodi[/B]')
	if choice == 1:
		log("Force Closing Kodi: Platform[%s]" % str(platform()), xbmc.LOGNOTICE)
		os._exit(1)

##########################
### PURGE DATABASE #######
##########################
def purgeDb(name):
	#dbfile = name.replace('.db','').translate(None, digits)
	#if dbfile not in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']: return False
	#textfile = os.path.join(DATABASE, name)
	log('Purging DB %s.' % name, xbmc.LOGNOTICE)
	if os.path.exists(name):
		try:
			textdb = database.connect(name)
			textexe = textdb.cursor()
		except Exception, e:
			log("DB Connection Error: %s" % str(e), xbmc.LOGERROR)
			return False
	else: log('%s not found.' % name, xbmc.LOGERROR); return False
	textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	for table in textexe.fetchall():
		if table[0] == 'version': 
			log('Data from table `%s` skipped.' % table[0], xbmc.LOGDEBUG)
		else:
			try:
				textexe.execute("DELETE FROM %s" % table[0])
				textdb.commit()
				log('Data from table `%s` cleared.' % table[0], xbmc.LOGDEBUG)
			except Exception, e: log("DB Remove Table `%s` Error: %s" % (table[0], str(e)), xbmc.LOGERROR)
	textexe.close()
	log('%s DB Purging Complete.' % name, xbmc.LOGNOTICE)
	show = name.replace('\\', '/').split('/')
	LogNotify("[COLOR %s]Purge Database[/COLOR]" % COLOR1, "[COLOR %s]%s Complete[/COLOR]" % (COLOR2, show[len(show)-1]))

def oldThumbs():
	start  = getSize(THUMBS)
	dbfile = os.path.join(DATABASE, latestDB('Textures'))
	use    = 10
	week   = TODAY - timedelta(days=7)
	ids    = []
	images = []
	if os.path.exists(dbfile):
		try:
			textdb = database.connect(dbfile)
			textexe = textdb.cursor()
		except Exception, e:
			log("DB Connection Error: %s" % str(e), xbmc.LOGERROR)
			return False
	else: log('%s not found.' % dbfile, xbmc.LOGERROR); return False
	textexe.execute("SELECT idtexture FROM sizes WHERE usecount < %s AND lastusetime < %s" % (use, str(week)))
	for rows in textexe:
		ids.append(rows["idtexture"])
		textexe.execute("SELECT cachedurl FROM texture WHERE id = %s" % rows["idtexture"])
		for rows2 in textexe:
			images.append(rows2["cachedurl"])
	log("%s total thumbs cleaned up." % str(len(images)), xbmc.LOGNOTICE)
	for id in ids:       
		textexe.execute("DELETE FROM sizes   WHERE idtexture = %s" % id)
		textexe.execute("DELETE FROM texture WHERE id        = %s" % id)
	textexe.execute("VACUUM")
	textdb.commit()
	textexe.close()
	for image in images:
		path = os.path.join(THUMBS, image)
		try:
			os.remove(path)
		except:
			pass
	finish = getSize(THUMBS)
	removed = convertSize(start - finish)
	if len(images) > 0: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Thumbs: %s Files / %.02f MB[/COLOR]!' % (COLOR2, str(len(images)), removed))
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Clear Thumbs: None Found![/COLOR]' % COLOR2)