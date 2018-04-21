# SI-507-final-project

## Data sources
The Open Movie Database(Through Web API)
    You need to apply for API key(http://www.omdbapi.com/apikey.aspx)
    And put the API key into secret.py like this:
        omdb_api=yourkey
http://www.imdb.com/(Crawling multiple pages)

## Installation of Third party Library needed to run the program
To install using pip, enter the following command at a Bash or Windows command prompt:
pip install beautifulsoup4
pip install requests
pip install bokeh

## Brief description of code structure
ui.py   using Bokeh to construct the web-based GUI
class app
    get_layout_query: generate the gui layout
    search_click:callback function when Search button is clicked
    select_click:callback function when select widget is changed
util.py   to provide the functionality for ui.py.
three important functions
   get_omdb_record(param,mode)
        :param param: Title or imdbID
        :param mode: 0 for imdbID,1 for title
        :return:
            a tuple of the tv details:(imdbID,title,totalseason,Release_date,imdb_rating)
            for example,('tt0944947', 'Game of Thrones', 8, 'series', '17 Apr 2011', 9.5).
   get_season_data(imdb_id)
        :param imdb_id: The imdbID of the tv series
        :return:
            a dict(key:seasons,value:season url)
   get_episode_data(imdb_id,season,season_url)
        :param imdb_id: The imdbID of the tv series
        :param season: A season of the tv series
        :param season url: The url of the season
        :return:
            a list of episode record for a season
            record:
            a tuple of the episode details:(title,data,rating,des,url,belong,season)

## Brief user guide
Use the bokeh serve command to run the program by executing:
     bokeh serve --show ui.py
at your command prompt. Then the URL
     http://localhost:5006/ui
will be displayed in your browser.
