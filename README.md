# spotify_playlist_csv
Create a .csv from a spotify playlist

# Instructions

Firstly, for your safety, I recommend you build the exe from source code. But if you don't know how to do that
you can download the .exe in the dists directory.

1. Get the `Spotify_playlist_to_CSV.exe` file and put it in a folder somewhere
2. Double-click on the .exe to run it. This will generate the settings file `spotify_playlist_to_csv.ini`
3. Open the settings file in a text editor (NOT MS Word. Use something like notepad)
4. In the settings file you will see two lines like: `client_id=PUT_YOUR_CLIENT_ID_HERE
client_secret=PUT_YOUR_CLIENT_SECRET_HERE`.  
5. You need to get your own IDs from spotify to fill in these two options. There are instructions at https://developer.spotify.com/documentation/general/guides/authorization/app-settings/  You can choose any app name you want.
6. Find the client id and the client secret from your spotify app's overview screen. You need to press the green "SHOW CLIENT SECRET" words to see the client secret.
7. Copy the client id and the client secret into the `spotify_playlist_to_csv.ini` file (see step 4)
8. You only have to do the client id and client secret once, unless they are changed at the spotify end.
9. The rest of the .ini file shows you the columns (and their order) you want in the output. You can't add anything extra here, but you can delete (or comment) those columns you don't want.
10. Create a text file (again, don't use MS Word. Use notepad or similar) with one playlist id per line.
11. Drag the text file onto the .exe.
12. Wait. It's not very fast :-)

You can also run it from the command line and pass in the playlists file on the command line.

# Building from source

Brief instructions for python coders to create the exe on Windows:

1. clone the repo
2. Install spotipy and pyinstaller in your virtual environment.
3. Run `pyinstaller .\main.spec`