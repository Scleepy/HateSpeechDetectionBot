import json

with open ("./Database/database.json", "r") as file:
    database = json.load(file)

def update_database(serverID, userID): 

    flag = 0

    if serverID in database.keys():
        if userID in database[serverID].keys():

            warnings = database[serverID][userID]['warnings']
            total_kicked = database[serverID][userID]['totalkicked']

            if(total_kicked == 3): #user banned, set to initial value
                flag = 1 #flag to ban
                warnings = 0
                total_kicked = 2

            elif(warnings == 3): #user kicked, set warnings to 0 and increment kicked counter
                flag = 2 #flag to kick
                warnings = 0
                total_kicked = total_kicked + 1

            else: #user warned, increment kicked counter
                warnings = warnings + 1
    
        else: #create new user, set warnings to 1
            warnings = 1
            total_kicked = 0
        
        database[serverID][userID] = {
            'warnings': warnings, 
            'totalkicked': total_kicked
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
