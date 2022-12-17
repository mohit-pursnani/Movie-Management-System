import json

import pandas as pd
import numpy as np
import psycopg2
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import matplotlib.pyplot as plt
from uszipcode import SearchEngine
from configparser import ConfigParser
import mpu


@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

def fetch_data(sql: str):
    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

def SearchMovieName():

    st.subheader("Search for a Movie by Movie Name")
    

    with st.form(key='searchform'):
            movie_query=st.text_input("Enter a Movie Name")
            submit_button=st.form_submit_button(label="Search")
            movie_name=movie_query.strip().title()

            if submit_button:
                try:
                    movie_details=f"SELECT m.name as movie_name, m.language, m.country, m.release_date, m.length, mc.casts_name, mpd.producer_name, md.director_name, mg.genre FROM (SELECT m.id as id, STRING_AGG (p.name, ', ') AS producer_name FROM movie m, producer p, produced_by pdby WHERE p.id = pdby.producer_id AND m.id = pdby.movie_id GROUP BY m.id) as mpd, (SELECT m.id as id, STRING_AGG (c.name, ', ') AS casts_name FROM movie m, casts c, starred_by sby WHERE c.id = sby.cast_id AND m.id = sby.movie_id GROUP BY m.id) as mc, (SELECT m.id as id, STRING_AGG (d.name, ', ') AS director_name FROM movie m, director d, directed_by dby WHERE d.id = dby.director_id AND m.id = dby.movie_id GROUP BY m.id) as md, (SELECT m.id as id, STRING_AGG (g.type, ', ') AS genre FROM movie m, genre g, movie_belong_to mbt WHERE g.id = mbt.genre_id AND m.id = mbt.movie_id GROUP BY m.id) as mg, movie m WHERE lower(m.name) LIKE lower('%{movie_name}%') AND m.id = mpd.id AND m.id = md.id AND m.id = mc.id AND m.id = mg.id;"
                    m_details=fetch_data(movie_details)
                    for i in m_details:
                        mname=set()
                        lang=set()
                        coun=set()
                        rel_date=set()
                        mlen=set()
                        prod=set()
                        cast=set()
                        direc=set()
                        mgenre=set()
                        mname.add(i[0])
                        lang.add(i[1])
                        coun.add(i[2])
                        rel_date.add(str(i[3]))
                        mlen.add(str(i[4]))
                        cast.add(i[5])
                        prod.add(i[6])
                        direc.add(i[7])
                        mgenre.add(i[8])
                        st.caption("Expand to see movie details")
                        with st.expander('{}'.format(next(iter(i)))):
                            st.markdown("#### _Casts_")
                            for c in cast:
                                st.caption(c)
                            st.markdown("#### _Genre_")
                            for g in mgenre:
                                st.caption(g)
                            st.markdown("#### _Language_")
                            st.caption(next(iter(lang)))
                            st.markdown("#### _Country_")
                            st.caption(next(iter(coun)))
                            st.markdown("#### _Year of Release_")
                            st.caption(next(iter(rel_date)))
                            st.markdown("#### _Movie Length_")
                            st.caption(next(iter(mlen)))
                            st.markdown("#### _Producers_", True)
                            for p in prod:
                                st.caption(p)
                            st.markdown("#### _Director_")
                            for d in direc:
                                st.caption(d)
                except:
                    st.error("Try searching for another movie")

def SearchMovieProducer():
    st.subheader("Search for a Movie by Producer Name")    

    with st.form(key='searchform'):
            movie_query=st.text_input("Enter a Producer's Name")
            submit_button=st.form_submit_button(label="Search")
            producer_name=movie_query.strip().title()

            if submit_button:
                try:
                    movie_details=f"SELECT m.name as movie_name, m.language, m.country, m.release_date, m.length, mc.casts_name, mpd.producer_name, md.director_name, mg.genre  FROM (     SELECT m.id as id, STRING_AGG (p.name, ', ') AS producer_name      FROM movie m, producer p, produced_by pdby      WHERE p.id = pdby.producer_id AND m.id = pdby.movie_id GROUP BY m.id     ) as mpd, (         SELECT m.id as id, STRING_AGG (c.name, ', ') AS casts_name          FROM movie m, casts c, starred_by sby          WHERE c.id = sby.cast_id AND m.id = sby.movie_id          GROUP BY m.id) as mc, (SELECT m.id as id, STRING_AGG (d.name, ', ') AS director_name FROM movie m, director d, directed_by dby WHERE d.id = dby.director_id AND m.id = dby.movie_id GROUP BY m.id) as md, (SELECT m.id as id, STRING_AGG (g.type, ', ') AS genre FROM movie m, genre g, movie_belong_to mbt WHERE g.id = mbt.genre_id AND m.id = mbt.movie_id GROUP BY m.id) as mg, movie m  WHERE lower(mpd.producer_name) LIKE lower('%{producer_name}%') AND m.id = mpd.id AND m.id = md.id AND m.id = mc.id AND m.id = mg.id;"
                    m_details=fetch_data(movie_details)
                    for i in m_details:
                        mname=set()
                        lang=set()
                        coun=set()
                        rel_date=set()
                        mlen=set()
                        prod=set()
                        cast=set()
                        direc=set()
                        mgenre=set()
                        mname.add(i[0])
                        lang.add(i[1])
                        coun.add(i[2])
                        rel_date.add(str(i[3]))
                        mlen.add(str(i[4]))
                        cast.add(i[5])
                        prod.add(i[6])
                        direc.add(i[7])
                        mgenre.add(i[8])
                        st.caption("Expand to see movie details")
                        with st.expander('{}'.format(next(iter(i)))):
                            st.markdown("#### _Casts_")
                            for c in cast:
                                st.caption(c)
                            st.markdown("#### _Genre_")
                            for g in mgenre:
                                st.caption(g)
                            st.markdown("#### _Language_")
                            st.caption(next(iter(lang)))
                            st.markdown("#### _Country_")
                            st.caption(next(iter(coun)))
                            st.markdown("#### _Year of Release_")
                            st.caption(next(iter(rel_date)))
                            st.markdown("#### _Movie Length_")
                            st.caption(next(iter(mlen)))
                            st.markdown("#### _Producers_", True)
                            for p in prod:
                                st.caption(p)
                            st.markdown("#### _Director_")
                            for d in direc:
                                st.caption(d)
                except:
                    st.error("Try searching for another Producer")

def SearchMovieDirector():
    st.subheader("Search for a Movie by Director Name")

    with st.form(key='searchform'):
            movie_query=st.text_input("Enter a Director's Name")
            submit_button=st.form_submit_button(label="Search")
            director_name=movie_query.strip().title()

            if submit_button:
                try:
                    movie_details=f"SELECT m.name as movie_name, m.language, m.country, m.release_date, m.length, mc.casts_name, mpd.producer_name, md.director_name, mg.genre  FROM (     SELECT m.id as id, STRING_AGG (p.name, ', ') AS producer_name      FROM movie m, producer p, produced_by pdby      WHERE p.id = pdby.producer_id AND m.id = pdby.movie_id GROUP BY m.id     ) as mpd,      (         SELECT m.id as id, STRING_AGG (c.name, ', ') AS casts_name          FROM movie m, casts c, starred_by sby          WHERE c.id = sby.cast_id AND m.id = sby.movie_id GROUP BY m.id     ) as mc,      (         SELECT m.id as id, STRING_AGG (d.name, ', ') AS director_name          FROM movie m, director d, directed_by dby          WHERE d.id = dby.director_id AND m.id = dby.movie_id GROUP BY m.id     ) as md,      (         SELECT m.id as id, STRING_AGG (g.type, ', ') AS genre          FROM movie m, genre g, movie_belong_to mbt          WHERE g.id = mbt.genre_id AND m.id = mbt.movie_id          GROUP BY m.id) as mg, movie m  WHERE lower(md.director_name) LIKE lower('%{director_name}%') AND m.id = mpd.id AND m.id = md.id AND m.id = mc.id AND m.id = mg.id;"
                    m_details=fetch_data(movie_details)
                    for i in m_details:
                        mname=set()
                        lang=set()
                        coun=set()
                        rel_date=set()
                        mlen=set()
                        prod=set()
                        cast=set()
                        direc=set()
                        mgenre=set()
                        mname.add(i[0])
                        lang.add(i[1])
                        coun.add(i[2])
                        rel_date.add(str(i[3]))
                        mlen.add(str(i[4]))
                        cast.add(i[5])
                        prod.add(i[6])
                        direc.add(i[7])
                        mgenre.add(i[8])
                        st.caption("Expand to see movie details")
                        with st.expander('{}'.format(next(iter(i)))):
                            st.markdown("#### _Casts_")
                            for c in cast:
                                st.caption(c)
                            st.markdown("#### _Genre_")
                            for g in mgenre:
                                st.caption(g)
                            st.markdown("#### _Language_")
                            st.caption(next(iter(lang)))
                            st.markdown("#### _Country_")
                            st.caption(next(iter(coun)))
                            st.markdown("#### _Year of Release_")
                            st.caption(next(iter(rel_date)))
                            st.markdown("#### _Movie Length_")
                            st.caption(next(iter(mlen)))
                            st.markdown("#### _Producers_", True)
                            for p in prod:
                                st.caption(p)
                            st.markdown("#### _Director_")
                            for d in direc:
                                st.caption(d)
                except:
                    st.error("Try searching for another Director")


def SearchMovieActor():
    st.subheader("Search for a Movie by Cast Name")
    

    with st.form(key='searchform'):
            movie_query=st.text_input("Enter a Cast's Name")
            submit_button=st.form_submit_button(label="Search")
            cast_name=movie_query.strip().title()

            if submit_button:
                try:
                    movie_details = f"SELECT m.name as movie_name, m.language, m.country, m.release_date, m.length, mc.casts_name, mpd.producer_name, md.director_name, mg.genre  FROM (         SELECT m.id as id, STRING_AGG (p.name, ', ') AS producer_name          FROM movie m, producer p, produced_by pdby          WHERE p.id = pdby.producer_id AND m.id = pdby.movie_id GROUP BY m.id     ) as mpd,      (         SELECT m.id as id, STRING_AGG (c.name, ', ') AS casts_name          FROM movie m, casts c, starred_by sby          WHERE c.id = sby.cast_id AND m.id = sby.movie_id          GROUP BY m.id     ) as mc,      (         SELECT m.id as id, STRING_AGG (d.name, ', ') AS director_name          FROM movie m, director d, directed_by dby          WHERE d.id = dby.director_id AND m.id = dby.movie_id GROUP BY m.id     ) as md,      (         SELECT m.id as id, STRING_AGG (g.type, ', ') AS genre          FROM movie m, genre g, movie_belong_to mbt          WHERE g.id = mbt.genre_id AND m.id = mbt.movie_id          GROUP BY m.id     ) as mg, movie m  WHERE lower(mc.casts_name) like lower('%{cast_name}%') AND m.id = mpd.id AND m.id = md.id AND m.id = mc.id AND m.id = mg.id;"
                    m_details=fetch_data(movie_details)
                    for i in m_details:
                        mname=set()
                        lang=set()
                        coun=set()
                        rel_date=set()
                        mlen=set()
                        prod=set()
                        cast=set()
                        direc=set()
                        mgenre=set()
                        mname.add(i[0])
                        lang.add(i[1])
                        coun.add(i[2])
                        rel_date.add(str(i[3]))
                        mlen.add(str(i[4]))
                        cast.add(i[5])
                        prod.add(i[6])
                        direc.add(i[7])
                        mgenre.add(i[8])
                        st.caption("Expand to see movie details")
                        with st.expander('{}'.format(next(iter(i)))):
                            st.markdown("#### _Casts_")
                            for c in cast:
                                st.caption(c)
                            st.markdown("#### _Genre_")
                            for g in mgenre:
                                st.caption(g)
                            st.markdown("#### _Language_")
                            st.caption(next(iter(lang)))
                            st.markdown("#### _Country_")
                            st.caption(next(iter(coun)))
                            st.markdown("#### _Year of Release_")
                            st.caption(next(iter(rel_date)))
                            st.markdown("#### _Movie Length_")
                            st.caption(next(iter(mlen)))
                            st.markdown("#### _Producers_", True)
                            for p in prod:
                                st.caption(p)
                            st.markdown("#### _Director_")
                            for d in direc:
                                st.caption(d)
                except:
                    st.error("Try searching for another Cast")



def SearchMovie():
    search_menu=[ 'Search for a Movie by Name', 'Search for a Movie by Producer','Search for a Movie by Director', 'Search for a Movie by Actor' ]

    search_val = st.selectbox('Filters',search_menu)
    if search_val=='Search for a Movie by Name':
        SearchMovieName()    
    elif search_val=='Search for a Movie by Producer':
        SearchMovieProducer()        
    elif search_val == 'Search for a Movie by Director':
        SearchMovieDirector()    
    elif search_val=='Search for a Movie by Actor':
        SearchMovieActor()
  

def TopRatedGenreMovie():
    st.subheader("Top 5 movies of selected genre")
    genre_type = "Select Type from Genre;"
    try:
        genre_names = query_db(genre_type)["type"].tolist()
        genre_name = st.selectbox("Choose a genre", genre_names)
    except:
        st.write("Sorry! Something went wrong, please try again.")

    try:
        if genre_name:
            genre_query = f"Select m.name as movie_name,avg(VR.rating) as Rating from Movie M,Genre G,Movie_belong_to MB,Viewed_Rated_by VR where MB.Movie_Id=M.id and M.id=VR.Movie_Id and MB.Genre_Id=G.Id and G.Type='{genre_name}' group by M.Name having avg(VR.Rating)>=3 order by Rating desc limit 5;"
            movie_genre = query_db(genre_query)
            for i in range(len(movie_genre)) :
                st.write(str(movie_genre.loc[i, "movie_name"])+" has an average rating of " +str(round(movie_genre.loc[i, "rating"],2)))
    except:
        st.write("Sorry! Something went wrong, please try again.")


def RangeMovies():
    st.subheader("Select the range of years in which you want to browse movies")
    try:
        start_year, end_year = st.select_slider(
        'Select range of year ',
        options=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        value=(2001, 2022))
        st.write('Movies between', str(start_year), 'and', str(end_year), 'are')
        year_query=f"Select Name, Release_date as Release_Date from Movie where EXTRACT(year from  Release_Date) BETWEEN {start_year} AND {end_year};"
    except:
        st.write("Sorry! Something went wrong, please try again.")
    
    try:
        year_query_output = query_db(year_query)
        st.write(year_query_output)
    
    except:
        st.write("Sorry! Something went wrong, please try again.")
   
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def MovieRevenue():
    st.subheader("Select the range of years in which you want stats about movies' revenues")
    try:
        start_year, end_year = st.select_slider(
        'Select range of year ',
        options=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
        value=(2001, 2022))
        st.write('Movies between', str(start_year), 'and', str(end_year), 'are')
        revenue_query=f" SELECT m.name as Name,CAST(EXTRACT(YEAR FROM m.release_date) AS int) as year, r.collectedrevenue as Revenue FROM Movie m, Revenue r, (SELECT EXTRACT(YEAR FROM m.release_date) as year, MAX(r.collectedrevenue) as maxcollectedrevenue FROM Movie m, Revenue r WHERE m.id = r.id AND EXTRACT(YEAR FROM m.release_date) >= {start_year} AND EXTRACT(YEAR FROM m.release_date) <= {end_year} GROUP by EXTRACT(YEAR FROM m.release_date)) as mr WHERE EXTRACT(YEAR FROM m.release_date) = mr.year AND m.id=r.id AND mr.maxcollectedrevenue = r.collectedrevenue order by M.release_date desc ;"
    except:
        st.write("Sorry! Something went wrong, please try again.")
    
    try:
        revenue_query_output = query_db(revenue_query)
        st.write(revenue_query_output)
        fig, ax = plt.subplots()
        fig.set_figheight(12)
        fig.set_figwidth(16)
        g= ax.barh(revenue_query_output['name'], revenue_query_output['revenue']/10000000, color=['red','cyan'], alpha=0.5)
        
        ax.bar_label(g, labels=revenue_query_output['year'])
        plt.ylabel('Movies')
        plt.xlabel('Revenue')
        st.pyplot(fig)
    
    
    except:
        st.write("Sorry! Something went wrong, please try again")

def GenresDistribution():

    st.subheader("Distribution of genres performed by a particular actor")
    
    cast_query = "select Name from Casts order by Name;"
    try:
        cast_name_query = query_db(cast_query)
        cast_name = st.selectbox("Choose an actor", cast_name_query)
    except:
        st.write("Sorry! Something went wrong, please try again.")
        
    try:
        genre_query = f"SELECT  g.type, COUNT(*) as count_of_movies FROM casts c, starred_by s, genre g, movie_belong_to mb WHERE lower(c.name) = lower('{cast_name}') AND c.id = s.cast_id AND g.id = mb.genre_id AND s.movie_id = mb.movie_id GROUP BY c.name,g.type;"             
        cast_genre = query_db(genre_query)
        st.write(cast_genre)
        wp = { 'linewidth' : 1, 'edgecolor' : "white" }
        labels = cast_genre['type']
        sizes = cast_genre['count_of_movies']

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops = wp, textprops = dict(color ="black"))
        ax1.axis('equal')  

        st.pyplot(fig1)
            
    except:
        st.write("Sorry! Something went wrong with your query, please try again.")


def StreamingPlatformMovies():
    st.write("Which movie are you searching for?")
    movie_type = "Select Name from Movie order by Name;"
    try:
        movie_name_output = query_db(movie_type)["name"].tolist()
        movie_name = st.selectbox("Choose a movie", movie_name_output)
    except:
        st.write("Sorry! Something went wrong, please try again.")
    try:
        if movie_name:
            sp_query = f"Select SP.Name as Streaming_Platform from Movie M, StreamingPlatform SP, Streamed_On SO WHERE M.name= '{movie_name}' and M.id = SO.Movie_Id and SO.Streaming_Platform_Id = SP.Id;"
            
    
            movie_sp = query_db(sp_query)
            if movie_sp.shape[0]:
                st.write("Platforms streaming" , movie_name, "are:")
                st.write(movie_sp)
            else:
                st.write("Sorry!", movie_name, "is currently not being streamed on any platform")
    except:
        st.write("Sorry! Something went wrong, please try again.")

def MoviebyZipCode():
    st.subheader("Search nearby Theaters and their Show Dates and Time based on your Zip Code")

    zip1 = st.text_input("Enter your Zip Code")
    try:
        if zip1:
            st.write("Movies Near Zip Code ", zip1)
            search = SearchEngine()
            zip1 = search.by_zipcode(zip1)
            lat1 =zip1.lat
            long1 =zip1.lng

            zip_query=f"SELECT m.name as movie_name, t.name as theater_name, t.zip_code FROM Theater t, played_at p, movie m WHERE p.theater_id = t.id AND p.movie_id = m.id;"
            zip_query_output = fetch_data(zip_query)
            zip_list = query_db(zip_query)["zip_code"].tolist()
            i = 0
            df = pd.DataFrame(columns=["Movie", "Theater Name", "Theater Zip Code", "Distance(miles)"])
            for zip in zip_list:    
                zip2 =search.by_zipcode(zip)
                lat2 =zip2.lat
                long2 =zip2.lng        
                j = zip_query_output[i]
                df.loc[i]=[j[0], j[1], j[2], round(mpu.haversine_distance((lat1,long1),(lat2,long2)), 2)]
                i+=1
            df = df.sort_values(by=['Distance(miles)'])
            df.reset_index(drop=True, inplace=True)
            st.write(df)

            s_date_query = "select distinct s.s_date from Show s order by s.s_date;"
            s_date = query_db(s_date_query)
            show_date = st.selectbox("Choose a show date", s_date)
            s_time_query=f"SELECT m.name as movie_name, t.name as theater_name, t.zip_code,  s.s_time as show_time FROM Theater t, played_at p, movie m, show s WHERE s.s_date = '{show_date}' AND p.theater_id = t.id AND p.movie_id = m.id AND s.theater_id = t.id;"
            s_time = query_db(s_time_query).astype(str)
            st.write(s_time)

    except:
        st.write("Sorry! Something went wrong with your query, please try again.")       
    

        
        


def main():
    st.markdown("<h1 style='text-align: center; color: #F0E68C;'>Movie Management System</h1>", unsafe_allow_html=True)
    lottie_movie = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_khzniaya.json")
    st_lottie(lottie_movie, speed=1, height=150, key=None)
    menu=[ 'Search for a Movie', 'Search top rated movie of a particular genre','Movies in range of years', 'Highest Revenue Movies each year in range of years', 'Distribution of Genres by Actor', 'Search Nearby Movies by Zipcode', 'Search Streaming Platform for any movie']

    val = st.selectbox('Menu',menu)
    if val=='Search for a Movie':
        SearchMovie()    
    elif val=='Search top rated movie of a particular genre':
        TopRatedGenreMovie()        
    elif val == 'Movies in range of years':
        RangeMovies()    
    elif val=='Highest Revenue Movies each year in range of years':
        MovieRevenue()
    elif val=='Distribution of Genres by Actor':
        GenresDistribution()
    elif val =='Search Nearby Movies by Zipcode':
        MoviebyZipCode()
    elif val == 'Search Streaming Platform for any movie':
        StreamingPlatformMovies()

if __name__ == "__main__":
    main()
