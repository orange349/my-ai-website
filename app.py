from flask import Flask, render_template, jsonify, request
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'


# 模拟数据生成函数
def generate_metrics_data():
    """生成仪表盘指标数据"""
    return {
        'model_accuracy': round(random.uniform(85, 99), 1),
        'response_time': random.randint(50, 200),
        'active_users': random.randint(1000, 5000),
        'data_processed': random.randint(10000, 50000),
        'system_status': '正常运行',
        'uptime': '99.9%'
    }


def generate_performance_data():
    """生成性能图表数据"""
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
    accuracy_data = [round(random.uniform(80, 98), 1) for _ in range(30)]
    response_data = [random.randint(80, 250) for _ in range(30)]

    df = pd.DataFrame({
        'Date': dates,
        '准确率': accuracy_data,
        '响应时间(ms)': response_data
    })
    return df


def generate_usage_data():
    """生成使用情况数据"""
    features = ['图像识别', '自然语言处理', '预测分析', '数据挖掘', '自动化']
    usage = [random.randint(100, 1000) for _ in range(5)]
    return pd.DataFrame({
        '功能': features,
        '使用次数': usage
    })


# 路由定义
@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """仪表盘页面"""
    # 生成指标数据
    metrics = generate_metrics_data()

    # 生成性能图表
    perf_df = generate_performance_data()
    perf_fig = px.line(perf_df, x='Date', y=['准确率', '响应时间(ms)'],
                       title='AI模型性能趋势',
                       labels={'value': '数值', 'variable': '指标'})
    perf_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    perf_chart = json.dumps(perf_fig, cls=plotly.utils.PlotlyJSONEncoder)

    # 生成使用情况图表
    usage_df = generate_usage_data()
    usage_fig = px.bar(usage_df, x='功能', y='使用次数',
                       title='功能使用情况', color='使用次数',
                       color_continuous_scale='Blues')
    usage_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    usage_chart = json.dumps(usage_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html',
                           metrics=metrics,
                           perf_chart=perf_chart,
                           usage_chart=usage_chart)


@app.route('/pricing')
def pricing():
    """定价页面"""
    plans = [
        {
            'name': '基础版',
            'price': '¥999',
            'period': '/月',
            'features': ['最多5个AI模型', '100GB数据处理', '基础技术支持', '标准准确率'],
            'recommended': False
        },
        {
            'name': '专业版',
            'price': '¥2,999',
            'period': '/月',
            'features': ['最多20个AI模型', '500GB数据处理', '优先技术支持', '高准确率', 'API访问'],
            'recommended': True
        },
        {
            'name': '企业版',
            'price': '定制',
            'period': '',
            'features': ['无限AI模型', '定制数据量', '24/7专属支持', '最高准确率', '完整API访问', '定制功能'],
            'recommended': False
        }
    ]
    return render_template('pricing.html', plans=plans)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """联系页面"""
    if request.method == 'POST':
        # 这里处理表单提交
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # 在实际应用中，这里应该保存到数据库或发送邮件
        return render_template('contact.html', success=True)

    return render_template('contact.html', success=False)


@app.route('/api/real-time-metrics')
def real_time_metrics():
    """实时指标API"""
    metrics = generate_metrics_data()
    return jsonify(metrics)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)