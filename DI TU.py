import streamlit as st
import time
import pandas as pd
from datetime import datetime
from streamlit_leaflet import LeafletMap
from pyproj import Transformer
from shapely.geometry import Polygon, Point
from shapely.ops import nearest_points
 # ---------------------- 无人机心跳类（保留原有逻辑） ----------------------
class DroneHeartbeat:
     def __init__(self):
         self.data = []
         self.sequence = 0
         self.max_records = 100
         # 新增：无人机当前位置（初始化为学校近似中心）
         self.current_lat = 32.2322
         self.current_lon = 118.749
     def send_heartbeat(self, target_lat=None, target_lon=None):
         self.sequence += 1
         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         # 模拟正常/异常状态
         status = "正常" if self.sequence % 5 != 0 else "异常"
         
         # 模拟无人机移动：向目标点缓慢靠近（无目标则保持原位置）
         if target_lat and target_lon:
             self.current_lat += (target_lat - self.current_lat) * 0.0001
             self.current_lon += (target_lon - self.current_lon) * 0.0001
         
         self.data.append({
             "时间": current_time,
             "连接状态": status,
             "无人机纬度": self.current_lat,
             "无人机经度": self.current_lon
         })
         # 只保留最近100条数据
         if len(self.data) > self.max_records:
             self.data = self.data[-self.max_records:]
     def check_connection(self):
         pass
     def get_dataframe(self):
         return pd.DataFrame(self.data)
 # ---------------------- 地图与路径规划工具类 ----------------------
 class MapPlanner:
     def __init__(self):
         # 坐标系转换：GCJ-02 -> WGS-84（部分地图底层需求）
         self.transformer = Transformer.from_crs("EPSG:4479", "EPSG:4326", always_xy=True)
         # 障碍物列表（初始为空，支持用户圈选）
         self.obstacles = []
     def gcj02_to_wgs84(self, lat, lon):
         """GCJ-02转WGS-84，适配国内地图"""
         x, y = self.transformer.transform(lon, lat)
         return y, x
     def add_obstacle(self, lat, lon, radius=50):
         """添加圆形障碍物（单位：米，适配校园场景）"""
         # 经纬度转米：1度≈111319米
         lat_step = radius / 111319
         lon_step = radius / (111319 * abs(lat))
         # 生成多边形边界
polygon = Polygon([
             (lon - lon_step, lat - lat_step),
             (lon + lon_step, lat - lat_step),
             (lon + lon_step, lat + lat_step),
             (lon - lon_step, lat + lat_step)
         ])
         self.obstacles.append(polygon)
     def check_path_collision(self, start_lat, start_lon, end_lat, end_lon):
         """检测AB点路径与障碍物碰撞"""
         path_line = LineString([(start_lon, start_lat), (end_lon, end_lat)])
         for obs in self.obstacles:
             if path_line.intersects(obs):
                 return True, obs.centroid
         return False, None
 # ---------------------- Streamlit 主界面逻辑 ----------------------
 # 初始化会话状态
 if "drone" not in st.session_state:
     st.session_state.drone = DroneHeartbeat()
 if "is_running" not in st.session_state:
     st.session_state.is_running = False
 if "map_planner" not in st.session_state:
     st.session_state.map_planner = MapPlanner()
 if "point_a" not in st.session_state:
     st.session_state.point_a = {"lat": 32.2322, "lon": 118.749}  # 初始A点
 if "point_b" not in st.session_state:
     st.session_state.point_b = {"lat": 32.2343, "lon": 118.749}  # 初始B点
 t.title("🚁 无人机通信心跳监测+路径规划可视化")
 st.subheader("实时监控+3D地图AB点规划+障碍物标注")
 # 分栏布局：控制面板 + 地图
 col1, col2 = st.columns([1, 2])
 with col1:
     st.subheader("⚙️ 控制面板")
     # 1. AB点坐标设置（匹配作业要求：GCJ-02）
     st.subheader("起点A (GCJ-02)")
     a_lat = st.number_input("纬度", value=32.2322, format="%.6f", step=0.0001, key="a_lat")
     a_lon = st.number_input("经度", value=118.749, format="%.6f", step=0.0001, key="a_lon")
     if st.button("设置A点"):
         st.session_state.point_a = {"lat": a_lat, "lon": a_lon}
         st.success("A点设置成功！")
     st.subheader("终点B (GCJ-02)")
     b_lat = st.number_input("纬度", value=32.2343, format="%.6f", step=0.0001, key="b_lat")
     b_lon = st.number_input("经度", value=118.749, format="%.6f", step=0.0001, key="b_lon")
     if st.button("设置B点"):
         st.session_state.point_b = {"lat": b_lat, "lon": b_lon}
         st.success("B点设置成功！")
     # 2. 飞行参数
     st.subheader("飞行参数")
     fly_height = st.slider("设定飞行高度(m)", min_value=10, max_value=100, value=50, step=5)
     st.info(f"当前飞行高度：{fly_height}m")
     # 3. 心跳控制按钮
     st.subheader("心跳监测")
  if st.button("▶️ 开始监测", type="primary"):
             st.session_state.is_running = True
             st.rerun()
     else:
         if st.button("⏹️ 停止监测", type="secondary"):
             st.session_state.is_running = False
             st.rerun()
     if st.button("🗑️ 清空数据", type="secondary"):
         st.session_state.drone = DroneHeartbeat()
         st.session_state.map_planner = MapPlanner()
         st.rerun()
     # 4. 障碍物圈选（简化操作：点击地图添加）
     st.subheader("障碍物标注")
     st.info("👉 直接在右侧地图点击，自动添加圆形障碍物（半径50m）")
     if st.button("清除所有障碍物"):
         st.session_state.map_planner.obstacles = []
         st.success("障碍物已清除！")
 with col2:
     st.subheader("🗺️ 3D/2D 地图视图")
     # 初始化地图（初始中心：学校近似中心，缩放级别18）
     m = LeafletMap(
         center=(st.session_state.point_a["lat"], st.session_state.point_a["lon"]),
         zoom=18,
tile="https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&sty
        le=8&x={x}&y={y}&z={z}",
         attr="高德地图",
         key="map"
     )
     # 绘制AB点
     a_point = st.session_state.point_a
     b_point = st.session_state.point_b
     m.add_marker(location=(a_point["lat"], a_point["lon"]), popup="起点A", icon="red")
     m.add_marker(location=(b_point["lat"], b_point["lon"]), popup="终点B", icon="green")
     # 绘制AB点路径
     path_coords = [(a_point["lat"], a_point["lon"]), (b_point["lat"], b_point["lon"])]
     # 检测路径碰撞
     is_collision, collision_point = st.session_state.map_planner.check_path_collision(
         a_point["lat"], a_point["lon"], b_point["lat"], b_point["lon"]
     )
     # 路径颜色：红色（碰撞）/ 蓝色（正常）
     path_color = "red" if is_collision else "blue"
     m.add_polygon(locations=path_coords, color=path_color, fill=False, weight=3)
     # 绘制障碍物
     for obs in st.session_state.map_planner.obstacles:
         obs_lon, obs_lat = obs.centroid.x, obs.centroid.y
         m.add_circle(location=(obs_lat, obs_lon), radius=50, color="orange", fill=True,fill_opacity=0.3)fill_opacity=0.3)
         # 绘制无人机实时位置（来自心跳数据）
     drone_df = st.session_state.drone.get_dataframe()
     if not drone_df.empty:
         latest_drone = drone_df.iloc[-1]
         drone_lat = latest_drone["无人机纬度"]
         drone_lon = latest_drone["无人机经度"]
         m.add_marker(location=(drone_lat, drone_lon), popup="无人机", icon="blue")
     # 地图渲染
     m()
     # 地图切换提示
     st.caption("💡 可通过地图控件切换2D/3D视图，放大后圈选障碍物更精准")
 # ---------------------- 数据展示区 ----------------------
 st.subheader("📊 实时心跳与路径状态")
 df = st.session_state.drone.get_dataframe()
 col_data1, col_data2 = st.columns(2)
 with col_data1:
     if not df.empty:
         st.dataframe(df[["时间", "心跳序号", "连接状态", "无人机纬度", "无人机经度"]], use_container_width=True)
     else:
         st.info("暂无心跳数据")
 with col_data2:
     # 路径状态提示
     if is_collision:
         st.error(f"❌ AB点路径与障碍物碰撞！碰撞点：{collision_point}")
     else:
         st.success("✅ AB点路径无障碍物，可安全飞行")
     # 心跳状态统计
     if not df.empty:
         normal_count = len(df[df["连接状态"] == "正常"])
         error_count = len(df[df["连接状态"] == "异常"])
         st.metric("正常心跳数", normal_count)
         st.metric("异常心跳数", error_count)
 # 实时刷新逻辑（保留原有心跳逻辑，新增地图联动）
 if st.session_state.is_running:
     # 传入AB点，模拟无人机向目标移动
     st.session_state.drone.send_heartbeat(
         target_lat=st.session_state.point_b["lat"],
         target_lon=st.session_state.point_b["lon"]
     )
     st.session_state.drone.check_connection()
     time.sleep(1)
     st.rerun()    
         
    
