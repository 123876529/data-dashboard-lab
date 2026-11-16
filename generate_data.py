import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
categories = ["电子产品", "服装", "食品", "家居", "图书"]
records = []
start_date = datetime(2025, 1, 1)

for i in range(500):
    date = start_date + timedelta(days=np.random.randint(0, 365))
    cat = np.random.choice(categories)
    price = round(np.random.uniform(20, 2000), 2)
    qty = np.random.randint(1, 20)
    records.append({
        "order_id": f"ORD{i+1:04d}",
        "date": date.strftime("%Y-%m-%d"),
        "category": cat,
        "price": price,
        "quantity": qty,
        "amount": round(price * qty, 2),
    })

df = pd.DataFrame(records)
df.dropna(inplace=True)
df = df[df["amount"] > 0]
df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")

# 创建文件夹并保存数据
os.makedirs("data", exist_ok=True)
df.to_csv("data/sales_data.csv", index=False, encoding="utf-8-sig")
print(f"数据生成完成：{len(df)} 条记录")