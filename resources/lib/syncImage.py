# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import os
import urllib
import urllib2
import hashlib
import base64

__addon__               = xbmcaddon.Addon()
__addonname__           = __addon__.getAddonInfo('name')
__lang__                = __addon__.getLocalizedString

import debug
import sendRequest
import art

def sync(self, ImagesXBMC, ImagesSORT):
    # get panels list from XBMC
    
    ImagesSite = sendRequest.send(self, 'showimages')
    debug.debug('[ImagesSITE]: ' + str(ImagesSite))
    
    # prepare hash
    hashImagesXBMC = hashlib.md5(str(ImagesXBMC)).hexdigest()
    debug.debug('[hashImagesXBMC]: ' + str(hashImagesXBMC))
    if hashImagesXBMC != self.hashSITE['images'] or self.imageNeeded == True:
        debug.debug('[IMAGES UPDATE NEEDED]')
    else:
        debug.debug('[IMAGES UPDATE NOT NEEDED]')
        return False
    
    #prepare images to add
    ImagesToAdd = {}
    for v_type in ImagesXBMC.keys():
        ImagesToAdd[v_type] = {}
        for img_type in ImagesXBMC[v_type].keys():
            # check if user want sync images
            if self.setSITE['xbmc_'+img_type+'s'] == '1':
                ImagesToAdd[v_type][img_type] = set(ImagesXBMC[v_type][img_type].keys()) - set(ImagesSite[v_type][img_type])
    debug.debug('[ImagesToAdd]: ' + str(ImagesToAdd))
    
    #prepare images to remove
    ImagesToRemove = {}
    for v_type in ImagesXBMC.keys():
        ImagesToRemove[v_type] = {}
        for img_type in ImagesXBMC[v_type].keys():
            ImagesToRemove[v_type][img_type] = set(ImagesSite[v_type][img_type]) - set(ImagesXBMC[v_type][img_type].keys())
    debug.debug('[ImagesToRemove]: ' + str(ImagesToRemove))
    
    # adding new images
    for type in ImagesSORT['images']:
        
        for img_type in ImagesSORT[type]:
            
            if len(ImagesToAdd[type][img_type]) > 0:
                debug.debug('=== ADDING ' + type.upper() + ' ' + img_type.upper() + ' IMAGES ===')
                
                countToAdd = len(ImagesToAdd[type][img_type])
                addedCount = 0
                self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32204) + ' ' + __lang__(32121) + ' (' + __lang__(self.lang[type]) + ' - ' + __lang__(self.lang[img_type]) + ')')
                
                for id in ImagesToAdd[type][img_type]:
                    # progress bar update
                    p = int((float(100) / float(countToAdd)) * float(addedCount))
                    self.progBar.update(p, str(addedCount + 1) + '/' + str(countToAdd) + ' - ' + self.namesXBMC[type][id])
                    
                    if 'poster' == img_type and 'episodes' in type:
                        t = art.create(ImagesXBMC[type][img_type][id], 'p', 200, 113, 70)
                    if 'poster' == img_type and 'episodes' not in type:
                        t = art.create(ImagesXBMC[type][img_type][id], 'p', 200, 294, 70)
                    if 'fanart' == img_type:
                        t = art.create(ImagesXBMC[type][img_type][id], 'f', 1280, 720, 70)
                    if 'thumb' == img_type:
                        t = art.create(ImagesXBMC[type][img_type][id], 'a', 75, 100, 70)
                    if 'exthumb' == img_type:
                        ex_size = self.setSITE['xbmc_exthumbs_q'].split('x')
                        t = art.create('image://' + urllib.quote_plus(ImagesXBMC[type][img_type][id].encode('utf-8')) + '/', 'e', int(ex_size[0]), int(ex_size[1]), 70)
                    
                    if len(t) > 0:
                        if 'actors' in type:
                            name = 'actors/' + str(id) + '.jpg'
                        else:
                            f = '_f' if 'fanart' in img_type else ''
                            name = type + '_' + str(id) + f + '.jpg'
                        value = {
                            'name': name,
                            'img': base64.b64encode(t)
                        }
                        if sendRequest.send(self, 'addimages', value) is False:
                            self.progBar.close()
                            return False
                    addedCount += 1
                self.progBar.close()
                
                if addedCount > 0:
                    debug.notify(__lang__(32104).encode('utf-8') + ' ' + __lang__(32121).encode('utf-8') + ' (' + __lang__(self.lang[type]).encode('utf-8') + ' - ' + __lang__(self.lang[img_type]).encode('utf-8') + '): ' + str(addedCount))
    
    # removing images
    toRemove = {}
    removedCount = 0
    for type, vals in ImagesToRemove.items():
        for img_type, v in vals.items():
            if len(v) > 0:
                debug.debug('=== REMOVING ' + type.upper() + ' ' + img_type.upper() + ' IMAGES ===')
                for file in v:
                    if 'poster' == img_type:
                        toRemove[removedCount] = type + '_' + str(file) + '.jpg'
                    if 'fanart' == img_type:
                        toRemove[removedCount] = type + '_' + str(file) + '_f.jpg'
                    if 'thumb' == img_type:
                        toRemove[removedCount] = 'actors/' + str(file) + '.jpg'
                    if 'exthumb' == img_type:
                        toRemove[removedCount] = type + '_' + str(file) + '.jpg'
                        removedCount += 1
                        toRemove[removedCount] = type + '_' + str(file) + 'm.jpg'
                    removedCount += 1
    if len(toRemove) > 0:
        if sendRequest.send(self, 'removeimages', toRemove) is False:
            return False
        debug.notify(__lang__(32105).encode('utf-8') + ' ' + __lang__(32121).encode('utf-8') + ': ' + str(removedCount))
    
    # update hash
    value = { 'images': str(hashImagesXBMC) }
    if sendRequest.send(self, 'updatehash', value) is False:
        return False
        