import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotdl.search import SongObject
from spotdl.search import song_gatherer
from spotdl.search import SpotifyClient
from spotdl.download import DownloadManager
from pathlib import Path

# my spotify credentials
client_id =     'bdc300360d8a4873a3474ff1efa894ef'
client_secret = 'ed336bc24a764d94861fe89fae5d1350'

# spotipy spotify client for handling spotipy actions
auth_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# spotdl spotify client for handling spotdl actions
SpotifyClient.init(
    client_id="5f573c9620494bae87890c0f08a60293",
    client_secret="212476d9b0f3472eaa762d90b19b0ba8",
    user_auth=False,
)

# initialize spotdl download manager
downloader = DownloadManager()

# get output path
output_path = str(Path('app/song_downloads').absolute())

# get track metadata from spotify track, and embed it in the response
# (this is for frontend displaying)
def get_track_from_track_url(track_url: str) -> dict:

    # response definition
    response = {
        'status': {
            'signal': '',
            'description': ''
        },
        # gonna use an array to be consistent with the 
        # get_tracks_from_playlist_url function
        'track': [],
    }

    # try to get the song and metadata from the url using spotipy
    try:
        item = sp.track(track_id=track_url)
    except:
        response['status']['signal'] = 'error'
        response['status']['description'] = 'could not retrieve metadata from track using spotipy.'
        return response

    # populate the track array in the reponse only with the metadata i need
    response['track'] = [{ 
        'name': item['name'],
        'artists': item['artists'],
        'album': {
            'name': item['album']['name'],
            'artists': item['album']['artists'],
            'images': item['album']['images'],
            'external_urls': item['album']['external_urls'],
            'release_date': item['album']['release_date']
        },
        'preview_url': item['preview_url'],
        'uri': item['uri'],
        'external_urls': item['external_urls']
    }]

    return response


# get all tracks from spotify playlist along with their metadata, embed them
# in the response and return it (this is for frontend displaying)
def get_tracks_from_playlist_url(playlist_id: str) -> dict:

    # response definition
    response = {
        'status': {
            'signal': '',
            'description': ''
        },
        'playlist_tracks': [],
    }

    # try to get songs and metadata from playlist using spotipy
    try:
        playlist = sp.playlist_items(playlist_id)
    except:
        response['status']['signal'] = 'error'
        response['status']['description'] = 'could not retrieve metadata from playlist using spotipy.'
        return response

    # 'items' are the tracks on the playlist, that's how spotipy calls them
    playlist_items = playlist['items']

    # populate the playlist_tracks array in the reponse only with the metadata i need
    for item in playlist_items:
        if not item['track']['album']['name']:
            continue
        response['playlist_tracks'].append(
            {
                'name': item['track']['name'],
                'artists': item['track']['artists'],
                'album': {
                    'name': item['track']['album']['name'],
                    'artists': item['track']['album']['artists'],
                    'images': item['track']['album']['images'],
                    'external_urls': item['track']['album']['external_urls'],
                    'release_date': item['track']['album']['release_date']
                },
                'preview_url': item['track']['preview_url'],
                'uri': item['track']['uri'],
                'external_urls': item['track']['external_urls']
            }
        )
    
    return response


# try to get spotdl SongObject from spotify track url, then try to download the song
# using that SongObject with help of spotdl and save it in the specified output path, 
# return response with: status, file_name and storage_path.
async def download_single_song(spotify_track_url: str) -> dict:

    # response definition
    response = {
        'status': {
            'signal': '',
            'description': ''
        },
        'file_name': '',
        'storage_path': '',
    }

    # if output_path (defined in this module) doesn't exists
    if not os.path.isdir(output_path):
        response['status']['signal'] = 'error'
        response['status']['response'] = 'output_path does not exists.'
        return response

    # try to get SongObject from url song
    try:
        song_obj = song_gatherer.from_spotify_url(spotify_track_url)
    except:
        response['status']['signal'] = 'error'
        response['status']['description'] = 'could not retrieve SongObject.'
        return response

    # change directory to output path and perform download
    print("OUTPUTPATH")
    print(output_path)
    print("OUTPUTPATH")
    os.chdir(output_path)

    # try to download the song
    try:
        await downloader.download_song(song_obj)
    except:
        response['status']['signal'] = 'error'
        response['status']['description'] = 'could not perform the download.'
        return response

    # Return output path
    # return output_path + '/'+ song_obj.display_name + '.mp3'

    # if everything went ok
    response['status']['signal'] = 'success'
    response['status']['description'] = 'everything went ok in download_single_song.'
    response['status']['file_name'] = song_obj.display_name + 'mp3'
    response['status']['storage_path'] = output_path + '/'+ song_obj.display_name + '.mp3'

    return response