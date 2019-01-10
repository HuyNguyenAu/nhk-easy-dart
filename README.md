# NHK Easy Dart

## Description:
Download all NHK Easy articles of a particular month, and combine them into a single HTML file.

## Requirements:
### Enviroment: 
#### Python:
Python 3.
#### Dart:
Dart 2.
### Modules:
#### Python:
Requests (https://pypi.org/project/requests/), BS4 (https://pypi.org/project/beautifulsoup4/).
#### Dart:
http (https://pub.dartlang.org/packages/http).
## Usage:
#### Python:
```shell
python nhk-easy.py <month>

# where <month> specified month number from 01 - 12. 
```
#### Dart:
```shell
// main.dart
import 'nhk_easy.dart'

var html = await createHTML();
print(html);
```
