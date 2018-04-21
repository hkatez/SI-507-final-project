import sqlite3
import os
from contextlib import closing
import requests
import json
from bs4 import BeautifulSoup,element
from secrets import omdb_api

IMDB_URL="https://www.imdb.com"



class Omdb_Record():
    def __init__(self,res):
        self.imdbID=res[0]
        self.title=res[1]
        self.totalseason=res[2]
        self.type=res[3]
        self.released_data=res[4]
        self.imdbrating=res[5]

    def __str__(self):
        seq="Title: {} imdbId: {} Totalseasons: {}".format(self.title,self.imdbID,self.totalseason)
        return seq


def get_param(name,mode):
    if mode==1:
        name=name.replace(" ","+")
        query_dict={"t":name}
    else:
        query_dict={"i":name}
    return query_dict


def get_data_from_ombd(query_dict,code="utf-8"):
    json_name='omdb_tv.json'
    try:
        cache_file = open(json_name, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

        # if there was no file, no worries. There will be soon!
    except:
        CACHE_DICTION = {}

    baseurl="http://www.omdbapi.com/?apikey=%s"%omdb_api
    param=""
    for key in query_dict:
        param+="&%s=%s"%(key,query_dict[key])
    unique_ident = baseurl+param
    print(unique_ident)
    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(unique_ident)
        resp.encoding=code
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(json_name,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


def get_record_from_tv_json_data(data):
    imdbID=data["imdbID"]
    title=data["Title"]
    boxoffice=int(data["totalSeasons"])
    if boxoffice=="N/A":
        boxoffice=None
    type=data["Type"]
    released=data["Released"]
    imdbRating=data["imdbRating"]
    record=(imdbID,title,boxoffice,type, released, imdbRating)
    return record


def get_url(imdb_id):
    url=IMDB_URL+"/title/%s/"%imdb_id
    return url


def get_HTML_text(url,json_name,code="utf-8"):
    try:
        cache_file = open(json_name, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

        # if there was no file, no worries. There will be soon!
    except:
        CACHE_DICTION = {}

    if url in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[url]
    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        resp.raise_for_status()
        resp.encoding=code
        # CACHE_DICTION[url] = json.loads(resp.text)
        CACHE_DICTION[url] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(json_name,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[url]


def get_season_list(html):
    soup=BeautifulSoup(html,"html.parser")
    seasons_list=soup.find_all("div",id="title-episode-widget")[0]
    seasons_and_year=seasons_list.find("div",attrs={"class":"seasons-and-year-nav"})
    seasons_div=seasons_and_year.find_all("div")[2]
    season_urls={}
    for href in seasons_div:
        if not isinstance(href,element.NavigableString):
            season_urls[href.get_text()]=IMDB_URL+href.get("href")

    # print(season_urls)
    return season_urls


def get_episode_details(html):
    # print(html)
    soup=BeautifulSoup(html,"html.parser")
    detail_eplist=soup.find_all("div",attrs={"class":"list detail eplist"})[0]
    # item_divs=detail_eplist.find_all("div")
    episode_details=[]
    for div in detail_eplist.children:
        if div.name:
            data=div.find("div",attrs={"class":"airdate"}).get_text()
            data=data.replace("\n","").replace(" ","")
            title=div.find("a",attrs={"itemprop":"name"}).get_text()
            rating=div.find("span",attrs={"class":"ipl-rating-star__rating"}).get_text()
            des=div.find("div",attrs={"class":"item_description"}).get_text()
            url=IMDB_URL+div.find("a",attrs={"itemprop":"name"}).get("href")
            # title,air_date,rating,des,url
            item_detail=(title,data,rating,des,url)
            # print(item_detail)
            episode_details.append(item_detail)

    return episode_details


def get_start():
    if not os.path.exists('imdb.db'):
        create_db()


def create_db():
    db_name='imdb.db'
    if os.path.exists(db_name):
        os.remove(db_name)
    """
    season
    ========================
    imdb_id
    title
    season
    total_season
    season_url
    """
    season="""CREATE TABLE season
        (imdb_id char NOT NULL,
        title char NOT NULL,
        season INT,
        total_season INT,
        season_url MESSAGE_TEXT );"""
    """
    episode
    ========================
    title
    data
    rating
    des
    url
    belong
    season
    """
    episode="""CREATE TABLE episode
        (title char NOT NULL,
        data char NOT NULL,
        rating char,
        des MESSAGE_TEXT,
        url MESSAGE_TEXT,
        belong char,
        season INT);"""
    """
    tv_series
    ========================
    "imdbRating": "7.6",
    "totalSeasons": "4",
    "Title": "The Rider",
    "imdbID": "tt6217608",
    "Type": "movie",
    "Released": "13 Apr 2018",
    """
    tv_series="""CREATE TABLE tv_series
        (imdbID char PRIMARY KEY NOT NULL,
        title char NOT NULL,
        totalSeasons INT,
        type CHAR(50),
        released date,
        imdbRating REAL);"""
    with closing(sqlite3.connect(db_name)) as connection:
        c = connection.cursor()
        c.execute(season)
        c.execute(episode)
        c.execute(tv_series)


def insert_records(record,table):
    db_name='imdb.db'
    conn=sqlite3.connect(db_name)
    c = conn.cursor()
    value_list=["?" for i in range(len(record))]
    value_str=",".join(value_list)
    sql_str="INSERT INTO %s VALUES"%table+" (%s)"%value_str
    c.execute(sql_str,record)
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def get_data_from_db(param,mode,season=None):
    rows=None
    db_name="imdb.db"
    if mode==0:
        conn=sqlite3.connect(db_name)
        tsql = "SELECT * FROM tv_series WHERE imdbID='%s'"%param
        c = conn.cursor()
        with conn:
            rows = c.execute(tsql).fetchall()
    elif mode==1:
        conn=sqlite3.connect(db_name)
        tsql = "SELECT * FROM tv_series WHERE title='%s'"%param
        c = conn.cursor()
        with conn:
            rows = c.execute(tsql).fetchall()
    elif mode==2:
        conn=sqlite3.connect(db_name)
        tsql = "SELECT * FROM season WHERE imdb_id='%s'"%param
        c = conn.cursor()
        with conn:
            rows = c.execute(tsql).fetchall()
    elif mode==3:
        conn=sqlite3.connect(db_name)
        tsql = "SELECT * FROM episode WHERE belong='%s' and season=%s"%(param,season)
        c = conn.cursor()
        with conn:
            rows = c.execute(tsql).fetchall()

    return rows


def get_omdb_record(param,mode):
    """
    :param param: Title or imdbID
    :param mode: 0 for imdbID,1 for title
    :return:
    a tuple of the tv details:(imdbID,title,totalseason,Release_date,imdb_rating)
    for example,('tt0944947', 'Game of Thrones', 8, 'series', '17 Apr 2011', 9.5).
    """
    res=get_data_from_db(param,mode)
    if res is None or len(res)==0:
        query_dict=get_param(param,mode)
        data=get_data_from_ombd(query_dict)
        res=get_record_from_tv_json_data(data)
        table="tv_series"
        insert_records(res,table)
    else:
        res=res[0]
    omdb_res=Omdb_Record(res)
    return omdb_res


def get_season_data(imdb_id):
    res=get_data_from_db(imdb_id,2)
    if res is None or len(res)==0:
        omdb_res=get_omdb_record(imdb_id,0)
        title=omdb_res.title
        total_season=omdb_res.totalseason
        id_url=get_url(imdb_id)
        imdb_cache="imdb.json"
        html=get_HTML_text(id_url,imdb_cache)
        season_urls=get_season_list(html)
        table="season"
        for season in season_urls:
            season_item=(imdb_id,title,int(season),total_season,season_urls[season])
            insert_records(season_item,table)
    else:
        season_urls={}
        for record in res:
            season_urls[str(record[2])]=record[4]
    return season_urls


def get_episode_data(imdb_id,season,season_url):
    res=get_data_from_db(imdb_id,3,season)
    if res is None or len(res)==0:
        res=[]
        episode_cache="Episode.json"
        html=get_HTML_text(season_url,episode_cache)
        episode_details=get_episode_details(html)
        table="episode"
        for episode in episode_details:
            record=episode+(imdb_id,int(season))
            res.append(record)
            insert_records(record,table)
    return res