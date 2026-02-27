import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
import matplotlib.pyplot as plt
import re

# 定义数据文本
lemethod_static_text = """
('lemethod_50_1_8_1000M_0.6_0_a', 13777.629513502121)
('lemethod_50_1_8_800M_0.6_0_a', 11546.70026254654)
('lemethod_50_1_8_700M_0.6_0_a', 9748.25587797165)
('lemethod_50_1_8_500M_0.6_0_a', 6889.60485959053)
('lemethod_50_1_8_900M_0.6_0_a', 12610.491896867752)
('lemethod_50_1_8_400M_0.6_0_a', 5790.1327929496765)
('lemethod_50_1_8_240M_0.6_0_a', 3290.0889167785645)
('lemethod_50_1_8_300M_0.6_0_a', 4203.773760318756)
('lemethod_50_1_8_600M_0.6_0_a', 8236.326235294342)
"""

lemethod_dynamic_text = """
('lemethod_50_1_5_300M_0.9_1_a', 4273.3850309848785)
('lemethod_50_1_5_240M_0.9_1_a', 3495.0027499198914)
('lemethod_50_1_5_600M_0.9_1_a', 7880.417015552521)
('lemethod_50_1_5_400M_0.9_1_a', 5618.673431634903)
('lemethod_50_1_5_500M_0.9_1_a', 6805.026723384857)
('lemethod_50_1_5_700M_0.9_1_a', 9046.178564786911)
('lemethod_50_1_5_1000M_0.9_1_a', 13098.732275009155)
('lemethod_50_1_5_800M_0.9_1_a', 10632.447079181671)
('lemethod_50_1_5_900M_0.9_1_a', 11930.21201133728)
"""

default_static_text = """
('default_50_1000M_0_a', 61091.92679667473)
('default_50_240M_0_a', 14098.512595891953)
('default_50_300M_0_a', 17585.899214744568)
('default_50_600M_0_a', 36552.806321144104)
('default_50_900M_0_a', 54248.361621141434)
('default_50_400M_0_a', 23631.344161510468)
('default_50_800M_0_a', 47870.46883177757)
('default_50_700M_0_a', 41363.50402927399)
('default_50_500M_0_a', 30393.862632989883)
"""

default_dynamic_text = """
('default_50_1000M_1_a', 61445.63865566254)
('default_50_240M_1_a', 14085.683629512787)
('default_50_700M_1_a', 42950.271661281586)
('default_50_900M_1_a', 53526.71126914024)
('default_50_500M_1_a', 30951.299822092056)
('default_50_300M_1_a', 17817.093485593796)
('default_50_600M_1_a', 35873.68512964249)
('default_50_400M_1_a', 24254.852313041687)
('default_50_800M_1_a', 47044.15779590607)
"""

def parse_model_data(text, prefix):
    """从文本解析 (size, time) 列表，size为整数MB"""
    data = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        # 提取时间和型号
        # 格式: ('default_50_1000M_0_a', 61091.92679667473)
        match = re.search(r"'[^']*_(\d+)M_[^']*',\s*([\d.]+)", line)
        if match:
            size = int(match.group(1))
            time = float(match.group(2))
            data.append((size, time))
    return data

# 解析四组数据
ls = parse_model_data(lemethod_static_text, 'lemethod')
ld = parse_model_data(lemethod_dynamic_text, 'lemethod')
ds = parse_model_data(default_static_text, 'default')
dd = parse_model_data(default_dynamic_text, 'default')

# 按模型大小排序
ls.sort(key=lambda x: x[0])
ld.sort(key=lambda x: x[0])
ds.sort(key=lambda x: x[0])
dd.sort(key=lambda x: x[0])

# 提取x和y
x_ls = [p[0] for p in ls]
y_ls = [p[1] for p in ls]
x_ld = [p[0] for p in ld]
y_ld = [p[1] for p in ld]
x_ds = [p[0] for p in ds]
y_ds = [p[1] for p in ds]
x_dd = [p[0] for p in dd]
y_dd = [p[1] for p in dd]

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(x_ds, y_ds, marker='o', linestyle='-', color='tab:blue', label='静态默认')
plt.plot(x_dd, y_dd, marker='s', linestyle='-', color='tab:orange', label='动态默认')
plt.plot(x_ls, y_ls, marker='^', linestyle='-', color='tab:green', label='静态LeMethod')
plt.plot(x_ld, y_ld, marker='D', linestyle='-', color='tab:red', label='动态LeMethod')

plt.xlabel('模型大小（MB）', fontsize=12)
plt.ylabel('总耗时（秒）', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('scale_model.png', dpi=300)
print("Saved scale_model.png")
