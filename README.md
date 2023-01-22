# PySdarot
 
A Python module to interact with the Sdarot API. For educational purposes only, of course.

## Installation

Start by installing the extra modules neeed to run this project:
```cmd
pip install -r requirements.txt
```

## Usage

The PySdarot modules offers 2 ways of using it- through a Python API, or by running it with
command line arguments.

### Command Line

#### Initial Setup

Start by running the `config` commmand to add the current TLD. For example, if the current URL is sdarot.tv:
```cmd
python pysdarot.py config --tld tv
```

To search up shows/movies, you don't need to sign in. However, to download them, you will need to. You can add your
username and password like this:
```
python pysdarot.py config --username my_sdarot_user --password my_sdarot_pass
```

#### Searching for shows

You can find content using the `search` command:
```cmd
python pysdarot.py search money heist
```

This is what the command gave me, note the number on the left is the **show ID**: 
```text
[+] Found the following shows:
[3284] בית הנייר / Money Heist
[7375] בית הנייר: מטוקיו ועד ברלין / Money Heist: From Tokyo to Berlin
[8085] בית הנייר: קוריאה - קוריאנית / Money Heist Korea Joint Economic Area
[8830] בית הנייר: קוריאה - אנגלית / Money Heist: Korea – Joint Economic Area
```

#### Downloading shows

Once you've found your show, let's download it. The following command will download the show with ID 3284, 
which is Money Heist (we got this from the previous [`search` command](#Searching for shows)). The number `1` indicates
we want to download the first season, and the number `2` indicates we want to download the second episode of that
season. 
```cmd
python pysdarot.py download 3284 1 2
```
To download the entire season in one go, use `-1` as the episode number. This example will downlaod the 
entirety of the first season:
```cmd
python pysdarot.py download 3284 1 -1
```

#### More help

To see all the commands and functionality, you can open the help menu like this:
```cmd
python pysdarot.py -h
```

### Python API

The PySdarot Python API makes it easy to programmatically download shows and movies from the website.
There are many great examples in the `examples` folder (really, [check them out!](examples)), but anyways here
is a very short snippet of how to import and use the base API class:

```python
from pysdarot import PySdarot

# Username and password are only required if you want to download
s = PySdarot('.tw', 'my_sdarot_user', 'my_sdarot_pass')
```
The above code will create a new instance of the API class, where the domain is configured as `sdarot.tw`, and it
will log into your account using your username and password.

## License
[GNU AFFERO GENERAL PUBLIC LICENSE, SEE README](README.md)