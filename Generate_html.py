import requests
import datetime
import os
from dotenv import load_dotenv

# === 1. API 키 불러오기 ===
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# === 2. 뉴스 수집 ===
def get_llm_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "large language model OR LLM OR ChatGPT OR Gemini",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    res = requests.get(url, params=params)
    data = res.json()
    articles = data.get("articles", [])
    return [(a["title"], a["description"], a["url"]) for a in articles]

# === 3. HTML 저장 ===
def save_as_html(news_list):
    today = datetime.date.today().strftime("%Y-%m-%d")
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>LLM 뉴스 요약 - {today}</title>
    </head>
    <body>
      <h1>📰 LLM 뉴스 요약 ({today})</h1>
      <ul>
    """
    for title, desc, url in news_list:
        html += f"<li><b>{title}</b><br>{desc}<br><a href='{url}'>[원문]</a><br><br></li>\n"
    html += "</ul></body></html>"

    # 절대경로 저장
    save_path = r"E:\E_2025\LLM\Newspaper\news.html"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ news.html 생성 완료!")
    print("📁 저장 위치:", save_path)

# === 4. 실행 ===
if __name__ == "__main__":
    news = get_llm_news()
    save_as_html(news)