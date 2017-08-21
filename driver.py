from ground import GroundClient

original_schema = {
	"id" : "integer id of the tweet",
	"tweet" : "text of the tweet",
	"place" : "city state from which the tweet originated",
	"city" : "city from which the tweet originated",
	"country" : "country from which the tweet originated",
	"code": "two character country code",
	"training" : "boolean whether record is used for training"
}

alternative_schema = {
	"id" : "integer id of the tweet",
	"tweet" : "text of the tweet",
	"code" : "country from which the tweet originated",
	"city" : "city from which the tweet originated",
	"country" : "two character country code",
	"training" : "boolean whether record is used for training"
}

client = GroundClient()
client.createNode("table_tweets")
client.createNodeVersion("table_tweets", tags=original_schema)
client.createNodeVersion("table_tweets", tags=alternative_schema)