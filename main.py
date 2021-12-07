# Tezos_Art_Bot pulls a random NFT from hic dex and displays them in discord chat with a link and info when $art is called.
#TO DO: Add rate limiter function for discord

import random
import os
import discord
from replit import db
from keep_alive import keep_alive
import requests
import json
import pandas as pd

my_secret = os.environ['botsy_like']
client  = discord.Client()
# Get a random number to use to pick from list of NFT's


def get_quote():
  """Returns a random Quote from zenquote API"""
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']  
  return quote


def get_art(number):
  """Returns a pseudoRandom NFT from HicDex API"""
  query = """query MyQuery {
  hic_et_nunc_token(limit: 10, order_by: {title: asc}) {
    display_uri
    id
  }
}"""
  url = 'https://api.hicdex.com/v1/graphql'
  r = requests.post(url, json={'query': query})
  json_data = json.loads(r.text)
  df = pd.DataFrame(json_data)
  
  df_ipfs_hash = df["data"]["hic_et_nunc_token"][number]["display_uri"]
  print(df_ipfs_hash)
  df_objkt_id = df["data"]["hic_et_nunc_token"][number]["id"]
  
  img_string = df_ipfs_hash[7:]
  link_string = f"https://hic.art/{df_objkt_id}"
  #link_string = f"https://objkt.link/{df_objkt_id}"
  img_url = f"https://cloudflare-ipfs.com/ipfs/{img_string}"
  
  print(img_url)
  print(link_string)
  return link_string

@client.event
async def on_ready():
  """Send message when bot logs on"""
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  """Defines action in Discord when bot recieves commands"""
  if message.author == client.user:
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if message.content.startswith('$art'):
    num = random.randrange(0,10)
    art = get_art(num)
    await message.channel.send(art)

keep_alive()
client.run(my_secret)
