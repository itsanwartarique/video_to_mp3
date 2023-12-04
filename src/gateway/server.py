from fastapi import FastAPI, File,UploadFile,Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from auth import access,validate
import uvicorn, json, sqlite3,producer,io
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
)

class User(BaseModel):
    username : str
    password : str

@app.get("/")
def home():
    return "Gateway"

# login
@app.post("/login")
def login(user:User):
    token,err = access.login(user)

    if not err:
        return token
    else:
        return err

# upload
@app.post("/upload")
def upload(token : str = Header(...),file: UploadFile = File(...)):
    # Validate token
    access, err = validate.token(token)
    
    if err:
        return err
    
    access = json.loads(access)

    if access[0]["admin"] :
        # save the file to db
        conn = sqlite3.connect("../db/storage.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO videos (filename,video_data) VALUES (?,?)
        ''',(file.filename,file.file.read(),))
        conn.commit()
        vid_id = cursor.lastrowid
        conn.close()
        # publish id to rabbitmq to convert to mp3
        username = access[0]["username"]
        producer.publish(username=username,video_id=vid_id)

    return f"video id : {vid_id} uploaded"



# download
@app.get("/download{id}")
def download(mp3_id: int, token : str = Header(...)):
    # Validate token
    access, err = validate.token(token)
    
    if err:
        return err
    
    access = json.loads(access)

    if access[0]["admin"] :
        conn = sqlite3.connect("../db/audio.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT mp3_data FROM mp3 WHERE id = ?
        ''',(mp3_id,))

        res = cursor.fetchone()

        if res:
            mp3_data = res[0]
            return StreamingResponse(io.BytesIO(mp3_data), media_type="application/octet-stream", headers={"Content-Disposition": f'attachment; filename="audio.mp3"'})
        else:
            return "error"



if __name__ == "__main__":
    uvicorn.run("server:app",host="0.0.0.0",port=8001)
