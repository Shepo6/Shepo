import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil,urlresolver,random,liveresolver
from resources.libs.common_addon import Addon
import base64
from metahandler import metahandlers

addon_id        = 'plugin.video.boxinghits'
addon           = Addon(addon_id, sys.argv)
selfAddon       = xbmcaddon.Addon(id=addon_id)
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
fanarts         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
searchicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'search.jpg'))
whatsnewicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'whatsnew.jpg'))
nextpage        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'next.png'))
baseurl         = 'http://shepobuilds.comlu.com/base.xml'
sd_path         = xbmc.translatePath(os.path.join('special://home/addons/', 'plugin.video.sportsdevil'))
ytpl            = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
ytpl2           = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
ytplpg1         = 'https://www.googleapis.com/youtube/v3/playlistItems?pageToken='
ytplpg2         = '&part=snippet&playlistId='
ytplpg3         = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
adultpass       = selfAddon.getSetting('password')
metaset         = selfAddon.getSetting('enable_meta')
messagetext     ='http://shepobuilds.comlu.com/info.xml'
RUNNER 			= base64.b64decode(b'aHR0cDovL3NpbXRlY2gubmV0MTYubmV0L3lvdXR1YmUucGhwP2lkPQ==')
SEARCH_LIST     = base64.b64decode(b'aHR0cDovL3Bhc3RlYmluLmNvbS9yYXcvTlR2MEpkeDg=')
                                                               
def GetMenu():
        xbmc.executebuiltin('Container.SetViewMode(500)')
        url = baseurl
        link=open_url(baseurl)
        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
            try:
                if '<channel>' in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        url=re.compile('<channel>(.+?)</channel>').findall(item)[0]
                        addDir(name,url,6,iconimage,fanart)
                if '<sportsdevil>' in item:
                        links=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)
                        if len(links)==1:
                             name=re.compile('<title>(.+?)</title>').findall(item)[0]
                             iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                             url=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)[0]
                             referer=re.compile('<referer>(.+?)</referer>').findall(item)[0]
                             check = referer
                             suffix = "/"
                             if not check.endswith(suffix):
                                 refer = check + "/"
                             else:
                                 refer = check
                             link = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
                             url = link + '%26referer=' +refer
                             addItem(name,url,4,iconimage,fanart)   
                        elif len(links)>1:
                             name=re.compile('<title>(.+?)</title>').findall(item)[0]
                             iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                             fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                             addItem(name,url2,8,iconimage,fanart)       
                elif '<folder>'in item:
                                data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                for name,url,iconimage,fanart in data:
                                        addDir(name,url,1,iconimage,fanart)
                else:
                                links=re.compile('<link>(.+?)</link>').findall(item)
                                if len(links)==1:
                                        data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                        lcount=len(match)
                                        for name,url,iconimage,fanart in data:
                                                if 'youtube.com/playlist' in url:
                                                        addDir(name,url,2,iconimage,fanart)
                                                else:
                                                        addLink(name,url,2,iconimage,fanart)
                                elif len(links)>1:
                                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                                        addLink(name,url2,3,iconimage,fanart)
            except:pass
            view(link)
        addDir('[B][COLOR red]Boxing Hits Info[/COLOR][/B]',url,10,whatsnewicon,fanarts)
        addDir('[B][COLOR red]Search[/COLOR][/B]',url,5,searchicon,fanarts)

def popup():
        message=open_url2(messagetext)
        if len(message)>1:
                path = xbmcaddon.Addon().getAddonInfo('path')
                comparefile = os.path.join(os.path.join(path,''), 'compare.txt')
                r = open(comparefile)
                compfile = r.read()       
                if compfile == message:pass
                else:
                        showText('[B][COLOR red]Boxing Hits[/COLOR] [COLOR snow]Info[/COLOR][/B]', message)
                        text_file = open(comparefile, "w")
                        text_file.write(message)
                        text_file.close()
                        
def GetContent(name,url,iconimage,fanart):
        url2=url
        link=open_url(url)

        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
            try:
                if '<channel>' in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        url=re.compile('<channel>(.+?)</channel>').findall(item)[0]
                        addDir(name,url,6,iconimage,fanart)
                if '<image>' in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        url=re.compile('<image>(.+?)</image>').findall(item)[0]
                        addDir(name,iconimage,9,iconimage,fanart)
                if '<sportsdevil>' in item:
                        links=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)
                        if len(links)==1:
                             name=re.compile('<title>(.+?)</title>').findall(item)[0]
                             iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                             url=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)[0]
                             referer=re.compile('<referer>(.+?)</referer>').findall(item)[0]
                             check = referer
                             suffix = "/"
                             if not check.endswith(suffix):
                                 refer = check + "/"
                             else:
                                 refer = check
                             link = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
                             url = link + '%26referer=' +refer
                             addItem(name,url,4,iconimage,fanart)   
                        elif len(links)>1:
                             name=re.compile('<title>(.+?)</title>').findall(item)[0]
                             iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                             fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                             addItem(name,url2,8,iconimage,fanart)
    
                elif '<folder>'in item:
                                data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                for name,url,iconimage,fanart in data:
                                        addDir(name,url,1,iconimage,fanart)
                else:
                                links=re.compile('<link>(.+?)</link>').findall(item)
                                if len(links)==1:
                                        data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                        lcount=len(match)
                                        for name,url,iconimage,fanart in data:
                                                if 'youtube.com/playlist' in url:
                                                        addDir(name,url,2,iconimage,fanart)
                                                else:
                                                        addLink(name,url,2,iconimage,fanart)
                                elif len(links)>1:
                                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                                        addLink(name,url2,3,iconimage,fanart)
            except:pass
            view(link)

def NEW():
        message=open_url2(messagetext)
        if len(message)>1:
                path = xbmcaddon.Addon().getAddonInfo('path')
                showText('[B][COLOR red]Boxing Hits[/COLOR] [COLOR snow]Info[/COLOR][/B]', message)
                quit()


def YOUTUBE_CHANNEL(url):

	CHANNEL = RUNNER + url
	link = open_url(CHANNEL)
	patron = "<video>(.*?)</video>"
	videos = re.findall(patron,link,re.DOTALL)

	items = []
	for video in videos:
		item = {}
		item["name"] = find_single_match(video,"<name>([^<]+)</name>")
		item["url"] = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9") + find_single_match(video,"<id>([^<]+)</id>")
		item["author"] = find_single_match(video,"<author>([^<]+)</author>")
		item["iconimage"] = find_single_match(video,"<iconimage>([^<]+)</iconimage>")
		item["date"] = find_single_match(video,"<date>([^<]+)</date>")
		
		addLink('[COLOR white]' + item["name"] + ' - on ' + item["date"] + '[/COLOR]',item["url"],7,item["iconimage"],fanart)

	
def SEARCH():
	keyb = xbmc.Keyboard('', '[COLOR snow]Search[/COLOR] [COLOR red]Boxing Hits[/COLOR]')
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchterm=keyb.getText()
		searchterm=searchterm.upper()
	else:quit()
	link=open_url('http://shepobuilds.comlu.com/search.xml')
	slist=re.compile('<link>(.+?)</link>').findall(link)
	for url in slist:
                url2=url
                link=open_url(url)
                entries= re.compile('<item>(.+?)</item>').findall(link)
                for item in entries:
                        match=re.compile('<title>(.+?)</title>').findall(item)
                        for title in match:
                                title=title.upper()
                                if searchterm in title:
                                    try:
                                        if '<sportsdevil>' in item:
                                                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                                                url=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)[0]
                                                referer=re.compile('<referer>(.+?)</referer>').findall(item)[0]
                                                link = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
                                                url = link + '%26referer=' +referer
                                                if 'tp' in url:
                                                        addLink(name,url,4,iconimage,fanarts)       
                                        elif '<folder>'in item:
                                                        data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                                        for name,url,iconimage,fanart in data:
                                                                if 'tp' in url:
                                                                        addDir(name,url,1,iconimage,fanarts)
                                        else:
                                                        links=re.compile('<link>(.+?)</link>').findall(item)
                                                        if len(links)==1:
                                                                data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                                                lcount=len(match)
                                                                for name,url,iconimage,fanart in data:
                                                                        if 'youtube.com/playlist' in url:
                                                                                addDir(name,url,2,iconimage,fanarts)
                                                                        else:
                                                                                if 'tp' in url: 
                                                                                        addLink(name,url,2,iconimage,fanarts)
                                                        elif len(links)>1:
                                                                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                                                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                                                addLink(name,url2,3,iconimage,fanarts)
                                    except:pass       
                        
		
def GETMULTI(name,url,iconimage):
	streamurl=[]
	streamname=[]
	streamicon=[]
	link=open_url(url)
	urls=re.compile('<title>'+re.escape(name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
	iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
	links=re.compile('<link>(.+?)</link>').findall(urls)
	i=1
	for sturl in links:
                sturl2=sturl
                if '(' in sturl:
                        sturl=sturl.split('(')[0]
                        caption=str(sturl2.split('(')[1].replace(')',''))
                        streamurl.append(sturl)
                        streamname.append(caption)
                else:
                        streamurl.append( sturl )
                        streamname.append( 'Link '+str(i) )
                i=i+1
	name='[COLOR red]'+name+'[/COLOR]'
	dialog = xbmcgui.Dialog()
	select = dialog.select(name,streamname)
	if select < 0:
		quit()
	else:
		url = streamurl[select]
		print url
		if urlresolver.HostedMediaFile(url).valid_url(): stream_url = urlresolver.HostedMediaFile(url).resolve()
                elif liveresolver.isValid(url)==True: stream_url=liveresolver.resolve(url)
                else: stream_url=url
                liz = xbmcgui.ListItem(name,iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setPath(stream_url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                
def GETMULTI_SD(name,url,iconimage):

    sdbase = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='
    streamurl=[]
    streamname=[]
    streamicon=[]
    streamnumber=[]
    link=open_url(url)
    urls=re.compile('<title>'+re.escape(name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
    links=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(urls)
    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
    i=1

    for sturl in links:
                sturl2=sturl
                if '(' in sturl:
                        sturl=sturl.split('(')[0]
                        caption=str(sturl2.split('(')[1].replace(')',''))
                        streamurl.append(sturl)
                        streamname.append(caption)
                        streamnumber.append('Stream ' + str(i))
                else:
                        streamurl.append( sturl )
                        streamname.append( 'Link '+str(i) )

                i=i+1
    name='[COLOR red]'+name+'[/COLOR]'
    dialog = xbmcgui.Dialog()
    select = dialog.select(name,streamname)
    if select < 0:
        quit()
    else:
        check = streamname[select]
        suffix = "/"
        if not check.endswith(suffix):
              refer = check + "/"
        else:
              refer = check
        url = sdbase + streamurl[select] + "%26referer=" + refer
        print url

        xbmc.Player().play(url)

def PLAYSD(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url, liz, False)
        
def PLAYLINK(name,url,iconimage):
        if not'http'in url:url='http://'+url
        if 'youtube.com/playlist' in url:
                searchterm = url.split('list=')[1]
                ytapi = ytpl + searchterm + ytpl2
                req = urllib2.Request(ytapi)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = link.replace('\r','').replace('\n','').replace('  ','')     
                match=re.compile('"title": "(.+?)".+?"videoId": "(.+?)"',re.DOTALL).findall(link)
                try:
                        np=re.compile('"nextPageToken": "(.+?)"').findall(link)[0]
                        ytapi = ytplpg1 + np + ytplpg2 + searchterm + ytplpg3
                        addDir('Next Page >>',ytapi,2,nextpage,fanart)
                except:pass



                
                for name,ytid in match:
                        url = 'https://www.youtube.com/watch?v='+ytid
                        iconimage = 'https://i.ytimg.com/vi/'+ytid+'/hqdefault.jpg'
                        if not 'Private video' in name:
                                if not 'Deleted video' in name:
                                        addLink(name,url,2,iconimage,fanart)
                
        if 'https://www.googleapis.com/youtube/v3' in url:
                searchterm = re.compile('playlistId=(.+?)&maxResults').findall(url)[0]
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link = link.replace('\r','').replace('\n','').replace('  ','')     
                match=re.compile('"title": "(.+?)".+?"videoId": "(.+?)"',re.DOTALL).findall(link)
                try:
                        np=re.compile('"nextPageToken": "(.+?)"').findall(link)[0]
                        ytapi = ytplpg1 + np + ytplpg2 + searchterm + ytplpg3
                        addDir('Next Page >>',ytapi,2,nextpage,fanart)
                except:pass


                
                for name,ytid in match:
                        url = 'https://www.youtube.com/watch?v='+ytid
                        iconimage = 'https://i.ytimg.com/vi/'+ytid+'/hqdefault.jpg'
                        if not 'Private video' in name:
                                if not 'Deleted video' in name:
                                        addLink(name,url,2,iconimage,fanart)

                
                                     
        if urlresolver.HostedMediaFile(url).valid_url(): stream_url = urlresolver.HostedMediaFile(url).resolve()
        elif liveresolver.isValid(url)==True: stream_url=liveresolver.resolve(url)
        else: stream_url=url
        liz = xbmcgui.ListItem(name,iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setPath(stream_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                            
def PLAYVIDEO(url):

	xbmc.Player().play(url)

def open_url(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'KO')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('\n','').replace('\r','').replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>').replace('<utube>','<link>https://www.youtube.com/watch?v=').replace('</utube>','</link>')#.replace('></','>x</')
        return link
    except:quit()

def open_url2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'KO')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def open_url3(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'KO')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]                    
        return param


def addLinkMeta(name,url,mode,iconimage,itemcount,isFolder=False):
        splitName=name.partition('(')
	simplename=""
	simpleyear=""
	if len(splitName)>0:
                simplename=splitName[0]
		simpleyear=splitName[2].partition(')')
	if len(simpleyear)>0:
		simpleyear=simpleyear[0]
	mg = metahandlers.MetaData()
	meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
	liz.setInfo( type="Video", infoLabels= meta )
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)
	if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
	else: liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
	return ok
	
def addDir(name,url,mode,iconimage,fanart,description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name, url, mode, iconimage, fanart, description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart)
    liz.setProperty("IsPlayable","true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def addItem(name,url,mode,iconimage,fanart, description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def SHOW_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)
    sys.exit(1)

def find_single_match(text,pattern):

    result = ""
    try:    
        single = re.findall(pattern,text, flags=re.DOTALL)
        result = single[0]
    except:
        result = ""

    return result

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass

def view(link):
        try:
                match= re.compile('<layouttype>(.+?)</layouttype>').findall(link)[0]
                if layout=='thumbnail': xbmc.executebuiltin('Container.SetViewMode(500)')              
                else:xbmc.executebuiltin('Container.SetViewMode(50)')  
        except:pass

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
if mode==None or url==None or len(url)<1: GetMenu()
elif mode==1:GetContent(name,url,iconimage,fanart)
elif mode==2:PLAYLINK(name,url,iconimage)
elif mode==3:GETMULTI(name,url,iconimage)
elif mode==4:PLAYSD(name,url,iconimage)
elif mode==5:SEARCH()
elif mode==6:YOUTUBE_CHANNEL(url)
elif mode==7:PLAYVIDEO(url)
elif mode==8:GETMULTI_SD(name,url,iconimage)
elif mode==9:SHOW_PICTURE(url)
elif mode==10:NEW()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
