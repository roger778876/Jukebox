import sys
import spotipy
import spotipy.util as util
from collections import OrderedDict # for search_song(), when removing duplicates
# from track_list

scope = 'user-read-currently-playing user-read-playback-state'

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

      track_list.append(title + " by " + artists)

    else:
      track_list.append("track is explicit")

  # removes duplicates from the track_list
  track_list = list(OrderedDict.fromkeys(track_list))
  i = 1
  for track in track_list:
    print str(i) + ". " + track
    i += 1

# REQUIRES: sp = spotify object, uri = Spotify URI of track
# EFFECTS:  Prints the title/artist corresponding to the URI
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
      search_uri(sp, query)
    else:
      search_song(sp, query, 1)

  else:
    print "Can't get token for", username


main()