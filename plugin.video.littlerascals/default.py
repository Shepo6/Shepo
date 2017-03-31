# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Noobs Addon by coldkeys
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: Shepo
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.littlerascals'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1  = "stampylonghead"
YOUTUBE_CHANNEL_ID_2  = "TheDiamondMinecart"
YOUTUBE_CHANNEL_ID_3  = "PopularMMOs"
YOUTUBE_CHANNEL_ID_4  = "UCpG5AvE1_okaOOuQRhFokzw"
YOUTUBE_CHANNEL_ID_5  = "UCWbHJTyhqEHoyfgZWwI6v1A"
YOUTUBE_CHANNEL_ID_6  = "SkyDoesMinecraft"
YOUTUBE_CHANNEL_ID_7  = "CaptainSparklez"
YOUTUBE_CHANNEL_ID_8  = "BlueXephos"
YOUTUBE_CHANNEL_ID_9  = "DisneyCollectorBR"
YOUTUBE_CHANNEL_ID_10  = "littlebabybum"
YOUTUBE_CHANNEL_ID_11  = "TheBajanCanadian"
YOUTUBE_CHANNEL_ID_12  = "SSundee"
YOUTUBE_CHANNEL_ID_13  = "JeromeASF"
YOUTUBE_CHANNEL_ID_14  = "LittleLizardGaming"
YOUTUBE_CHANNEL_ID_15  = "UCzTlXb7ivVzuFlugVCv3Kvg"
YOUTUBE_CHANNEL_ID_16  = "UC70Dib4MvFfT1tU6MqeyHpQ"
YOUTUBE_CHANNEL_ID_17  = "UCa6Hg8HmooiDNaCT0_1NbQQ"
YOUTUBE_CHANNEL_ID_18  = "UC2nZMhZ2qG5-xpqb440WLYg"
YOUTUBE_CHANNEL_ID_19  = "UC4f1zAG2BTkfOQV4_nFbpBQ"
YOUTUBE_CHANNEL_ID_20  = "biggranny000"
YOUTUBE_CHANNEL_ID_21  = "UCZlXWfndRF4PWcemogYeu2g"
YOUTUBE_CHANNEL_ID_22  = "MayaTOOTS"
YOUTUBE_CHANNEL_ID_23  = "RomanAtwoodVlogs"

# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

# Minecraft menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="[COLOR red]----- YOUTUBERS -----[/COLOR]",
        url="",
        thumbnail="",
        folder=False )

    plugintools.add_item(
        #action="", 
        title="stampylonghead",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-bY_OkstVA0g/AAAAAAAAAAI/AAAAAAAAAAA/x2CqwQ35Dco/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DanTDM",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-KEJYjuwz0-c/AAAAAAAAAAI/AAAAAAAAAAA/ScEc76PWvak/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="PopularMMOs",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-ZTmDqvhaw30/AAAAAAAAAAI/AAAAAAAAAAA/1wk5CSaMbc8/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Real Life Minecraft Heroes",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-pFVlyUyIkoc/AAAAAAAAAAI/AAAAAAAAAAA/l9ngpgXaI-g/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Little Kelly Minecraft",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-i7OKEqKP1zE/AAAAAAAAAAI/AAAAAAAAAAA/BxMYl0Uor5o/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sky Does Minecraft",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-dNukrTQa8eI/AAAAAAAAAAI/AAAAAAAAAAA/q0fNXIKFTw4/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CaptainSparklez",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-Ns-YNJxjh28/AAAAAAAAAAI/AAAAAAAAAAA/0Tf1gK8GBbE/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="YOGSCAST Lewis & Simon",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-FMO2nSO2pP8/AAAAAAAAAAI/AAAAAAAAAAA/QZLWwqsqMIU/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Fun Toys Collector Disney Toys Review",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-sSB36cFW0N4/AAAAAAAAAAI/AAAAAAAAAAA/4XxC7rLRwKo/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LittleBabyBum",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://pbs.twimg.com/profile_images/799635276146573312/oUGm9K6R.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bajan Canadian",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://s-media-cache-ak0.pinimg.com/736x/0c/4d/9c/0c4d9cecf3614859b159b100543b23b1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SSundee",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-LmPoIkSWSyk/AAAAAAAAAAI/AAAAAAAAAAA/fOy9V1ArBNM/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="JeromeASF",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="http://vignette1.wikia.nocookie.net/youtube/images/4/40/Jeromeasf.png/revision/latest?cb=20130517045317",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LittleLizardGaming",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-G4DBj_OGNq4/AAAAAAAAAAI/AAAAAAAAAAA/CKcNcDcKJYU/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LDShadowLady",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-iWbYZ42vq8I/AAAAAAAAAAI/AAAAAAAAAAA/VafCJoAaKMI/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="PrestonPlayz",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://static-s.aa-cdn.net/img/gp/20600005067114/J4bwcAjrIpOj1z1ObwRJjfcdItZXqRi-g8um7WFzcxvvK6T0CaUrp3yBUjqMPC_JtVk=w300?v=1",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="iBallisticSquid",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="http://vignette1.wikia.nocookie.net/magicanimalclub/images/b/b1/2c0efeb65e36bcada165078835fe8e07.jpg/revision/latest?cb=20131207141809",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ExplodingTNT",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="http://vignette4.wikia.nocookie.net/explodingtnt/images/b/b7/Mouse.jpg/revision/latest?cb=20160429043522",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="TheAtlanticCraft",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-t5u86HR2xxY/AAAAAAAAAAI/AAAAAAAAAAA/77TRgrztPJI/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="biggranny000",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-pUjqb9EcmZs/AAAAAAAAAAI/AAAAAAAAAAA/z1wDtuGters/s900-c-k-no-mo-rj-c0xffffff/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Alex",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://t0.rbxcdn.com/05cacd37787a05a371dfb0dc8564f926",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Pals",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://i.ytimg.com/vi/qMSvfHJq0oE/maxresdefault.jpg",
        folder=True )

	plugintools.add_item( 
        #action="", 
        title="The Pals",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://s-media-cache-ak0.pinimg.com/736x/b3/3f/7e/b33f7e3793e9aced1db66c049432763c.jpg",
        folder=True )
run()
