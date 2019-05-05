import sys
import spotipy
import spotipy.util as util
from collections import OrderedDict # for search_song(), when removing duplicates
# from track_list

scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'

# def curr_song(sp):
#   if (type(sp)):
#     print sp.currently_playing()["item"]["name"]

# def devices(sp):
#   for device in sp.devices()["devices"]:
#     print device["name"]


# REQUIRES: sp = spotify object, query = search text, 
#           filter_explicit = do not display explicit songs.
# EFFECTS:  Prints a title/artist list of the top 10 results corresponding 
#           to the search query.
#           Calls the search() function from spotipy.
#           Filters out explicit songs if requested.
#           Asks user to choose song from list, then plays it.
def search_song(sp, query, filter_explicit=1):
  # returns a dict of the search results; index by ["tracks"]["items"] to get
  # to a list of "limit" amount of tracks
  sp_results = sp.search(q=query, limit=10, offset=0, type="track")
  track_list = []

  for result in sp_results["tracks"]["items"]:
    is_explicit = result["explicit"]
    if (not(filter_explicit and is_explicit)):
      title = result["name"]
      artists = ""

      artist_list = result["artists"]
      for i in range(0, len(artist_list)):
        artists += artist_list[i]["name"]
        if (i != len(artist_list) - 1):
          artists += ", "

      # TODO make it add a tuple to track_list, not just add the URI
      # to the end of the string
      song_uri = result["uri"]

      track_list.append(title + " by " + artists + " (" + song_uri + ")")

    else:
      track_list.append("track is explicit")

  # removes duplicates from the track_list
  track_list = list(OrderedDict.fromkeys(track_list))
  i = 0
  for track in track_list:
    i += 1
    print str(i) + ". " + track

  # return early if there's no results
  if (i == 0):
    print "No results found."
    return

  # ask user to choose a song, then plays it
  choice = int(raw_input("Choose a song: "))
  if (choice < 1 or choice > i):
    print "Invalid choice!"
  else:
    uri = track_list[choice - 1][-37:-1]
    play_song(sp, uri)


# REQUIRES: sp = spotify object, uri = Spotify URI of track.
# EFFECTS:  Prints the title/artist corresponding to the URI.
def search_uri(sp, uri):
  sp_track = sp.track(uri)
  track = ""

  title = sp_track["name"]
  artists = ""

  artist_list = sp_track["artists"]
  for i in range(0, len(artist_list)):
    artists += artist_list[i]["name"]
    if (i != len(artist_list) - 1):
      artists += ", "

  track += title + " by " + artists

  print track


def get_title_artist(sp, uri):
  sp_track = sp.track(uri)
  title_artist = ""

  title = sp_track["name"]
  artists = ""

  artist_list = sp_track["artists"]
  for i in range(0, len(artist_list)):
    artists += artist_list[i]["name"]
    if (i != len(artist_list) - 1):
      artists += ", "

  title_artist += title + " by " + artists
  return title_artist


# REQUIRES: sp = spotify object, uri = Spotify URI of track.
# EFFECTS: If there is an active device, plays the song to that device.
def play_song(sp, uri):
  device_list = sp.devices()
  if (len(device_list["devices"]) == 0):
    print "No active devices!"
  else:
    uri_to_list = [uri]
    sp.start_playback(uris=uri_to_list)

    print "Playing " + get_title_artist(sp, uri)


def main():
  if len(sys.argv) > 1:
    username = sys.argv[1]
  else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

  token = util.prompt_for_user_token(username, scope) #, clientID, clientSecret, redirectURL)

  if token:
    sp = spotipy.Spotify(auth=token)
    # curr_song(sp)
    # devices(sp)

    query = raw_input("Enter query: ")

    if (query[0:14] == "spotify:track:"):
      # search_uri(sp, query)
      play_song(sp, query)
    else:
      search_song(sp, query, 0) # TODO set back to 1 to turn on filter_explicit

  else:
    print "Can't get token for", username


main()