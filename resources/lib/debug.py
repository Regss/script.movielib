# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__icon__                = __addon__.getAddonInfo('icon')

def debug(msg):
    xbmc.log('>>>> Movielib <<<< ' + msg, level=xbmc.LOGDEBUG)
    
def notice(msg):
    xbmc.log('>>>> Movielib <<<< ' + msg, level=xbmc.LOGLOGNOTICE)
    
def notify(msg):
    if 'true' in __addon__.getSetting('notify'):
        xbmc.executebuiltin('Notification(Movielib, ' + msg + ', 4000, ' + __icon__ + ')')
        
