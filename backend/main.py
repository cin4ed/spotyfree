from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import spotyactions

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/search")
async def search(q: str):

    # response definition
    response = {
        'status': {
            'signal': '',
            'description': '',
            'valid_query': False
        },
        'resource': [],
    }

    # validate url and handle search
    if "open.spotify.com" and "track" in q:
        data  = spotyactions.get_track_from_track_url(q)

        response['status']['valid_query'] = True
        
        if data['status'] == 'error':
            debulog(data, 'cannot get metadata from track')

            response['status']['signal'] = 'error'
            response['status']['description'] = 'could not get metadata about the track.'
            return response

        response['status']['signal'] = 'success'
        response['status']['description'] =  'metadata retrieved successfully'
        response['resource'] = data['track']
        return response

    if 'open.spotify.com' and 'playlist' in q:
        data = spotyactions.get_tracks_from_playlist_url(q)

        response['status']['valid_query'] = True

        if data['status'] == 'error':
            debulog(data, 'cannot get metadata from playlist')

            response['status']['signal'] = 'error'
            response['status']['description'] = 'could not get metadata from the playlist.'
            return response

        response['status']['signal'] = 'success'
        response['status']['description'] =  'metadata retrieved successfully'
        response['resource'] = data['playlist_tracks']
        return response

    # if the url is considered invalid
    response['status']['singal'] = 'error'
    response['status']['description'] = 'invalid url'
    response['status']['valid_query'] = False

    return response


# background task called from the download function
def delete_song(song_path: str):
    try:
        os.remove(song_path)
    except:
        debulog(f'{song_path} does not exists.', 'Error in delete_song')


@app.get("/download")
async def download(q: str, background_tasks: BackgroundTasks):

    # response definition
    response = {
        'status': {
            'signal': '',
            'description': ''
        },
        'file_name': ''
    }
    
    # query download and await it
    # file_path = await spotyactions.download_single_song(q)
    data = await spotyactions.download_single_song(q)

    # handle error
    if data['status']['signal'] == 'error':
        debulog(data, 'cannot download song')
        response['status']['signal'] = 'error'
        response['status']['description'] = 'could not download song.'
        return response

    # populate response
    # response['status']['signal'] = 'success'
    # response['status']['description'] = 'song downloaded succesfully'
    # response['file_name'] = data['file_name']

    # ^ idk how to return the response as json and the file at the same time,
    # so i guess we only show error if happens, i would left this here in case
    # i need it in the future

    song_path = data['status']['storage_path']

    background_tasks.add_task(delete_song, song_path)

    return FileResponse(song_path)


# kind of logger
def debulog(data, txt):
    print()
    print(f'------------ {txt} ------------')
    print(data)
    print(f'------------ {txt} ------------')
    print()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)