from ground import GroundClient

client = GroundClient()
print client.createEdge("edge1", "node1", "node2")