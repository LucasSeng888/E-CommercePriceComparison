import pandas as pd
import openai
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from config import GEMINI_API_KEY # 假设 API Key 放在 config.py

# 初始化 Jinja2 环境
# 假设模板文件在 'templates/' 文件夹下
env = Environment(loader=FileSystemLoader('templates'))

# 添加 Jinja2 的 truncate 过滤器，用于在 HTML 中截断长标题
def truncate_filter(s, length, killwords=False, end='...'):
    if len(s) <= length:
        return s
    return s[:length] + end

env.filters['truncate'] = truncate_filter

def generate_trend_chart(df_history):
    """(加分项) 生成过去7天的价格趋势图 HTML"""
    # 警告：由于 pandas/plotly 的复杂性，这里只返回一个占位符，
    # 实际项目中需要使用 Plotly 或 Chart.js 生成图表 HTML 字符串。
    
    if df_history.empty or 'date' not in df_history.columns:
        return "<p class='text-center text-slate-500'>暂无足够的历史数据生成图表。</p>"
    
    # 假设这里的代码能够生成 Plotly 或 Chart.js 的 HTML 字符串
    # 实际代码省略，仅返回占位符确保报告能运行
    
    # --- 实际图表代码占位符 ---
    return "<div class='w-full h-96 bg-slate-100 rounded-lg flex items-center justify-center text-slate-400'>[价格趋势图表占位符 - 需引入 Plotly/Chart.js 渲染逻辑]</div>"


def generate_ai_summary(stats):
    """使用 Gemini API 生成一句话总结"""
    
    # 如果 API Key 未配置，跳过 AI 总结
    if not GEMINI_API_KEY or not stats:
        return "AI 总结不可用 (未配置 API Key 或无数据)。"

    # 初始化 OpenAI client (假设使用 OpenAI 库调用 Gemini)
    # 注意: 实际项目中，如果 API URL 不同，您需要使用 requests 或谷歌官方 SDK
    # 为了简化和兼容性，我们使用一个通用的 API 结构来演示意图。
    client = openai.OpenAI(api_key=GEMINI_API_KEY)
    
    # 准备用于总结的提示词
    # 假设 stats 包含 min_price, max_price, avg_price, best_platform, currency
    prompt = f"""
    你是专业的购物助手。根据最新价格统计，撰写一句简洁的购买建议。
    当前最低价: {stats.get('min_price', 'N/A')}
    最高价: {stats.get('max_price', 'N/A')}
    平均价: {stats.get('avg_price', 'N/A')}
    最低价平台: {stats.get('best_platform', '未知')}
    请用中文，格式类似于：“目前最低价为 [最低价]，建议从 [最低价平台] 购买。”
    """
    
    try:
        response = client.chat.completions.create(
            # 假设使用一个基础模型
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "你是一位专业的电商购物助手，只输出一句简洁的中文结论。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=60
        )
        # 返回 AI 生成的文本
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"AI 总结生成失败 (请检查 API Key 和网络连接): {e}")
        return "AI 总结生成失败，请检查 API 配置。"


def render_html(stats, latest_prices, chart_html, ai_summary):
    """渲染最终 HTML 文件"""
    template = env.get_template('report_template.html')
    
    html_content = template.render(
        stats=stats,
        prices=latest_prices,
        chart_html=chart_html,
        ai_summary=ai_summary,
        generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # 写入 HTML 文件，覆盖旧文件
    try:
        with open("price_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ 报告已生成/更新: price_report.html")
    except Exception as e:
         print(f"❌ 写入 HTML 文件失败: {e}")