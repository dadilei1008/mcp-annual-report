from fastmcp import FastMCP
import requests

mcp = FastMCP("my-mcp-service")

@mcp.tool()
def search_annual_report(stock_code: str, year: int) -> str:
    """查询A股年报公告（示意）"""
    return f"模拟：已定位 {stock_code} {year} 年年报公告（需接入真实数据源）"

@mcp.tool()
def extract_financial_ratios(stock_code: str, year: int) -> str:
    """抽取核心财务指标"""
    return (
        f"{stock_code} {year} 财务示意："
        "经营现金流、资产负债率、ROE、毛利率。"
    )

@mcp.tool()
def fraud_risk_check(stock_code: str, year: int) -> str:
    """简易财务舞弊风险检查。"""
    report = search_annual_report(stock_code, year)
    if "未找到" in report or "失败" in report:
        return report
    risk_points = [
        "年报是否披露内部控制审计意见",
        "是否发生会计师事务所变更",
        "营收与经营现金流是否背离",
        "关联交易披露完整性",
    ]
    return (
        f"【{stock_code} {year} 舞弊风险初筛】\n"
        f"当前规则待办：\n- " + "\n- ".join(risk_points)
    )

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
