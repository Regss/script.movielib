# -*- coding: utf-8 -*-

import xbmcvfs
import os
import base64
import hashlib
import art
import debug

def prep(self, m, t):
    #panels values
    panelsValue = {}
    for panel in self.panels:
        if panel == 'actor':
            valt = [];
            if 'cast' in m:
                for cast in m['cast']:
                    if len(cast['name']) > 0:
                        valt.append(cast['name'].strip().encode('utf-8'))
            panelsValue[panel] = valt
        else:
            valt = []
            if panel in m:
                for l in m[panel]:
                    if len(l) > 0:
                        valt.append(l.strip().encode('utf-8'))
            panelsValue[panel] = valt
    
    # trailer
    if 'trailer' in m and m['trailer'][:4] == 'http':
        trailer = m['trailer']
    elif 'trailer' in m and m['trailer'][:29] == 'plugin://plugin.video.youtube':
        ytid = m['trailer'].split('=')
        trailer = 'http://www.youtube.com/embed/' + ytid[2][0:11]
    else:
        trailer = ''
    
    val = {
        'table': t,
        'id': str(m[t[:-1]+'id']),
        'title': m['title'].encode('utf-8'),
        'plot': m['plot'].encode('utf-8'),
        'rating': str(round(float(m['rating']), 1)) if 'rating' in m else '',
        'year': str(m['year']) if 'year' in m else '',
        'runtime': str(m['runtime'] / 60) if 'runtime' in m else '',
        'genre[]': panelsValue['genre'] if 'genre' in m else '',
        'director[]': panelsValue['director'] if 'director' in m else '',
        'originaltitle': m['originaltitle'].encode('utf-8') if 'originaltitle' in m else '',
        'country[]': panelsValue['country'] if 'country' in m else '',
        'set': m['set'].encode('utf-8') if 'set' in m else '',
        'imdbid': m['imdbnumber'] if 'imdbnumber' in m else '',
        'actor[]': panelsValue['actor'] if 'cast' in m else '',
        'studio[]': panelsValue['studio'] if 'studio' in m else '',
        'premiered': m['premiered'] if 'premiered' in m else '',
        'episode': str(m['episode']) if 'episode' in m else '',
        'season': str(m['season']) if 'season' in m else '',
        'tvshow': str(m['tvshowid']) if 'tvshowid' in m else '',
        'firstaired': m['firstaired'] if 'firstaired' in m else '',
        'file': m['file'].replace('\\', '/').encode('utf-8') if 'file' in m else '',
        'play_count': str(m['playcount']),
        'last_played': m['lastplayed'],
        'date_added': m['dateadded'],
        'trailer': trailer,
        'hash': hashlib.md5(str(m)).hexdigest()
    }
    
    # streamdetails
    if 'streamdetails' in m:
        stream = []
        if len(m['streamdetails']['video']) > 0:
            for s in m['streamdetails']['video']:
                stream.append(';'.join(['v',s['codec'], str(s['aspect']), str(s['width']), str(s['height']), str(s['duration'] / 60), '', '', '', '']))
        
        if len(m['streamdetails']['audio']) > 0:
            for s in m['streamdetails']['audio']:
                stream.append(';'.join(['a', '', '', '', '', '', s['codec'], str(s['channels']), s['language'], '']))
        
        if len(m['streamdetails']['subtitle']) > 0:
            for s in m['streamdetails']['subtitle']:
                stream.append(';'.join(['s', '', '', '', '', '', '', '', '', s['language']]))
        
        val.update({
            'stream[]': stream
        })
    
    # add only values support for this video type
    values = {}
    for q in self.tn[t]['values']:
        if q in val and len(val[q]) > 0:
            values[q] = val[q]
        
    debug.debug(str(values))
    return values
        'runtime': str(m['runtime'] / 60) if 'runtime' in m else '',
        'genre[]': panelsValue['genre'] if 'genre' in m else '',
        'director[]': panelsValue['director'] if 'director' in m else '',
        'originaltitle': m['originaltitle'].encode('utf-8') if 'originaltitle' in m else '',
        'country[]': panelsValue['country'] if 'country' in m else '',
        'set': m['set'].encode('utf-8') if 'set' in m else '',
        'imdbid': m['imdbnumber'] if 'imdbnumber' in m else '',
        'actor[]': panelsValue['actor'] if 'cast' in m else '',
        'studio[]': panelsValue['studio'] if 'studio' in m else '',
        'premiered': m['premiered'] if 'premiered' in m else '',
        'episode': str(m['episode']) if 'episode' in m else '',
        'season': str(m['season']) if 'season' in m else '',
        'tvshow': str(m['tvshowid']) if 'tvshowid' in m else '',
        'firstaired': m['firstaired'] if 'firstaired' in m else '',
        'file': m['file'].replace('\\', '/').encode('utf-8') if 'file' in m else '',
        'play_count': str(m['playcount']),
        'last_played': m['lastplayed'],
        'date_added': m['dateadded'],
        'trailer': trailer,
        'hash': hashlib.md5(str(m)).hexdigest()
    }
    
    # streamdetails
    if 'streamdetails' in m:
        stream = []
        if len(m['streamdetails']['video']) > 0:
            for s in m['streamdetails']['video']:
                stream.append(';'.join(['v',s['codec'], str(s['aspect']), str(s['width']), str(s['height']), str(s['duration'] / 60), '', '', '', '']))
        
        if len(m['streamdetails']['audio']) > 0:
            for s in m['streamdetails']['audio']:
                stream.append(';'.join(['a', '', '', '', '', '', s['codec'], str(s['channels']), s['language'], '']))
        
        if len(m['streamdetails']['subtitle']) > 0:
            for s in m['streamdetails']['subtitle']:
                stream.append(';'.join(['s', '', '', '', '', '', '', '', '', s['language']]))
        
        val.update({
            'stream[]': stream
        })
    
    # add only values support for this video type
    values = {}
    for q in self.tn[t]['values']:
        if q in val and len(val[q]) > 0:
            values[q] = val[q]
        
    debug.debug(str(values))
    return values
