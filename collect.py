import sys
import os.path
import pathlib
import urllib.request
import dash_table
import dash
import time
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import webbrowser
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dash.dependencies import Input, Output
from datetime import date as dt
from threading import Timer
from random import randint

# Check input

if sys.argv[2] != '0':
    print('Your second input should be 0!')
    sys.exit()
elif int(sys.argv[3]) < int(sys.argv[2]):
    print('Your third input should be greater than 0 ')
    sys.exit()
elif int(sys.argv[3]) < 5:
    print('You need collect more than 5 videos')

start_video = int(sys.argv[2])
if not sys.argv[3] == 'end':
   end_video = int(sys.argv[3])
start = time.time()
yt_channel = sys.argv[1]

def timer(start, end):
   hours, rem = divmod(end-start, 3600)
   minutes, seconds = divmod(rem, 60)
   return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def is_emoji(title):
    valid_symbols = "!@#$%^&*/()_-+={}[] 0123456789\'\"?.:...’,“”…"
    for s in title:
        if (not s.isalpha() and (s not in valid_symbols)):
            return True
    return False


def remove_emoji(vd_title):
    title = vd_title
    valid_symbols = "!@#$%^&*/()_-+={}[] 0123456789\'\"?.:...’,“”…"
    emoji = []
    for s in title:
        if (not s.isalpha() and (s not in valid_symbols) and (s not in emoji)):
            emoji.append(s)
    for emo in emoji:
        title = title.replace(emo, '')
    return title

def insert_to_df():
    try:
        df_export.Title = title_ls
        # print("Title list: ", len(title_ls))
        # print("Title list is OK")
    except ValueError:
        print("Something wrong in title list")

    try:
        df_export.Time = time_ls
        # print("Time list: ", len(time_ls))
        # print("Time list is OK")
    except ValueError:
        print("Something wrong in time list")

    try:
        df_export.View = view_ls
        # print("View list: ", len(view_ls))
        # print("View list is OK")
    except ValueError:
        print("Something wrong in view list")

    try:
        df_export.Date = date_ls
        # print("Date list: ", len(date_ls))
        # print("Date list is OK")
    except ValueError:
        print("Something wrong in date list")

    try:
        df_export.Like = like_ls
        # print("Like list: ", len(like_ls))
        # print("Like list is OK")
    except ValueError:
        print("Something wrong in like list")

    try:
        df_export.Dislike = dislike_ls
        # print("Dislike list: ", len(dislike_ls))
        # print("Dislike list is OK")
    except ValueError:
        print("Something wrong in dislike list")

    try:
        df_export.Comment = comment_ls
        # print("Comment list: ", len(comment_ls))
        # print("Comment list is OK")
    except ValueError:
        print("Something wrong in Comment list")

    # df_export.to_csv(f'{sys.argv[1]}_{sys.argv[3]}_to_{i}.csv', encoding='utf-8-sig', index=False)


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()

driver.get(f'https://www.youtube.com/results?search_query={yt_channel}&sp=EgIQAg%253D%253D')

driver.implicitly_wait(5)

try:
    f = open(os.path.join(pathlib.Path().parent.absolute(),f'assets\\{yt_channel}_avatar.png'))
    f.close()
except IOError:
    time.sleep(1)
    try:
        img = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[1]/div/div[1]/a/div/yt-img-shadow/img')
        src = img.get_attribute('src')
        # download the image
        urllib.request.urlretrieve(src, os.path.join(pathlib.Path().parent.absolute(), f'assets\\{yt_channel}_avatar.png'))
    except:
        print('Try again')
        img = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[1]/div/div[1]/a/div/yt-img-shadow/img')
        src = img.get_attribute('src')
        # download the image
        urllib.request.urlretrieve(src, os.path.join(pathlib.Path().parent.absolute(),f'assets\\{yt_channel}_avatar.png'))
try:
   profile = driver.find_element_by_xpath('//*[@id="avatar-section"]/a')
   time.sleep(0.5)
   profile.click()
   video_playlist = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
       (By.XPATH, '//*[@id="tabsContent"]/paper-tab[2]'))
   )               
   video_playlist.click()
   time.sleep(1)
except:
   driver.close()
try:
    subscribers = driver.find_element_by_xpath(
        '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string')
    sub = subscribers.text[:-12]
    print(sub)
except:
    subscribers = driver.find_element_by_xpath(
        '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string')
    sub = subscribers.text[:-12]
    print(sub)
df = pd.DataFrame(data={'Title': []})
video_ls = []

# Scroll down
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
scroll_time = 1
temp = 0
videos = driver.find_elements_by_css_selector('#video-title')
if sys.argv[3] == 'end':
   while (temp != len(videos)):
      temp = len(videos)
      driver.execute_script("window.scrollTo(0, {screen_height}*{scroll_time});".format(screen_height=screen_height, scroll_time=scroll_time))
      scroll_time += 1
      driver.execute_script("window.scrollTo(0, {screen_height}*{scroll_time});".format(screen_height=screen_height, scroll_time=scroll_time))
      scroll_time += 1
      time.sleep(0.5)
      videos = driver.find_elements_by_css_selector('#video-title')
      time.sleep(scroll_pause_time)
   end_video = len(videos)
   print('Collected all videos!')
else:
   while ((temp != len(videos)) & (len(videos) < end_video)):
      temp = len(videos)
      time.sleep(0.5)
      driver.execute_script("window.scrollTo(0, {screen_height}*{scroll_time});".format(screen_height=screen_height, scroll_time=scroll_time))
      scroll_time += 1
      driver.execute_script("window.scrollTo(0, {screen_height}*{scroll_time});".format(screen_height=screen_height, scroll_time=scroll_time))
      scroll_time += 1
      videos = driver.find_elements_by_css_selector('#video-title')
      time.sleep(scroll_pause_time)
   print(f'Collected {end_video} videos: ')

# Save video title to list-->DataFrame-->CSV
print('Processing..........')
time.sleep(1)
try:
   videos = driver.find_elements_by_css_selector('#video-title')
except:
   videos = driver.find_elements_by_css_selector('#video-title')
for video in videos:
   video_ls.append(video.text)

end = time.time()
print(f'Total time need for scarping {end_video} video titles:', timer(start, end))

# Close
driver.close()

#--------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------

start = time.time()

driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get('https://www.youtube.com')

driver.implicitly_wait(5)

search = driver.find_element_by_id('search')

# df_import = pd.read_csv(f"C:/Users/STARTSUPER/Desktop/web_scraping/{yt_channel}_videos_title.csv")
d = {'Title': [], 'Time': [], 'View': [], 'Date': [],'Like': [], 'Dislike': [], 'Comment': []}
df_export = pd.DataFrame(data=d)

video_title_list = video_ls[start_video:end_video]
title_ls = []
time_ls = []
view_ls = []
date_ls = []
like_ls = []
dislike_ls = []
comment_ls = []

i = start_video

def collect(video_title, suffix, filter):
    if is_emoji(video_title):
        search.send_keys(remove_emoji(video_title) + ' '+suffix)
    else:
        search.send_keys(video_title+' '+suffix)
    search.send_keys(Keys.ENTER)

    # Select filter type
    if filter == 'Rating':
        filter_button = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a')
        filter_button.click()
        filters = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[4]/a')
        filters.click()
    elif filter == 'Video':
        filter_button = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a')
        filter_button.click()
        filters = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[2]/ytd-search-filter-renderer[1]/a')
        filters.click()
    elif filter == 'Shortcut':
        str = ' '
        video_title_2 = str.join(video_title.split(' ', 3)[:3])
        print('Title after cut: ', video_title_2)
        search.send_keys(Keys.CONTROL, "a", Keys.DELETE)
        search.send_keys(video_title_2+' '+suffix)
        search.send_keys(Keys.ENTER)
    time.sleep(0.5)

    images = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//*[@id="video-title"]/yt-formatted-string'))
    )
    print('All videos have chosen!')

    for im in images:
        print(im.text)
        time.sleep(0.1)
        if im.text == video_title:
            print('-->', im.text)
            image = im
            break

    if image.text == video_title:
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(1)
        try:
            image.click()
            print("-->Clicked")
        except:
            print('Opps')
            insert_to_df()
    else:
        driver.find_element_by_tag_name(
            'body').send_keys(Keys.CONTROL + Keys.HOME)
        print('------------')
        print(image.text+" :", type(image.text))
        print(video_title+" :", type(video_title))
    time.sleep(0.5)
    if i == start_video:
      driver.find_element_by_tag_name('body').send_keys('m')

for title in video_title_list[start_video:end_video]:
    try:
        print('Collecting...')
        collect(title, suffix=yt_channel, filter='')
    except:
        print('-----------------------')
        try:
            print("Try again.....")
            search.send_keys(Keys.CONTROL, "a", Keys.DELETE)
            collect(title, suffix=yt_channel, filter='')
        except:
            try:
                print('-----------------------')
                print("Try again 2nd time (No youtube username, no filter)")
                search.send_keys(Keys.CONTROL, "a", Keys.DELETE)
                collect(title, suffix='', filter='')
            except:
                try:
                    print('-----------------------')
                    print("Try again 3rd time (No youtube username, filter by rating)")
                    search.send_keys(Keys.CONTROL, "a", Keys.DELETE)
                    collect(title, suffix='', filter='Rating')
                except:
                    try:
                        print('-----------------------')
                        print("Try again 4th time (Have youtube username, filter by rating)")
                        search.send_keys(Keys.CONTROL, "a", Keys.DELETE)
                        collect(title, suffix=yt_channel, filter='Rating')
                    except:
                        try:
                            print('-----------------------')
                            print("Try again 5th time (Have youtube username, filter by video)")
                            search.send_keys(Keys.CONTROL, "a", Keys.DELETE)
                            collect(title, suffix=yt_channel, filter='Video')
                        except:
                            try:
                                print('-----------------------')
                                print("Try again 6th time (Have youtube username, filter by shortcut)")
                                search.send_keys(
                                    Keys.CONTROL, "a", Keys.DELETE)
                                collect(title, suffix=yt_channel,
                                        filter='Shortcut')
                            except:
                                print("Can't find the video!")
                                print(
                                    f"Stop at video {i}/{len(video_title_list)}: ", title)
                                insert_to_df()
                                driver.close()

    try:
        ad = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[17]/div[1]/div[2]/span[1]/div')
        print('There is a ad!')
        time.sleep(1)
        skip_button = driver.find_element_by_class_name(
            'ytp-ad-skip-button-container')
        print('Found skip button!')
        skip_button.click()
    except:
        print('There is no ad!')
    
    # Get elements of video -> Print results
    print('------------------------------------------')
    print(f'Video {i+1}:')

    title_ls.append(title)
    print("Video:", title)

    try:
        view = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]')
        view_ls.append(view.text[:-6])
        print("Views: ", view.text[:-6])
    except:
        view_ls.append(0)
        print("Views: 0")

    try:
        date = driver.find_element_by_xpath(
            '//*[@id="date"]/yt-formatted-string')
        date_ls.append(date.text)
        print("Date: ", date.text)
    except:
        date_ls.append(0)
        print("Date: Unknown!")

    try:
        like = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string')
        if like.text == 'LIKE':
            like_ls.append(0)
            print("Views: 0")
        else:
            like_ls.append(like.text)
        print("Like: ", like.text)
    except:
        like_ls.append(0)
        print("Like: 0")

    try:
        dislike = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string')
        if dislike.text == 'DISLIKE':
            dislike_ls.append(0)
            print("Dislike: 0")
        else:
            dislike_ls.append(dislike.text)
        print("Dislike: ", dislike.text)
    except:
        dislike_ls.append(0)
        print("Dislike: 0")

    # Scroll down to get number of comment
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(1)
    try:
        comment = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string')
        comment_ls.append(comment.text[:-9])
        print("Comment: ", comment.text[:-9])
    except:
        comment_ls.append(0)
        print('Comment: Comments in this video are turned off')

    # Click -> arrow key to find video time
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(0.5)
    driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_RIGHT)
    try:
        video_time = driver.find_element_by_class_name('ytp-time-duration')
        if video_time.text == '':
            time_ls.append(0)
        else:
            time_ls.append(video_time.text)
        print("Time: ", video_time.text)
    except:
        time_ls.append(0)
        print("Time: 0")

    print('------------------------------------------')

    # Clear search bar
    search = driver.find_element_by_id('search')
    search.send_keys(Keys.CONTROL, "a", Keys.DELETE)
    i += 1

insert_to_df()

end = time.time()
print(f'Total time need for scraping {end_video - start_video} videos:', timer(start, end))
driver.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------
# Data cleaning
print('------------------------------------------')
print('Cleaning data.....')

if 'Unnamed: 0' in df_export.columns:
    df_export.drop('Unnamed: 0',axis=1, inplace=True)

df_export.drop(df_export[df_export.Time.isnull()].index.to_list(), inplace=True)

df_export.loc[:,'Time'] = df_export.Time.apply(lambda x: round(float(x.split(':')[0]) + (float(x.split(':')[1])/60),2))
df_export.loc[:,'Date'] = df_export.Date.apply(lambda x: x.replace('Streamed live on ',''))
df_export.loc[:,'Date'] = df_export.Date.apply(lambda x: x.replace('Premiered ',''))
df_export.Date = pd.to_datetime(df_export.Date)

df_export.View = pd.to_numeric(df_export.View.str.replace(',',''))

for s in range(1,10):
    if str(s)+'K' in df_export.Like.unique():
        print(str(s)+'K')
try:
    df_export.loc[(df_export.Like.str.len()==2) & (df_export.Like.str.contains('K',regex=False)),'Like'] = df_export[(df_export.Like.str.len()==2) & (df_export.Like.str.contains('K',regex=False))].Like.apply(lambda x: x.replace('K','000')).astype('int')
except:
    pass
try:
    df_export.loc[(df_export.Like.str.len()==4) & (df_export.Like.str.contains('.',regex=False)),'Like'] = df_export[(df_export.Like.str.len()==4) & (df_export.Like.str.contains('.',regex=False))].Like.apply(lambda x: x.replace('.','')).apply(lambda x: x.replace('K','00')).astype('int')
except:
    pass
try:
    df_export.loc[(df_export.Like.str.len()==3) & (df_export.Like.str.contains('K',regex=False)),'Like'] = df_export[(df_export.Like.str.len()==3) & (df_export.Like.str.contains('K',regex=False))].Like.apply(lambda x: x.replace('K','000')).astype('int')
except:
    pass
try:
    df_export.loc[(df_export.Like.str.len()==4) & (df_export.Like.str.contains('K',regex=False)),'Like'] = df_export[(df_export.Like.str.len()==4) & (df_export.Like.str.contains('K',regex=False))].Like.apply(lambda x: x.replace('K','000')).astype('int')
except:
    pass
df_export.Like = pd.to_numeric(df_export.Like)

try:
    df_export.loc[(df_export.Dislike.str.len()==2) & (df_export.Dislike.str.contains('K',regex=False)),'Dislike'] = df_export[(df_export.Dislike.str.len()==2) & (df_export.Dislike.str.contains('K',regex=False))].Dislike.apply(lambda x: x.replace('K','000')).astype('int')
except:
    pass
try:
    df_export.loc[(df_export.Dislike.str.len()==4) & (df_export.Dislike.str.contains('.',regex=False)),'Dislike'] = df_export[(df_export.Dislike.str.len()==4) & (df_export.Dislike.str.contains('.',regex=False))].Dislike.apply(lambda x: x.replace('.','')).apply(lambda x: x.replace('K','00')).astype('int')
except:
    pass
try:
    df_export.loc[(df_export.Dislike.str.len()==3) & (df_export.Dislike.str.contains('K',regex=False)),'Dislike'] = df_export[(df_export.Dislike.str.len()==3) & (df_export.Dislike.str.contains('K',regex=False))].Dislike.apply(lambda x: x.replace('K','000')).astype('int')
except:
    pass
try:
    df_export.loc[(df_export.Dislike.str.len()==4) & (df_export.Dislike.str.contains('K',regex=False)),'Dislike'] = df_export[(df_export.Dislike.str.len()==4) & (df_export.Dislike.str.contains('K',regex=False))].Dislike.apply(lambda x: x.replace('K','000')).astype('int')
except:
    pass
df_export.Dislike = pd.to_numeric(df_export.Dislike)
df_export[df_export.Comment.isnull()]
if str(df_export.Comment.dtype) == 'object':
    df_export.Comment = pd.to_numeric(df_export.Comment.str.replace(',', ''))
df_export.to_csv(f'{yt_channel}_full.csv', encoding='utf-8-sig', index=False)
#-------------------------------------------------------------------------------------------------------------------------------------------------------

app = dash.Dash(
    __name__,
    external_stylesheets=[os.path.join(
        pathlib.Path().parent.absolute(), 'assets\\style.css')]
)

colors = {
    'background': '#111111',
    'text': 'white'
}

app.title = f'{yt_channel} Channel Dashboard'

# df_export = pd.read_csv(f'{yt_channel}_full.csv')

fig = px.line(df_export, x="Date", y='View',
              title='Total views by time', color_discrete_sequence=['#05F4B7'], custom_data=['Title'])

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],

    hoverlabel=dict(
        font_size=16,
    ),

    xaxis={
        'showgrid': False,
        'title': 'Time'
    },
    yaxis={
        'title': 'Views',
        'showgrid': False
    },
    title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 25,
            'family': 'Arial'
        }
    }
)

fig.update_traces(
    hovertemplate="<br>".join([
        'Date: <b>%{x}</b>',
        'Total views: <b>%{y:,}</b>',
        'Title: <b>%{customdata[0]}</b>',
    ])
)

fig2 = px.bar(
    df_export.sort_values(by=['View'])[-5:],
    orientation='h',
    x='View',
    y='Title',
    text='View',
    title='Top 5 videos with most views',
    color_discrete_sequence=['#05F4B7', '#086972', '#071a52'])

fig2.update_traces(
    texttemplate='%{text:.2s}',
    textposition='inside',
    hovertemplate='Title: <b>%{y}</b> <br>View: <b>%{x:,}</b>',
)

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],

    hoverlabel=dict(
        font_size=16,
    ),
    xaxis={
        'showgrid': False,
        'title': 'Views',
    },
    yaxis={
        'title': None,
    },
    title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 25,
            'family': 'Arial'}
    },

)

fig3 = px.bar(
    df_export.sort_values(by=['Like'])[-5:],
    orientation='h',
    barmode='group',
    x=["Like", "Dislike", "Comment"],
    y="Title",
    title="Top 5 videos with most likes",
    color_discrete_sequence=['#05F4B7', '#b31e6f', '#ee5a5a', ])

fig3.update_traces(
    texttemplate='%{x:.2s}',
    textposition='inside',
    hovertemplate='Title: <b>%{y}</b> <br>Engagement: <b>%{x:,}</b>',


)

fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    legend_title_text='Types of engagement',
    hoverlabel=dict(
        font_size=16,
    ),
    xaxis={
        'showgrid': False,
        'title': 'Number of engagements',

    },
    yaxis={
        'title': None,
    },
    legend=dict(
        # yanchor="bottom",
        # y=0.01,
        # xanchor="right",
        # x=0.99,
        title_font_size=8,
        font=dict(
            size=8,
        ),
        itemsizing='trace'
    ),
    title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 25,
            'family': 'Arial',
        }
    }
)

today = f'Updated {dt.today().strftime("%B %d, %Y")}'

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(f'{yt_channel} Channel Dashboard',
                    className='header_title',),
            html.P(f'{today}', className='header_sub'),
            html.Img(
                src=app.get_asset_url(f'{yt_channel}_avatar.png'),
                alt='Youtuber Avatar',
                className='avatar',
                style={
                    'display': 'flex', 'vertical-align': 'middle'}
            ),
        ], className='header'),
    ]),

    html.Div([
        html.Div([
            html.P('Total videos collected', className='P2'),
            html.P(df_export.Title.count(), className='P1')
        ], className='card', style={'display': 'inline-block', 'width': '20%'}),

        html.Div([
            html.P('Total views', className='P2'),
            html.P(f'{df_export.View.sum():,}', className='P1')
        ], className='card', style={'display': 'inline-block', 'width': '20%'}),



        html.Div([
            html.P('Average video duration', className='P2'),
            html.P(str(round(df_export.Time.mean()-df_export.Time.mean() % 1))+':' +
                   str(round(df_export.Time.mean() % 1*60)), className='P1')
        ], className='card', style={'display': 'inline-block', 'width': '20%', 'float': 'right'}),

        html.Div([
            html.P('Subscribers', className='P2'),
            html.P(f'{sub}', className='P1')
        ], className='card', style={'display': 'inline-block', 'width': '20%', 'float': 'right'}),
    ]),

    html.Div([
        html.Div([
            dcc.Graph(
                id='view_by_time',
                figure=fig,
                className='card3',
                style={
                    'color': '#12151F',
                    'backgroundcolor': '#12151F',
                }
            ),
        ])
    ]),

    html.Div([
        html.Div([
            dcc.Graph(
                id='like_chart',
                figure=fig3, className='card3', style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='view_chart',
                    figure=fig2
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}, className='card3'),
        ]),
    ])
])

print('----------------------------------------------------------------------------')
print('Ctrl+C to turn it off!')
print('----------------------------------------------------------------------------')
port = 8050  # or simply open on the default `8050` port

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=port, use_reloader=False)
