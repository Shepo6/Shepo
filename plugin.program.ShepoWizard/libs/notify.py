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

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
from resources.libs import wizard as wiz
from datetime import date, datetime, timedelta

ADDON_ID       = uservar.ADDON_ID
ADDON          = wiz.addonId(ADDON_ID)
VERSION        = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH      = wiz.addonInfo(ADDON_ID,'path')
ADDONTITLE     = uservar.ADDONTITLE
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
PACKAGES       = os.path.join(ADDONS,   'packages')
ADDONDATA      = os.path.join(USERDATA, 'addon_data', ADDON_ID)
FANART         = os.path.join(ADDONPATH,   'notificationwithoutlogo.jpg')
ICON           = os.path.join(ADDONPATH,   'icon.png')
ART            = os.path.join(ADDONPATH,   'resources', 'art')
ADVANCED       = os.path.join(USERDATA,  'advancedsettings.xml')
NOTIFY         = wiz.getS('notify')
NOTEID         = wiz.getS('noteid')
NOTEDISMISS    = wiz.getS('notedismiss')
BUILDNAME      = wiz.getS('buildname')
BUILDVERSION   = wiz.getS('buildversion')
LATESTVERSION  = wiz.checkBuild(BUILDNAME, 'version')
TODAY          = date.today()
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
UPDATECHECK    = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
FONTSETTINGS   = uservar.FONTSETTINGS if not uservar.FONTSETTINGS == '' else "Font14"
BACKGROUND     = uservar.BACKGROUND if not uservar.BACKGROUND == '' or not wiz.workingURL(uservar.BACKGROUND) else FANART
HEADERTYPE     = uservar.HEADERTYPE if uservar.HEADERTYPE == 'Image' else 'Text'
HEADERMESSAGE  = uservar.HEADERMESSAGE
FONTHEADER     = uservar.FONTHEADER if not uservar.FONTHEADER == '' else "Font16"
HEADERIMAGE    = uservar.HEADERIMAGE
THEME1         = uservar.THEME1
THEME2         = uservar.THEME2
THEME3         = uservar.THEME3
THEME4         = uservar.THEME4
THEME5         = uservar.THEME5
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2

############################
###NOTIFICATIONS############
####THANKS GUYS @ TVADDONS##
######MODIFIED BY AFTERMATH#
ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108

def artwork(file):
	if   file == 'button': return os.path.join(ART, 'Button', 'button-focus_lightblue.png'), os.path.join(ART, 'Button', 'button-focus_grey.png')
	elif file == 'radio' : return os.path.join(ART, 'RadioButton', 'MenuItemFO.png'), os.path.join(ART, 'RadioButton', 'MenuItemNF.png'), os.path.join(ART, 'RadioButton', 'radiobutton-focus.png'), os.path.join(ART, 'RadioButton', 'radiobutton-nofocus.png')
	elif file == 'slider': return os.path.join(ART, 'Slider', 'osd_slider_nib.png'), os.path.join(ART, 'Slider', 'osd_slider_nibNF.png'), os.path.join(ART, 'Slider', 'slider1.png'), os.path.join(ART, 'Slider', 'slider1.png')

def notification(msg='', resize=True, L=40, T=25, W=1200, H=664, TxtColor='0xFFFFFFFF', Font=FONTSETTINGS, BorderWidth=15):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), BACKGROUND, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
			self.addControl(self.BG)
			#title
			if HEADERTYPE == 'Image':
				iLogoW=144; iLogoH=68
				self.iLogo=xbmcgui.ControlImage((L+(W/2))-(iLogoW/2),T+10,iLogoW,iLogoH,HEADERIMAGE,aspectRatio=0)
				self.addControl(self.iLogo)
			else:
				title = HEADERMESSAGE
				times = int(float(FONTHEADER[-2:]))
				temp = title.replace('[', '<').replace(']', '>')
				temp = re.sub('<[^<]+?>', '', temp)
				title_width = len(str(temp))*(times - 1)
				title = THEME3 % title
				self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font=FONTHEADER,textColor='0xFF1E90FF')
				self.addControl(self.title)
				self.title.setText(title)
			#body
			msg = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+BorderWidth+10,T+30+BorderWidth,W-(BorderWidth*2)-20,H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			#buttons
			
			focus, nofocus = artwork('button')
			w1      = int((W-(BorderWidth*5))/3); h1 = 35
			t       = int(T+H-h1-(BorderWidth*1.5))
			space   = int(L+(BorderWidth*1.5))
			dismiss = int(space+w1+BorderWidth)
			later   = int(dismiss+w1+BorderWidth)
			
			self.buttonDismiss=xbmcgui.ControlButton(dismiss,t,w1,h1,"Dismiss",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonRemindMe=xbmcgui.ControlButton(later,t,w1,h1,"Remind Me Later",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonDismiss); self.addControl(self.buttonRemindMe)
			self.buttonRemindMe.controlLeft(self.buttonDismiss); self.buttonRemindMe.controlRight(self.buttonDismiss)
			self.buttonDismiss.controlLeft(self.buttonRemindMe); self.buttonDismiss.controlRight(self.buttonRemindMe)
			self.setFocus(self.buttonRemindMe);

		def doRemindMeLater(self):
			try:
				wiz.setS("notedismiss","false")
				wiz.log("[Notification] NotifyID %s Remind Me Later" % wiz.getS('noteid'), xbmc.LOGNOTICE)
			except: pass
			self.CloseWindow()

		def doDismiss(self):
			try:    
				wiz.setS("notedismiss","true")
				wiz.log("[Notification] NotifyID %s Dismissed" % wiz.getS('noteid'), xbmc.LOGNOTICE)
			except: pass
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doRemindMeLater()
			elif action == ACTION_NAV_BACK: self.doRemindMeLater()

		def onControl(self,control):
			if   control==self.buttonRemindMe: self.doRemindMeLater()
			elif control== self.buttonDismiss: self.doDismiss()
			else:
				try:    self.setFocus(self.buttonRemindMe)
				except: pass
		
		def CloseWindow(self): self.close()
	if resize==False: maxW=1280; maxH=720; W=int(maxW/1.5); H=int(maxH/1.5); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth)
	TempWindow.doModal()
	del TempWindow

def testNotification(msg='', resize=True, L=40, T=25, W=1200, H=664, TxtColor='0xFFFFFFFF', Font=FONTSETTINGS, BorderWidth=15):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border)
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), BACKGROUND, aspectRatio=0, colorDiffuse='0xFFFFFFFFF')
			self.addControl(self.BG)
			#title
			if HEADERTYPE == 'Image':
				iLogoW=144; iLogoH=68
				self.iLogo=xbmcgui.ControlImage((L+(W/2))-(iLogoW/2),T+10,iLogoW,iLogoH,HEADERIMAGE,aspectRatio=0)
				self.addControl(self.iLogo); 
			else:
				title = HEADERMESSAGE
				times = int(float(FONTHEADER[-2:]))
				temp = title.replace('[', '<').replace(']', '>')
				temp = re.sub('<[^<]+?>', '', temp)
				title_width = len(str(temp))*(times - 1)
				title = THEME3 % title
				self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font=FONTHEADER,textColor='0xFF1E90FF')
				self.addControl(self.title)
				self.title.setText(title)
			#body
			msg = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+BorderWidth+10,T+30+BorderWidth,W-(BorderWidth*2)-20,H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			#buttons
			focus, nofocus = artwork('button')
			w1      = int((W-(BorderWidth*5))/3); h1 = 35
			t       = int(T+H-h1-(BorderWidth*1.5))
			space   = int(L+(BorderWidth*1.5))
			dismiss = int(space+w1+BorderWidth)
			later   = int(dismiss+w1+BorderWidth)
			
			self.buttonDismiss=xbmcgui.ControlButton(dismiss,t,w1,h1,"Dismiss",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonRemindMe=xbmcgui.ControlButton(later,t,w1,h1,"Remind Me Later",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonDismiss); self.addControl(self.buttonRemindMe)
			self.buttonRemindMe.controlLeft(self.buttonDismiss); self.buttonRemindMe.controlRight(self.buttonDismiss)
			self.buttonDismiss.controlLeft(self.buttonRemindMe); self.buttonDismiss.controlRight(self.buttonRemindMe)
			self.setFocus(self.buttonRemindMe)

		def doRemindMeLater(self):
			wiz.log("[Test Notification] Remind Me Later", xbmc.LOGNOTICE)
			self.CloseWindow()

		def doDismiss(self):
			wiz.log("[Test Notification] C", xbmc.LOGNOTICE)
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doRemindMeLater()
			elif action == ACTION_NAV_BACK: self.doRemindMeLater()

		def onControl(self,control):
			if   control==self.buttonRemindMe: self.doRemindMeLater()
			elif control== self.buttonDismiss: self.doDismiss()
			else:
				try:    self.setFocus(self.buttonRemindMe)
				except: pass

		def CloseWindow(self): self.close()
	if resize==False: maxW=1280; maxH=720; W=int(maxW/1.5); H=int(maxH/1.5); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal()
	del TempWindow

def updateWindow(TxtColor='0xFFFFFFFF', Font='font13', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
			if BUILDNAME == "" or not wiz.checkBuild(BUILDNAME, 'version'):
				bgArt   = FANART
				icon    = ICON
				build   = "Test Window"
				version = '1.0'
				latest  = '1.0'
			else:
				bgArt   = wiz.checkBuild(BUILDNAME, 'fanart')
				icon    = wiz.checkBuild(BUILDNAME, 'icon')
				build   = BUILDNAME
				version = BUILDVERSION
				latest  = wiz.checkBuild(BUILDNAME, 'version')
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth, T+BorderWidth, W-(BorderWidth*2), H-(BorderWidth*2), bgArt, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
			self.addControl(self.BG)
			#title
			times = int(float(Font[-2:]))
			title = ADDONTITLE
			temp = title.replace('[', '<').replace(']', '>')
			temp = re.sub('<[^<]+?>', '', temp)
			title_width = len(str(temp))*(times - 1)
			title   = THEME2 % title
			self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font='font14',textColor='0xFF1E90FF')
			self.addControl(self.title)
			self.title.setText(title)
			#update
			if version < latest: msg = "Update avaliable for installed build:\n[COLOR %s]%s[/COLOR]\n\nYour Current Shepo Build Version v[COLOR %s]%s[/COLOR]\nLatest Shepo Build Version: v[COLOR %s]%s[/COLOR]\n\n[COLOR %s]*Recommened: Fresh install (Below)[/COLOR]" % (COLOR1, build, COLOR1, version, COLOR1, latest, COLOR1)
			else: msg = "Running latest version of installed build:\n[COLOR %s]%s[/COLOR]\n\nYour Current Shepo Build Version: v[COLOR %s]%s[/COLOR]\nLatest Shepo Build Version: v[COLOR %s]%s[/COLOR]\n\n[COLOR %s]*Recommended: Fresh install (Below)[/COLOR]" % (COLOR1, build, COLOR1, version, COLOR1, latest, COLOR1)
			msg = THEME2 % msg
			self.update=xbmcgui.ControlTextBox(L+(BorderWidth*2),T+BorderWidth+30,W-150-(BorderWidth*3),H-(BorderWidth*2)-30,font=Font,textColor=TxtColor)
			self.addControl(self.update)
			self.update.setText(msg)
			#icon
			self.Icon=xbmcgui.ControlImage(L+W-(BorderWidth*2)-150, T+BorderWidth+35, 150, 150, icon, aspectRatio=0, colorDiffuse='0xAFFFFFFF')
			self.addControl(self.Icon)
			#buttons
			focus, nofocus = artwork('button')
			w1      = int((W-(BorderWidth*5))/3); h1 = 35
			t       = int(T+H-h1-(BorderWidth*1.5))
			fresh   = int(L+(BorderWidth*1.5))
			normal  = int(fresh+w1+BorderWidth)
			ignore  = int(normal+w1+BorderWidth)
			
			self.buttonFRESH=xbmcgui.ControlButton(fresh,t, w1,h1,"Fresh Install",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonNORMAL=xbmcgui.ControlButton(normal,t,w1,h1,"Normal Install",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonIGNORE=xbmcgui.ControlButton(ignore,t,w1,h1,"Ignore 3 days",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonFRESH); self.addControl(self.buttonNORMAL); self.addControl(self.buttonIGNORE)
			self.buttonIGNORE.controlLeft(self.buttonNORMAL); self.buttonIGNORE.controlRight(self.buttonFRESH)
			self.buttonNORMAL.controlLeft(self.buttonFRESH); self.buttonNORMAL.controlRight(self.buttonIGNORE)
			self.buttonFRESH.controlLeft(self.buttonIGNORE); self.buttonFRESH.controlRight(self.buttonNORMAL)
			self.setFocus(self.buttonFRESH)

		def doFreshInstall(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Fresh Install build]" % (BUILDVERSION, LATESTVERSION), xbmc.LOGNOTICE)
			wiz.log("[Check Updates] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=install&name=%s&url=fresh' % (ADDON_ID, urllib.quote_plus(BUILDNAME))
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		def doNormalInstall(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Normal Install build]" % (BUILDVERSION, LATESTVERSION), xbmc.LOGNOTICE)
			wiz.log("[Check Updates] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=install&name=%s&url=normal' % (ADDON_ID, urllib.quote_plus(BUILDNAME))
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		def doIgnore(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Ignore 3 Days]" % (BUILDVERSION, LATESTVERSION), xbmc.LOGNOTICE)
			wiz.log("[Check Updates] [Next Check: %s]" % str(THREEDAYS), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(THREEDAYS))
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doIgnore()
			elif action == ACTION_NAV_BACK: self.doIgnore()
			elif action == ACTION_MOVE_LEFT and not F: self.setFocus(self.buttonIGNORE)
			elif action == ACTION_MOVE_RIGHT and not F: self.setFocus(self.buttonIGNORE)

		def onControl(self,control):
			if   control==self.buttonIGNORE: self.doIgnore()
			elif control==self.buttonNORMAL: self.doNormalInstall()
			elif control==self.buttonFRESH:  self.doFreshInstall()
			else:
				try:    self.setFocus(self.buttonIGNORE); 
				except: pass

		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(700); H=int(350); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow

def firstRun(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font12',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
			self.addControl(self.BG)
			#title
			title = ADDONTITLE
			times = int(float(Font[-2:]))
			temp = title.replace('[', '<').replace(']', '>')
			temp = re.sub('<[^<]+?>', '', temp)
			title_width = len(str(temp))*(times - 1)
			title   = THEME3 % title
			self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font='font14',textColor='0xFF1E90FF')
			self.addControl(self.title)
			self.title.setText(title)
			#welcome message
			msg   = "Currently no build installed from %s.\n\nSelect 'Build Menu' to install a Shepo Build or 'Ignore' to never see this message again.\n\n Thank you for choosing The %s." % (ADDONTITLE, ADDONTITLE)
			msg   = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+(BorderWidth*2),T+30+BorderWidth,W-(BorderWidth*4),H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			#buttons
			focus, nofocus = artwork('button')
			w1        = int((W-(BorderWidth*5))/3); h1 = 35
			t         = int(T+H-h1-(BorderWidth*1.5))
			save      = int(L+(BorderWidth*1.5))
			buildmenu = int(save+w1+BorderWidth)
			ignore    = int(buildmenu+w1+BorderWidth)
			self.buttonSAVEMENU=xbmcgui.ControlButton(save,t,w1,h1,"Save Data Menu",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonBUILDMENU=xbmcgui.ControlButton(buildmenu,t,w1,h1,"Build Menu",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonIGNORE=xbmcgui.ControlButton(ignore,t,w1,h1,"Ignore",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonSAVEMENU); self.addControl(self.buttonBUILDMENU); self.addControl(self.buttonIGNORE)
			self.buttonIGNORE.controlLeft(self.buttonBUILDMENU); self.buttonIGNORE.controlRight(self.buttonSAVEMENU)
			self.buttonBUILDMENU.controlLeft(self.buttonSAVEMENU); self.buttonBUILDMENU.controlRight(self.buttonIGNORE)
			self.buttonSAVEMENU.controlLeft(self.buttonIGNORE); self.buttonSAVEMENU.controlRight(self.buttonBUILDMENU)
			self.setFocus(self.buttonIGNORE)

		def doSaveMenu(self):
			wiz.log("[Check Updates] [User Selected: Open Save Data Menu] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=savedata' % ADDON_ID
			xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)

		def doBuildMenu(self):
			wiz.log("[Check Updates] [User Selected: Open Build Menu] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=builds' % ADDON_ID
			xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)

		def doIgnore(self):
			wiz.log("[First Run] [User Selected: Ignore Build Menu] [Next Check: %s]" % str(NEXTCHECK), xbmc.LOGNOTICE)
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doIgnore()
			elif action == ACTION_NAV_BACK: self.doIgnore()
			elif action == ACTION_MOVE_LEFT and not F: self.setFocus(self.buttonBUILDMENU)
			elif action == ACTION_MOVE_RIGHT and not F: self.setFocus(self.buttonIGNORE)

		def onControl(self,control):
			if   control==self.buttonIGNORE: self.doIgnore()
			elif control==self.buttonBUILDMENU:  self.doBuildMenu()
			elif control==self.buttonSAVEMENU:  self.doSaveMenu()
			else:
				try:    self.setFocus(self.buttonIGNORE); 
				except: pass

		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(700); H=int(300); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow

def contact(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font12',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
			self.addControl(self.BG)
			#title
			title = ADDONTITLE
			times = int(float(Font[-2:]))
			temp = title.replace('[', '<').replace(']', '>')
			temp = re.sub('<[^<]+?>', '', temp)
			title_width = len(str(temp))*(times - 1)
			title = THEME3 % title
			self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font='font14',textColor='0xFF1E90FF')
			self.addControl(self.title)
			self.title.setText(title)
			#icon
			self.Icon=xbmcgui.ControlImage(L+(BorderWidth*2), T+BorderWidth+40, 150, 150, ICON, aspectRatio=0, colorDiffuse='0xAFFFFFFF')
			self.addControl(self.Icon)
			#welcome message
			msg = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+160+(BorderWidth*3),T+45,W-170-(BorderWidth*3),H-(BorderWidth*2)-50,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)

		def doExit(self):
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doExit()
			elif action == ACTION_NAV_BACK: self.doExit()

		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(700); H=int(250); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow

def apkInstaller(apk):
	class APKInstaller(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.shut=kwargs['close_time']
			xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
			xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")

		def onFocus(self,controlID): pass

		def onClick(self,controlID): self.CloseWindow()

		def onAction(self,action):
			if action in [ACTION_PREVIOUS_MENU, ACTION_BACKSPACE, ACTION_NAV_BACK, ACTION_SELECT_ITEM, ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_LONG_CLICK]: self.CloseWindow()

		def CloseWindow(self):
			xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
			xbmc.sleep(400)
			self.close()
	
	xbmc.executebuiltin('Skin.SetString(apkinstaller, Thank you for Downloading using Shepo APK Installer, Now that %s has been downloaded[CR]Click install on the next window!)' % apk)
	popup = APKInstaller('APK.xml', ADDON.getAddonInfo('path'), 'DefaultSkin', close_time=34)
	popup.doModal()
	del popup

def autoConfig(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font12',BorderWidth=10):
			buttonfocus, buttonnofocus = artwork('button')
			radiobgfocus, radiobgnofocus, radiofocus, radionofocus = artwork('radio')
			slidernibfocus, slidernibnofocus, sliderfocus, slidernofocus = artwork('slider')
			image_path = os.path.join(ART, 'ContentPanel.png')
			boxbg = os.path.join(ART, 'bgg2.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
			self.addControl(self.BG)
			top = T+BorderWidth
			leftside = L+BorderWidth
			rightside = L+(W/2)-(BorderWidth*2)
			firstrow = top+30
			secondrow = firstrow+275+(BorderWidth/2)
			currentwidth = ((W/2)-(BorderWidth*4))/2
			
			header = '[COLOR %s]Advanced Settings Configurator[/COLOR]' % (COLOR2)
			self.Header=xbmcgui.ControlLabel(L, top, W, 30, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header)
			top += 30+BorderWidth
			self.bgarea = xbmcgui.ControlImage(leftside, firstrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea)
			self.bgarea2 = xbmcgui.ControlImage(rightside+BorderWidth+BorderWidth, firstrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea2)
			self.bgarea3 = xbmcgui.ControlImage(leftside, secondrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea3)
			self.bgarea4 = xbmcgui.ControlImage(rightside+BorderWidth+BorderWidth, secondrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.bgarea4)
			
			header = '[COLOR %s]Video Cache Size[/COLOR]' % (COLOR2)
			self.Header2=xbmcgui.ControlLabel(leftside+BorderWidth, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header2)
			freeMemory = int(float(wiz.getInfo('System.Memory(free)')[:-2])*.33)
			recMemory = int(float(wiz.getInfo('System.Memory(free)')[:-2])*.23)
			msg3 = "[COLOR %s]Number of bytes used for buffering streams in memory.  When set to [COLOR %s]0[/COLOR] the cache will be written to disk instead of RAM.  Note: For the memory size set here, Kodi will require 3x the amount of RAM to be free. Setting this too high might cause Kodi to crash if it can't get enough RAM(1/3 of Free Memory: [COLOR %s]%s[/COLOR])[/COLOR]" % (COLOR2, COLOR1, COLOR1, freeMemory)
			self.Support3=xbmcgui.ControlTextBox(leftside+int(BorderWidth*1.5), firstrow+30+BorderWidth, (W/2)-(BorderWidth*4), 150, font='font12', textColor=TxtColor)
			self.addControl(self.Support3)
			self.Support3.setText(msg3)
			self.videoCacheSize=xbmcgui.ControlSlider(leftside+int(BorderWidth*1.5), firstrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
			self.addControl(self.videoCacheSize)
			self.videomin = 0; self.videomax = freeMemory if freeMemory < 2000 else 2000
			self.recommendedVideo = recMemory if recMemory < 500 else 500; self.currentVideo = self.recommendedVideo
			videopos = wiz.percentage(self.currentVideo, self.videomax)
			self.videoCacheSize.setPercent(videopos)
			current1 = '[COLOR %s]Current:[/COLOR] [COLOR %s]%s MB[/COLOR]' % (COLOR1, COLOR2, self.currentVideo)
			recommended1 = '[COLOR %s]Recommended:[/COLOR] [COLOR %s]%s MB[/COLOR]' % (COLOR1, COLOR2, self.recommendedVideo)
			self.currentVideo1=xbmcgui.ControlTextBox(leftside+BorderWidth,firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.currentVideo1)
			self.currentVideo1.setText(current1)
			self.recommendedVideo1=xbmcgui.ControlTextBox(leftside+BorderWidth+currentwidth,firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.recommendedVideo1)
			self.recommendedVideo1.setText(recommended1)
			
			header = '[COLOR %s]CURL Timeout/CURL Low Speed[/COLOR]' % (COLOR2)
			self.Header3=xbmcgui.ControlLabel(rightside+BorderWidth, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header3)
			msg3 = "[COLOR %s][B]curlclienttimeout[/B] is the time in seconds for how long it takes for libcurl connection will timeout and [B]curllowspeedtime[/B] is the time in seconds for libcurl to consider a connection lowspeed.  For slower connections set it to 20.[/COLOR]" % COLOR2
			self.Support3=xbmcgui.ControlTextBox(rightside+int(BorderWidth*3.5), firstrow+30+BorderWidth, (W/2)-(BorderWidth*4), 150, font='font12', textColor=TxtColor)
			self.addControl(self.Support3)
			self.Support3.setText(msg3)
			self.CURLTimeout=xbmcgui.ControlSlider(rightside+int(BorderWidth*3.5),firstrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
			self.addControl(self.CURLTimeout)
			self.curlmin = 0; self.curlmax = 20
			self.recommendedCurl = 10; self.currentCurl = self.recommendedCurl
			curlpos = wiz.percentage(self.currentCurl, self.curlmax)
			self.CURLTimeout.setPercent(curlpos)
			current2 = '[COLOR %s]Current:[/COLOR] [COLOR %s]%ss[/COLOR]' % (COLOR1, COLOR2, self.currentCurl)
			recommended2 = '[COLOR %s]Recommended:[/COLOR] [COLOR %s]%ss[/COLOR]' % (COLOR1, COLOR2, self.recommendedCurl)
			self.currentCurl2=xbmcgui.ControlTextBox(rightside+(BorderWidth*3),firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.currentCurl2)
			self.currentCurl2.setText(current2)
			self.recommendedCurl2=xbmcgui.ControlTextBox(rightside+(BorderWidth*3)+currentwidth,firstrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.recommendedCurl2)
			self.recommendedCurl2.setText(recommended2)
			
			header = '[COLOR %s]Read Buffer Factor[/COLOR]' % (COLOR2)
			self.Header4=xbmcgui.ControlLabel(leftside, secondrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header4)
			msg3 = "[COLOR %s]The value of this setting is a multiplier of the default limit. If Kodi is loading a typical bluray raw file at 36 Mbit/s, then a value of 2 will need at least 72 Mbit/s of network bandwidth. However, unlike with the RAM setting, you can safely increase this value however high you want, and Kodi won't crash.[/COLOR]" % COLOR2
			self.Support3=xbmcgui.ControlTextBox(leftside+int(BorderWidth*1.5), secondrow+30+BorderWidth, (W/2)-(BorderWidth*4), 150, font='font12', textColor=TxtColor)
			self.addControl(self.Support3)
			self.Support3.setText(msg3)
			self.readBufferFactor=xbmcgui.ControlSlider(leftside+int(BorderWidth*1.5), secondrow+210,(W/2)-(BorderWidth*5),20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
			self.addControl(self.readBufferFactor)
			self.readmin = 0; self.readmax = 10
			self.recommendedRead = 5; self.currentRead = self.recommendedRead
			readpos = wiz.percentage(self.currentRead, self.readmax)
			self.readBufferFactor.setPercent(readpos)
			current3 = '[COLOR %s]Current:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, self.currentRead)
			recommended3 = '[COLOR %s]Recommended:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, self.recommendedRead)
			self.currentRead3=xbmcgui.ControlTextBox(leftside+BorderWidth,secondrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.currentRead3)
			self.currentRead3.setText(current3)
			self.recommendedRead3=xbmcgui.ControlTextBox(leftside+BorderWidth+currentwidth,secondrow+235,currentwidth,20,font=Font,textColor=TxtColor)
			self.addControl(self.recommendedRead3)
			self.recommendedRead3.setText(recommended3)
			
			header = '[COLOR %s]Buffer Mode[/COLOR]' % (COLOR2)
			self.Header4=xbmcgui.ControlLabel(rightside+BorderWidth, secondrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
			self.addControl(self.Header4)
			msg4 = "[COLOR %s]This setting will force Kodi to use a cache for all video files, including local network, internet, and even the local hard drive. Default value is 0 and will only cache videos that use internet file paths/sources.[/COLOR]" % COLOR2
			self.Support4=xbmcgui.ControlTextBox(rightside+int(BorderWidth*3.5), secondrow+30+BorderWidth, (W/2)-(BorderWidth*4), 110, font='font12', textColor=TxtColor)
			self.addControl(self.Support4)
			self.Support4.setText(msg4)
			B1 = secondrow+130+BorderWidth; B2 = B1+30; B3 = B2+30; B4 = B3+30;
			self.Button0 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B1, (W/2)-(BorderWidth*4), 30, '0: Buffer all internet filesystems', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.Button1 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B2, (W/2)-(BorderWidth*4), 30, '1: Buffer all filesystems', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.Button2 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B3, (W/2)-(BorderWidth*4), 30, '2: Only buffer true internet filesystems', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.Button3 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3), B4, (W/2)-(BorderWidth*4), 30, '3: No Buffer', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
			self.addControl(self.Button0)
			self.addControl(self.Button1)
			self.addControl(self.Button2)
			self.addControl(self.Button3)
			self.Button0.setSelected(False)
			self.Button1.setSelected(False)
			self.Button2.setSelected(True)
			self.Button3.setSelected(False)
			
			self.buttonWrite=xbmcgui.ControlButton(leftside,T+H-40-BorderWidth,(W/2)-(BorderWidth*2),35,"Write File",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
			self.buttonCancel=xbmcgui.ControlButton(rightside+BorderWidth*2,T+H-40-BorderWidth,(W/2)-(BorderWidth*2),35,"Cancel",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
			self.addControl(self.buttonWrite); self.addControl(self.buttonCancel)
			
			self.buttonWrite.controlLeft(self.buttonCancel); self.buttonWrite.controlRight(self.buttonCancel); self.buttonWrite.controlUp(self.Button3); self.buttonWrite.controlDown(self.videoCacheSize)
			self.buttonCancel.controlLeft(self.buttonWrite); self.buttonCancel.controlRight(self.buttonWrite); self.buttonCancel.controlUp(self.Button3); self.buttonCancel.controlDown(self.videoCacheSize)
			self.videoCacheSize.controlUp(self.buttonWrite); self.videoCacheSize.controlDown(self.CURLTimeout)
			self.CURLTimeout.controlUp(self.videoCacheSize); self.CURLTimeout.controlDown(self.readBufferFactor)
			self.readBufferFactor.controlUp(self.CURLTimeout); self.readBufferFactor.controlDown(self.Button0)
			self.Button0.controlUp(self.CURLTimeout); self.Button0.controlDown(self.Button1); self.Button0.controlLeft(self.readBufferFactor); self.Button0.controlRight(self.readBufferFactor);
			self.Button1.controlUp(self.Button0); self.Button1.controlDown(self.Button2); self.Button1.controlLeft(self.readBufferFactor); self.Button1.controlRight(self.readBufferFactor);
			self.Button2.controlUp(self.Button1); self.Button2.controlDown(self.Button3); self.Button2.controlLeft(self.readBufferFactor); self.Button2.controlRight(self.readBufferFactor);
			self.Button3.controlUp(self.Button2); self.Button3.controlDown(self.buttonWrite); self.Button3.controlLeft(self.readBufferFactor); self.Button3.controlRight(self.readBufferFactor);
			self.setFocus(self.videoCacheSize)
			
		def doExit(self):
			self.CloseWindow()
			
		def updateCurrent(self, control):
			if control == self.videoCacheSize:
				self.currentVideo = (self.videomax)*self.videoCacheSize.getPercent()/100
				current = '[COLOR %s]Current:[/COLOR] [COLOR %s]%s MB[/COLOR]' % (COLOR1, COLOR2, int(self.currentVideo))
				self.currentVideo1.setText(current)
				
			elif control == self.CURLTimeout:
				self.currentCurl = (self.curlmax)*self.CURLTimeout.getPercent()/100
				current = '[COLOR %s]Current:[/COLOR] [COLOR %s]%ss[/COLOR]' % (COLOR1, COLOR2, int(self.currentCurl))
				self.currentCurl2.setText(current)
				
			elif control == self.readBufferFactor:
				self.currentRead = (self.readmax)*self.readBufferFactor.getPercent()/100
				current = '[COLOR %s]Current:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, int(self.currentRead))
				self.currentRead3.setText(current)
				
			elif control in [self.Button0, self.Button1, self.Button2, self.Button3]:
				self.Button0.setSelected(False)
				self.Button1.setSelected(False)
				self.Button2.setSelected(False)
				self.Button3.setSelected(False)
				control.setSelected(True)

		def doWrite(self):
			#self.currentVideo = int((self.videomax-20)*self.videoCacheSize.getPercent()/100+20)*1024*1024
			#self.currentCurl = int((self.curlmax)*self.CURLTimeout.getPercent()/100)
			#self.currentRead = int((self.readmax)*self.readBufferFactor.getPercent()/100)
			if   self.Button0.isSelected(): buffermode = 0
			elif self.Button1.isSelected(): buffermode = 1
			elif self.Button2.isSelected(): buffermode = 2
			elif self.Button3.isSelected(): buffermode = 3
			if os.path.exists(ADVANCED):
				choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]There is currently an active [COLOR %s]AdvancedSettings.xml[/COLOR], would you like to remove it and continue?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B]Remove Settings[/B]", nolabel="[B]Cancel Write[/B]")
				if choice == 0: return
				try: os.remove(ADVANCED)
				except: f = open(ADVANCED, 'w'); f.close()
			if KODIV < 17:
				with open(ADVANCED, 'w+') as f:
					f.write('<advancedsettings>\n')
					f.write('	<network>\n')
					f.write('		<buffermode>%s</buffermode>\n' % buffermode)
					f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % int(self.currentVideo*1024*1024))
					f.write('		<readbufferfactor>%s</readbufferfactor>\n' % self.currentRead)
					f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
					f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
					f.write('	</network>\n')
					f.write('</advancedsettings>\n')
				f.close()
			else:
				with open(ADVANCED, 'w+') as f:
					f.write('<advancedsettings>\n')
					f.write('	<cache>\n')
					f.write('		<buffermode>%s</buffermode>\n' % buffermode)
					f.write('		<memorysize>%s</memorysize>\n' % int(self.currentVideo*1024*1024))
					f.write('		<readfactor>%s</readfactor>\n' % self.currentRead)
					f.write('	</cache>\n')
					f.write('	<network>\n')
					f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
					f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
					f.write('	</network>\n')
					f.write('</advancedsettings>\n')
				f.close()
			self.CloseWindow()
			
		def onControl(self, control):
			if   control==self.buttonWrite: self.doWrite()
			elif control==self.buttonCancel:  self.doExit()

		def onAction(self, action):
			try: F=self.getFocus()
			except: F=False
			if   F      == self.videoCacheSize:   self.updateCurrent(self.videoCacheSize)
			elif F      == self.CURLTimeout:      self.updateCurrent(self.CURLTimeout)
			elif F      == self.readBufferFactor: self.updateCurrent(self.readBufferFactor)
			elif F      in [self.Button0, self.Button1, self.Button2, self.Button3] and action in [ACTION_MOUSE_LEFT_CLICK, ACTION_SELECT_ITEM]: self.updateCurrent(F)
			elif action == ACTION_PREVIOUS_MENU:  self.doExit()
			elif action == ACTION_NAV_BACK:       self.doExit()
			
		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(900); H=int(650); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow