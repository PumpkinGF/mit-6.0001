Changes to be made before running as of Sept, 2023

ps5.py
def main_thread(master): section
comment out stories.extend(process("http://news.yahoo.com/rss/topstories")) 
yahoo no longer has description


feedparser.py

section starting with # base64 support for Atom feeds that contain embedded binary data
base64.decodestring -> base64.decodebytes

import collections -> import collections.abc as collections
Callable method now comes from collections.abc instead of collections