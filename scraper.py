# import re
# import time
# from playwright.sync_api import sync_playwright
# from datetime import datetime

# def clean_price(price_str, currency_symbol):
#     """清理价格字符串，移除货币符号和逗号，转换为浮点数"""
#     if not price_str:
#         return None
#     # 移除货币符号、逗号和两端空格
#     clean_str = price_str.replace(currency_symbol, '').replace(',', '').strip()
#     # 提取数字部分（处理类似 "RM1,299.00 - RM1,599.00" 的区间价格，只取第一个）
#     match = re.search(r"(\d+\.?\d*)", clean_str)
#     if match:
#         try:
#             return float(match.group(1))
#         except ValueError:
#             return None
#     return None

# def fetch_product_data(product_config):
#     """使用 Playwright 获取单个商品的页面数据，并针对性处理不同平台的反爬"""
#     print(f"正在尝试抓取: {product_config['platform']} - {product_config['url']}...")
#     data = {
#         "platform": product_config['platform'],
#         "title": "抓取失败",
#         "price": None,
#         "currency": product_config['currency_symbol'],
#         "url": product_config['url'],
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "date": datetime.now().strftime("%Y-%m-%d") 
#     }
    
#     # 将 browser 和 context 变量的声明/初始化全部移入 with 块内
#     browser = None
    
#     try:
#         with sync_playwright() as p:
#             try:
#                 # 启动浏览器，并使用伪装的User-Agent
#                 browser = p.chromium.launch(headless=False, slow_mo=500) 
#                 context = browser.new_context(
#                     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
#                     viewport={"width": 1920, "height": 1080}
#                 )
#                 page = context.new_page()
                
#                 # --- 核心改进: 区分平台等待策略 ---
                
#                 if product_config['platform'] == "Amazon":
#                     # Amazon: 使用稳定策略
#                     page.goto(product_config['url'], timeout=60000, wait_until="domcontentloaded")
#                 else:
#                     # Shopee/Lazada: 等待所有网络空闲，并给予足够时间
#                     page.goto(product_config['url'], timeout=120000, wait_until="networkidle") 
                    
#                     # --- 模拟用户滚动和悬停 ---
#                     print(f"尝试 {product_config['platform']}：模拟滚动和悬停...")
                    
#                     # 1. 模拟向下滚动
#                     page.mouse.wheel(0, 500) 
#                     time.sleep(2)
                    
#                     # 2. 模拟回到顶部
#                     page.mouse.wheel(0, -500)
#                     time.sleep(2)
                    
#                     # 3. 模拟悬停
#                     page.hover("body") 
#                     time.sleep(2)

#                 # --- 统一提取逻辑 ---
                
#                 # 提取标题
#                 title_el = page.query_selector(product_config['selectors']['title'])
#                 if title_el:
#                     data["title"] = title_el.inner_text().strip()
                
#                 # 提取价格
#                 price_selector = product_config['selectors']['price']
                
#                 # 关键：将价格等待时间增加到 40 秒
#                 try:
#                     page.wait_for_selector(price_selector, state="visible", timeout=40000)
#                 except Exception as e:
#                     # 如果 40 秒后仍未出现，打印警告并继续尝试抓取
#                     print(f"警告: {product_config['platform']} 价格元素等待超时 (40s)。尝试继续抓取。")
                
#                 price_el = page.query_selector(price_selector)
                
#                 if price_el:
#                     # 尝试获取渲染后的文本
#                     raw_price = price_el.inner_text()
                    
#                     # 再次尝试获取 text_content() 以防 inner_text() 失败
#                     if not raw_price:
#                         raw_price = price_el.text_content()

#                     data["price"] = clean_price(raw_price, product_config['currency_symbol'])

#                 if data["price"] is None:
#                     print(f"错误: 未能在 {product_config['platform']} 提取到有效价格。")
#                 else:
#                     print(f"成功: {product_config['platform']} 价格为 {data['currency']}{data['price']}")

#             except Exception as e:
#                 print(f"抓取 {product_config['platform']} 时发生严重错误: {e}")
#                 # 针对超时提供更精确的提示
#                 if "timeout" in str(e).lower():
#                     print("提示: 可能是网络太慢或反爬触发了验证码/重定向。")
            
#             finally:
#                 # 确保浏览器在内层 try-except 结束时被关闭
#                 if browser:
#                     try:
#                         browser.close()
#                     except Exception as close_e:
#                         # 这个警告通常是 Playwright 内部清理残留，可以忽略
#                         pass # 避免打印警告，因为我们知道 event loop 可能会关闭
                        
#     except Exception as e:
#         # 捕捉 sync_playwright() 本身的错误
#         print(f"Playwright 环境启动错误: {e}")
            
#     return data

import re
import time
import os
from playwright.sync_api import sync_playwright
from datetime import datetime

# 确保存在用于保存调试文件的目录
DEBUG_DIR = "debug_output"
os.makedirs(DEBUG_DIR, exist_ok=True)

def clean_price(price_str, currency_symbol):
    """清理价格字符串，移除货币符号和逗号，转换为浮点数"""
    if not price_str:
        return None
    # 移除货币符号、逗号和两端空格
    if price_str.upper().startswith("RM"):
        currency_symbol = "RM"
    clean_str = price_str.replace(currency_symbol, '').replace(',', '').strip()
    # 提取数字部分（处理类似 "RM1,299.00 - RM1,599.00" 的区间价格，只取第一个）
    match = re.search(r"(\d+\.?\d*)", clean_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def fetch_product_data(product_config):
    """使用 Playwright 获取单个商品的页面数据，并针对性处理不同平台的反爬"""
    platform = product_config['platform']
    url = product_config['url']
    currency_symbol = product_config['currency_symbol']
    
    print(f"正在尝试抓取: {platform} - {url}...")
    data = {
        "platform": platform,
        "title": "抓取失败",
        "price": None,
        "currency": currency_symbol,
        "url": url,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d") 
    }
    
    browser = None
    
    # 始终在无头模式下运行，以提高效率
    is_amazon = platform.startswith("Amazon")
    is_ebay = platform.startswith("eBay")
    
    try:
        with sync_playwright() as p:
            try:
                # 启动浏览器，并使用伪装的User-Agent
                browser = p.chromium.launch(headless=True) 
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080}
                )
                page = context.new_page()
                
                # --- 核心改进: 区分平台等待策略 ---
                if is_amazon:
                    # Amazon 速度快，等待 DOM 加载
                    page.goto(url, timeout=60000, wait_until="domcontentloaded")
                else:
                    # 其他平台（如 eBay）需要等待网络空闲
                    page.goto(url, timeout=120000, wait_until="networkidle") 
                    
                    # 模拟用户滚动和悬停
                    print(f"尝试 {platform}：模拟滚动和悬停...")
                    page.mouse.wheel(0, 500) 
                    time.sleep(1)
                    page.mouse.wheel(0, -500)
                    time.sleep(1)
                    page.hover("body") 
                    time.sleep(1)
                    
                    # 针对 eBay 的额外滚动
                    if is_ebay:
                        page.mouse.wheel(0, 200)
                        time.sleep(1)


                # --- 统一提取逻辑 ---
                
                price_selector = product_config['selectors']['price']
                title_selector = product_config['selectors']['title']

                # 提取标题
                title_el = page.query_selector(title_selector)
                if title_el:
                    data["title"] = title_el.inner_text().strip()
                else:
                    print(f"警告: 未能在 {platform} 提取到标题: {title_selector}")

                # 关键改进：显式等待价格元素的文本内容加载完成（非空且长度大于5）
                price_el = None
                try:
                    print(f"正在等待 {platform} 价格元素内容加载: {price_selector}...")
                    
                    # 1. 确保元素可见
                    page.wait_for_selector(price_selector, state="visible", timeout=10000)

                    # 2. 接着使用 wait_for_function 等待元素的内容长度大于5
                    # 价格元素可能先出现，但内容是空白的，等 AJAX 填充
                    page.wait_for_function(
                        f"document.querySelector('{price_selector}') && document.querySelector('{price_selector}').textContent.trim().length > 5", 
                        timeout=30000 # 额外给 30 秒等待内容填充
                    )
                    
                    price_el = page.query_selector(price_selector)
                    
                except Exception as e:
                    print(f"警告: {platform} 价格元素内容等待超时 (30s)。尝试继续抓取。")
                
                
                if price_el:
                    raw_price = price_el.inner_text()
                    if not raw_price:
                        raw_price = price_el.text_content()

                    data["price"] = clean_price(raw_price, currency_symbol)

                if data["price"] is None:
                    print(f"错误: 未能在 {platform} 提取到有效价格。")
                    
                    # --- 失败快照（仅针对非 Amazon 平台）---
                    if is_ebay:
                        filename_base = f"{platform.split(' ')[0]}_failure_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        screenshot_path = os.path.join(DEBUG_DIR, f"{filename_base}.png")
                        html_path = os.path.join(DEBUG_DIR, f"{filename_base}.html")
                        
                        # 保存全页面截图
                        page.screenshot(path=screenshot_path, full_page=True)
                        print(f"✅ {platform} 失败截图已保存到: {screenshot_path}")
                        
                        # 保存页面 HTML
                        with open(html_path, 'w', encoding='utf-8') as f:
                            f.write(page.content())
                        print(f"✅ {platform} 失败 HTML 已保存到: {html_path}")
                        
                        print("提示：请查看 debug_output 文件夹中的快照以确认页面内容是否加载。")
                        
                else:
                    print(f"成功: {platform} 价格为 {data['currency']}{data['price']}")

            except Exception as e:
                print(f"抓取 {platform} 时发生严重错误: {e}")
                if "timeout" in str(e).lower():
                    print("提示: 可能是网络太慢或反爬触发了验证码/重定向。")
            
            finally:
                if browser:
                    try:
                        browser.close()
                    except Exception:
                        pass 
                        
    except Exception as e:
        print(f"Playwright 环境启动错误: {e}")
            
    return data