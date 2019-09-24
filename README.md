# Chinese python code to English

It translates docstrings, comments and strings. In current version it uses 
[free implementation of Google Translate](https://pypi.org/project/googletrans/). So sometimes it can be not very stable. 
I added Google urls rotation and timeouts to avoid ip ban in case you want to translate big package

**Requires python 3.6+**

# installation
I highly recommend to use virualenv
```
git clone https://github.com/day0market/pychinesecodetoenglish.git
cd  CodeTranslator
pip install -r requirements.txt 
```

# Run
```
python run.py [-h] [--level LEVEL] [--force] source_path destination_path

positional arguments:
  source_path       path to package you want to translate
  destination_path  path where you want to put translated file

optional arguments:
  -h, --help        show this help message and exit
  --level LEVEL     logging level
  --force           force re translate if file already exists


```

It will translate only *.py and *.md files from package. All other files will be just copied to 
destination folder. Please note: .git and __pychache__ folders will be skiped.

