import streamlit as st
from streamlit_leaflet import LeafletMap
from datetime import datetime

# ---------------------- 页面配置 ----------------------
st.set_page_config(page_title="无人机地图Demo", layout="wide")
st.title("无人机智能化应用 - 地图Demo")

# ---------------------- 坐标输入 ----------------------
col1, col2 = st.columns(2)
with col1:
    st.subheader("起点A")
    lat_a = st.number_input("纬度A", value=32.2322, format="%.4f")
    lon_a = st.number_input("经度A", value=118.749, format="%.4f")
with col2:
    st.subheader("终点B")
    lat_b = st.number_input("纬度B", value=32.2343, format="%.4f")
    lon_b = st.number_input("经度B", value=118.749, format="%.4f")

# ---------------------- 飞行参数 ----------------------
height = st.slider("设定飞行高度(m)", min_value=10, max_value=150, value=50)

# ---------------------- 地图显示 ----------------------
st.subheader("校园地图")
map_center = [(lat_a + lat_b)/2, (lon_a + lon_b)/2]  # 地图中心取两点中点

m = LeafletMap(center=map_center, zoom=18)
# 标记起点A
m.add_marker(location=[lat_a, lon_a], popup="起点A", icon="red")
# 标记终点B
m.add_marker(location=[lat_b, lon_b], popup="终点B", icon="green")
# 绘制AB连线
m.add_polyline(locations=[[lat_a, lon_a], [lat_b, lon_b]], color="blue", weight=3)

# 渲染地图
m.to_streamlit(height=500)

# ---------------------- 心跳模拟（极简版） ----------------------
if st.button("模拟发送心跳包"):
    st.success(f"[{datetime.now()}] 无人机位置: ({lat_a}, {lon_a}) | 飞行高度: {height}m") 
