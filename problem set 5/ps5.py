# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================

# Problem 1

# TODO: NewsStory


# NewsStory (get method)
class NewsStory(object):
    
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

# PhraseTrigger
# check punctuation
print(string.punctuation)


# +
# PhraseTrigger
class PhraseTrigger(Trigger): # Trigger的继承类
    def __init__(self, phrase):
        self.phrase = phrase
        
    def is_phrase_in(self, text):
        # TRUE if phrase is in text, FALSE if not
        # ignore uppercase lowercase
        
        # 先都变成小写的string
        phrase_lower = str(self.phrase).lower()
        text_lower = str(text).lower()
        
        # text去掉所有space和punc后phrase在text里出现
        # 依然要保留分隔，不能变成一整条string，否则会错误trigger类似‘purplecow’
        # 将所有punctuation都replace成空格，split成list，再join成一个空格间隔的phrase（看phrase例子）
        
        # replace all punctuation with spaces
        for char in string.punctuation:
            text_lower = text_lower.replace(char, ' ')
        # split the text into a list
        text_list = text_lower.split()
        # join the list back to text
        text_join = ' '.join(text_list)
        
# wrong criterion: 'purple cow' in 'purple cows'
#         if phrase_lower in text_join:
#             return True
#         else:
#             return False
        
# wrong criterion 2: 'purple cow' in 'purple cows cow' 会通过test，但不对
#         if phrase_low in text_join and set(phrase_low.split()).issubset(set(text_join.split())):
#             return True # phrase在text里，并且phrase里的所有单词都在text里
#         else:
#             return False

        # loop through the two words lists, see if there is a match
        # two lists: phrase_low.split(), text_join.split()
        for i in range(len(text_join.split()) - len(phrase_lower.split()) + 1):
            if text_join.split()[i : i + len(phrase_lower.split())] == phrase_lower.split():
                return True
        return False


# -

string.punctuation

# try the structure in a function
phrase = 'PURPLE COW'
phrase_lower = str(phrase).lower()
text = 'The purple cow is soft and cuddly.'
text_lower = str(text).lower()
for char in string.punctuation:
    text_lower = text_lower.replace(char, '')
# split the text into a list
text_list = text_lower.split()
# join the list back to text
text_join = ' '.join(text_list)
print(text_join)
if phrase_lower in text_join:
    print(True)
else:
    print(False)


# Problem 3
# TODO: TitleTrigger

# +
# TitleTrigger

# 需要把NewsStory里的title pass到PhraseTrigger里
# 需要另外写一个evaluate method（否则沿用之前的evaluate会报错NotImplementedError）

class TitleTrigger(PhraseTrigger):
#     def __init__(self, story):
#         super().__init__(self)
        
    def evaluate(self, story):
        # 要用的method是is_phrase_in(self, text)，text要用的是story.get_title()
        return self.is_phrase_in(story.get_title())   


# -

# debug用
symbols   = NewsStory('', 'purple@#$%cow', '', '', datetime.now())
s2  = TitleTrigger('purple cow')
s2.evaluate(symbols)
symbols.get_title()
s2.is_phrase_in('purple@#$%cow')


# Problem 4
# TODO: DescriptionTrigger

# DescriptionTrigger
# 和TitleTrigger类似
class DescriptionTrigger(PhraseTrigger):
        
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())   


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# abstract class: no method, 不能实例化
class TimeTrigger:
    def __init__(self, time_str):
        self.time = datetime.strptime(time_str, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone('EST'))


# test strptime
time_str = '3 Oct 2016 17:00:10'
x = datetime.strptime(time_str, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone('EST'))
print(x)

# Problem 6
# TODO: BeforeTrigger and AfterTrigger


# +
class BeforeTrigger(TimeTrigger): # compare story.get_pubdate to time

    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) < self.time
    
class AfterTrigger(TimeTrigger): # compare story.get_pubdate to time

    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) > self.time


# -

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
# TODO: OrTrigger


class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # for every story: if any trigger fires, append
    keep = []
    for story in stories:
        if any(trigger.evaluate(story) for trigger in triggerlist):
            keep.append(story)
    return keep


any(x > 1 for x in [1,2,3])


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip() # remove whitespace from the right end of a string including newline characters ('\n')
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    #print(lines) # for now, print it so you see what it contains!
    
    # 分别处理ADD开头的行及不以ADD开头的行
    # ADD开头：把之后的每一个“，”隔开的元素添加到trigger的list中
    # 不以ADD开头：构造一个词典，对应trigger名字和trigger内容
    user_triggers = [] # trigger list
    trigger_dict = {} # 名字和内容对应的dictionary
    
    for line in lines:
        char = line.split(',')
        if char[0] == 'ADD':
            for i in char[1:]:
#                 user_triggers.append(char[i])
                user_triggers.append(trigger_dict[i])
        elif char[1] == 'TITLE':
            trigger_dict[char[0]] = TitleTrigger(char[2]) # key - value
        elif char[1] == 'DESCRIPTION':
            trigger_dict[char[0]] = DescriptionTrigger(char[2])
        elif char[1] == 'BEFORE':
            trigger_dict[char[0]] = BeforeTrigger(char[2])
        elif char[1] == 'AFTER':
            trigger_dict[char[0]] = AfterTrigger(char[2])
        elif char[1] == 'NOT':
            trigger_dict[char[0]] = NotTrigger(trigger_dict[char[2]])
        elif char[1] == 'AND':
            trigger_dict[char[0]] = AndTrigger(trigger_dict[char[2]], trigger_dict[char[3]])
        elif char[1] == 'OR':
            trigger_dict[char[0]] = OrTrigger(trigger_dict[char[2]], trigger_dict[char[3]])
# trigger_dict = {t1:DescriptionTrigger(Presidential Election), t2:TitleTrigger(Hillary Clinton), ...}
# t5, NOT, t1
# NotTrigger(t1) doesn't make sense, should be NotTrigger(t1在dict中对应的value)

    return user_triggers



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("prisoner")
        t2 = DescriptionTrigger("U.S.")
        t3 = DescriptionTrigger("Iran")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()



