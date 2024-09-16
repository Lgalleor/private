#get total rewards assigned to user
import pymongo 
import os

def lambda_handler(event, context):
    # Load environment variables (AWS Lambda provides these in the environment)
    MONGO_URI = os.getenv('MONGO_URI')
    DB_NAME = 'completecodes'

    # Set up the MongoDB client
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection_rewards = db['rewards']

    # Define the aggregation query
    query = [
        {
            #busca los rewards que tienen el status como locked
            "$match": {
                "status": "locked"
            }
        },
        {
            #agrupa por usuario y por contrato y calcula el total de todos los rewards que tenga ese usuario en cada contrato
            "$group": {
                "_id": {
                    "username": "$username",
                    "contract": "$contract"
                },
                "totalReward_Assigned": {
                    "$sum": "$total_reward_assigned_to_user"
                }
            }
        },
        {
            "$limit": 20  # Limit the result to 20 documents
        }
    ]

    # Execute the aggregation query
    try:
        res = list(collection_rewards.aggregate(query))  # Aggregation query with limit
        
        if not res:
            return {
                'statusCode': 200,
                'body': "La colección está vacía o no tiene documentos."
            }
        else:
            # Return the results as a response
            return {
                'statusCode': 200,
                'body': res
            }
    
    except Exception as e:
        # Handle connection errors
        return {
            'statusCode': 500,
            'body': f"Error conectando a la base de datos: {str(e)}"
        }
    
    finally:
        # Close the MongoDB client connection
        client.close()
