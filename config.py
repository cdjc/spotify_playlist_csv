import configparser
import sys
from dataclasses import dataclass

ini_filename = 'spotify_playlist_to_csv.ini'

base_ini_file = '''
# Config file for spotify-playlist-to-csv
#
# Lines (like this one) that start with a # are comments

[Authentication]
# Generate a client_id and client_secret by and put them below.
# Following the instructions at https://developer.spotify.com/documentation/general/guides/authorization/app-settings/

client_id=PUT_YOUR_CLIENT_ID_HERE
client_secret=PUT_YOUR_CLIENT_SECRET_HERE

[CSV Output Columns]
# Comment out the lines you don't want in the CSV
# Reorder the lines to change the order of the columns in the CSV
# More information on what these mean is at https://developer.spotify.com/documentation/web-api/reference/#/

# number is the number in the playlist 
number
id
href
album_id
album_name
album_date
artist_names
artist_ids
duration
name
popularity
explicit
isrc

end_of_fade_in
start_of_fade_out
loudness_db
bpm
bpm_confidence
time_signature
time_signature_confidence
key
key_confidence
major_minor_confidence

danceability
energy
speechiness
acousticness
instrumentalness
liveness
valence
'''


@dataclass
class Options:
    client_id: str
    client_secret: str
    columns: list[str]


def parse_options(cfg: configparser.ConfigParser) -> Options:
    sections = cfg.sections()
    if not cfg.has_section('Authentication'):
        print('No [Authentication] section in ini file. Use the generated .ini file or remove it and rerun to regenerate.')
        sys.exit(1)
    if not cfg.has_section('CSV Output Columns'):
        print('No [CSV Output Columns] section in ini file. Use the generated .ini file or remove it and rerun to regenerate.')
        sys.exit(1)
    columns = cfg.options('CSV Output Columns')

    if not cfg.has_option('Authentication','client_id'):
        print('No "client_id" option in the [Authentication] section of the .ini fle')
        sys.exit(1)
    if not cfg.has_option('Authentication','client_secret'):
        print('No "client_secret" option in the [Authentication] section of the .ini fle')
        sys.exit(1)
    client_id = cfg['Authentication']['client_id']
    client_secret = cfg['Authentication']['client_secret']

    return Options(client_id=client_id, client_secret=client_secret, columns=columns)


def read_options() -> Options:
    cfg = configparser.ConfigParser(allow_no_value=True)
    try:
        options = cfg.read(ini_filename)
    except Exception as error:
        print(error)
        sys.exit(1)
    if not options:
        with open(ini_filename, 'w') as f:
            f.write(base_ini_file)
        print(f'Created .ini file {ini_filename}. Read the file and set the client_id and client_secret options')
        sys.exit(0)
    return parse_options(cfg)
