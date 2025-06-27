from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .analysis import analyze_video_comments, get_video_id

# .envファイルから環境変数を読み込む
load_dotenv(dotenv_path='C:/Users/haddy/Desktop/gemini/backend/.env')

app = FastAPI()

# CORS設定
origins = [
    "http://localhost:3000",  # Next.jsのデフォルトポート
    "localhost:3000",
    "https://youtube-comment-fe.vercel.app", # デプロイされたフロントエンドのURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube Sentiment Analysis API"}

@app.get("/analyze")
def analyze_comments_endpoint(video_url: str):
    video_id = get_video_id(video_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="無効なYouTube動画URLです。")
    
    result = analyze_video_comments(video_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
