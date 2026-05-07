import requests
import pandas as pd
from datetime import datetime
import os

# 1. 设定我们要抓取的数据接口 (这里以免费获取东京实时天气为例)
url = "https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current_weather=true"

print("🔄 正在向气象接口发送请求...")
response = requests.get(url)
data = response.json() # 将抓取到的数据转换为字典格式

# 2. 提取我们需要的数据字段
temp = data['current_weather']['temperature']   # 温度
windspeed = data['current_weather']['windspeed'] # 风速
time = data['current_weather']['time']           # 时间

print(f"✅ 抓取成功！当前时间: {time}, 温度: {temp}℃, 风速: {windspeed}km/h")

# 3. 将数据打包成 Pandas 的 DataFrame (表格格式)
df_new = pd.DataFrame({
    'Date': [time],
    'Temperature_C': [temp],
    'WindSpeed_kmh': [windspeed]
})

# 4. 将数据保存到 CSV 文件中 (如果文件不存在就新建，存在就在末尾追加)
file_name = "weather_data.csv"
if os.path.exists(file_name):
    df_new.to_csv(file_name, mode='a', header=False, index=False)
    print("📝 数据已追加到旧文件中。")
else:
    df_new.to_csv(file_name, mode='w', header=True, index=False)
    print("✨ 创建了新文件并写入数据。")