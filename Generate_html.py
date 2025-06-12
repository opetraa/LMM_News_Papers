import requests
import datetime
import os
import openai

# 🔑 환경변수
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# === 1. 뉴스 수집 ===
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
    res.raise_for_status()
    data = res.json()
    return [(a["title"], a["description"], a["url"]) for a in data.get("articles", [])]

# === 2. GPT 요약 (한글로) ===
def summarize_to_korean(title, description):
    if not description:
        description = title
    prompt = f"""
다음 영어 뉴스 내용을 한국어로 간결하게 요약해줘:

제목: {title}
내용: {description}

👉 요약 (한글):
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ 요약 실패:", e)
        return "요약 실패"

# === 3. HTML 저장 ===
def save_as_html(news_list):
    today = datetime.date.today().strftime("%Y-%m-%d")
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>LLM 뉴스 한글 요약 - {today}</title>
    </head>
    <body>
      <h1>📰 LLM 뉴스 한글 요약 ({today})</h1>
      <ul>
    """
    for title, desc, url in news_list:
        summary = summarize_to_korean(title, desc)
        html += f"<li><b>{title}</b><br>{summary}<br><a href='{url}'>[원문]</a><br><br></li>\n"
    html += "</ul></body></html>"

    # 저장
    with open("news_ko.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ news_ko.html 생성 완료!")

# === 4. 실행 ===
if __name__ == "__main__":
    news = get_llm_news()
    save_as_html(news)
