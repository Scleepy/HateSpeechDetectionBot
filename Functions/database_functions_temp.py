import json

with open ("./Database/database.json", "r") as file:
    database = json.load(file)

def update_database(serverID, userID): 

    flag = 0

    if serverID in database.keys():
        if userID in database[serverID].keys():

            warnings = database[serverID][userID]['warnings']
            total_kicked = database[serverID][userID]['totalkicked']

            if(total_kicked == 3):
                flag = 1 #flag to ban
                database[serverID][userID] = {
                    'warnings': 0,
                    'totalkicked': 0
                }

            elif(warnings == 3):
                flag = 2 #flag to kick
                database[serverID][userID] = {
                    'warnings': 0,
                    'totalkicked': total_kicked + 1
                }

            else:

                database[serverID][userID] = {
                    'warnings': warnings + 1,
                    'totalkicked': total_kicked
                }

        else:
            database[serverID][userID] = {
                'warnings': 1, 
                'totalkicked': 0
        }
        
    else:
        database[serverID] = {
            userID: {
                'warnings': 1,
                'totalkicked': 0
            }
        }

    with open ("./Database/database.json", "w") as file:
        json.dump(database, file, indent = 4)

    return flag

def get_total_warnings(serverID, userID):
    return database[serverID][userID]['warnings']

def get_total_kicked(serverID, userID):
    return database[serverID][userID]['totalkicked']