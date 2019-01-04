import requests
import sys
import json
import codecs
import os
import re
from bs4 import BeautifulSoup
from datetime import date


def main():
    # Request a reponse from the url and store it.
    # Contains all the data we need.
    # The structure of the JSON is:
    # Root node: Date: Article 0, 1, 2, 3, ...
    response = requests.get('http://www3.nhk.or.jp/news/easy/news-list.json')

    # utf-8-sig better at decoding than utf-8.
    response.encoding = 'utf-8-sig'

    # Since the url we are using is a json file, we need
    # parse it using json. response.text contains content in unicode.
    # Load the content of the response and convert it to something
    # python can understand.
    doc_json = json.loads(response.text)

    month = sys.argv[1]

    # Extract all articles in defined month.
    parse(doc_json, month)

# Get all of the articles in specified month.
def parse(doc_json, month):
    # Store the articles parsed as a dictionary.
    articles = {}

    # Loop through the doc_json as a list of dicts'(key, value)
    # tuple pairs. Root node is node 0.
    for date_node, news_node in doc_json[0].items():
        # Regex match: digits[0-9] + minus and all following ones
        # + month + -digits[0-9] and all following digits.
        # eg. 2018-08-21 = (\d+)(-+)month(-\d+).
        regex_pattern = r'(\d+)' + r'(-+)' + re.escape(str(month)) + r'(-\d+)'

        # Find all the child nodes of the root node that has the pattern
        # defined in regex.
        matched = re.search(regex_pattern, date_node)

        # If matched is found...
        if matched:
            # Create a dictionary entry, and use the date as the key,
            # and the content as the value.
            # Content is the child nodes (news) of the matched
            # date nodes.
            articles[matched.group()] = news_node
    # Extract each article and title, then create an html file.
    parseMonth(articles, month)

# Get all the news items in the month specified and create a format html file
# that has all the


def parseMonth(articles, month):
    # Return month as a string.
    month = str(month)
    # Get today's date, then format it to year-month-day.
    # Then split date into a list with the delimiter '-'.
    # Finally get the year, which is the first item.
    year = ''.join(date.today().strftime("%Y-%m-%d").split('-')[0:1])
    # Create new string of year_month.
    join_str = year + '_' + month
    # Get current execution directory.
    save_path = os.getcwd()
    # Create new output path for the html file.
    output = save_path + '/' + join_str + '/' + join_str + '.html'
    # Store output path (folder).
    folder = join_str

    # Check if the folder for the month specified exists.
    if os.path.isdir(folder) == False:
        # If not, create it.
        os.makedirs(folder)
        print("Directory \"" + folder + "/\" created")
    # If so, do nothing, and abort.
    elif os.listdir(folder):
        print("Directory \"" + folder + "/\" exists!\n\nAbort.\n")
        return

    # Store all the news items and it's content.
    items = []
    contents = []

    # For each news item, append the news item to items and append the content
    # to contents.
    for date_node, content in articles.items():
        for news in content:
            item = parseNews(news)
            items.append(item)
            contents.append(item["content"])

    # Then reverse the list, because it is last to first, but we want first to last.
    contents.reverse()

    # Open a stream to write.
    with open(output, "w", encoding="UTF-8") as stream_f:
        # XML declaration. Write to stream_f.
        print('<?xml version="1.0" encoding="UTF-8" ?>', file=stream_f)
        # HTML declaration.
        print("<!>", file=stream_f)
        # Set HTML language to japanese.
        print("<html lang='ja'>", file=stream_f)
        # HTTP header for char encoding for doc. Content is composed of xhtml and xml.
        print('''<head><meta http-equiv="content-type" content="application/xhtml+xml; 
        charset=UTF-8" >''', file=stream_f)
        #
        print('''<style type="text/css">body { margin-left: 1em; margin-right: 1em; 
        margin-top: 2em; margin-bottom: 2em; writing-mode:tb-rl; 
        -epub-writing-mode: vertical-rl; -webkit-writing-mode: vertical-rl; 
        line-break: normal; -epub-line-break: normal; -webkit-line-break: normal; 
        color: #eee; font-size: larger; background: #111; line-height: 200%; 
        font-family: "Hiragino Sans", sans-serif; } p { text-indent: 1em; 
        font-size: medium } h1 { font-weight: bold; font-size: large; }
        </style>''', file=stream_f)
        print("</head>", file=stream_f)
        print("<body>", file=stream_f)
        print("<br />".join(contents), file=stream_f)
        print("</body>", file=stream_f)
        print("</html>", file=stream_f)
        print("File \"" + output + "\" created")
    print("The month's news were downloaded from NHK.")

# Return and get the title, date, and news item content.


def parseNews(news):
    # Get the news_id, which is a unique identifier used in the url of the news item.
    news_id = news['news_id']
    # Get the publish time of the news item. Replace all ':' to '-'.
    # So final news_time is 'year-month-day hour-minute-seconds'.
    news_time = news['news_prearranged_time'].replace(':', '-')
    # Get the news item title (Japanese).
    title = news['title']
    # Get the title with ruby. Not to be confused with the Ruby programming language.
    # The ruby tag is used to annotate characters with smaller ones above.
    # In this case, we are dealing with furigana.
    title_ruby = news['title_with_ruby']
    # Create the new url for the news item.
    news_uri = ('http://www3.nhk.or.jp/news/easy/' + str(news_id) + '/' + str(news_id)
                + '.html')

    # Get the response from the url. This shoudl be the news item.
    response = requests.get(news_uri)
    response.encoding = 'utf-8'

    # We will use BeautifulSoup to parse the response as a html.
    soup = BeautifulSoup(response.text, 'html.parser')
    # Get the news item time.
    date = soup.find('p', attrs={'id': 'js-article-date'})
    # Get the news item title and including the ruby tags.
    title = soup.find(
        'h1', attrs={'class': 'article-main__title'})  # .find('h2')
    # Get the content of the news item.
    article = soup.find('div', attrs={'id': 'js-article-body'})

    # Find all elements in article that have 'a'.
    # Then strip all tags.
    for a in article.findAll('a'):
        a.unwrap()
        #voice = {}

    # Return as a dictionary with the values: title + date + article, and the voice?
    # Created a dictionary with voice and voice array? Probably unused.
    return {
        "content": str(title) + str(date) + str(article),
        # "voice": voice
    }


main()
