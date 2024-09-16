#prueba que no se si esta bien
import pymongo # type: ignore
import os
#aqui importamos la url de mi usuario de mongoDB desde el fichero .env
from env import load_env()

load_env()

 # Conexion de MongoDB
MONGO_URI = os.getenv('MONGO_URI')
print(MONGO_URI)
DB_NAME = 'completecodes'
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection_rewards = db['rewards']

print('hola')
#function to conect mongodb and get the funds list by users and contract
def lambda_handler():
    
    print('hola2')

    #query para encontrar solo los que estan block
    query = [{
        "$match": {
            "status": "locked"
        }
    }, 
    {
        "$group": {
            "_id":{
                "username": "$username",
                "contract": "$contract"
            },
        "totalReward_Assigned":{
            "$sum":"$total_reward_assigned_to_user"
            }
        }
    }    
    ]

    #ahora accedemos a la base de datos 
    res = list(collection_rewards.aggregate(query).limit(20))

    # Verificar conexión y obtener algunos documentos
    print("Verificando conexión y obteniendo documentos...")
    try:
        res = list(collection_rewards.find(query))  # Obtén los primeros 5 documentos
        
        if not res:
            print("La colección está vacía o no tiene documentos.")
        else:
            print("Documentos encontrados en la colección:")
        for doc in res:
            print(doc)
    
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
    
    
    #escribe la lista
    #for result in res:
    #   print (result)

    finally:     
        #cierro conexion
        client.close()
    
lambda_handler()   
