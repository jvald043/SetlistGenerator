import os
import pprint
import config
import csv
import sys
from spotify_helper import spotify_init
from setlist_helper import get_musicbrainz_id, get_setlist_info

#########################################################################
# Test Variables
artist_name = 'Rise Against'

#########################################################################


def main():
    # This Application will retrieve the songs from setlist FM
    # and create a setlist on Spotify from the latest songs played.
    # Intention is to have a setlist of any band's show based on the songs they have previously played
    # and create a playlist out of it, to prepare for the show

    # Get Variables from User
    # artist_name = input("Enter Artist Name: ")

    # Future: provide second web page to finalize artist based on more information, when count > 1

    # Retrieve mbrainz ID for use in Setlist FM
    mbid = get_musicbrainz_id(artist_name)

    # Get .json setlist_data from setlist FM
    setlist_data = get_setlist_info(mbid)

    pprint.pprint(setlist_data)

    # Set Workbooks for .csv to have a list of songs
    f = open('Concerts/' + artist_name + 'ConcertSetlistCreator.csv', 'wt', encoding='utf-8')

    # Write .csv Headers
    writer = csv.writer(f, delimiter=',')

    writer.writerow(
        (
            'Artist',
            'Tour',
            'VenueName',
            'Song',
            'Set'
        )
    )

    try:
        int(setlist_data['total'])>5
    except:
        print('Not Enough Playlist Data or Does not have any setlist data on setlistFM')
        sys.exit(1)

    # Loop through most recent 15 setlists unless setlists is less than 7
    counter = 15

    if len(setlist_data['setlist']) < counter:
        counter = len(setlist_data['setlist'])

    # Create a Setlist from just the latest Tour name, and one of all songs, later make a set out of it.
    # Last Tour Name
    current_tour_name = ''
    list_of_last_tour_songs = []
    list_of_songs = []
    list_of_venues = []

    for i in range(counter):
        is_tour = False
        current_tour = 'N/A'
        # If tour is not blank, record name of tour
        if 'tour' in setlist_data['setlist'][i]:
            is_tour = True
            if is_tour:
                current_tour = setlist_data['setlist'][i]['tour']['name']
            if not current_tour_name:
                current_tour_name = setlist_data['setlist'][i]['tour']['name']
            list_of_venues.append(setlist_data['setlist'][i]['venue']['name'])
        # If no setlist_data Available
        if len(setlist_data['setlist'][i]['sets']['set']) == 0:
            writer.writerow(
                (  # Artist
                    setlist_data['setlist'][i]['artist']['name'],
                    # Tour
                    current_tour,
                    # Event ID
                    setlist_data['setlist'][i]['venue']['name'],
                    # Songs
                    'No Setlist Created Yet',
                    # Set
                    'N/A'
                )
            )
        else:
            for sets in setlist_data['setlist'][i]['sets']['set']:
                song_set = 'Main'
                for songs in sets['song']:
                    if 'encore' in sets:
                        song_set = 'encore ' + str(sets['encore'])
                    try:
                        # If last tour name is equal to setlist of this set
                        if is_tour:
                            current_tour = setlist_data['setlist'][i]['tour']['name']
                            if current_tour_name == setlist_data['setlist'][i]['tour']['name']:
                                list_of_last_tour_songs.append(songs['name'])
                        else:
                            current_tour = 'N/A'
                        list_of_songs.append(songs['name'])
                        writer.writerow(
                            (
                                # Artist
                                setlist_data['setlist'][i]['artist']['name'],
                                # Tour
                                current_tour,
                                # Event ID
                                setlist_data['setlist'][i]['venue']['name'],
                                # Songs
                                songs['name'],
                                # Set
                                song_set
                            )
                        )
                    except:
                        writer.writerow(
                            (
                                # Artist
                                setlist_data['setlist'][i]['artist']['name'],
                                # Tour
                                current_tour,
                                # Event ID
                                setlist_data['setlist'][i]['venue']['name'],
                                # Songs
                                'No Setlist Created Yet',
                                # Set
                                'N/A'
                            )
                        )
    f.close()


    # List of songs
    print(list_of_last_tour_songs)
    # print(list_of_songs)

    # reduce lists by duplicates
    list_of_last_tour_songs = list(dict.fromkeys(list_of_last_tour_songs))
    list_of_songs = list(dict.fromkeys(list_of_songs))

    # print(list_of_last_tour_songs)
    print(list_of_songs)

    # Once Setlist is created, push setlist to Spotify
    # Create spotify client and scope to modify playlist
    spot = spotify_init()

    # get URI for Track
    spotify_songs = {}
    for songs in list_of_songs:
        spot_results = spot.search(q='track:' + songs + ' artist:' + artist_name, type='track', limit=5)
        if spot_results['tracks']['total'] != 0:
            spotify_songs[songs] = spot_results['tracks']['items'][0]['uri']
    print(spotify_songs)

    # create a playlist with Artist Name
    playlist = spot.user_playlist_create(
        config.CLIENT_USER_ID,
        'Upcoming ' + artist_name + ' tour playlist',
        public=True,
        description='Playlist created of songs played by '
                    + artist_name +
                    ' during their ' +
                    current_tour_name + ' tour')
    # print playlist URL to share
    print(playlist['external_urls']['spotify'])

    for uri in spotify_songs.values():
        spot.user_playlist_add_tracks(
            config.CLIENT_USER_ID,
            playlist['id'],
            [uri])


if __name__ == '__main__':
    main()
