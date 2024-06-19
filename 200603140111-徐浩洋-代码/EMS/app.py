
from flask import request,Flask, jsonify, render_template  # 导入Flask库和render_template函数
import mysql.connector  # 导入mysql.connector库
import numpy as np  # 导入numpy库并重命名为np
import plotly.graph_objs as go  # 从plotly库导入graph_objs模块并重命名为go
import json  # 导入json库
import plotly  # 导入plotly库
import pymodbus
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime  # 从datetime模块导入datetime类
from flask import jsonify
from pymodbus.client import ModbusTcpClient


app = Flask(__name__)  # 创建Flask应用程序实例

# 数据库连接信息
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'ami'
}


# 假设的Modbus通信配置
#modbus_config = {
#   'host': '192.168.1.10',  # Modbus设备IP地址
#   'port': 502,  # Modbus TCP端口号
#   'unit': 1,  # Modbus从站地址
#   'timeout': 1,  # 通信超时时间（秒）
#}






# 欢迎页面
@app.route('/')  # 定义路由'/'，对应欢迎页面
def welcome():  # 定义欢迎页面视图函数
    return render_template('welcome.html')  # 返回渲染后的welcome.html模板

# 定义员工信息集合
employees = {
    '电网电力市场部': [{'name': '王工', 'phone': '15000000000'}],
    '电网运维部': [{'name': '张工', 'phone': '13500000000'}],
    '输电部': [{'name': '高工', 'phone': '13500000000'}],
    '配电部': [{'name': '方工', 'phone': '13500000000'}],
    '发电部': [{'name': '蒋工', 'phone': '13500000000'}],
    '客户服务部': [{'name': '江工', 'phone': '13500000000'}],
    '电网通信与信息技术部': [{'name': '李工', 'phone': '19800000000'}],
    '电网应急响应与安全管理部': [{'name': '才工', 'phone': '16888888888'}],
    '电网法律与合规部': [{'name': '丁工', 'phone': '12222222222'}],
    '技术支持与创新部': [{'name': '徐工', 'phone': '14555555555'}],
}

# 部门选择页面
@app.route('/select-department')
def select_department():
    return render_template('select-department.html', departments=list(employees.keys()))

# 显示员工信息页面
@app.route('/department-employees', methods=['POST'])
def department_employees():
    department = request.form['department']
    department_employees = employees.get(department, [])
    return render_template('department-employees.html', employees=department_employees)

# 使用手册页面
@app.route('/manual')  # 定义路由'/manual'，对应使用手册页面
def manual():  # 定义使用手册页面视图函数
    # 这里可以定义一些帮助信息或者使用指南
    manual_content = {
        "welcome": "欢迎来到监控应用使用手册。",
        "introduction": "本应用提供了一个实时监控功耗消耗的平台，并能检测异常。",
        "navigation": "使用顶部的导航栏可以在不同页面间切换。",
        "monitor": "监控页面展示了功耗消耗的实时曲线，并标记了异常点。",
        "parameters": "参数页面允许用户调整监控参数。",
        "bot": "机器人页面提供了与监控相关的聊天机器人功能。",
        "threshold": "用户可以在监控页面调整异常检测的阈值。",
        "contact": "如有疑问，请联系系统管理员。"
    }
    return render_template('manual.html', manual_content=manual_content)  # 返回渲染后的manual.html模板

# 更新配置路由
# 全局配置变量
app.config['DATABASE_CONFIG'] = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'ami'
}

@app.route('/update-config')
def update_config():
    return render_template('update-config.html')

# 定义一个路由，用于发送Modbus命令
@app.route('/sendcommand',methods=['GET', 'POST'])
def send_modbus_command_route():
       return render_template('sendcommand.html')
    #   data = request.get_json()
    #  command = data.get('command')
#  address = data.get('address')

# Modbus客户端实例
#client = pymodbus.client.ModbusTcpClient(**modbus_config)

# 定义Modbus命令函数
#def send_modbus_command(command, address):
    #   try:
        # 连接到Modbus设备
    #      client.connect()
    #
        # 发送Modbus命令
    #     response = client.write_coil(address, command)

        # 断开连接
    #     client.close()

    #       return {'status': 'success', 'message': 'Command executed successfully'}
    #   except Exception as e:
#      return {'status': 'error', 'message': str(e)}

@app.route('/config')
def config_manager():
    return render_template('config.html', config=app.config['DATABASE_CONFIG'])



@app.route('/parameters')
def parameters():
    return render_template('parameters.html')

@app.route('/bot')
def bot():
    return render_template('bot.html')

@app.route('/more')
def more():
    return render_template('more.html')

# 应用配置，用于存储阈值
app.config['CURRENT_THRESHOLD'] = 93.84

# 更新阈值路由
@app.route('/update-threshold', methods=['POST'])
def update_threshold():
    data = request.get_json()
    new_threshold = float(data.get('threshold', app.config['CURRENT_THRESHOLD']))  # 将阈值转换为浮点数
    app.config['CURRENT_THRESHOLD'] = new_threshold  # 更新应用配置中的阈值
    return jsonify({'message': '阈值已更新', 'newThreshold': new_threshold})


# 定义API端点以获取监控数据
@app.route('/api/monitoring_data', methods=['GET'])
def get_monitoring_data():
       return render_template('api/api.html')
    # 假设您有一个获取监控数据的方法
    # data = MonitoringData.query.all()
    # return jsonify([{'time': d.time, 'power_consumption': d.power_consumption} for d in data])
    # 为了示例，我们返回一些硬编码的数据
    #   data = {'time': datetime.datetime.now(), 'power_consumption': 100.0}
#   return jsonify(data)
# 定义API端点以更新监控数据
@app.route('/api/monitoring_data', methods=['POST'])
def update_monitoring_data():
        return render_template('api/api.html')
    #   data = request.get_json()
    # new_data = MonitoringData(time=data['time'], power_consumption=data['power_consumption'])
    # db.session.add(new_data)
    # db.session.commit()
    # return jsonify({'message': 'Data updated successfully'}), 201
    # 为了示例，我们只是打印接收到的数据
    #    print(f"Received data: {data}")
#   return jsonify({'message': 'Data received'}), 200
# 定义API端点以集成CPS命令
@app.route('/api/cps_command', methods=['POST'])
def cps_command():
        return render_template('api/api.html')
    #   command = request.get_json()
    # 这里应该是处理CPS命令的逻辑
    # 例如，command['action'] 可能是 "start" 或 "stop"
    # 您需要根据命令执行相应的操作
#   print(f"Received command: {command}")
    #   return jsonify({'message': 'Command received and executed'}), 200



# 监控页面
@app.route('/monitor')  # 定义路由'/monitor'，对应监控页面
def monitor():  # 定义监控页面视图函数
    # 连接数据库
    cnx = mysql.connector.connect(**config)  # 使用config配置信息连接数据库
    cursor = cnx.cursor()  # 创建数据库游标

    # 选择所有时间和功耗消耗的数据
    cursor.execute("SELECT Time, PowerConsumption FROM ami")  # 执行查询语句
    data = cursor.fetchall()  # 获取查询结果

    # 转换数据格式为列表形式
    times = [record[0] for record in data]  # 提取时间数据
    power_consumption = [record[1] for record in data]  # 提取功耗消耗数据

    # 绘制功耗消耗曲线
    fig = go.Figure()  # 创建绘图对象
    fig.add_trace(go.Scatter(x=times, y=power_consumption, mode='lines', name='Power Consumption'))  # 添加功耗消耗曲线
    graphJSON = fig.to_json()  # 将图形数据转换为JSON格式

    # 初始化状态转移矩阵、过程噪声协方差矩阵和测量噪声协方差
    A = np.array([[1, 1], [0, 1]])  # 初始化状态转移矩阵
    Q = np.array([[0.05, 0.01], [0.01, 0.05]])  # 初始化过程噪声协方差矩阵
    R = 0.5  # 初始化测量噪声协方差

    # 初始化卡方检测相关变量
    x_hat = np.array([[power_consumption[0]], [0]])  # 初始化估计值
    P = np.eye(2)  # 初始化协方差矩阵

    # 记录异常状态位置
    anomaly_positions = []  # 初始化异常状态位置列表

    # 对于每个时间步，进行功耗消耗曲线绘制和卡方检测
    for i in range(1, len(power_consumption)):  # 遍历每个时间步
        # 计算预测值
        x_hat = A @ np.array([[power_consumption[i - 1]], [0]])  # 计算预测值
        P = A @ P @ A.T + Q  # 更新协方差矩阵

        # 计算卡方统计量
        chisq = (power_consumption[i] - x_hat[0][0]) ** 2 / R  # 计算卡方统计量
        current_threshold = app.config['CURRENT_THRESHOLD']
        # 如果卡方统计量超过阈值，标记为异常状态
        if chisq > current_threshold:
            anomaly_positions.append(i)
    # 绘制功耗消耗曲线和异常标记
    trace = go.Scatter(x=times, y=power_consumption, mode='lines', name='Power Consumption')  # 创建功耗消耗曲线对象

    # 根据异常位置生成异常标记数据
    anomaly_times = [times[i] for i in anomaly_positions]  # 将异常时间转换为时间格式
    anomalies = go.Scatter(x=anomaly_times, y=[power_consumption[i] for i in anomaly_positions],
                           mode='markers', name='Anomalies')  # 创建异常标记对象
    data = [trace, anomalies]  # 组合数据
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)  # 将数据转换为JSON格式

    # 将异常时间转换为字符串格式
    anomaly_times_strings = [time.strftime('%H:%M:%S') for time in anomaly_times]  # 将异常时间转换为字符串格式
    anomaly_times_json = json.dumps(anomaly_times_strings)  # 将异常时间转换为JSON格式

    # 关闭数据库连接
    cursor.close()  # 关闭游标
    cnx.close()  # 关闭数据库连接

    return render_template('monitor.html', graphJSON=graphJSON, anomaly_times=anomaly_times_json,current_threshold=current_threshold)  # 返回渲染后的monitor.html模板




if __name__ == '__main__':
    app.run(debug=True)  # 运行Flask应用程序，并开启调试模式