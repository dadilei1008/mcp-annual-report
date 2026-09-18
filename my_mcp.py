from fastmcp import FastMCP
import requests

mcp = FastMCP("cninfo-annual-report-mcp")

CNINFO_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cninfo.com.cn/new/disclosure/overview",
}

@mcp.tool()
def search_annual_report(stock_code: str, year: int, exchange: str = "sse") -> str:
    """查A股年度报告。exchange: sse=上交所, szse=深交所, bse=北交所"""
    data = {
        "pageNum": 1,
        "pageSize": 5,
        "tabName": "fulltext",
        "column": exchange,
        "stock": stock_code,
        "category": "category_ndbg_szsh",
        "seDate": f"{year}-01-01~{year}-12-31",
        "sortName": "time",
        "sortType": "desc",
    }
    try:
        r = requests.post(CNINFO_URL, headers=HEADERS, data=data, timeout=10)
        r.raise_for_status()
        items = r.json().get("announcements") or []
        if not items:
            return f"未找到 {stock_code} {year} 年年度报告"
        return "\n\n".join(
            f"{a.get('announcementTime')} | {a.get('announcementTitle')}\nhttps://static.cninfo.com.cn/{a.get('adjunctUrl','')}"
            for a in items
        )
    except Exception as e:
        return f"查询失败：{e}"

@mcp.tool()
def search_notices(stock_code: str, keyword: str = "年度报告", limit: int = 5) -> str:
    """按关键词查巨潮历史公告：季报/半年报/处罚/重组等"""
    data = {
        "pageNum": 1,
        "pageSize": limit,
        "tabName": "fulltext",
        "stock": stock_code,
        "searchkey": keyword,
        "sortName": "time",
        "sortType": "desc",
    }
    try:
        r = requests.post(CNINFO_URL, headers=HEADERS, data=data, timeout=10)
        r.raise_for_status()
        items = r.json().get("announcements") or []
        if not items:
            return f"未找到 {stock_code} 含「{keyword}」的公告"
        return "\n\n".join(
            f"{a.get('announcementTime')} | {a.get('announcementTitle')}\nhttps://static.cninfo.com.cn/{a.get('adjunctUrl','')}"
            for a in items
        )
    except Exception as e:
        return f"查询失败：{e}"
