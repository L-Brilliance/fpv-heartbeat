import streamlit as st
import time
import pandas as pd
from datetime import datetime

# 直接在主文件里定义心跳类，避免任何模块导入问题
class DroneHeartbeat:
    def __init__(self):
        self.data = []
        self.sequence = 0
        self.max_records = 100  # 限制数据量，防止页面卡顿

    def send_heartbeat(self):
        self.sequence += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 模拟正常/异常状态
        status = "正常" if self.sequence % 5 != 0 else "异常"
        self.data.append({
            "时间": current_time,
            "心跳序号": self.sequence,
            "连接状态": status
        })
        # 只保留最近100条数据
        if len(self.data) > self.max_records:
            self.data = self.data[-self.max_records:]

    def check_connection(self):
        # 这里可以扩展真实连接检测逻辑
        pass

    def get_dataframe(self):
        return pd.DataFrame(self.data)

# ---------------------- Streamlit 主界面逻辑 ----------------------
# 初始化会话状态（避免重复初始化和DOM错误）
if "drone" not in st.session_state:
    st.session_state.drone = DroneHeartbeat()
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# 页面标题
st.title("🚁 无人机通信心跳监测可视化")
st.subheader("实时监控无人机连接状态与心跳数据")

# 控制按钮区
col1, col2 = st.columns(2)
with col1:
    if not st.session_state.is_running:
        if st.button("▶️ 开始监测", type="primary"):
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏹️ 停止监测", type="secondary"):
            st.session_state.is_running = False
            st.rerun()

with col2:
    if st.button("🗑️ 清空数据", type="secondary"):
        st.session_state.drone = DroneHeartbeat()
        st.rerun()

# 数据展示区（安全更新，避免DOM报错）
placeholder = st.empty()
with placeholder.container():
    st.subheader("📊 实时心跳数据")
    df = st.session_state.drone.get_dataframe()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.subheader("📈 心跳序号变化趋势")
        st.line_chart(df, x="时间", y="心跳序号", color="连接状态", use_container_width=True)
    else:
        st.info("点击「开始监测」按钮，获取无人机实时心跳数据")

# 后台数据更新（非阻塞，避免黑屏）
if st.session_state.is_running:
    st.session_state.drone.send_heartbeat()
    st.session_state.drone.check_connection()
    time.sleep(1)  # 1秒更新一次
    st.rerun()


