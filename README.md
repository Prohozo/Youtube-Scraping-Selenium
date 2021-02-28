# VERSION 2
## Features
- Automatic scrape data from a youtube channel you want
- Automatic skip youtube ads
- Automatic clean all the data you collect
- Automatic build dashboard
## Output example
- :heart:[Marques Brownlee](http://mkbhd-app.herokuapp.com)
- :blue_heart:[Dave2D](http://dave2d-app.herokuapp.com)
## Video Demo
[![Youtube Channel Dashboard](http://img.youtube.com/vi/dziScYK_M-w/0.jpg)](http://www.youtube.com/watch?v=dziScYK_M-w "Youtube Channel Dashboard Automation | Selenium🤝🏼Dash")
## Install packages
```
pip install -r requirements.txt
```
## Install web driver
- Check your Google Chrome version and download the corresponding version at https://chromedriver.chromium.org/downloads
- Put that in C:\Program Files (x86) or you can change the path whatever you want at line 97 in collect.py

## How to run it
There are three arguments:

- **First arg**: Youtube channel name, e.g.,"Bill Gates", "Dave2D"
    - If the Youtube channel name contains space you need to put that in a quotation marks: ""
- **Second arg**: 0, index show that the first video is the lastest video
    - You should always type 0 if not there would be an error
- **Third arg**: some number, e.g., 50, 10, 100
    - Index show that how many video do you want to scraping, if you want all videos just type: end

```
python collect.py {Youtube channel name} 0 {number of videos} 
```

![Alt text](./README_IMAGES/howtouse.png?raw=true "How to use it in cmd")

## Progress in CMD
![Alt text](./README_IMAGES/progress.png?raw=true "Progress")

## Result
![Alt text](./README_IMAGES/results.png?raw=true "Result")

## Contact
- [Twitter](https://twitter.com/prohozo)
- <tandatvovan@gmail.com>