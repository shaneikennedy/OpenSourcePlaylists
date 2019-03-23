# Open Source Playlists
[![Build status](https://travis-ci.com/shaneikennedy/OpenSourcePlaylists.svg?token=3Vq1AidxBDpgcxcDaRPg&branch=master)](https://travis-ci.com/shaneikennedy/OpenSourcePlaylists)

## Motivation
I often hear people ask "What are some good playlists for ____ ?" and then you listen to that for a while but get sick of it eventually and wish you could just add a few new songs. And while Spotify gives us collaborative palylists, the number of collaborators are limited to people you know and there isn't a review process for adding/removing songs. 

With Open Source Playlists, playlists become massively collaborative. Just open a PR to add a song to a playlist or even open source one of your own playlists.

## How it works
Playlists are defined in yaml files located in the `/playlists/` folder. 
These yaml files have the format:
```yaml
playlist-name:
    songs:
    - name: 'Song name'
      artists: 'Artist1, Artist2...'
      uri: 'song uri'
```
The fields `name` and `artist` are just so that someone can look at the yaml file and know what's in this playlist, but the uri is the only thing that actually matters for adding a song to an open source palylist. On every merge to master Travis CI will run a deploy job that reads every playlist file and update the corresponding playlists in the OpenSourcePlaylists Spotify account.

The [Open Source Playlists on Spotify](https://open.spotify.com/user/3mgko5aytd0cncyc6us4f8zyj?si=BU44RwmiQ7yVY78aacR14Q) account is where you can find/follow any playlists that are defined in this repository.

## Contributing

### Getting set up
**Note**:This repo uses python3.6 and later
You can the docker container provided, but for adding/updating a playlist it makes more sense to use a virtual environment:
```bash
$ python3 -m venv env
$ source env/bin/activate
$ python -m pip install -r requirements.txt
```
After forking this repo you can contribute a few ways
#### Adding a song to a playlist
Find the song you'd like to add on spotify and copy the song uri as shown below:
![](/img/copy-sp-uri.png) 
Then update the `/playlists/` yaml file of your choice and open a PR!

#### Open sourcing your own playlist
I've added a utility script `/src/open_source_my_playlist.py` that is used as follows:
`$ python src/open_source_my_playlist 'your_username' 'your_playlist_name' `

**Note**: Using this script requires that you have a spotify client id and client secret exported as environment variables, and it requires you to set up a Spotify development project with a redirect uri. You can set up a spotify dev project [here](https://developer.spotify.com/dashboard/). 

This script will output a yaml file in the required format, just make sure it's in the `/playlists/` folder and then you're ready to open a PR!

#### General improvements
I am open to any ideas on how to make this easier to use, so feel free to open an issue with an idea or a PR if you are up for doing it yourself.


## Getting my PR merged
I won't be very picky here, as long as you're not trying to add a song by Cannibal Corpse to a playlist called 'Soft Study Music' or something along the lines of that scenario, I will most likely approve the PR.
