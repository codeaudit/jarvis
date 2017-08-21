from ground import GroundClient

# engineerTags: {
#       "name": {
#           "key": "name", 
#           "value": "an-engineer", 
#           "type": "string"
#       },
#       "age": {
#           "key": "age", 
#           "value": 25, 
#           "type": "integer"
#       }, 
#       "department": {
#           "key": "department", 
#           "value": "engineering", 
#           "type": "string"
#       }
#   }

original_schema = {
	"id" : {
		"key" : "id",
		"value" : "integer id of the tweet",
		"type" : "string"
	},
	"tweet" : {
		"key" : "tweet",
		"value" : "text of the tweet",
		"type" : "string"
	},
	"place" : {
		"key" : "place",
		"value" : "city state from which the tweet originated",
		"type" : "string"
	},
	"city" : {
		"key" : "city",
		"value" : "city from which the tweet originated",
		"type" : "string"
	},
	"country" : {
		"key" : "country",
		"value" : "country from which the tweet originated",
		"type" : "string"
	},
	"code": {
		"key" : "code",
		"value" : "two character country code",
		"type" : "string"
	},
	"training" : {
		"key" : "training",
		"value" : "boolean whether record is used for training",
		"type" : "string"
	}
}

alternative_schema = {
	"id" : {
		"key" : "id",
		"value" : "integer id of the tweet",
		"type" : "string"
	},
	"tweet" : {
		"key" : "tweet",
		"value" : "text of the tweet",
		"type" : "string"
	},
	"code" : {
		"key" : "code",
		"value" : "country from which the tweet originated",
		"type" : "string"
	},
	"city" : {
		"key" : "city",
		"value" : "city from which the tweet originated",
		"type" : "string"
	},
	"country" : {
		"key" : "country",
		"value" : "two character country code",
		"type" : "string"
	},
	"training" : {
		"key" : "training",
		"value" : "boolean whether record is used for training",
		"type" : "string"
	}
}

client = GroundClient()
# client.createNode("table_tweets")
client.createNodeVersion(1, tags=original_schema)
client.createNodeVersion(1, tags=alternative_schema)