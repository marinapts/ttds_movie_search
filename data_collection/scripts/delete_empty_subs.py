"""
This script recursively goes through the subtitles folders and deletes subtitles files that are empty.
"""
import os
import glob

SUBTITLES_FOLDER = './subtitles'

def is_empty(fpath):
    return not os.path.isfile(fpath) or os.path.getsize(fpath) == 0


count_empty = 0
for filepath in glob.iglob(SUBTITLES_FOLDER+'/*.srt'):
    if is_empty(filepath):
        count_empty += 1
        os.remove(filepath)

print("{} files deleted.".format(count_empty))
