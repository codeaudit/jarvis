import requests, json, numpy as np

class GroundClient:
	
	headers = {"Content-type": "application/json"}
	
	def __init__(self, host='localhost', port=9000):
		self.host = host
		self.port = str(port)
		self.url = "http://" + self.host + ":" + self.port

	### EDGES ###
	def createEdge(self, sourceKey, fromNodeId, toNodeId, name="null"):
		d = {
			"sourceKey": sourceKey,
			"fromNodeId": fromNodeId,
			"toNodeId": toNodeId,
			"name": name
		}
		requests.post(self.url + "/edges", headers=self.headers, 
			data=json.dumps(d))

	def createEdgeVersion(self, edgeId, toNodeVersionStartId):
		d = {
			"edgeId": edgeId,
			"toNodeVersionStartId": toNodeVersionStartId
		}
		requests.post(self.url + "/versions/edges", headers=self.headers,
			data=json.dumps(d))

	def getEdge(self, sourceKey):
		return requests.get(self.url + "/edges/" + str(sourceKey)).json()

	def getEdgeVersion(self, edgeId):
		return requests.get(self.url + "/versions/edges" + str(edgeId)).json()

	### NODES ###
	def createNode(self, sourceKey, name="null"):
		d = {
			"sourceKey": sourceKey,
			"name": name
		}
		requests.post(self.url + "/nodes", headers=self.headers, 
			data=json.dumps(d))

	def createNodeVersion(self, nodeId):
		d = {
			"nodeId": nodeId
		}
		requests.post(self.url + "/versions/nodes", headers=self.headers, 
			data=json.dumps(d))

	def getNode(self, sourceKey):
		return requests.get(self.url + "/nodes/" + str(sourceKey)).json()

	def getNodeVersion(self, nodeId):
		return requests.get(self.url + "/versions/nodes/" + str(nodeId)).json()

	### GRAPHS ###
	def createGraph(self, sourceKey, name="null"):
		d = {
			"sourceKey": sourceKey,
			"name": name
		}
		requests.post(self.url + "/graphs", headers=self.headers, 
			data=json.dumps(d))

	def createGraphVersion(self, graphId, edgeVersionIds):
		d = {
			"graphId": graphId,
			"edgeVersionIds": edgeVersionIds
		}
		requests.post(self.url + "/versions/graphs", headers=self.headers,
			data=json.dumps(d))

	def getGraph(self, sourceKey):
		return requests.get(self.url + "/graphs/" + str(sourceKey)).json()

	def getGraphVersion(self, graphId):
		return requests.get(self.url + "/versions/graphs/" + str(graphId)).json()


