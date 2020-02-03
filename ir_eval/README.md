# IR: Indexing and Ranking

## Indexing
Indexing part consists of following processes:
  - [x] Parsing subtitle files and write them into database.
  - [x] Generate inverted index 
  - [ ] Update the sentences in DB with the character information extracted from the quote-character matched quotes.
  
### Subtitle Parser
subtitle_parser.py contains the class SubtitleParser. It iterates all of the .srt files in given directory, parses and write them into sentences collection of db with document and movie id information.

### Inverted Index 
index_generator.py file is a command-line runnable script. It takes two arguments, stemming and remove_stopwords. It enables/disables the stemming and removing stopwords functions in the preprocess according to the arguments set. It updates the index collections in the databese. If remove_stopwords is enabled, it updates the inverted_index collection. Otherwise it updates the inverted_index_with_stopwords collection. An example running script as follows:

```commandline
$ python index_generator.py --stemming True --remove_stopwords True
```
