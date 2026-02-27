import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
import matplotlib.pyplot as plt
import re

# ==================== 数据定义 ====================
# 直接复制题目中给出的文本
lemethod_dynamic_text = """
('lemethod_20_1_3_240M_0.9_1_a', 2538.3279745578766)
('lemethod_40_1_4_240M_0.9_1_a', 3150.367321252823)
('lemethod_10_1_3_240M_0.9_1_a', 2218.841932296753)
('lemethod_85_1_8_240M_0.9_1_a', 3971.104033946991)
('lemethod_50_1_5_240M_0.9_1_a', 3495.0027499198914)
('lemethod_80_1_8_240M_0.9_1_a', 4052.4658329486847)
('lemethod_55_1_5_240M_0.9_1_a', 3305.547732114792)
('lemethod_65_1_6_240M_0.9_1_a', 3684.041827917099)
('lemethod_70_1_7_240M_0.9_1_a', 3860.801153898239)
('lemethod_35_1_3_240M_0.9_1_a', 3054.2890412807465)
('lemethod_90_1_8_240M_0.9_1_a', 3982.0633957386017)
('lemethod_60_1_6_240M_0.9_1_a', 3700.7065510749817)
('lemethod_95_1_9_240M_0.9_1_a', 4340.301110029221)
('lemethod_25_1_3_240M_0.9_1_a', 2860.391548871994)
('lemethod_15_1_3_240M_0.9_1_a', 2591.6239914894104)
('lemethod_30_1_3_240M_0.9_1_a', 2982.287831544876)
('lemethod_45_1_4_240M_0.9_1_a', 3238.9606590270996)
('lemethod_75_1_7_240M_0.9_1_a', 3919.6574087142944)
('lemethod_100_1_9_240M_0.9_1_a', 4211.067704677582)
"""

lemethod_static_text = """
('lemethod_90_1_14_240M_0.6_0_a', 4128.325797080994)
('lemethod_55_1_9_240M_0.6_0_a', 3285.653203725815)
('lemethod_15_1_3_240M_0.6_0_a', 2088.55544424057)
('lemethod_85_1_13_240M_0.6_0_a', 4062.9409594535828)
('lemethod_60_1_9_240M_0.6_0_a', 3609.8160054683685)
('lemethod_30_1_5_240M_0.6_0_a', 2695.985447406769)
('lemethod_40_1_6_240M_0.6_0_a', 2804.371499300003)
('lemethod_95_1_15_240M_0.6_0_a', 4628.8682997226715)
('lemethod_35_1_5_240M_0.6_0_a', 2768.2093937397003)
('lemethod_20_1_3_240M_0.6_0_a', 2333.390537261963)
('lemethod_50_1_8_240M_0.6_0_a', 3290.0889167785645)
('lemethod_80_1_13_240M_0.6_0_a', 3806.9258394241333)
('lemethod_65_1_10_240M_0.6_0_a', 3783.4233162403107)
('lemethod_75_1_12_240M_0.6_0_a', 3993.4696724414825)
('lemethod_25_1_4_240M_0.6_0_a', 2529.8970682621)
('lemethod_45_1_7_240M_0.6_0_a', 2944.6313445568085)
('lemethod_10_1_3_240M_0.6_0_a', 1738.2607219219208)
('lemethod_70_1_11_240M_0.6_0_a', 3726.388567209244)
('lemethod_100_1_16_240M_0.6_0_a', 4710.304752111435)
"""

default_dynamic_text = """
('default_45_240M_1_a', 14601.79453921318)
('default_25_240M_1_a', 8674.264544010162)
('default_60_240M_1_a', 18141.561836719513)
('default_20_240M_1_a', 7343.564475536346)
('default_75_240M_1_a', 20603.955714941025)
('default_70_240M_1_a', 18667.15565943718)
('default_100_240M_1_a', 27631.928013324738)
('default_40_240M_1_a', 12179.976054668427)
('default_95_240M_1_a', 28148.63996362686)
('default_30_240M_1_a', 9259.616561412811)
('default_80_240M_1_a', 21786.026332378387)
('default_35_240M_1_a', 10127.619410037994)
('default_65_240M_1_a', 18079.583578824997)
('default_50_240M_1_a', 14085.683629512787)
('default_85_240M_1_a', 21850.648270606995)
('default_15_240M_1_a', 5400.9088768959045)
('default_55_240M_1_a', 15024.658378601074)
('default_90_240M_1_a', 25056.278143644333)
('default_10_240M_1_a', 3441.053349494934)
"""

default_static_text = """
('default_25_240M_0_a', 8152.445867538452)
('default_15_240M_0_a', 5277.766409397125)
('default_75_240M_0_a', 20940.19470500946)
('default_30_240M_0_a', 8991.876920223236)
('default_35_240M_0_a', 10164.289767503738)
('default_90_240M_0_a', 24213.22121334076)
('default_55_240M_0_a', 15035.20434308052)
('default_45_240M_0_a', 14055.135337591171)
('default_80_240M_0_a', 20954.17534804344)
('default_40_240M_0_a', 11142.362161874771)
('default_65_240M_0_a', 18426.731356859207)
('default_10_240M_0_a', 3268.3630044460297)
('default_20_240M_0_a', 6411.3104956150055)
('default_95_240M_0_a', 27333.738883972168)
('default_50_240M_0_a', 14098.512595891953)
('default_70_240M_0_a', 19539.83097410202)
('default_85_240M_0_a', 21437.86607336998)
('default_60_240M_0_a', 17955.175944805145)
('default_100_240M_0_a', 26875.29162478447)
"""

def parse_data(text):
    """从文本中提取 (节点数, 总耗时) 列表"""
    pattern = r'lemethod_(\d+)_'
    if 'default' in text:
        pattern = r'default_(\d+)_'
    data = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        # 提取时间
        match = re.search(r'\([^,]+,\s*([\d.]+)\)', line)
        if not match:
            continue
        time = float(match.group(1))
        # 提取节点数
        node_match = re.search(pattern, line)
        if node_match:
            nodes = int(node_match.group(1))
            data.append((nodes, time))
    return data

# 解析四组数据
lemethod_dyn = parse_data(lemethod_dynamic_text)
lemethod_stat = parse_data(lemethod_static_text)
default_dyn = parse_data(default_dynamic_text)
default_stat = parse_data(default_static_text)

# 按节点数排序
lemethod_dyn.sort(key=lambda x: x[0])
lemethod_stat.sort(key=lambda x: x[0])
default_dyn.sort(key=lambda x: x[0])
default_stat.sort(key=lambda x: x[0])

# 提取 x 和 y
x_ld = [p[0] for p in lemethod_dyn]
y_ld = [p[1] for p in lemethod_dyn]
x_ls = [p[0] for p in lemethod_stat]
y_ls = [p[1] for p in lemethod_stat]
x_dd = [p[0] for p in default_dyn]
y_dd = [p[1] for p in default_dyn]
x_ds = [p[0] for p in default_stat]
y_ds = [p[1] for p in default_stat]

# ==================== 静态组图 ====================
plt.figure(figsize=(8, 5))
plt.plot(x_ds, y_ds, marker='o', linestyle='-', color='tab:blue', label='Default static')
plt.plot(x_ls, y_ls, marker='^', linestyle='-', color='tab:green', label='LeMethod static')
plt.xlabel('Number of worker nodes', fontsize=12)
plt.ylabel('Total time (s)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('scale_nodes_static.png', dpi=300)
# plt.savefig('scale_nodes_static.pdf')
print("Saved scale_nodes_static.png")

# ==================== 动态组图 ====================
plt.figure(figsize=(8, 5))
plt.plot(x_dd, y_dd, marker='s', linestyle='-', color='tab:orange', label='Default dynamic')
plt.plot(x_ld, y_ld, marker='D', linestyle='-', color='tab:red', label='LeMethod dynamic')
plt.xlabel('Number of worker nodes', fontsize=12)
plt.ylabel('Total time (s)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('scale_nodes_dynamic.png', dpi=300)
# plt.savefig('scale_nodes_dynamic.pdf')
print("Saved scale_nodes_dynamic.png")

# ==================== 绘制 ====================
plt.figure(figsize=(10, 6))

plt.plot(x_ds, y_ds, marker='o', linestyle='-', color='tab:blue', label='静态默认')
plt.plot(x_dd, y_dd, marker='s', linestyle='-', color='tab:orange', label='动态默认')
plt.plot(x_ls, y_ls, marker='^', linestyle='-', color='tab:green', label='静态LeMethod')
plt.plot(x_ld, y_ld, marker='D', linestyle='-', color='tab:red', label='动态LeMethod')

plt.xlabel('工作节点数量', fontsize=12)
plt.ylabel('总耗时（秒）', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

plt.savefig('scale_nodes.png', dpi=300)
# plt.savefig('scale_nodes.pdf')
print("Saved scale_nodes.png")
