from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import csv
import os
import time

DOWNLOAD_LIMIT = 200
SUBTITLES_DIRECTORY = './subtitles'
download_count = 0
override_filenames = dict()

ost = OpenSubtitles()
ost.login('kasparas42180', 'ksfy3SGGPoqI')
movies_file = open('output.csv')
movies = csv.DictReader(movies_file)
for movie in movies:
    if download_count >= DOWNLOAD_LIMIT:
        break
    url = movie['url']
    imdb_id = url.split('/')[-2]
    if os.path.exists("./subtitles/{}.srt".format(imdb_id)):
        # print("Subtitles for this movie {} have already been downloaded. Skipping...".format(movie['title']))
        continue

    print("=== #{} {} ({}) ===".format(movie['index'], movie['title'], imdb_id))

    subtitles = ost.search_subtitles([{'sublanguageid': 'eng', 'imdbid': imdb_id[2:]}])
    subtitles = sorted(subtitles, key=lambda i: int(i['SubDownloadsCnt']), reverse=True)
    id_subtitle_file = subtitles[0].get('IDSubtitleFile')
    override_filenames[id_subtitle_file] = "{}.srt".format(imdb_id)

    print("Top subtitles file ID {} : {} downloads".format(id_subtitle_file, subtitles[0].get('SubDownloadsCnt')))
    ost.download_subtitles([id_subtitle_file], output_directory='./subtitles', extension='srt',
                           override_filenames=override_filenames)
    if not os.path.exists("./subtitles/{}.srt".format(imdb_id)):
        print("Something went wrong... The subtitles file was not saved successfully.")
        break
    download_count += 1
    time.sleep(1)

# Count how many subtitles we have already
print("We now have {} unique subtitle files.".format(len([name for name in os.listdir(SUBTITLES_DIRECTORY) if os.path.isfile(os.path.join(SUBTITLES_DIRECTORY, name))])))


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
