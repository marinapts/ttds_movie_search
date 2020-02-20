from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import csv
import os
import sys
import re
import time
import io
import glob
from datetime import datetime

OPENSUBTITLES_ACCOUNT_NAME = 'ADD_YOUR_OWN_HERE'
OPENSUBTITLES_ACCOUNT_PASSWORD = 'ADD_YOUR_OWN_HERE'
DOWNLOAD_LIMIT = 1004

SLEEP_TIME = 0.4  # seconds to wait before downloading next subtitle. Limit: 40 requests per 10 seconds
SUBTITLES_DIRECTORY = './subtitles'
MOVIES_FILE = './data/missing.csv'
LOG_FILE = './logs/log.txt'
OWNED_IDS_FILE = './data/owned_ids.txt'
UNAVAILABLE_IDS_FILE = './data/unavailable_ids.txt'

log_file = io.open(LOG_FILE, encoding='utf-8', mode='a')
def log(msg):
    log_file.write("{}- {}\n".format(datetime.now().strftime("%m/%d %H:%M:%S"), msg))
    log_file.flush()

owned_ids = set()
with open(OWNED_IDS_FILE, 'r') as file:
    for line in file:
        id = re.sub(r'\s+', '', line)
        if re.match(r'tt\d+', id):
            owned_ids.add(id)

unavailable_ids = set()
with open(UNAVAILABLE_IDS_FILE, 'r') as file:
    for line in file:
        id = re.sub(r'\s+', '', line)
        if re.match(r'tt\d+', id):
            unavailable_ids.add(id)
unavailable_ids_file = open(UNAVAILABLE_IDS_FILE, 'a')
def log_unavailable(unavailable_id):
    log("Subtitles for {} unavailable.".format(unavailable_id))
    unavailable_ids_file.write("{}\n".format(unavailable_id))
    unavailable_ids_file.flush()
owned_ids_file = open(OWNED_IDS_FILE, 'a')
def log_owned(imdb_id):
    log("Subtitles for {} have been downloaded successfully.".format(imdb_id))
    owned_ids.add(imdb_id)
    owned_ids_file.write("{}\n".format(imdb_id))
    owned_ids_file.flush()

download_count = 0
override_filenames = dict()

ost = OpenSubtitles()
ost.login(OPENSUBTITLES_ACCOUNT_NAME, OPENSUBTITLES_ACCOUNT_PASSWORD)

movies_file = io.open(MOVIES_FILE, encoding='utf-8', mode='r')
movies = csv.DictReader(movies_file)
for movie in movies:
    if download_count >= DOWNLOAD_LIMIT:
        log("Download limit of {} reached.".format(DOWNLOAD_LIMIT))
        break
    imdb_id = movie['id']
    if os.path.exists("./subtitles/{}.srt".format(imdb_id)):
        # print("Subtitles for this movie {} have already been downloaded. Skipping...".format(movie['title']))
        continue

    if imdb_id in unavailable_ids:  # we already know that this id is unavailable in OpenSubtitles. Skip...
        continue

    log("=== {} ({}) ratings:{} ===".format(movie['title'], imdb_id, movie['numOfRatings']))

    subtitles = ost.search_subtitles([{'sublanguageid': 'eng', 'imdbid': imdb_id[2:]}])
    if subtitles is None or len(subtitles) == 0:  # not found. Log and Skip...
        log_unavailable(imdb_id)
        time.sleep(SLEEP_TIME)
        continue

    subtitles = sorted(subtitles, key=lambda i: int(i['SubDownloadsCnt']), reverse=True)
    id_subtitle_file = subtitles[0].get('IDSubtitleFile')
    override_filenames[id_subtitle_file] = "{}.srt".format(imdb_id)

    log("Top subtitles file ID {} : {} downloads".format(id_subtitle_file, subtitles[0].get('SubDownloadsCnt')))
    try:
        ost.download_subtitles([id_subtitle_file], output_directory='./subtitles', extension='srt',
                               override_filenames=override_filenames)
    except:
        log("Error downloading subtitles: {}".format(sys.exc_info()[0]))
        time.sleep(SLEEP_TIME)
        continue

    if not os.path.exists("./subtitles/{}.srt".format(imdb_id)):
        print("Something went wrong... The subtitles file was not saved successfully.")
        break

    log_owned(imdb_id)  # we have downloaded it successfully. Let's log it.
    download_count += 1
    time.sleep(SLEEP_TIME)

# Count how many subtitles we have already
print("We now have {} unique subtitle files.".format(len(owned_ids)))
print("{} subtitles downloaded just now.".format(download_count))
print("{} subtitles files in {}".format(sum(1 for _ in glob.iglob(SUBTITLES_DIRECTORY+'/*.srt')), SUBTITLES_DIRECTORY))
log_file.close()
unavailable_ids_file.close()
owned_ids_file.close()


"""
ost = OpenSubtitles()
ost.login('kasparas42180', 'ksfy3SGGPoqI')

data = ost.search_subtitles([{'sublanguageid': 'eng', 'imdbid': '0111161'}])

example = {'MatchedBy': 'imdbid', 'IDSubMovieFile': '0', 'MovieHash': '0', 'MovieByteSize': '0', 'MovieTimeMS': '0',
           'IDSubtitleFile': '1955363451',
           'SubFileName': 'The Shawshank Redemption (1994) 720p BrRip x264 [Dual Audio] [Hindi-English]-LokiST [Silve.srt',
           'SubActualCD': '1', 'SubSize': '126991', 'SubHash': '3267e1f0e8f1c41c7d3fa135db0c4e23',
           'SubLastTS': '02:17:43', 'SubTSGroup': '', 'InfoReleaseGroup': 'SilverRG', 'InfoFormat': 'BluRay',
           'InfoOther': 'DualAudio', 'IDSubtitle': '6783270', 'UserID': '1012060', 'SubLanguageID': 'eng',
           'SubFormat': 'srt', 'SubSumCD': '1', 'SubAuthorComment': '', 'SubAddDate': '2016-11-03 05:35:07',
           'SubBad': '0', 'SubRating': '10.0', 'SubSumVotes': '1', 'SubDownloadsCnt': '99111',
           'MovieReleaseName': '720p BrRip x264 [Dual Audio] [Hindi-English]-LokiST [SilverRG]', 'MovieFPS': '23.976',
           'IDMovie': '2047', 'IDMovieImdb': '111161', 'MovieName': 'The Shawshank Redemption', 'MovieNameEng': '',
           'MovieYear': '1994', 'MovieImdbRating': '9.3', 'SubFeatured': '0', 'UserNickName': 'SuperMau',
           'SubTranslator': '', 'ISO639': 'en', 'LanguageName': 'English', 'SubComments': '0',
           'SubHearingImpaired': '0', 'UserRank': 'trusted', 'SeriesSeason': '0', 'SeriesEpisode': '0',
           'MovieKind': 'movie', 'SubHD': '1', 'SeriesIMDBParent': '0', 'SubEncoding': 'UTF-8',
           'SubAutoTranslation': '0', 'SubForeignPartsOnly': '0', 'SubFromTrusted': '1', 'QueryCached': 1,
           'SubDownloadLink': 'http://dl.opensubtitles.org/en/download/src-api/vrf-19bc0c53/sid-CBQ4nEcBMUK3aN-SLYVoEusrU7f/file/1955363451.gz',
           'ZipDownloadLink': 'http://dl.opensubtitles.org/en/download/src-api/vrf-f5650bba/sid-CBQ4nEcBMUK3aN-SLYVoEusrU7f/sub/6783270',
           'SubtitlesLink': 'http://www.opensubtitles.org/en/subtitles/6783270/sid-CBQ4nEcBMUK3aN-SLYVoEusrU7f/the-shawshank-redemption-en',
           'QueryNumber': '0', 'QueryParameters': {'imdbid': '0111161', 'sublanguageid': 'eng'}, 'Score': 35.99111}

# sort data entries by 'SubDownloadsCnt'
data = sorted(data, key=lambda i: int(i['SubDownloadsCnt']), reverse=True)
id_subtitle_file = data[0].get('IDSubtitleFile')
override_filenames[id_subtitle_file] = 'tt0111161.srt'

ost.download_subtitles([id_subtitle_file], output_directory='./subtitles', extension='srt', override_filenames=override_filenames)
"""
