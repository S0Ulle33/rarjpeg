Rarjpeg finder
==============

**Rarjpeg finder** is a small console script to work with Rarjpegs.

Features
--------

-   **Easy to use**: You can easily download Rarjpeg finder and start using it right away.
-   **Checks entire folder**: You can specify not only one file, but whole folder.
-   **Extracts content**: After scanning, it'll unpack the archives in the specified folder (see Usage for details).

Requirements
------------

-   Python 3.6 or higher
-   `rarfile`

Installing
----------

Clone it or download manually.
```shell

    git clone https://github.com/S0Ulle33/rarjpeg.git
    cd rarjpeg
```

Install using system pip
```shell
    pip install -r requirements.txt
```
or using pipenv.
```shell
    pipenv install
```

Usage
-----

Folder to unpack by default is `extracted_rarjpegs`, you can specify that in `rarjpeg_class.py` in `EXTRACT_FOLDER` variable.

```
usage: find_rarjpeg.py TARGET [-e]

Checks TARGET image or folder for rarjpeg(-s).

positional arguments:
  target         name of the FILE or DIRECTORY to check

optional arguments:
  -h, --help     show this help message and exit
  -e, --extract  extract files from found rarjpegs
```
