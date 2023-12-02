from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn, sqlite3, jwt,os

load_dotenv()
app = FastAPI()

SECRET = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM")

class User(BaseModel):
    username: str
    password: str

def createJWT(username,secret,algorithm,authz):
    return jwt.encode(
        # payload
        {
           "username": username,
           "admin": authz 
        },
        # secret
        secret,
        # Algorithm
        algorithm
)


@app.get("/")
def home():
    return "hello, world"

@app.post("/signup")
def signup(user:User):
    username,password = user.username,user.password

    conn = sqlite3.connect("auth.db")
    cursur = conn.cursor()

    cursur.execute('''
        INSERT INTO users (username,password) VALUES (?,?)
''',(username,password,))
    
    conn.commit()
    conn.close()
    return "new user added"


# login 
@app.post("/login")
def login(data:User):
    username,password = data.username, data.password
    
    # connect with db
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT password FROM users WHERE username = ?
    ''',(username,))

    res = cursor.fetchone()

    if res:
        if password != res[0]:
            return "invalid credentials", 401
        return createJWT(username=username,secret=SECRET,algorithm=ALGORITHM,authz=True)
    else:
        return "invalid credentials", 401
    

# validate
@app.post("/validate")
def validate(token):
    try:
        decoded = jwt.decode(token,SECRET,algorithms=[ALGORITHM])
    except:
        return "not authorized", 403
    return decoded,200

if __name__ == "__main__":
    uvicorn.run("server:app",host="0.0.0.0",port=8000)