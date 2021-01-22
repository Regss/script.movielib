# -*- coding: utf-8 -*-

import xbmcvfs
import xbmc
import xbmcaddon
import os
from PIL import Image
from io import StringIO
from urllib.request import urlopen
import json
import urllib


__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__thumbpath__           = xbmc.translatePath('special://thumbnails/').replace('\\', '/')

import debug

def create(source, i, width, height, q):
    
    file_path = ''
    output = ''
    
    if (source[:5] == 'image'):
    
        # try read image from thumbnail folder
        jsonGet = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Textures.GetTextures", "params": {  "properties":["url", "cachedurl"], "filter": {"field": "url", "operator": "is", "value":"' + source + '"}}, "id": 1}')
        jsonGet = unicode(jsonGet, 'utf-8', errors='ignore')
        jsonGetResponse = json.loads(jsonGet)
        
        if 'result' in jsonGetResponse and 'textures' in jsonGetResponse['result'] and len(jsonGetResponse['result']['textures']) > 0:
            for t in jsonGetResponse['result']['textures']:
                if 'cachedurl' in t and t['cachedurl'] != '':
                    file_path = __thumbpath__ + t['cachedurl'].replace('\\', '/')
                    f = xbmcvfs.File(file_path)
                    file = cStringIO.StringIO(f.read())
                    f.close()
        else:
        
            # try read image from source
            file_path = source
            if file_path[8:12] == 'http':
                try:
                    link = urllib.unquote(file_path[8:][:-1]).encode('utf-8')
                    file = cStringIO.StringIO(urllib.request.urlopen(link).read())
                except:
                    file = ''
            else:
                f = xbmcvfs.File(file_path)
                file = cStringIO.StringIO(f.read())
                f.close()
            
        # read image
        try:
            image = Image.open(file)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            h = image.size[1]
            if h > 10:
                if (h > height):
                    image.load()
                    image = image.resize((width, height), Image.ANTIALIAS)
                image_bin = cStringIO.StringIO()
                image.save(image_bin, 'JPEG', quality=int(q))
                output = image_bin.getvalue()
                image_bin.close()
        
        except Exception as Error:
            debug.debug(str(jsonGetResponse))
            debug.debug(source)
            debug.debug(str(Error))
            
            # try only copy image without using PIL
            debug.debug('Trying to just copy...')
            try:
                f = xbmcvfs.File(file_path)
                output = f.read()
                f.close()
        
            except Exception as Error:
                debug.debug(str(Error))
    
    return output
    
                    file = ''
            else:
                f = xbmcvfs.File(file_path)
                file = cStringIO.StringIO(f.read())
                f.close()
            
        # read image
        try:
            image = Image.open(file)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            h = image.size[1]
            if h > 10:
                if (h > height):
                    image.load()
                    image = image.resize((width, height), Image.ANTIALIAS)
                image_bin = cStringIO.StringIO()
                image.save(image_bin, 'JPEG', quality=int(q))
                output = image_bin.getvalue()
                image_bin.close()
        
        except Exception as Error:
            debug.debug(str(jsonGetResponse))
            debug.debug(source)
            debug.debug(str(Error))
            
            # try only copy image without using PIL
            debug.debug('Trying to just copy...')
            try:
                f = xbmcvfs.File(file_path)
                output = f.read()
                f.close()
        
            except Exception as Error:
                debug.debug(str(Error))
    
    return output
    
