# # data_manager.py
# import pandas as pd
# import os
# from config import CSV_FILENAME

# def save_to_history(new_data_list):
#     """将新抓取的数据追加到 CSV 文件"""
#     if not new_data_list:
#         return
    
#     df_new = pd.DataFrame(new_data_list)
    
#     # 确保只保留成功抓取到价格的数据
#     df_new = df_new.dropna(subset=['price'])

#     if not os.path.exists(CSV_FILENAME):
#         df_new.to_csv(CSV_FILENAME, index=False)
#     else:
#         # 追加模式，不写入表头
#         df_new.to_csv(CSV_FILENAME, mode='a', header=False, index=False)
#     print(f"数据已保存到 {CSV_FILENAME}")

# def load_history():
#     """读取历史数据"""
#     if not os.path.exists(CSV_FILENAME):
#         return pd.DataFrame()
#     return pd.read_csv(CSV_FILENAME)

# def get_latest_stats(df_history):
#     """获取最新一天的统计数据"""
#     if df_history.empty:
#         return None, []

#     # 获取最近的日期
#     latest_date = df_history['date'].max()
#     df_latest = df_history[df_history['date'] == latest_date].copy()

#     if df_latest.empty:
#         return None, []

#     # 转换价格为数字类型以进行计算
#     df_latest['price'] = pd.to_numeric(df_latest['price'])

#     stats = {
#         "min_price": df_latest['price'].min(),
#         "max_price": df_latest['price'].max(),
#         "avg_price": round(df_latest['price'].mean(), 2),
#         "latest_date": latest_date,
#         "best_platform": df_latest.loc[df_latest['price'].idxmin()]['platform']
#     }
    
#     # 将 dataframe 转为字典列表供前端渲染
#     latest_prices_list = df_latest.to_dict('records')
    
#     return stats, latest_prices_list

import csv
import os
import pandas as pd
from datetime import datetime

# 文件名
HISTORY_FILE = 'price_history.csv'

def initialize_history_file():
    """
    初始化 CSV 文件，如果文件不存在则写入标题行。
    """
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 写入表头
            writer.writerow(['platform', 'title', 'price', 'currency', 'url', 'timestamp', 'date'])
        print(f"✅ 创建历史文件: {HISTORY_FILE}")

def save_data_to_history(data):
    """
    将抓取到的数据（包含有效价格）保存到 CSV 文件中。
    """
    if data['price'] is None:
        return

    try:
        with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 写入数据行
            writer.writerow([
                data['platform'], 
                data['title'], 
                data['price'], 
                data['currency'], 
                data['url'], 
                data['timestamp'],
                data['date']
            ])
    except Exception as e:
        print(f"❌ 保存数据到 CSV 时发生错误: {e}")

def load_history():
    """读取历史数据"""
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame()
        
    # 强制读取所有列为字符串
    df = pd.read_csv(HISTORY_FILE, dtype={'price': str, 'currency': str})
    
    # 🚨 CRITICAL FIX: 立即将 price 列转换为数字类型
    # errors='coerce' 会将无法转换的值设为 NaN
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # 移除无法转换为数字的行，确保后续计算的稳定性
    return df.dropna(subset=['price'])

def get_latest_stats(df_history):
    """获取最新一天的统计数据"""
    if df_history.empty:
        return None, []

    # 确保日期列存在并获取最近的日期
    if 'date' not in df_history.columns:
         # 如果 CSV 中没有 'date' 列，从 'timestamp' 中提取
         df_history['date'] = pd.to_datetime(df_history['timestamp']).dt.strftime("%Y-%m-%d")
         
    latest_date = df_history['date'].max()
    df_latest = df_history[df_history['date'] == latest_date].copy()

    if df_latest.empty:
        return None, []

    # 注意：由于 load_history 已经处理了类型转换，这里只需确保价格列不为空
    df_latest = df_latest.dropna(subset=['price']) # 移除无效价格

    if df_latest.empty:
         return None, []

    # 计算统计数据
    stats = {
        "min_price": round(df_latest['price'].min(), 2),
        "max_price": round(df_latest['price'].max(), 2),
        "avg_price": round(df_latest['price'].mean(), 2),
        "latest_date": latest_date,
        "best_platform": df_latest.loc[df_latest['price'].idxmin()]['platform']
    }
    
    # 将 dataframe 转为字典列表供前端渲染
    latest_prices_list = df_latest.to_dict('records')
    
    return stats, latest_prices_list