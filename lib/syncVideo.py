# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import hashlib
import time

__addon__               = xbmcaddon.Addon()
__addonname__           = __addon__.getAddonInfo('name')
__lang__                = __addon__.getLocalizedString

import debug
import prepareValues
import sendRequest

def sync(self, videosXBMC):
    
    for table in videosXBMC.keys():
        
        # check hash video library
        if hashlib.md5(str(videosXBMC[table])).hexdigest() == self.hashSITE[table]:
            debug.debug('[' + table.upper() + ' UPDATE NOT NEEDED]')
        else:
            debug.debug('[' + table.upper() + ' UPDATE NEEDED]')
            
            # if video has been updated force clean database and sync images
            self.cleanNeeded = True
            self.imageNeeded = True
            
            # get id and hash from site
            videosSite = sendRequest.send(self, 'showvideo&table=' + table, '')
            debug.debug('[' + table + 'SITE]: ' + str(videosSite))
            
            # prepare videos to add and remove
            videoToAdd = set(videosXBMC[table].keys()) - set(videosSite.keys())
            debug.debug('[' + table + 'ToAdd]: ' + str(videoToAdd))
            videoToRemove = set(videosSite.keys()) - set(videosXBMC[table].keys())
            debug.debug('[' + table + 'ToRemove]: ' + str(videoToRemove))
            
            # prepare videos to update
            videoToUpdate = {}
            for m in videosXBMC[table].keys():
                if m in videosSite:
                    
                    # if hashes not match update video
                    if hashlib.md5(str(videosXBMC[table][m])).hexdigest() != videosSite[m]:
                        
                        # add hash to video array
                        videoToUpdate[m] = videosXBMC[table][m]
            debug.debug('[' + table + 'ToUpdate]: ' + str(videoToUpdate.keys()))
            
            # add videos
            if len(videoToAdd) > 0:
                debug.debug('=== ADDING ' + table.upper() + ' VIDEOS ===')
                if add(self, videosXBMC, videoToAdd, table, 'add') is False:
                    self.progBar.close()
                    return False
                self.progBar.close()
                
            # remove videos
            if len(videoToRemove) > 0:
                debug.debug('=== REMOVING ' + table.upper() + ' VIDEOS ===')
                if remove(self, videoToRemove, table) is False:
                    return False
                
            # update videos
            if len(videoToUpdate) > 0:
                debug.debug('=== UPDATING ' + table.upper() + ' VIDEOS ===')
                if add(self, videosXBMC, videoToUpdate, table, 'update') is False:
                    self.progBar.close()
                    return False
                self.progBar.close()
                
            # update hash
            value = {table: hashlib.md5(str(videosXBMC[table])).hexdigest()}
            sendRequest.send(self, 'updatehash', value)
        
def add(self, videosXBMC, videoToAdd, table, opt):
    
    # init progres bar
    addedCount = 0
    countToAdd = len(videoToAdd)
    self.progBar.create(__lang__(32200), __addonname__ + ', ' + __lang__(32204 if opt == 'add' else 32209) + ' ' + __lang__(self.lang[table]))
    
    for video in videoToAdd:
        start_time = time.time()
        
        # progress bar update
        p = int((float(100) / float(countToAdd)) * float(addedCount))
        progYear = ' (' + str(videosXBMC[table][video]['year']) + ')' if 'year' in videosXBMC[table][video] else ''
        self.progBar.update(p, str(addedCount + 1) + '/' + str(countToAdd) + ' - ' + videosXBMC[table][video]['title'] + progYear)
        
        # get values
        values = prepareValues.prep(self, videosXBMC[table][video], table)
        
        # send requst
        if sendRequest.send(self, opt + 'video&t=' + table, values) is False:
            return False
        else:
            addedCount += 1
        debug.debug('[TIME]: ' + str(time.time() - start_time)[0:5])
        
    if addedCount > 0:
        debug.notify(__lang__(32104 if opt == 'add' else 32103).encode('utf-8') + ' ' + __lang__(self.lang[table]).encode('utf-8') + ': ' + str(addedCount))

def remove(self, videoToRemove, table):
    
    removedCount = 0
    
    # get values
    values = {}
    for video in videoToRemove:
        removedCount += 1
        values[removedCount] = video
    
    # send requst
    if sendRequest.send(self, 'removevideo&t=' + table, values) is False:
        return False
        
    if removedCount > 0:
        debug.notify(__lang__(32105).encode('utf-8') + ' ' + __lang__(self.lang[table]).encode('utf-8') + ': ' + str(removedCount))
