"""
http://localhost:5006/ui
bokeh serve --show ui.py
Test data for search:
By imdb_ID:
tt0944947
tt5491994
tt0185906
By title:
The Wire
Shameless
Dekalog
"""

from bokeh.io import show
from bokeh.layouts import layout
from bokeh.plotting import figure, curdoc
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, RadioButtonGroup, Select, TextInput
from bokeh.models.widgets import Paragraph

from util import *


class app():
    def __init__(self):
        self.imdb_id=None
        get_start()
        self.get_layout_query()
        self.combine()

    def get_layout_query(self):
        heading_text="A program that displays every episode's rating for the tv_series."
        heading=Paragraph(text=heading_text,width=400)
        self.Search = Button(label="Search")
        self.btnGroupchoose = RadioButtonGroup(name='choose', labels=["By imdbID", "By Title"], active=0)
        paragraph = Paragraph(text="Search way")
        self.Parameter_input = TextInput(value="", title="ID or Title:", placeholder="ID or Title")
        self.select = Select(title="Season:", value="None", options=["None"])
        self.Status=Paragraph(text="Status:",width=200)
        self.Tvtext=Paragraph(text="Tv:",width=200)
        self.Seasontext=Paragraph(text="Season:",width=200)

        x=[]
        y=[]
        source = ColumnDataSource(data=dict(x=x, y=y))

        p = figure(x_range=x,plot_height=400,title="Season rating",
                   toolbar_location=None, tools="")

        p.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
        p.xaxis.major_label_orientation = 1

        self.Search.on_click(self.search_click)
        self.select.on_change('value',self.select_click)

        self.layout_query = layout(
            [
                [heading],
                [[widgetbox(paragraph, width=100),widgetbox(self.btnGroupchoose)],
                [widgetbox(self.Parameter_input)],
                [widgetbox(self.Search, width=100)],],
                [[self.Status,self.Tvtext,self.Seasontext],self.select],
                p
            ]
        )

    def search_click(self):
        try:
            mode=self.btnGroupchoose.active
            param=self.Parameter_input.value
            # print(param,mode)
            ombd_res=get_omdb_record(param,mode)
            global imdb_id
            self.imdb_id=ombd_res.imdbID
            # print(imdb_id)
            season_res=get_season_data(self.imdb_id)
            seasons=list(season_res.keys())
            seasons=sorted(seasons)
            # print(seasons)
            self.select.options=seasons
            self.select.value=seasons[0]

            self.Status.text="Status:successful search"
            self.Tvtext.text="Tv:"+ombd_res.title
            self.Seasontext.text="Season:"+self.select.value

            season=seasons[0]
            season_res=get_season_data(self.imdb_id)
            season_url=season_res[season]
            episode_list=get_episode_data(self.imdb_id,season,season_url)
            episode_names=[]
            episode_ratings=[]
            for episode in episode_list:
                name=episode[0]
                rating=float(episode[2])
                episode_names.append(name)
                episode_ratings.append(rating)
            # print(episode_names,episode_ratings)

            source_data=dict(x=episode_names, y=episode_ratings)
            source = ColumnDataSource(data=source_data)
            p = figure(x_range=episode_names,plot_height=400,title="Season rating",
                       toolbar_location=None, tools="")
            p.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
            p.xaxis.major_label_orientation = 1
            self.layout_query.children[-1]=p

        except Exception as e:
            self.select.options=["None"]
            self.Status.text="Status:No result"
            self.Tvtext.text="Tv:"
            self.Seasontext.text="Season:"

    def select_click(self,attrname, old, new):
        season=self.select.value
        if season!="None":
            self.Seasontext.text="Season:"+self.select.value
            season_res=get_season_data(self.imdb_id)
            season_url=season_res[season]
            episode_list=get_episode_data(self.imdb_id,season,season_url)
            episode_names=[]
            episode_ratings=[]
            for episode in episode_list:
                name=episode[0]
                rating=float(episode[2])
                episode_names.append(name)
                episode_ratings.append(rating)
            # print(episode_names,episode_ratings)
            source_data=dict(x=episode_names, y=episode_ratings)
            source = ColumnDataSource(data=source_data)
            p = figure(x_range=episode_names,plot_height=400,title="Season rating",
                       toolbar_location=None, tools="")
            p.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
            p.xaxis.major_label_orientation = 1
            self.layout_query.children[-1]=p

    def combine(self):
        curdoc().add_root(self.layout_query)
        curdoc().title = "imdb_rating"
        show(self.layout_query)


app()