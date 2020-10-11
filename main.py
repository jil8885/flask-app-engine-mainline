# External Module
import uvicorn
from fastapi import FastAPI


# Internal Module
from kakao.url import kakao_url

# Server Object
app = FastAPI()

# NameSpace
app.include_router(kakao_url, prefix="/kakao")

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8080)
