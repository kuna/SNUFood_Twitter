import sys
import setting
import time
from BeautifulSoup import BeautifulSoup
import urllib2

def parse(when):
    res = []
    day = time.localtime().tm_wday

    if (day > 4):
        res.append(u"�б� �� ����")
        res.append(u"�б� �� ����")
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
        menu = row.findAll("td")[4].text.strip()
        if (menu == ""):
            menu = u"(��ī��)"
        res.append(unicode(menu))
    elif (when == 'dinner'):
        menu = row.findAll("td")[6].text.strip()
        if (menu == ""):
            menu = u"(��ī��)"
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
        menu = menus[1].strip()
        if (menu == ""):
            menu = u"(��ī��)"
        res.append(unicode(menu))
    elif (when == 'dinner'):
        menu = menus[2].strip()
        if (menu == ""):
            menu = u"(��ī��)"
        res.append(unicode(menu))    

    return res
        

def startBot():
    # check time per 10 sec
    try:
        isLunch = False
        isDinner = False
        while (True):
            print parse('lunch')
            
            timeStamp = time.strftime("%H:%M")
            if (timeStamp == "12:05" and not isLunch):
                print 'its lunchtime!'
                res = parse('lunch')
                if (res == None):
                    print 'failed to parse ...'

                isLunch = True

            elif (timeStamp == '5:30' and not isDinner):
                print 'its dinnertime!'
                res = parse('dinner')
                if (res == None):
                    print 'failed to parse ...'

                isDinner = True

            else:
                isLunch = False
                isDinner = False


            time.sleep(10)

            print timeStamp #nowclock

    except KeyboardInterrupt:
        print "bye!"

if (__name__=="__main__"):
    startBot()
