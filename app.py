import streamlit as st
import time
from HEARTBEAT import DroneHeartbeat

st.title("无人机通信心跳监测可视化")

drone = DroneHeartbeat()
placeholder = st.empty()

# 模拟运行10秒
for _ in range(10):
    drone.send_heartbeat()
    time.sleep(1)
    drone.check_connection()

df = drone.get_dataframe()
st.subheader("心跳数据列表")
st.dataframe(df)

st.subheader("心跳序号随时间变化")
st.line_chart(df, x="时间", y="序号", color="状态")
