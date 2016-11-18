from resources.globals import *
from resources.adobepass import ADOBE

#Add-on specific Adobepass variables
REQUESTOR_ID='nbcsports'
PUBLIC_KEY = 'nTWqX10Zj8H0q34OHAmCvbRABjpBk06w'
PRIVATE_KEY = 'Q0CAFe5TSCeEU86t'

def categories(): 
    req = urllib2.Request('http://stream.nbcsports.com/data/mobile/apps/NBCSports/configuration-ios.json')  
    req.add_header("User-Agent", UA_PC)      
    response = urllib2.urlopen(req)   
    json_source = json.load(response)                       
    response.close()   
    xbmc.log(str(json_source))
    for item in json_source['brands'][0]['sub-nav']:
        display_name = item['display-name']
        url = item['feed-url']
        addDir(display_name,url,4,ICON,FANART)
    

def getAllSports():    
    req = urllib2.Request(ROOT_URL+'apps/NBCSports/configuration-ios.json')    
    #http://stream.nbcsports.com/data/mobile/apps/NBCSports/configuration-ios.json
    response = urllib2.urlopen(req)   
    json_source = json.load(response)                       
    response.close()    

    try:
        for item in json_source['sports']:        
            code = item['code']
            name = item['name']                  
            addDir(name,ROOT_URL+'mcms/prod/'+code+'.json',4,ICON,FANART,'ALL')
    except:
        pass


def scrapeVideos(url,scrape_type=None):
    xbmc.log(url)
    req = urllib2.Request(url)
    req.add_header('Connection', 'keep-alive')
    req.add_header('Accept', '*/*')
    req.add_header('User-Agent', UA_NBCSN)
    req.add_header('Accept-Language', 'en-us')
    req.add_header('Accept-Encoding', 'deflate')
    

    response = urllib2.urlopen(req)    
    json_source = json.load(response)                           
    response.close()                

    if 'featured' in url:
        json_source = json_source['showCase']

    if 'live-upcoming' not in url:
        json_source = sorted(json_source, key=lambda k: k['start'], reverse = True)
    else:
        json_source = sorted(json_source, key=lambda k: k['start'], reverse = False)

    for item in json_source:        
      buildVideoLink(item)
    


def buildVideoLink(item):
    url = ''    
    #Use the ottStreamUrl (v3) until sound is fixed for newer (v4) streams in kodi
    try:      
        #url = item['iosStreamUrl']          
        url = item['ottStreamUrl']  
        if url == '' and item['iosStreamUrl'] != '':
            url = item['iosStreamUrl']          
        '''
        if CDN == 1 and item['backupUrl'] != '':
            url = item['backupUrl']
        '''
    except:
        try:
            if item['videoSources']:                
                '''
                if 'iosStreamUrl' in item['videoSources'][0]:
                    url =  item['videoSources'][0]['iosStreamUrl']
                    if CDN == 1 and item['videoSources'][0]['backupUrl'] != '':
                        url = item['backupUrl']
                '''
                if 'ottStreamUrl' in item['videoSources'][0]:
                    url =  item['videoSources'][0]['ottStreamUrl']
                    
                    if url == '' and item['iosStreamUrl'] != '':
                        url = item['iosStreamUrl']    
                    '''
                    if CDN == 1 and item['videoSources'][0]['backupUrl'] != '':
                        url = item['backupUrl']
                    '''
        except:
            pass
        pass
    
    #Set quality level based on user settings    
    #url = SET_STREAM_QUALITY(url)                    
    
    
    menu_name = item['title']
    name = menu_name                
    desc = item['info']     
    free = int(item['free'])
    if 'Watch Golf Channel LIVE' in name:
        free = 1

    # Highlight active streams   
    start_time = item['start']
    pattern = "%Y%m%d-%H%M"
    print "Start Time"
    print start_time
    #current_time =  datetime.utcnow().strftime(pattern) 
    #my_time = int(time.mktime(time.strptime(current_time, pattern)))         
    '''
    try:
        my_time = datetime.strptime(current_time,pattern)
    except TypeError:
        my_time = datetime.fromtimestamp(time.mktime(time.strptime(current_time, pattern)))
    '''
    #string (2008-12-07)
    #20160304-1800
    aired = start_time[0:4]+'-'+start_time[4:6]+'-'+start_time[6:8]
    genre = item['sportName']
    

    length = 0
    try:
        length = int(item['length'])
    except:        
        pass
    
    
    #event_start = int(time.mktime(time.strptime(start_time, pattern)))  
    #event_start = datetime.strptime(start_time,pattern)
    '''
    try:
        event_start = datetime.strptime(start_time,pattern)
    except TypeError:
        event_start = datetime.fromtimestamp(time.mktime(time.strptime(start_time, pattern)))
    '''
    #event_start = 0
    '''
    if length != 0:
        event_end = int(event_start + length)
    else:
        #Default to 24 hours if length not provided        
        event_end = int(event_start + 86400)
    '''
    #Allow access to stream 10 minutes early
    #event_start = event_start - (10*60)

    #Allow access to stream an hour after it's supposed to end
    #event_end = event_end + (60*60)
        
    #print url
    #print name + str(length) + " " + str(event_start) + " " + str(my_time) + " " + str(event_end) + " " + url + " FREE:" + str(free)
        
    info = {'plot':desc,'tvshowtitle':'NBCSN','title':name,'originaltitle':name,'duration':length,'aired':aired,'genre':genre}
    
    imgurl = "http://hdliveextra-pmd.edgesuite.net/HD/image_sports/mobile/"+item['image']+"_m50.jpg"    
    menu_name = filter(lambda x: x in string.printable, menu_name)
    #and (mode != 1 or (my_time >= event_start and my_time <= event_end) or 'Watch Golf Channel LIVE' in name)
    #if url != '' and (mode != 1 or (my_time >= event_start and my_time <= event_end) or 'Watch Golf Channel LIVE' in name):           
    ''' 
    try:
        start_date = datetime.strptime(start_time, "%Y%m%d-%H%M")
        #start_date = datetime.strftime(utc_to_local(start_date),xbmc.getRegion('dateshort')+' '+xbmc.getRegion('time').replace('%H%H','%H').replace(':%S',''))       
        start_date = datetime.strftime(start_date,"%Y-%m-%d %h:%M")       
        info['plot'] = 'Starting at: '+start_date+'\n\n'+info['plot']
    except:
        start_date = 'Unavailable'        
        #start_date = datetime.fromtimestamp(time.mktime(time.strptime(start_time, "%Y%m%d-%H%M")))
    '''
    start_date = stringToDate(start_time, "%Y%m%d-%H%M")
    start_date = datetime.strftime(utc_to_local(start_date),xbmc.getRegion('dateshort')+' '+xbmc.getRegion('time').replace('%H%H','%H').replace(':%S',''))       
    info['plot'] = 'Starting at: '+start_date+'\n\n'+info['plot']
    
    if url != '':
        if free:
            menu_name = '[COLOR='+FREE+']'+menu_name + '[/COLOR]'
            #addLink(menu_name,url,name,imgurl,FANART,info) 
            if str(PLAY_MAIN) == 'true':
                addFreeLink(menu_name,url,imgurl,FANART,None,info)              
            else:
                addDir(menu_name,url,6,imgurl,FANART,None,True,info)             
        elif FREE_ONLY == 'false':                        
            menu_name = '[COLOR='+LIVE+']'+menu_name + '[/COLOR]'
            if str(PLAY_MAIN) == 'true':
                addPremiumLink(menu_name,url,imgurl,FANART,None,info)             
            else:
                addDir(menu_name,url,5,imgurl,FANART,None,True,info)             
    
    else:
        #elif my_time < event_start:
        if free:
            menu_name = '[COLOR='+FREE_UPCOMING+']'+menu_name + '[/COLOR]'            
            if str(PLAY_MAIN) == 'true':
                addPremiumLink(menu_name,url,imgurl,FANART,None,info)             
            else:
                addDir(menu_name + ' ' + start_date,'/disabled',999,imgurl,FANART,None,False,info)
            
        elif FREE_ONLY == 'false':
            menu_name = '[COLOR='+UPCOMING+']'+menu_name + '[/COLOR]'            
            addDir(menu_name + ' ' + start_date,'/disabled',999,imgurl,FANART,None,False,info)
        
    

    
def signStream(stream_url, stream_name, stream_icon):   
    adobe = ADOBE(REQUESTOR_ID, PUBLIC_KEY, PRIVATE_KEY)       
    #1. Authorize device
    #2. Get media token
    #3. Sign stream (TV sign)
    
    resource_id = GET_RESOURCE_ID()  
    #media_token = adobe.POST_SHORT_AUTHORIZED(signed_requestor_id,authz)    
    adobe.authorizeDevice(resource_id)
    media_token = adobe.mediaToken(resource_id)
      
    signed_requestor_id = GET_SIGNED_REQUESTOR_ID() 
    #stream_url = adobe.TV_SIGN(media_token,resource_id, stream_url)

    xbmc.log(str(media_token))
    stream_url = adobe.tvSign(media_token, resource_id, stream_url)

    #Set quality level based on user settings    
    stream_url = SET_STREAM_QUALITY(stream_url)   
    
    listitem = xbmcgui.ListItem(path=stream_url)
    
    print "PLAY FROM MAIN!!!!"
    print str(PLAY_MAIN)

    if str(PLAY_MAIN) == 'true':
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        addLink(stream_name, stream_url, stream_name, stream_icon, FANART) 

def logout():
    adobe = ADOBE(REQUESTOR_ID, PUBLIC_KEY, PRIVATE_KEY)  
    adobe.deauthorizeDevice()
    '''
    try:
        os.remove(ADDON_PATH_PROFILE+'/device.id')
    except:
        pass
    try:
        os.remove(ADDON_PATH_PROFILE+'/provider.info')
    except:
        pass
    try:
        os.remove(ADDON_PATH_PROFILE+'/cookies.lwp')
    except:
        pass
    try:
        os.remove(ADDON_PATH_PROFILE+'/auth.token')
    except:
        pass
    '''
    ADDON.setSetting(id='clear_data', value='false')  



if CLEAR == 'true':
   logout()

params=get_params()
url=None
name=None
mode=None
scrape_type=None
icon_image = None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    scrape_type=urllib.unquote_plus(params["scrape_type"])
except:
    pass
try:
    icon_image=urllib.unquote_plus(params["icon_image"])
except:
    pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "scrape_type:"+str(scrape_type)
print "icon image:"+str(icon_image)


if mode==None or url==None or len(url)<1:        
        categories()        
elif mode==4:
        scrapeVideos(url,scrape_type)
elif mode==5:        
        signStream(url, name, icon_image)
        
elif mode==6:
    #Set quality level based on user settings    
    stream_url = SET_STREAM_QUALITY(url) 
    listitem = xbmcgui.ListItem(path=stream_url)

    if str(PLAY_MAIN) == 'true':
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        addLink(name, stream_url, name, icon_image, FANART)


#Don't cache live and upcoming list
if mode==1:
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
else:
    xbmcplugin.endOfDirectory(int(sys.argv[1]))