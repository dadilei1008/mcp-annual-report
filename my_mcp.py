from fastmcp import FastMCP
import requests

# 模拟浏览器请求头，解决 403 Forbidden
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://www.cninfo.com.cn/"
}

mcp = FastMCP("cninfo-annual-report-mcp")

@mcp.tool()
def search_annual_report(stock_code: str, year: int, exchange: str = "sse"):
    """
    查A股年度报告。exchange: sse=上交所, szse=深交所
    """
    # 注：此处为巨潮常规查询接口示例，若你原代码有特定接口可保留原url
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    params = {
        "pageNum": 1,
        "pageSize": 10,
        "column": exchange,
        "tabName": "fulltext",
        "stockCode": stock_code,
        "searchkey": f"{year}年年度报告",
        "category": "category_ndbg_szsh",
        "sortName": "time",
        "sortType": "desc"
    }
    try:
        # 👇 关键：加上 headers=HEADERS
        res = requests.post(url, data=params, headers=HEADERS, timeout=10)
        res.raise_for_status()
        data = res.json()
        if data.get("announcements"):
            ann = data["announcements"][0]
            pdf_url = f"https://static.cninfo.com.cn/{ann['adjunctUrl']}"
            return f"查询成功！{stock_code} {year}年报PDF: {pdf_url}"
        return f"未找到 {stock_code} {year} 年报"
    except Exception as e:
        return f"查询失败: {e}"

@mcp.tool()
def search_notices(stock_code: str, keyword: str = "年度报告"):
    """按关键词查巨潮历史公告"""
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    params = {
        "pageNum": 1,
        "pageSize": 10,
        "column": "sse",
        "tabName": "fulltext",
        "stockCode": stock_code,
        "searchkey": keyword,
        "sortName": "time",
        "sortType": "desc"
    }
    try:
        # 👇 关键：加上 headers=HEADERS
        res = requests.post(url, data=params, headers=HEADERS, timeout=10)
        res.raise_for_status()
        data = res.json()
        return data.get("announcements", [])[:5]
    except Exception as e:
        return f"查询失败: {e}"

if __name__ == "__main__":
    mcp.run(transport="http")
