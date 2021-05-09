import json
import requests

DIGITALOCEAN_BASEURL = "https://api.digitalocean.com"

class Droplet:
  def __init__(self, name, token):
    self.name = name
    self.token = token

  def getDroplets(self):
    headers = {'Authorization': "Bearer " + self.token}
    resp = requests.get(headers=headers, url=DIGITALOCEAN_BASEURL + "/v2/droplets")  
    decode = json.loads(resp.text)

    return decode['droplets']

  def getDetailDroplet(self, id):
    headers = {'Authorization': "Bearer " + self.token}
    resp = requests.get(headers=headers,url=DIGITALOCEAN_BASEURL + "/v2/droplets/" + id)  
    decode = json.loads(resp.text)
    return decode['droplet']

  def toggleDropletStatus(self, id, toggleType):
    headers = {'Authorization': "Bearer " + self.token}
    payload = {'type': toggleType}

    resp = requests.post(headers=headers, url=DIGITALOCEAN_BASEURL + "/v2/droplets/" + id + "/actions", json=payload)
    decode = json.loads(resp.text)
    data = decode['action']
    result = {
      'type': data['type'],
      'status': data['status'],
      'startedAt': data['started_at']
    }
    return result
