from dataclasses import dataclass

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import csv
import config
import sys

#@dataclass
class Track:
    number: int
    id: str
    href: str
    album_id: str
    album_name: str
    album_date: str
    artist_names: str
    artist_ids: str
    duration: float
    name: str
    popularity: int
    explicit: bool
    isrc: str

    # audio analysis
    end_of_fade_in: float
    start_of_fade_out: float
    loudness_db: float
    bpm: float
    bpm_confidence: float
    time_signature: str
    time_signature_confidence: float
    key: str # key + major/minor
    key_confidence: float
    major_minor_confidence: float

    # audio features
    danceability: float
    energy: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float  # happiness


options = config.read_options()
badopts = set(options.columns) - set(Track.__annotations__.keys())
if badopts:
    print('Unknown columns in ini file:', ','.join(badopts))
    sys.exit(1)

try:
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=options.client_id,
                                                                         client_secret=options.client_secret))
except Exception as error:
    print(error)
    sys.exit(1)


#pl_id = 'https://open.spotify.com/playlist/0J7K5dvE7EOlM0Ev2a4pDQ'
pl_id = 'https://open.spotify.com/playlist/3LHgHAY5IbzqFYUXZskxOp'

def get_name(pl):
    try:
        return sp.playlist(pl, fields=['name'])['name']
    except Exception as error:
        print(error)
        sys.exit(1)

def get_items(pl):
    pl_items = []
    offset = 0
    count = 0
    while True:
        response = sp.playlist_items(pl, offset=offset)
        items = response['items']
        track_ids = [x['track']['id'] for x in items]
        if not items:
            return pl_items
        audio_features = sp.audio_features(track_ids)
        for item, af in zip(items, audio_features):
            item['audio_features'] = af
        for item in items:
            count += 1
            print(f'Track {count}/{len(items)}: {item["track"]["name"]}')
            item['audio_analysis'] = get_audio_analysis(item['track']['id'])
        pl_items += items
        offset += len(items)


def get_audio_analysis(track_id):
    return sp.audio_analysis(track_id)


def pl_item_to_track(item):
    track = item['track']

    album = track['album'] if 'album' in track else None
    t = Track()
    t.number = -1
    if album:
        t.album_id = album['id']
        t.album_name = album['name']
        t.album_date = album['release_date']
    t.artist_names = ','.join(a['name'] for a in track['artists'])
    t.artist_ids = ','.join(a['id'] for a in track['artists'])
    t.duration = int(track['duration_ms'])/1000
    t.explicit = track['explicit']
    t.id = track['id']
    t.name = track['name']
    t.popularity = track['popularity']
    t.isrc = track['external_ids']['isrc'] if 'isrc' in track['external_ids'] else 'unknown'
    t.href = track['external_urls']['spotify'] if 'spotify' in track['external_urls'] else 'unknown'

    def roundit(n):
        return round(n*1000)/1000

    # return

    # af = get_audio_features(t.id)
    af = item['audio_features']
    t.danceability = roundit(af['danceability'])
    t.energy = roundit(af['energy'])
    t.loudness_db = roundit(af['loudness'])
    t.speechiness = roundit(af['speechiness'])
    t.acousticness = roundit(af['acousticness'])
    t.instrumentalness = roundit(af['instrumentalness'])
    t.liveness = roundit(af['liveness'])
    t.valence = roundit(af['valence'])
                        
    t.href = af['track_href']

    # aa = get_audio_analysis(t.id)['track']
    aa = item['audio_analysis']['track']
    t.end_of_fade_in = aa['end_of_fade_in']
    t.start_of_fade_out = aa['start_of_fade_out']
    t.bpm = aa['tempo']
    t.bpm_confidence = aa['tempo_confidence']
    t.time_signature = aa['time_signature']
    t.time_signature_confidence = aa['time_signature_confidence']
    key = aa['key']
    if key == -1:
        t.key = 'unknown'
        t.key_confidence = 0.0
    else:
        #keys = ['C','C♯/D♭', 'D', 'D♯/E♭', 'E', 'F', 'F♯/G♭', 'G', 'G♯/A♭', 'A', 'A♯/B♭', 'B']
        keys = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

        mode = 'major' if aa['mode'] == 1 else 'minor'
        t.key = keys[key] + ' ' + mode
        t.key_confidence = aa['key_confidence']
        t.major_minor_confidence = aa['mode_confidence']

    return t


def write_csv(name, tracks: list[Track]):
    fname = name+'.csv'
    #fields = [x for x in tracks[0].__dir__() if not x.startswith('_')]
    fields = options.columns
    with open(fname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for track in tracks:
            writer.writerow(track.__dict__)


def main(pl_id):
    tracks = []
    name = get_name(pl_id)
    print(f'Playlist Name: {name}')
    items = get_items(pl_id)
    count = 1

    for item in items:
        # print(f'Track {count}/{len(items)}: {item["track"]["name"]}')
        tracks.append(pl_item_to_track(item))
        tracks[-1].number = count
        count += 1
    write_csv(name, tracks)

main(pl_id)
