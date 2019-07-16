# from pyecharts import Bar
#
# CLOTHES = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
# clothes_v1 = [5, 20, 36, 10, 75, 90]
# clothes_v2 = [10, 25, 8, 60, 20, 80]
#
# (Bar("柱状图数据堆叠示例")
#     .add("商家A", CLOTHES, clothes_v1, is_stack=True)
#     .add("商家B", CLOTHES, clothes_v2, is_stack=True)
#     .render())

# bar = Bar("我的第一个图表", "这里是副标题")
# bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
# # bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
# bar.render()
from pyecharts import Bar, Line, Overlap
from pyecharts.engine import create_default_environment
#
# bar = Bar("我的第一个图表", "这里是副标题")  # 柱状图
# bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90], mark_point=["average"])
#
# line = Line("我的第一个图表", "这里是副标题")  # 折线图
# line.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [7, 25, 39, 12, 89, 150], mark_line=["min", "max"])

# env = create_default_environment("html")
# 为渲染创建一个默认配置环境
# create_default_environment(filet_ype)
# file_type: 'html', 'svg', 'png', 'jpeg', 'gif' or 'pdf'
# overlap = Overlap()
# overlap.add(bar)
# overlap.add(line)
#
# env.render_chart_to_file(overlap, path='line-bar.html')
# env.render_chart_to_file(bar, path='bar.html')
# env.render_chart_to_file(line, path='line.html')

attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
v1 = [5, 20, 36, 10, 75, 90]
v2 = [10, 25, 8, 60, 20, 80]

bar = Bar("x 轴和 y 轴交换")
bar.add("商家A", attr, v1, label_color=['rgba(0,0,0,0)'], is_stack=True)
bar.add("商家B", attr, v2, is_label_show=True, is_stack=True, label_pos='inside')
env = create_default_environment("html")
env.render_chart_to_file(bar, path='bar.html')