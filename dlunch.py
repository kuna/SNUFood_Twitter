import sys
import settings
import time
from BeautifulSoup import BeautifulSoup
import urllib2
from tweepy import *

consumer_key = settings.consumer_key
consumer_secret = settings.consumer_secret
ACCESS_KEY = settings.ACCESS_KEY
ACCESS_SECRET = settings.ACCESS_SECRET

def parse(when):
    res = []
    day = time.localtime().tm_wday

    if (day > 4):
        res.append(u"학교 안 간다")
        res.append(u"학교 안 간다")
        return res

    # 301
    h = urllib2.urlopen('http://www.snuco.com/html/restaurant/restaurant_menu2.asp')
    if (h == None):
        return None

    data = h.read()
    soup = BeautifulSoup(data)
    content = soup.find("div",{'id':'Content'})
    if (content == None):
        print 'failed to find Content table'
        return None
    row = content.find("table").findAll("tr")[3]
    
    if (when == 'lunch'):
        menu = row.findAll("td")[4].text.replace("&nbsp;", "")
        if (menu == ""):
            menu = u"(아카링)"
        res.append(unicode(menu))
    elif (when == 'dinner'):
        menu = row.findAll("td")[6].text.replace("&nbsp;", "")
        if (menu == ""):
            menu = u"(아카링)"
        res.append(unicode(menu))


    # 302
    h = urllib2.urlopen('http://www.snuco.com/html/restaurant/restaurant_info1_04.asp')
    if (h == None):
        return None

    data = h.read()
    soup = BeautifulSoup(data)
    content = soup.find("select",{'name':'week'})
    if (content == None):
        print 'failed to find Content table'
        return None
    row = content.findAll("option")[ day ]['value']
    menus = row.split("|")
    
    if (when == 'lunch'):
        menu = menus[1].replace("&nbsp;", "")
        if (menu == ""):
            menu = u"(아카링)"
        res.append(unicode(menu))
    elif (when == 'dinner'):
        menu = menus[2].replace("&nbsp;", "")
        if (menu == ""):
            menu = u"(아카링)"
        res.append(unicode(menu))    

    return res
        

def startBot():
    # twitter access
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = API(auth)
    
    # check time per 10 sec
    try:
        isLunch = False
        isDinner = False
        while (True):
            timeStamp = time.strftime("%H:%M")
            if (timeStamp == "12:05"):
                if (not isLunch):
                    print 'its lunchtime!'
                    res = parse('lunch')
                    if (res == None):
                        print 'failed to parse ...'

                    api.update_status(u"@kuna_KR 오늘 점심(301동): " + res[0] + u" #bot")
                    api.update_status(u"@kuna_KR 오늘 점심(302동): " + res[1] + u" #bot")
                    isLunch = True

            elif (timeStamp == '5:30'):
                if (not isDinner):
                    print 'its dinnertime!'
                    res = parse('dinner')
                    if (res == None):
                        print 'failed to parse ...'

                    api.update_status(u"@kuna_KR 오늘 저녁(301동): " + res[0] + u" #bot")
                    api.update_status(u"@kuna_KR 오늘 저녁(302동): " + res[1] + u" #bot")
                    isDinner = True
            else:
                isLunch = False
                isDinner = False

            time.sleep(10)
            #print timeStamp #nowclock

    except KeyboardInterrupt:
        print "bye!"

if (__name__=="__main__"):
    startBot()
