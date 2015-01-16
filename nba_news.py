from newspaper import Article, Config
from bs4 import BeautifulSoup
from urllib2 import urlopen
import datetime
import re
from collections import OrderedDict
import pytz
from pytz import timezone
from dateutil.parser import parse


nba_url = "http://www.nba.com"
espn_url = "http://espn.go.com"

#lxml didn't work for espn
my_config = Config()
my_config.parser_class = "soup"

def normalize_url(url, link):
    if link.startswith("http://"):
        return link
    elif link.startswith("/"):
        return url + link
    else:
        return url + "/" + link

def get_soup_from_url(url):
    response = urlopen(url)
    try:
        data = response.read()
    except:
        print "**error visiting {}".format(url)
        raise
    return BeautifulSoup(data)

def print_article_dict(dict):
    print ""
    for field, value in dict.items():
        if field == "keywords":
            print "keywords: {}".format(value)
            continue
        if value != None:
            print "{}: {} ". format(field, value.encode('utf-8', 'replace'))
        else:
            print "{}: {} ". format(field, value)

""" search string for timezone keywords lind PT and return a the date formated with timezone
"""
def format_date (date_string, date):
    if date_string.find("PT") > -1:
        tzone = "US/Pacific"
    elif date_string.find("CT") > -1:
        tzone = "US/Central"
    elif date_string.find("ET") > -1:
        tzone = "US/Eastern"
    else:
        print "timezone from date_string not found"

    return (pytz.timezone(tzone).localize(date, is_dst=True))

def getESPN_date_from_article(soup):

    mday = soup.find("div", class_ = "monthday")
    if mday != None:
        date = mday.find_previous("span").text
        time = mday.find_next("div", class_ = "time").text
        timeofday = mday.find_next("div", class_ = "timeofday").text
        date = parse(date + " " + time + " " + timeofday)
        date = format_date (timeofday, date)
        resp_date = date.isoformat()
    else:
        dates = soup.find_all("div", class_ = "date")
        resp_date = None
        for date in dates:
            txt = date.text
            dt = None
            if txt.startswith("Publish Date: Today, "):
                dt = datetime.date.today()
                #print "{} {}".format(dt.isoformat(), txt[21:32])
                dt = parse("{} {}".format(dt.isoformat(), txt[21:32]))
            elif txt.startswith("Publish Date: Yesterday, "):
                dt = datetime.date.today()
                dt = dt - datetime.timedelta(days=1)
                #print "{} {}".format(dt.isoformat(), txt[25:36])
                dt = parse("{} {}".format(dt.isoformat(), txt[25:36]))
            elif txt.startswith("Publish Date: "):
                #print "{}".format(txt[14:38])
                dt = parse(txt[14:38])

            if dt != None:
                date = format_date(txt, dt)
                resp_date = date.isoformat()
                break
            else:
                continue

    if resp_date == None:
        gtl = soup.find("div", class_ = "game-time-location")
        if gtl != None:
            dt = gtl.find_next("p")
            if dt != None:
                date = parse(dt.text)
                date = format_date (dt.text, date)
                resp_date = date.isoformat()

    return resp_date

def getESPN_dot_com_team_news(team_short_name = None, visited_links = []):
    news = list()
    if team_short_name == None:
        return
    team_short_name = team_short_name.lower()

    try:
        espn_team_blog = short_name_to_espn_blog[team_short_name]
    except:
        return None

    url = espn_url + "/" + espn_team_blog + "/"
    soup = get_soup_from_url(url)

    if espn_team_blog.find('blog') > -1:
        headers = soup.find_all("div", class_ = "mod-header")
    else:
        headers = soup.find_all("li", class_ = "result")

    for header in headers:
        resp = OrderedDict()
        h3 = header.find("h3")
        if h3 == None:
            continue
        link = h3.find("a").get("href")
        if link == None:
            continue

        url = normalize_url(espn_url, link)

        if url in visited_links:
            continue
      
        #avoid blog post from other teams 
        #if url.find('blog') > -1: 
        #    if url.find(team_short_name) == -1:
        #        continue
            
        article = Article(url, my_config)
        article.download()
        article.parse()

        resp['title'] = article.title 
        resp['link'] = url
        resp['description'] = article.meta_description
        resp['text'] = article.text
        resp['image'] = article.top_image
        resp['keywords'] = article.meta_keywords

        #extra fields not provided by newspaper (author and date)
        article_soup = get_soup_from_url(url)
        if len(article.authors) < 1 :
            author = article_soup.find("cite", class_ = "byline")
            if author != None:
                author_txt = author.find("a")
                if author_txt != None:
                    author = author_txt.text
                else:
                    #print "found this as an author {}".format(author.text
                    author = author.text
            else:
                author = article_soup.find("cite", class_ = "source")
                if author != None:
                    author = author.text
            resp['author'] = author
        else:
            resp['author'] = article.authors[0]

        resp['date'] = getESPN_date_from_article(article_soup)

        print_article_dict(resp)
        news.append(resp)
    return news

"""
    Converts nba team short names to espn style names used in blogs.
    example: warriors -> "golden-state-warriors"
"""
short_name_to_espn_blog = {
'celtics' : 'blog/boston/celtics',
'nets' : 'blog/brooklyn-nets',
'knick' : 'blog/new-york-knicks',
'76ers' : 'nba/team/_/name/phi/philadelphia-76ers',
'raptors' : 'nba/team/_/name/tor/toronto-raptors',
'bulls' : 'blog/chicago-bulls',
'cavaliers' : 'blog/cleveland-cavaliers',
'pistons' : 'nba/team/_/name/det/detroit-pistons',
'pacers' : 'nba/team/_/name/ind/indiana-pacers',
'bucks' : 'nba/team/_/name/mil/milwaukee-bucks',
'hawks' : 'nba/team/_/name/atl/atlanta-hawks',
'hornets' : 'nba/team/_/name/cha/charlotte-hornets',
'heat' : 'blog/truehoopmiamiheat',
'magic' : 'nba/team/_/name/orl/orlando-magic',
'wizards' : 'nba/team/_/name/wsh/washington-wizards',
'warriors' : 'blog/golden-state-warriors',
'clippers' : 'blog/los-angeles-clippers',
'lakers' : 'blog/los-angeles-lakers',
'suns' : 'nba/team/_/name/phx/phoenix-suns',
'kings' : 'nba/team/_/name/sac/sacramento-kings',
'mavericks' : 'blog/dallas-mavericks',
'rockets' : 'nba/team/_/name/hou/houston-rockets',
'grizzlies' : 'nba/team/_/name/mem/memphis-grizzlies',
'pelicans' : 'nba/team/_/name/no/new-orleans-pelicans',
'spurs' : 'nba/team/_/name/sa/san-antonio-spurs',
'nuggets' : 'nba/team/_/name/den/denver-nuggets',
'timberwolves' : 'nba/team/_/name/min/minnesota-timberwolves',
'thunder' : 'nba/team/_/name/okc/oklahoma-city-thunder',
'blazers' : 'nba/team/_/name/por/portland-trail-blazers',
'jazz' : 'nba/team/_/name/utah/utah-jazz',
}

def getNBA_dot_com_team_news(team_short_name = None, visited_links = []):
    news = list()
    if team_short_name == None:
        return

    team_short_name = team_short_name.lower()

    url = nba_url + "/" + team_short_name + "/news"
    soup = get_soup_from_url(url)

    headers = soup.find_all("div", class_ = re.compile("post__information"))

    for header in headers:
        resp = OrderedDict()
        title = header.find("div", class_ = "post__title")
        if title == None:
            continue
        link = title.find("a").get("href")
        if link == None:
            continue

        url = normalize_url(nba_url, link)

        if url in visited_links:
            continue

        #avoiding articles in other languages for nba.com/china/
        if url.find("/china/") > -1:
            continue

        article = Article(url, my_config)
        article.download()
        article.parse()

        resp['title'] = article.title
        resp['link'] = url
        resp['description'] = article.meta_description
        resp['text'] = article.text
        resp['image'] = article.top_image
        resp['keywords'] = article.meta_keywords

        #nba.com doesn't show a clear author for articles 
        resp['author'] = "nba.com"

        article_soup = get_soup_from_url(url) 

        date = article_soup.find("div", class_ = "author-block__post-date")
        resp['date'] = None
        if date != None:
            txt = date.text
            if txt.startswith("Posted: "):
                #print "{}".format(txt[8:])
                dt = parse(txt[8:])
                #nba.com doesn't provide the time, we will use now
                now = datetime.datetime.now(pytz.timezone("US/Eastern"))
                dt = dt.replace(hour=now.hour, minute=now.minute, 
                                second=now.second, tzinfo=now.tzinfo)
                
                resp['date'] = dt.isoformat() 

        print_article_dict(resp)
        news.append(resp)
    return news


if __name__ == "__main__":
#    getESPN_dot_com_team_news("warriors")
    getESPN_dot_com_team_news("heat")
    getNBA_dot_com_team_news("heat")
