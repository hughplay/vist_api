# VIST API

*fork from [lichengunc/vist_api](https://github.com/lichengunc/vist_api)*

This API is used to load Visual StoryTelling Dataset ([VIST](http://visionandlanguage.net/VIST/index.html)).
The dataset currently contains Description-in-Isolation (DII) and Story-in-Sequence (SIS) annotations.

## Setup Google API client

`download.py` is rewritten by [Mr.Blue](https://github.com/hughplay) with the google Drive API v3. It downloads the dataset from the google drive based on `file_list.txt` and saves files in the `out_dir` directory (default is `./vist`). `download.py` supports resume download and check the sha1sum of the downloaded files. Befor running `download.py`, you need to setup the google API client. Please follow the instructions below to setup the google API client.

1. Go to [Google API Console](https://console.developers.google.com/apis) and create a new project.
1. Go to [Credentials](https://console.developers.google.com/apis/credentials).
1. Click "Create credentials" and select "OAuth client ID".
1. Select "Application type" as "Desktop app" and click "Create".
1. Click the "download icon" of the newly created client under "OAuth 2.0 Client IDs".
1. Click "DOWNLOAD JSON" and save the file as `credentials.json` in the root directory of this repository.
1. Run `pip install -r requirements.txt` to install the required packages.
1. Run `python download.py`.
1. Click the link in the terminal and follow the instructions to authorize the application.
1. If you run `python download.py` on the remote server, the final jump page in the browser cannot be accessed. In this case, you need to copy the URL from the browser and run `curl <URL>` in your remote server to complete the authorization.
1. After the authorization, there will be a file named `token.json` in the root directory of this repository. Next time you run `python download.py`, you can skip the authorization step.

References:

- https://developers.google.com/drive/api/guides/api-specific-auth
- https://developers.google.com/drive/api/quickstart/python
- https://developers.google.com/drive/api/guides/manage-downloads
- https://developers.google.com/drive/api/v3/reference/


## Download Dataset

```bash
# note the dataset is of big size ~300GB.
python download.py --out_dir ./vist
# Download Description-in-Isolation dataset
wget http://visionandlanguage.net/VIST/json_files/description-in-isolation/DII-with-labels.tar.gz
# Download Story-in-Sequence dataset
wget http://visionandlanguage.net/VIST/json_files/story-in-sequence/SIS-with-labels.tar.gz
```

## Usage
The "vist.py" is able to load both DII and SIS datasets.
```bash
# locate your vist_directory, which contains images and annotations
vist_dir = '/playpen/data/vist'
# SIS instance
sis = vist.Story_in_Sequence(vist_dir)
# DII instance
dii = vist.Description_in_Isolation(vist_dir)
```





