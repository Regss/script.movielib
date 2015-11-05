# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import os
from PIL import Image
import cStringIO
import json

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')
__thumbpath__           = xbmc.translatePath('special://thumbnails/').replace('\\', '/')

import debug

def create(source, i, width, height, q):
    
    if (source[:5] == 'image'):
        output = ''
        jsonGet = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Textures.GetTextures", "params": {  "properties":["url", "cachedurl"], "filter": {"field": "url", "operator": "is", "value":"' + source + '"}}, "id": 1}')
        jsonGet = unicode(jsonGet, 'utf-8', errors='ignore')
        jsonGetResponse = json.loads(jsonGet)
        
        if 'result' in jsonGetResponse and 'textures' in jsonGetResponse['result']:
            for t in jsonGetResponse['result']['textures']:
                if 'cachedurl' in t and t['cachedurl'] != '':
                    file = __thumbpath__ + t['cachedurl'].replace('\\', '/')
                   
                    # resize image
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
                        debug.debug(str(file))
                        debug.debug(str(Error))
    
    return output
    