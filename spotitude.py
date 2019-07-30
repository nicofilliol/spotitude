"""Spotitude.

Get a user's top 25 tracks and return a 5x5 grid visualization.
"""

from config import Config
from data import get_top_tracks
import spotipy
from visualization import make_visualization
import argparse


if __name__ == "__main__":
    # Parse the input parameters.
    parser = argparse.ArgumentParser(description="Spotitude Customization")
    parser.add_argument(
        "--time_range",
        type=str,
        default="short_term",
        help="Over what time frame the top tracks are computed. "
        + "Valid values: long_term, medium_term and short_term. (default: short_term)",
    )
    args = parser.parse_args()
    if args.time_range not in ["short_term", "medium_term", "long_term"]:
        raise ValueError(
            "Valid values for time_range are: long_term, medium_term and short_term."
        )

    # Get authentication token for Spotify API
    config = Config()
    token = config.get_token()

    if token:
        spotify = spotipy.Spotify(auth=token)
        # Get user's top tracks
        top_tracks_df = get_top_tracks(
            spotify, limit=25, time_range=args.time_range, save=True
        )

        # Create visualization
        make_visualization(top_tracks_df)

    import eel
    from playlist import Playlist
    import webbrowser

    eel.init(".")

    @eel.expose
    def create_playlist():
        """
            Handles button press from top tracks visualization
        """
        print("Playlist created...")
        spotitude_playlist = Playlist(spotify)
        spotitude_playlist.create_spotitude_playlist(
            args.time_range, top_tracks_df["id"].tolist()
        )
        webbrowser.open_new(spotitude_playlist.url)  # open playlist in web browser

    eel.start("index.html", mode="chrome-app")

