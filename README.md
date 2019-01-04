# NHK Easy To PDF

## Description:
Download all NHK Easy articles of a particular month, and combine them into a single PDF file.

TO USE:
```shell
python3 nhk-easy.py <mth>

# where <mth> is the specified mth 
# year is calculated using the sys clock
```

output of the program should create a dir where the script was ran.

eg: if you ran the python3 script in `~` (home dir for linux/macOS), it should create a folder `yyyy_mm` and would create 2 other files inside the dir with the extensions `.opf` and `.html` respectively.

In order to convert it into a `.mobi` file, you would need `kindlegen`, im not going to explain the how to here, search the interwebs for more information.

to be precise run the code
```
python3 nhk-easy.py <mth>

// then after the operation is done, run the code

kindlegen <xxxx.opf>
```
