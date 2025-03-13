import os
import tkinter as tk
from pynput.keyboard import Listener, Key
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

def setup():
    if not os.path.exists("spotify_binds"):
        os.mkdir("spotify_binds")
    
    config_path = "spotify_binds/config.json"
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump({}, f)
    
    with open(config_path, 'r') as f:
        config = json.load(f)

    if 'SPOTIFY_CLIENT_ID' not in config or 'SPOTIFY_CLIENT_SECRET' not in config or 'SPOTIFY_REDIRECT_URI' not in config:
        print("Please set up your Spotify API credentials.")
        client_id = input("Enter your Spotify Client ID: ")
        client_secret = input("Enter your Spotify Client Secret: ")
        redirect_uri = input("Enter your Spotify Redirect URI: ")
        config['SPOTIFY_CLIENT_ID'] = client_id
        config['SPOTIFY_CLIENT_SECRET'] = client_secret
        config['SPOTIFY_REDIRECT_URI'] = redirect_uri
        
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        print("Configuration saved!")
    else:
        print("Spotify API credentials already set.")
    
    return config

def on_press(key):
    try:
        if key.char == "p":  # Play/Pause
            current_playback = sp.current_playback()
            if current_playback and current_playback.get('is_playing'):
                sp.pause_playback()
            else:
                sp.start_playback()
        elif key.char == "n":  # Next track
            sp.next_track()
        elif key.char == "b":  # Previous track
            sp.previous_track()
        elif key.char == "v":  # Volume up
            sp.volume_up()
        elif key.char == "m":  # Volume down
            sp.volume_down()
    except AttributeError:
        pass
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")

def start_spotify(config):
    scope = "user-library-read user-modify-playback-state user-read-playback-state app-remote-control"
    auth_manager = SpotifyOAuth(client_id=config['SPOTIFY_CLIENT_ID'], client_secret=config['SPOTIFY_CLIENT_SECRET'], redirect_uri=config['SPOTIFY_REDIRECT_URI'], scope=scope)
    global sp
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
def main():
    config = setup()  # Get the config with credentials
    start_spotify(config)  # Start Spotify with correct credentials
    
    print("Press 'p' to Play/Pause, 'n' for Next, 'b' for Back, 'v' for Volume Up, 'm' for Volume Down.")
    
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
