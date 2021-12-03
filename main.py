# Tezos_Art_Bot pulls a random NFT from hic dex and displays them in discord chat with a link and info when $art is called.
# TO DO: Randomize objkt pull request
# TO DO: Add link and/or title/artist/objkt number

# import random
import os
import discord
from replit import db
import requests
import json
import pandas as pd

my_secret = os.environ['botsy_like']
client  = discord.Client()

# retrieve quote from api/turn into json and return it
def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']  
  return quote

# retrieve nft from hicetnunc
def get_art():
  query = """query MyQuery {
  hic_et_nunc_token(limit: 1, order_by: {timestamp: asc}, offset: 10) 
  {
    id
    display_uri
    }
  }"""
  url = 'https://api.hicdex.com/v1/graphql'
  r = requests.post(url, json={'query': query})
  json_data = json.loads(r.text)
  df = pd.DataFrame(json_data)
  df_ipfs_hash = df["data"]["hic_et_nunc_token"][0]["display_uri"]
  df_objkt_id = df["data"]["hic_et_nunc_token"][0]["id"]
  img_string = df_ipfs_hash[7:]
  link_string = f"https://hic.af/objkt/{df_objkt_id}"
  img_url = f"https://cloudflare-ipfs.com/ipfs/{img_string}"
  return img_url

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  # login message
  if message.author == client.user:
    return

  # return inspirational quote
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  # return art
  if message.content.startswith('$art'):
    art = get_art()
    await message.channel.send(art)


client.run(my_secret)
