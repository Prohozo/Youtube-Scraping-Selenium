from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException as er
import pandas as pd
import time
import urllib
import pathlib
import os
import sys
    

def collect_title(driver,PATH,youtube_channel_name, end_video):
    url_ls = []
    
    # Search channel
    driver.get(f'https://www.youtube.com/results?search_query={youtube_channel_name}&sp=EgIQAg%253D%253D')

    driver.implicitly_wait(5)

    # Get avatar of channel
    try:
        f = open(os.path.join(pathlib.Path().parent.absolute(),
                            f'assets\\{youtube_channel_name}_avatar.png'))
        f.close()
    except IOError:
        time.sleep(1)
        try:
            img = driver.find_element_by_xpath(
                '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[1]/div/div[1]/a/div/yt-img-shadow/img')
            src = img.get_attribute('src')
            # download the image
            urllib.request.urlretrieve(src, os.path.join(pathlib.Path().parent.absolute(), f'assets\\{youtube_channel_name}_avatar.png'))
        except:
            img = driver.find_element_by_xpath(
                '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer[1]/div/div[1]/a/div/yt-img-shadow/img')
            src = img.get_attribute('src')
            # download the image
            urllib.request.urlretrieve(src, os.path.join(pathlib.Path().parent.absolute(), f'assets\\{youtube_channel_name}_avatar.png'))
    
    # Go to the channel and click to video tab
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

    # Get subscribers of the channel
    try:
        subscribers = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string')
        subcribers = subscribers.text[:-12]
    except:
        subscribers = driver.find_element_by_xpath(
            '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string')
        subcribers = subscribers.text[:-12]
    df = pd.DataFrame(data={'Title': []})
    video_ls = []

    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    scroll_time = 1
    temp = 0
    # Wait 1 second and collect url of videos
    time.sleep(1)
    videos = driver.find_elements_by_css_selector('#video-title')

    # Scroll down to the bottom and get all videos 
    if sys.argv[3] == 'end':
        while (temp != len(videos)):
            temp = len(videos)
            # driver.execute_script("window.scrollTo(0, {screen_height}*{scroll_time});".format(
            #     screen_height=screen_height, scroll_time=scroll_time))
            # scroll_time += 2
            # driver.execute_script("window.scrollTo(0, {screen_height}*{scroll_time});".format(
            #     screen_height=screen_height, scroll_time=scroll_time))
            # scroll_time += 2
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(1)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(1)
            videos = driver.find_elements_by_css_selector('#video-title')
            print(f'Got {len(videos)}')
            time.sleep(scroll_pause_time)
        end_video = len(videos)
        print('Collected all videos!')
    # Scroll down and get number of videos
    else:
        while ((temp != len(videos)) & (len(videos) < end_video)):
            temp = len(videos)
            time.sleep(1)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(1)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(1)
            videos = driver.find_elements_by_css_selector('#video-title')
            time.sleep(scroll_pause_time)
            
        print(f'Collected {end_video} videos: ')

    # Save video title to list
    print('Processing..........')
    time.sleep(1)
    try:
        videos = driver.find_elements_by_css_selector('#video-title')
    except:
        videos = driver.find_elements_by_css_selector('#video-title')
    
    for video in videos:
        video_ls.append(video.text)
        try:
            url = video.get_attribute('href')
        except(er):
            url = video.get_attribute('href')
        if ('/watch?v=' in url) and url not in url_ls:
            url_ls.append(url)
    # Close
    # driver.close()
    return video_ls,subcribers, url_ls, end_video
