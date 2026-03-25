import streamlit as st
import time
from 心跳 import 无人机心跳

# 初始化会话状态
if "drone" not in st.session_state:
    st.session_state.drone = 无人机心跳()
if "data" not in st.session_state:
    st.session_state.data = []

st.title("无人机心跳监测可视化")

# 控制按钮
col1, col2 = st.columns(2)
with col1:
    if st.button("开始监测"):
        st.session_state.running = True
with col2:
    if st.button("停止监测"):
        st.session_state.running = False

# 数据展示区
placeholder = st.empty()
with placeholder.container():
    st.subheader("心跳数据")
    if st.session_state.data:
        df = st.session_state.drone.get_dataframe()
        st.dataframe(df)
        st.line_chart(df, x="时间", y="序号", color="状态")
    else:
        st.info("点击「开始监测」获取数据")

# 后台更新逻辑（非阻塞）
if st.session_state.get("running", False):
    st.session_state.drone.send_heartbeat()
    st.session_state.drone.check_connection()
    st.session_state.data = st.session_state.drone.get_dataframe()
    time.sleep(1)  # 短暂延迟后自动重跑
    st.rerun()  # 安全触发页面刷新

