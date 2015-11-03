# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcvfs
import os
from PIL import Image
import cStringIO
import urllib

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__datapath__            = xbmc.translatePath(os.path.join('special://profile/addon_data/', __addon_id__)).replace('\\', '/')

import debug

def create(source, i, width, height, q):
    
    if (source[:5] == 'image'):
        file = source
        # if it is a URL
        if source[8:12] == 'http':
            try:
                link = urllib.unquote(source[8:][:-1]).encode('utf-8')
                source = cStringIO.StringIO(urllib.urlopen(link).read())
            except:
                source = ''
        else:
            f = xbmcvfs.File(source)
            t = f.read()
            f.close()
            source = cStringIO.StringIO(t)
            
        # resize image
        try:
            image = Image.open(source)
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
            else:
                output = ''
        except Exception as Error:
            output = ''
            debug.debug(str(file))
            debug.debug(str(Error))
    else:
        output = ''
    return output
        