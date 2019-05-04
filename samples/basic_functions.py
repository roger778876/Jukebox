import sys
import spotipy
import spotipy.util as util

scope = 'user-read-currently-playing user-read-playback-state'

def curr_song(sp):
  if (type(sp)):
    print sp.currently_playing()["item"]["name"]

def devices(sp):
  for device in sp.devices()["devices"]:
    print device["name"]

def main():
  if len(sys.argv) > 1:
    username = sys.argv[1]
  else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

  token = util.prompt_for_user_token(username, scope) #, clientID, clientSecret, redirectURL)

  if token:
    sp = spotipy.Spotify(auth=token)
    curr_song(sp)
    devices(sp)

  else:
    print "Can't get token for", username



main()