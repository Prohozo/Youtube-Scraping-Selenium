### VERSION 1
## Features
- Automatic scrap data from youtube channel you want
- Automatic skip youtube ads
- Clean all the data you collect
## Install packages
```
    pip install -r requirements.txt
```
## Install web driver
- Check your Google Chrome version and download the corresponding version at https://chromedriver.chromium.org/downloads
- Put that in C:\Program Files (x86) or you can change the path whatever you want at line 97 in collect.py

## How to run it
There are three arguments:

- First arg: Youtube channel name, e.g.,"Bill Gates", "Marques Brownlee"
    - If Youtube channel contains space you need put that in a quotation marks: ""
- Second arg: 0, index show that the first video is the lastest video
    - You should always type 0 if not there would be an error
- Third arg: some number, e.g., 50, 10, 100
    - Index show that how many video do you want to scraping, if you want all videos just type: end

```
    python collect.py {Youtube channel name} 0 {number of videos} 
```

![Alt text](./images/howtouse.png?raw=true "How to use")

## Result
![Alt text](./images/2.png?raw=true "Result")
