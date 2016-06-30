#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex.yatsenko
#
# Created:     22/11/2013
# Copyright:   (c) alex.yatsenko 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import random

# "Rotwurst" ASCII obfuscation encoding created by Ben Bryant 09/18/11
# there are 79 printable ASCII chars without mixed case
# supported charset is 61 characters, plus 18 in charset2 will require two characters to encode
# charset2 not implemented/needed here, but offsetted 62nd char reserved for it
# encoded form is strictly alpha numeric (62 characters [a-zA-Z0-9])
# rotwurst encoding key set is the 62 alphanum characters in random order
# the key offset is increased for every character of input, so:
#   a in the first position is the first character of the key
#   b in the first position is the second character of the key
#   a in the second position is the second character of the key
#   b in the second position is the third character of the key
charset = "abcdefghijklmnopqrstuvwxyz0123456789 !\"#$%&'()*+,-./:;<=>?@_"
rotwkey = "7vq9bzrliyKBVJgGXNohZk2DuPH6CmUL4QcEF8AOpa3dWRxt1f5wnjYMIsS0eT"

# Additional notes:
# - if performance needed, use pre-generated ASCII offset tables instead of string.find
# - deterministic one-to-one, so no risk of duplicates introduced by encoding
# - someone can find out the rotwurst key using a few known clear/encoded pairs

def build_rotwurst_key():
  # one-time use to generate rotwkey! reuse rotwkey for life of encoded data
  random.seed()
  rot1 = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  rot2 = ""
  while len(rot1):
    c = random.choice(rot1)
    rot2 += c
    rot1 = rot1.replace(c,"")
  return rot2

def rotwurst_encode(t):
  # return rotwursted form of clear text, assumes all chars in t are in charset
  n = 0
  r = ""
  nLen = len(t)
  while n < nLen:
    f = charset.find(t[n])
    if f == -1:
      c = t[n]
      if c >= 'A' and c <= 'Z':
        c = c.lower()
      else:
        c = '_'
      f = charset.find(c)
    r += rotwkey[(f + n)%62]
    n = n + 1
  return r

def rotwurst_decode(t):
  # decode rotwursted text and return the clear text
  n = 0
  r = ""
  nLen = len(t)
  while n < nLen:
    r += charset[(rotwkey.find(t[n]) - n + 62)%62]
    n = n + 1
  return r
