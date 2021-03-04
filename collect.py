import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date as dt
from threading import Timer
from clean import clean_data
from title import collect_title
from check import check_input, is_emoji, remove_emoji
from plot import create_dashboard


def timer(start, end):
   hours, rem = divmod(end-start, 3600)
   minutes, seconds = divmod(rem, 60)
   return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)


def insert_to_df():
    try:
        df_export.ID = id_ls
    except ValueError:
        print("Something's wrong with Id list")

    try:
        df_export.Title = title_ls
    except ValueError:
        print("Something's wrong with title list")

    try:
        df_export.Time = time_ls
    except ValueError:
        print("Something's wrong with time list")

    try:
        df_export.View = view_ls
    except ValueError:
        print("Something's wrong with view list")

    try:
        df_export.Date = date_ls
    except ValueError:
        print("Something's wrong with date list")

    try:
        df_export.Like = like_ls
    except ValueError:
        print("Something's wrong with like list")

    try:
        df_export.Dislike = dislike_ls
    except ValueError:
        print("Something's wrong with dislike list")

    try:
        df_export.Url = url_ls
    except ValueError:
        print("Something's wrong with url list")

    try:
        df_export.Comment = comment_ls
    except ValueError:
        print("Something's wrong with Comment list")

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()
start = time.time()

yt_channel = sys.argv[1]
video_ls = []
url_ls = []
id_ls = []

# Check input
start_video, end_video = check_input()
video_ls, sub, url_ls, end_video = collect_title(
    driver, PATH, yt_channel, end_video)

#--------------------------------------------------------------------------------------------------------------------------------------------------

search = driver.find_element_by_id('search')

d = {'ID': [], 'Title': [], 'Time': [], 'View': [], 'Date': [], 'Like': [], 'Dislike': [], 'Comment': [], 'Url': []}
df_export = pd.DataFrame(data=d)
df_error = pd.DataFrame(data=d)

video_title_list = video_ls[start_video:end_video]
url_ls = url_ls[start_video:end_video]
title_ls = []
time_ls = []
view_ls = []
date_ls = []
like_ls = []
dislike_ls = []
comment_ls = []
current_ad = ''
i = start_video

for url in url_ls[start_video:end_video]:
    driver.get(url)
    # Indentify there is an ad or not and skip it
    try:
        ad = driver.find_element_by_class_name(
            'ytp-ad-player-overlay-instream-info')
        print(ad.text)
        current_ad = ad.text
        print('There is an ad!')
        time.sleep(5)
        skip_button = driver.find_element_by_class_name(
            'ytp-ad-skip-button-container')
        print('Found skip button!')
        skip_button.click()
    except:
        print('There is no ad!')

    # Get elements of video -> Print results
    print('------------------------------------------')
    print(f'Video {i+1}:')

    id_ls.append(url_ls[i][32:])
    print(f'Id: {url_ls[i][32:]}')

    title_ls.append(video_title_list[i])
    print("Video:", video_title_list[i])

    try:
        view = driver.find_element_by_xpath(
            '//*[@id="count"]/yt-view-count-renderer/span[1]')
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
        like = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string')
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
        dislike = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string')
        if dislike.text == 'DISLIKE':
            dislike_ls.append(0)
            print("Dislike: 0")
        else:
            dislike_ls.append(dislike.text)
        print("Dislike: ", dislike.text)
    except:
        dislike_ls.append(0)
        print("Dislike: 0")

    print(f'Url: {url_ls[i]}')

    # Scroll down to get number of comment
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(1)
    try:
        comment = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string')
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
            time_ad = int(current_ad.split('\n')[1][-2:])
            time.sleep(time_ad+1)
            driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_RIGHT)
            time_ls.append(str(video_time.text))
        else:
            time_ls.append(str(video_time.text))
        print("Time: ", video_time.text)
    except:
        time_ls.append('0')
        print("Time: 0")
    i += 1
    print('------------------------------------------')


insert_to_df()

end = time.time()
print(
    f'Total time needed for scraping {end_video - start_video} videos:', timer(start, end))
driver.close()

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Data cleaning
clean_data(df_export, yt_channel, df_error)
# Create Dashboard
create_dashboard(df_export, yt_channel, sub)
