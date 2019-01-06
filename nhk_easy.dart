import 'dart:async';
import 'dart:convert' show jsonDecode, utf8;
import 'package:http/http.dart' show Response, get;
import 'package:html/dom.dart';
import 'package:html/parser.dart' show parse;

final _url = 'http://www3.nhk.or.jp/news/easy/news-list.json',
    _content = 'Content-Type',
    _typeJSON = 'application/json; charset=utf-8',
    _typeHTML = 'text/html; charset=utf-8',
    _idKey = 'news_id',
    _urlBegin = 'http://www3.nhk.or.jp/news/easy/',
    _urlEnd = '.html',
    _fetchArticlesError = 'Failed to load articles.',
    _fetchNewsError = 'Failed to load news.';
final int _payload = 200;

Future<Iterable> _fetchArticles() async {
  try {
    final Response response = await get(_url, headers: {_content: _typeJSON});
    if (response.statusCode == _payload) {
      Map dates = (jsonDecode(utf8.decode(response.bodyBytes))).first;
      return dates.values.expand((map) => map);
    } else {
      throw Exception(_fetchArticlesError);
    }
  } catch (ex) {
    throw Exception(ex);
  }
}

Future<String> _fetchNews(Map article) async {
  final String id = article[_idKey],
      url = (_urlBegin + id + '/' + id + _urlEnd);

  try {
    final Response response = await get(url, headers: {_content: _typeHTML});
    if (response.statusCode == _payload) {
      final Document document = parse(utf8.decode(response.bodyBytes));
      document.querySelectorAll('img').forEach((x) => x.remove());
      document.querySelectorAll('.playerWrapper').forEach((x) => x.remove());
      document.querySelectorAll('.dicWin').forEach((x) => x.remove());
      document
          .querySelectorAll('rt')
          .forEach((x) => x.innerHtml = '(' + x.innerHtml + ')');
      Element date = document.querySelector('#js-article-date'),
          title = document.querySelector('.article-main__title'),
          article = document.querySelector('#js-article-body');
      return title.outerHtml + date.outerHtml + article.outerHtml;
    } else {
      throw Exception(_fetchNewsError);
    }
  } catch (ex) {
    throw Exception(ex);
  }
}

Future<String> fetchContent() async {
  try {
    final articles = await _fetchArticles();
    List content = [];
    for (Map article in articles) {
      content.add(await _fetchNews(article));
    }
    return content.join('<br/>\n');
  } catch (ex) {
    throw Exception(ex);
  }
}

Future<String> createHTML() async {
  String content = await fetchContent();
  String html = '\n<?xml version="1.0" encoding="UTF-8" ?>' +
      '\n<!>' +
      '\n<html lang=\'ja\'>' +
      '\n<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
      '\n<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8">' +
      '\n<style type="text/css">body { margin-left: 1em; margin-right: 1em;' +
      '\nmargin-top: 2em; margin-bottom: 2em;' +
      '\nline-break: normal; -epub-line-break: normal; -webkit-line-break: normal;' +
      '\ncolor: #eee; font-size: larger; background: #000; line-height: 200%;' +
      '\nfont-family: "Hiragino Sans", sans-serif; } p { text-indent: 1em;' +
      '\nfont-size: medium } h1 { font-weight: 600; font-size: large; } </style>' +
      '\n</head><body>' +
      content +
      '\n</body></html>';
  return html;
}
