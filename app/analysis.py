import os
import spacy
import ginza
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

# spaCyとGiNZAのモデルをロード
nlp = spacy.load('ja_ginza')

def get_video_id(url: str):
    """
    YouTubeのURLからvideo_idを抽出する
    """
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    
    query = urlparse(url).query
    params = parse_qs(query)
    if 'v' in params:
        return params['v'][0]
    return None

def analyze_video_comments(video_id: str):
    """
    指定されたYouTube動画のコメントを取得し、感情分析を行う
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        raise ValueError("YouTube APIキーが設定されていません。.envファイルを確認してください。")

    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    try:
        next_page_token = None
        while True:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100, # 取得するコメント数 (最大100)
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
    except Exception as e:
        # コメントが無効になっている場合などのエラーをハンドル
        print(f"An error occurred: {e}")
        return {"error": "コメントの取得に失敗しました。コメントが非公開になっているか、動画が存在しない可能性があります。"}


    # 簡単な単語ベースの感情分析
    sentiments = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
    }
    
    positive_words = ["好き", "良い", "面白い", "最高", "すごい", "楽しい", "かわいい", "かっこいい", "素敵"]
    negative_words = ["嫌い", "悪い", "つまらない", "最低", "ひどい", "悲しい"]

    for comment_text in comments:
        doc = nlp(comment_text)
        score = 0
        for token in doc:
            if token.lemma_ in positive_words:
                score += 1
            elif token.lemma_ in negative_words:
                score -= 1
        
        if score > 0:
            sentiments["positive"] += 1
        elif score < 0:
            sentiments["negative"] += 1
        else:
            sentiments["neutral"] += 1

    return sentiments
