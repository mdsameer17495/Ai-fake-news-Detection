import httpx
import re
from app.config import settings

STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'cannot', 'could',
    'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have',
    'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is',
    'it', 'its', 'itself', 'just', 'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once',
    'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so', 'some',
    'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this',
    'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where',
    'which', 'while', 'who', 'whom', 'why', 'with', 'would', 'you', 'your', 'yours', 'yourself', 'yourselves',
    'says', 'said', 'today', 'yesterday', 'tomorrow', 'according', 'reported', 'claims', 'claimed', 'news', 'article'
}

def extract_search_keywords(text: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', text)
    words = [w for w in cleaned.split() if len(w) >= 4 and w.lower() not in STOP_WORDS]
    unique_words = list(dict.fromkeys(words))
    return " ".join(unique_words[:4])

async def verify_news_sources(text: str):
    news_key = settings.NEWS_API_KEY.strip()
    if not news_key or news_key == "your_news_api_key_here":
        return {
            "status": "unconfigured",
            "message": "Live source verification is not configured. Add the News API key to enable this feature.",
            "articles": []
        }

    keywords = extract_search_keywords(text)
    if not keywords or len(keywords.strip()) < 3:
        keywords = "news"

    url = f"https://newsapi.org/v2/everything?q={keywords}&pageSize=6&sortBy=relevance&apiKey={news_key}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=6.0)
            if response.status_code == 200:
                data = response.json()
                raw_articles = data.get("articles", [])
                
                valid_articles = [a for a in raw_articles if a.get("title") and "[Removed]" not in a.get("title")]
                
                matching_articles = []
                for art in valid_articles[:5]:
                    matching_articles.append({
                        "source": art.get("source", {}).get("name") or "News Source",
                        "title": art.get("title", ""),
                        "publishedAt": art.get("publishedAt", "")[:10] if art.get("publishedAt") else "Recent",
                        "snippet": art.get("description") or art.get("content") or "No detailed description available.",
                        "url": art.get("url", "#")
                    })
                
                if matching_articles:
                    return {
                        "status": "matches_found",
                        "message": f"Found {len(matching_articles)} matching reports in trusted news sources",
                        "articles": matching_articles
                    }
                else:
                    return {
                        "status": "no_matches",
                        "message": "No matching reports found across trusted news indices for these keywords.",
                        "articles": []
                    }
            else:
                return {
                    "status": "api_error",
                    "message": f"News API HTTP {response.status_code}",
                    "articles": []
                }
    except Exception as e:
        return {
            "status": "connection_error",
            "message": f"Could not reach News API: {str(e)}",
            "articles": []
        }
