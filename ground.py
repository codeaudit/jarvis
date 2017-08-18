import requests, json, numpy as np

class GroundClient:
	
	headers = {"Content-type": "application/json"}
	
	def __init__(self, host='localhost', port=9000):
		self.host = host
		self.port = str(port)
		self.url = "http://" + self.host + ":" + self.port

	def createEdge(self, sourceKey, fromNodeId, toNodeId, name="null"):
		d = {
			"sourceKey": sourceKey,
			"fromNodeId": fromNodeId,
			"toNodeId": toNodeId,
			"name": name
		}
		return requests.post(self.url + "/edges", headers=self.headers, 
			data=json.dumps(d)).json()

	def createNode(self, sourceKey, name="null"):
		d = {
			"sourceKey": sourceKey,
			"name": name
		}
		return requests.post(self.url + "/nodes", headers=self.headers,
			data=json.dumps(d)).json()

