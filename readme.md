# 无人机通信心跳监测可视化

## 功能
1. 模拟无人机每秒发送心跳包（含序号和时间）
2. 地面站检测：3秒未收到心跳包则报警
3. Streamlit 网页可视化展示数据

## 运行
```bash
pip install -r requirements.txt
streamlit run app.py
