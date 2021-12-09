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


def get_quote():
  """Returns a random Quote from zenquote API"""
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']  
  return quote


def get_rand_art(number):
  """Returns a Random NFT from the HicDex API"""
  query = """query MyQuery {
  hic_et_nunc_token(limit: 10, order_by: {title: asc}) {
    display_uri
    id
  }
}
"""
  # post query to hicdex
  url = 'https://api.hicdex.com/v1/graphql'
  r = requests.post(url, json={'query': query})
  json_data = json.loads(r.text)
  # Convert to DataFrame
  df = pd.DataFrame(json_data)
  #Access token number and store in variable
  df_objkt_id = df["data"]["hic_et_nunc_token"][number]["id"]
  # Format into a string to be returned by function
  link_string = f"https://hic.art/{df_objkt_id}"
  return link_string

def get_fresh_art(number):
  """Returns a recently minted NFT from the HicDex API"""
  query = """query MyQuery {
  hic_et_nunc_token(limit: 10, order_by: {timestamp: desc}) {
    display_uri
    id
  }
}
"""
  # post query to hicdex
  url = 'https://api.hicdex.com/v1/graphql'
  r = requests.post(url, json={'query': query})
  json_data = json.loads(r.text)
  # Convert to DataFrame
  df = pd.DataFrame(json_data)
  #Access token number and store in variable
  df_objkt_id = df["data"]["hic_et_nunc_token"][number]["id"]
  # Format into a string to be returned by function
  link_string = f"https://hic.art/{df_objkt_id}"
  return link_string

def get_old_art(number):
  """Returns a low objkt number(older) NFT from the HicDex API"""
  query = """query MyQuery {
  hic_et_nunc_token(limit: 10, order_by: {timestamp: asc_nulls_first, title: asc}) {
    display_uri
    id
  }
}
"""
  # post query to hicdex
  url = 'https://api.hicdex.com/v1/graphql'
  r = requests.post(url, json={'query': query})
  json_data = json.loads(r.text)
  # Convert to DataFrame
  df = pd.DataFrame(json_data)
  #Access token number and store in variable
  df_objkt_id = df["data"]["hic_et_nunc_token"][number]["id"]
  # Format into a string to be returned by function
  link_string = f"https://hic.art/{df_objkt_id}"
  return link_string


def update_objkt_list(objkt_number):
  """Updates the replit DataBase and stores all NFTs called by the artbot"""
  if "objkt" in db.keys():
    objkt = db["objkt"]
    objkt.append(objkt_number)
    db["objkt"] = objkt
    
  else:
    db["objkt"] = [objkt_number]


@client.event
async def on_ready():
  """Send message when bot logs on"""
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  """Defines action in Discord when bot recieves commands"""
  if message.author == client.user:
    return
  
  # return quote
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  # return random nft and store in db
  if message.content.startswith('$art'):
    num = random.randrange(0,10)
    rand_art = get_rand_art(num)
    update_objkt_list(rand_art) 
    await message.channel.send(rand_art)

  if message.content.startswith('$fresh'):
    num = random.randrange(0,10)
    fresh_art = get_fresh_art(num)
    update_objkt_list(fresh_art) 
    await message.channel.send(fresh_art)
 
  if message.content.startswith('$old'):
    num = random.randrange(0,10)
    old_art = get_old_art(num)
    update_objkt_list(old_art) 
    await message.channel.send(old_art)

keep_alive()
client.run(my_secret)
