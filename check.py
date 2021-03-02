import sys

def check_input():
# Check input
    if sys.argv[2] != '0':
        print('Your second input should be 0!')
        sys.exit()
    elif sys.argv[3] == 'end':
        end_video = 100
    elif int(sys.argv[3]) < int(sys.argv[2]):
        print('Your third input should be greater than 0 ')
        sys.exit()
    elif int(sys.argv[3]) < 5:
        print('You need collect more than 5 videos')
    start_video = int(sys.argv[2])
    if not sys.argv[3] == 'end':
        end_video = int(sys.argv[3])
    return start_video, end_video

# Check if there is an emoji
def is_emoji(title):
    valid_symbols = "!@#$%^&*/()_-+={}[] 0123456789\'\"?.:...’,“”…"
    for s in title:
        if (not s.isalpha() and (s not in valid_symbols)):
            return True
    return False

# Rmove emoji in a title
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
