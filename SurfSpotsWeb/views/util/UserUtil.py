import urllib3, json, requests

http = urllib3.PoolManager()

def getUsers():
    req = http.request('GET',
                       'http://localhost:8000/api/users',)
    users = json.loads(req.data)
    
    return users

def getUser(pk):
    req = http.request('GET',
                       'http://localhost:8000/api/users/' + str(pk))
    user = json.loads(req.data)
    
    return user

def deleteUser(pk):
    req = http.request('DELETE',
                       'http://localhost:8000/api/users/' + str(pk))
    
def updateUser(pk, user):
    requests.put('http://localhost:8000/api/users/' + str(pk) + '/',
                  data=json.dumps(user),
                  headers= {'Content-type': 'application/json', 'Accept': 'application/json'})
    
def createUser(user):
    requests.post('http://localhost:8000/api/users/',
                  data=json.dumps(user),
                  headers= {'Content-type': 'application/json', 'Accept': 'application/json'})
    
