# # main.py
# import time
# import schedule 
# from config import PRODUCTS_TO_TRACK
# from scraper import fetch_product_data
# from data_manager import save_to_history, load_history, get_latest_stats
# from html_generator import render_html, generate_trend_chart, generate_ai_summary

# def run_task():
#     print("\n--- 开始执行比价任务 ---")
    
#     # 1. 抓取数据
#     current_data = []
#     for prod_config in PRODUCTS_TO_TRACK:
#         data = fetch_product_data(prod_config)
#         current_data.append(data)
#         # 礼貌性延迟，避免请求过快
#         time.sleep(2)
        
#     # 2. 保存数据
#     save_to_history(current_data)
    
#     # 3. 读取并分析数据
#     df_history = load_history()
#     stats, latest_prices = get_latest_stats(df_history)
    
#     chart_html = "<p>数据不足</p>"
#     ai_summary_text = "无数据"

#     if stats:
#         # 4. (加分项) 生成图表和 AI 总结
#         print("正在生成趋势图...")
#         chart_html = generate_trend_chart(df_history)
#         print("正在请求 AI 总结...")
#         ai_summary_text = generate_ai_summary(stats)
    
#     # 5. 生成 HTML 报告
#     render_html(stats, latest_prices, chart_html, ai_summary_text)
#     print("--- 任务完成 ---\n")

# # --- 运行方式 ---

# # 方式 1: 直接运行一次 (调试用)
# if __name__ == "__main__":
#     run_task()

# # 方式 2: (加分项) 每日定时运行
# # 取消下面代码的注释以启用定时任务
# # print("系统已启动，将每天早上 10:00 运行任务。请保持终端开启。")
# # schedule.every().day.at("10:00").do(run_task)
# #
# # while True:
# #     schedule.run_pending()
# #     time.sleep(60)

import time
from config import PRODUCTS_TO_TRACK
from scraper import fetch_product_data
# --- 导入修复：添加缺失的数据分析和 HTML 报告函数 ---
from data_manager import save_data_to_history, initialize_history_file, load_history, get_latest_stats
from html_generator import render_html, generate_trend_chart, generate_ai_summary 

def print_summary(results):
    """打印抓取结果的总结报告"""
    print("\n" + "="*50)
    print("         商品价格追踪报告         ")
    print("="*50)
    
    success_count = 0
    
    for data in results:
        platform = data.get('platform', '未知平台')
        title = data.get('title', '未知标题')
        # 限制标题长度以保持输出整洁
        display_title = title[:50] + '...' if len(title) > 50 else title
        
        price = data.get('price')
        currency = data.get('currency', '')
        
        print(f"\n[{platform}]")
        print(f"  商品: {display_title}") # 使用限制长度后的标题
        
        if price is not None:
            print(f"  价格: {currency}{price:.2f}")
            print("  状态: ✅ 成功抓取并已保存历史记录")
            success_count += 1
        else:
            print(f"  状态: ❌ 抓取失败 (反爬或内容未加载)")

    print("\n" + "="*50)
    print(f"总计尝试: {len(results)} | 成功: {success_count} | 失败: {len(results) - success_count}")
    print("价格历史记录已保存在 price_history.csv 文件中。")
    print("="*50)

def main():
    """主函数：运行爬虫、保存数据、分析数据并生成HTML报告"""
    print(">> 启动价格追踪程序...")
    initialize_history_file() # 确保历史文件存在
    
    all_results = []
    
    # 步骤 1: 抓取数据并保存
    for product_config in PRODUCTS_TO_TRACK:
        # 暂停一段时间，以降低被反爬的风险
        time.sleep(2) 
        
        # 调用爬虫函数。返回一个包含单个结果的列表
        results_list = fetch_product_data(product_config)
        
        # 确保 results_list 是一个列表
        if not isinstance(results_list, list):
            results_list = [results_list]

        # 遍历所有抓取到的产品结果
        for result in results_list:
            all_results.append(result)
            
            # 立即保存有效数据
            save_data_to_history(result)
            
    print_summary(all_results)
    
    # --- 步骤 2: 读取历史数据并生成报告 (新增逻辑) ---
    print("\n>> 开始生成 HTML 报告...")
    df_history = load_history()
    stats, latest_prices = get_latest_stats(df_history) # 获取统计数据和最新价格列表
    
    chart_html = "<p>暂无足够的历史数据生成图表。</p>"
    ai_summary_text = "无数据"

    if stats:
        # 生成图表和 AI 总结 (如果需要)
        print("正在生成趋势图和 AI 总结...")
        # 警告：此函数需要 html_generator.py 文件存在，且包含这些函数。
        chart_html = generate_trend_chart(df_history)
        ai_summary_text = generate_ai_summary(stats)
    
    # 渲染最终 HTML 文件
    # 警告：此函数需要 html_generator.py 文件存在。
    render_html(stats, latest_prices, chart_html, ai_summary_text)
    print(">> HTML 报告生成完毕: price_report.html")


if __name__ == "__main__":
    main()