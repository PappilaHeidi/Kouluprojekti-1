import duckdb as dd
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from datetime import datetime, timedelta




db_file = "/code/data/duckdb.database"

def fetch_nodes():
    con = dd.connect(database=db_file)
    array = con.sql("SELECT DISTINCT node_id FROM Silver_SensorData WHERE node_id").fetchall()
    con.close()
    return array

def read_db_to_df(tbl: str, node_name: str = None):
    '''
    Hakee rivit tietokannasta ja palauttaa dataframen

    Args:
        tbl (str): Taulun nimi 
        node_name (str): Noden nimi, jos None, hakee kaikki noden rivit

    Returns:
        pandas.DataFrame: df
    '''
    if node_name:
        con = dd.connect(database=db_file)
        df = con.sql(f"SELECT * FROM {tbl} WHERE node_id = {node_name}").df()
        con.close()
        return df
    else:
        con = dd.connect(database=db_file)
        df = con.sql(f"SELECT * FROM {tbl}").df()
        con.close()
        return df
    
def read_paths(df: pd.DataFrame):
    '''
    Hakee reittien alkamis- ja päättymispisteet ja palauttaa 
    suodatetun dataframen uusilla indekseillä ja sarakkeilla
    Hae yhtä reittiä: df_ensimmainen = df.loc[0]
    Kaikki löydetyt reitit: len(df.groupby(level=0))
    Args:
        df (pd.DataFrame): df

    Returns:
        pandas.DataFrame: df
    
    '''
    df = df[(df['x'] >= 550)] # filter for out of bounds carts that are outside of the shop routes
    df['time_diff'] = df['timestamp'].diff() #if new values are not added before 1min, we can assume the cart have left the shop
    #this is for finding the carts that are resting after a round trip in shop. They rest at either charging stations or out of the shop before they are taken in again
    iloc_list = []
    for index, value in df.iterrows():
        if (value['time_diff'] > pd.Timedelta(minutes=6)):
            iloc_list.append(index)
    paths_values = np.arange(0, len(iloc_list), 1) #will be used for multi-index value naming and finding new trips
    
    for i in range(len(iloc_list)-1): #needs to be iterated so we can use between values of iloc1-iloc2-ilocn and assign path values from list
        start_index = iloc_list[i]
        end_index = iloc_list[i+1]

        #all path samples that are < 150 or > 10000 rows, will be ignored
        if (len(df.loc[start_index:end_index]) > 150) and (len(df.loc[start_index:end_index]) < 10000): #filter out the impossible or incomplete customer paths. Short rows are indication of insufficient datasample
            df.loc[start_index:end_index, "paths"] = paths_values[i] #last index will be ignored since we cannot be certain of complete cart round
    
    #make multi-index df for easier query
    df.set_index(['paths', 'timestamp'], inplace=True)


    return df

def count_paths(df: pd.DataFrame):
    '''
    Laskee reittien määrän
    Args:
        df (pd.DataFrame): df

    Returns:
        int: reittien määrä
    '''
    return len(df.groupby(level=0))

def _path_check(df: pd.DataFrame, istart, iend): #checks for inconsistent paths and removes the rows for easier paths finding later
    '''
    Tekee välitarkistuksen yhdelle reitille ja poistaa rivejä jos epäjohdonmukaisuutta, kuten sinkoilevat datapisteet.
    Tämä auttaa löytämään huonot datapisteet ja suodattamaan reittejä myöhemmin.#

    Args:
        df (pd.DataFrame): df
        istart (int): start index
        iend (int): end index#

    Returns:
        pandas.DataFrame: df
    '''
    df_check = df.loc[istart:iend]#

    df_check['distance'] = ((df_check['x'] - df_check['x'].shift())**2 + (df_check['y'] - df['y'].shift())**2)**0.5
    threshold_distance = 800 #max ero edelliseen datapisteeseen
    df_mask = []#

    for indexes, rows in df.iterrows():
        if rows['distance'] > threshold_distance: # and rows['time_diff'] < pd.Timedelta(seconds=10)
            index_loc = (df.loc[indexes].shift().name) #vertausarvo indexinä
            i = 2#

            for index2, rows2 in df.loc[index_loc:].iterrows():
                df_test = df.loc[[index_loc,index2]]
                df_test['distance'] = ((df_test['x'] - df_test['x'].shift())**2 + (df_test['y'] - df_test['y'].shift())**2)**0.5
                i += 1#

                if df_test['distance'].iloc[-1] > threshold_distance:
                    df_mask.append(index2)#

                elif i == 3:
                    continue
                else:
                    break#

    df.drop(df_mask, inplace=True)#

    return df


def chart_df(df_start, df_end):
    '''
    Yhdistää kaksi dataframea yhteen area_chart plottausta varten.
    Vaatii reittiflagit. Käytä dataframet ensiksi "read_flags()"-funktion
    kautta.
    Args:
        df_start (pd.DataFrame): df
        df_end (pd.DataFrame): df

    Returns:
        pandas.DataFrame: df
    '''
    df1 = df_start.reset_index().drop(columns=['x', 'y', 'node_id'])
    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df1.index = df1['timestamp'].dt.date
    df1 = df1.groupby(df1.index)['paths'].nunique()
    df1 = df1.reset_index()
    df1['timestamp'] = pd.to_datetime(df1['timestamp'])

    df2 = df_end.reset_index().drop(columns=['x', 'y', 'node_id'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])
    df2.index = df2['timestamp'].dt.date
    df2 = df2.groupby(df2.index)['paths'].nunique()
    df2 = df2.reset_index()
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])
    

    # Create a dataframe with index numbers from 1-31
    index = pd.date_range(start='2023-01-01', end='2023-01-31', freq='D').strftime('%d').astype(int)

    # Create a dataframe with the column from df1 that matches datetime.days to index number
    data = df1.groupby(df1['timestamp'].dt.day)['paths'].sum().reindex(index=index, fill_value=0)
    data2 = df2.groupby(df2['timestamp'].dt.day)['paths'].sum().reindex(index=index, fill_value=0)
    
    # Create a new dataframe with the index numbers and the data

    chart_data = pd.DataFrame({'Päivät': index, 'kk1': data, 'kk2': data2})


    #new_df = new_df.drop_duplicates()
    #chart_data = pd.concat([test, test2], ignore_index=True)
    
    return chart_data


def draw(df, show_calibration_data = None):
    # Get image size with this method
    img = Image.open('../kauppa.jpg')
    width, height = img.size
    print("pixel size", img.size)


    # Create image widget
    file = open("../kauppa.jpg", "rb")
    image = file.read()
    #widgets.Image(
    #    value=image,
    #    format='png',
    #    width=width,
    #    height=height,
    #)

    # Draw on image
    d = ImageDraw.Draw(img)

    # Calibration of coordinates
    x_offset = 111  # x offset
    y_offset = 23   # y offset
    x_max = 1076;  # node_x_max = 10406
    y_max = 563;  # node_y_max = 5220
    x_scale = 1166/10500
    y_scale = 563/5150


    def scale_coords(x,y):
        xr = (x*x_scale)+x_offset
        yr = (y*y_scale)+y_offset
        return xr, yr

    for index, row in df.iterrows():
        (x,y) = scale_coords(row.x, row.y)
        #test
        
        d.rectangle((x,y,x+2,y+2), fill=(int(row.node_id)%255,0,0,20))
    
    def show_cal_data():
        #y-akselin 0-linja kuvassa
        #px = 26
        d.line(xy=(0, 26, 1280, 26), 
              fill=(0, 128, 0), width = 3)

        #x-akselin 0-linja kuvassa
        #
        d.line(xy=(112, 0, 112, 650),
               fill=(0, 128, 0),
                width = 3)
        
        #y-akseli alareuna
        d.line(xy=(0, 593, 1280, 593),
               fill=(0,500,20),
               width=3)
        
        #x-akseli oikea reuna
        d.line(xy=(1250, 0, 1250, 617),
               fill=(0,500,20),
               width=3)
        #triggerline
        d.line(xy=(200, 277, 200, 363),
               fill=(0,500,20),
               width=3)

        #Latausaseman sijainti 1krs
        d.rectangle((111,296, 135, 320),
                    fill=(255,100,100,255))
        
        #Latausaseman sijainti 0krs
        d.rectangle((130, 400, 180, 450),
                    fill=(255,100,100,255))

        # Teksti kiinnostaville kohteille kuvissa
        #latausaseman teksti
        d.text(xy=(95, 325), 
              text="Latausasema",
              font_size = 12,
              fill=(0, 127, 0))
        #latausaseman teksti
        d.text(xy=(181, 451), 
              text="Latausasema 0krs.",
              font_size = 12,
              fill=(0, 127, 0))
        #triggerline teksti
        d.text(xy=(174, 363), 
              text="Triggerline",
              font_size = 12,
              fill=(0, 127, 0))
        #x, y = 0 teksti
        d.text((115, 5),
               text= "x,y=0",
                font_size=12,
                 fill=(0,127,0))
        #x,y = max teksti
        d.text((1130, 600),
               text= "x,y=(10406, 5220)",
                font_size=12,
                 fill=(0,500, 20))
        
    if show_calibration_data:
        show_cal_data()
        
    return img

