from ground import GroundClient

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
client.createNode("table_tweets")
client.createNodeVersion("table_tweets", tags=original_schema)
client.createNodeVersion("table_tweets", tags=alternative_schema)