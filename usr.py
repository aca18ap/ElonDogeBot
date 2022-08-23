##returns the list of users and their unique twitter id from the txt file usr.txt
def getUsersFromFile():
    users = open("keys/users.txt")

    usersDictionary = {}
    print("Listening to users: ")
    for u in users:
        u = u.split()
        username = u[0]
        uid = u[1]
        print(username)
        usersDictionary.update({username: uid})
    users.close()

    return usersDictionary

##Returns the binance keys from bkeys.txt as dictionary 
def getBinanceKeys():
    f = open("keys/bkeys.txt", 'r')

    k = f.readlines()
    binanceApiKeys = {}

    for i in k:
        i = i.split()
        binanceApiKeys.update({i[0] : i[1]})

    f.close()

    return binanceApiKeys


##Returns the twitter keys from bkeys.txt as dictionary 
def getTwitterKeys():
    f = open("keys/tkeys.txt", 'r')

    k = f.readlines()
    twitterApiKeys = {}

    for i in k:
        i = i.split()
        twitterApiKeys.update({i[0] : i[1]})

    f.close()

    return twitterApiKeys

def getPushKey():
    f = open("keys/pbullet.txt",'r')
    k = f.readlines()
    k = k[0].split()
    return {k[0] : k[1]}

