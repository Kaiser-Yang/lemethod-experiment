import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']

# ==================== 数据定义 ====================
# 贪心概率调优结果（32节点，静态组）
greedy_static = [
    (0.6, 2704.3345057964325),
    (0.5, 2713.877676963806),
    (1.0, 2720.29834485054),
    (0.1, 2723.672041654587),
    (0.4, 2727.801529407501),
    (0.2, 2748.950067281723),
    (0.3, 2756.6114370822906),
    (0.7, 2774.665088415146),
    (0.8, 2777.117935180664),
    (0.9, 2803.403065443039)
]

# 贪心概率调优结果（32节点，动态组）
greedy_dynamic = [
    (0.9, 2985.306182861328),
    (0.1, 2986.8037102222443),
    (0.7, 2988.8796751499176),
    (1.0, 2995.769952058792),
    (0.4, 2996.0755155086517),
    (0.8, 2997.0085446834564),
    (0.6, 3001.2854228019714),
    (0.5, 3005.570837020874),
    (0.2, 3033.6022577285767),
    (0.3, 3045.4263558387756)
]

# 调度数量调优结果（32节点，静态组）
schedule_static = [
    (5, 2579.7233152389526),
    (4, 2621.7886576652527),
    (3, 2622.1098268032074),
    (7, 2683.771742582321),
    (6, 2703.45508146286),
    (2, 2713.993212223053),
    (1, 2720.29834485054),
    (8, 2863.6399369239807),
    (9, 2881.8238224983215),
    (13, 2952.755471944809),
    (10, 2979.7679069042206),
    (11, 3093.324608564377),
    (14, 3176.8998823165894),
    (12, 3202.662478208542),
    (15, 3420.5809841156006),
    (18, 3728.641146183014),
    (17, 3797.2028620243073),
    (21, 3926.8109736442566),
    (19, 3933.729520559311),
    (16, 3965.8288114070892),
    (22, 4132.412855386734),
    (20, 4158.596895456314),
    (23, 4281.37526512146),
    (24, 4362.851956367493),
    (25, 4638.54817199707),
    (26, 4707.450743675232),
    (27, 4924.71950340271),
    (28, 5148.704471826553),
    (29, 5317.488800287247),
    (30, 5422.872277259827),
    (31, 5713.463895559311),
    (32, 6004.415000915527)
]

# 调度数量调优结果（32节点，动态组）
schedule_dynamic = [
    (3, 2873.249228954315),
    (2, 2944.5967903137207),
    (5, 2960.741891860962),
    (4, 2962.4370877742767),
    (6, 2979.526656150818),
    (1, 2995.769952058792),
    (7, 3198.519252061844),
    (8, 3344.986218690872),
    (9, 3389.875543117523),
    (10, 3524.904333591461),
    (11, 3691.7322657108307),
    (12, 3706.240339756012),
    (13, 3842.9517426490784),
    (14, 3978.1325256824493),
    (15, 4141.700600862503),
    (18, 4373.580430269241),
    (19, 4439.73627281189),
    (17, 4449.431510686874),
    (20, 4574.82826924324),
    (22, 4603.289314508438),
    (21, 4628.788670301437),
    (16, 4661.256333589554),
    (23, 4897.624588727951),
    (24, 5041.25402712822),
    (25, 5259.357847213745),
    (26, 5357.3261282444),
    (27, 5631.159260511398),
    (28, 5750.4645302295685),
    (29, 6117.4502120018005),
    (30, 6274.9417378902435),
    (31, 6727.802109241486),
    (32, 6956.787885189056)
]

# ==================== 绘制贪心概率图 ====================
g_static = sorted(greedy_static, key=lambda x: x[0])
g_dynamic = sorted(greedy_dynamic, key=lambda x: x[0])
x_g_static = [p for p, _ in g_static]
y_g_static = [t for _, t in g_static]
x_g_dynamic = [p for p, _ in g_dynamic]
y_g_dynamic = [t for _, t in g_dynamic]

plt.figure(figsize=(8, 5))
plt.plot(x_g_static, y_g_static, marker='o', label='静态', color='blue')
plt.plot(x_g_dynamic, y_g_dynamic, marker='s', label='动态', color='red')
# 标记最优值
opt_static_idx = np.argmin(y_g_static)
opt_dynamic_idx = np.argmin(y_g_dynamic)
plt.plot(x_g_static[opt_static_idx], y_g_static[opt_static_idx], 'o', markersize=10, markeredgecolor='blue', markerfacecolor='none', label=f'静态最优（p={x_g_static[opt_static_idx]}）')
plt.plot(x_g_dynamic[opt_dynamic_idx], y_g_dynamic[opt_dynamic_idx], 's', markersize=10, markeredgecolor='red', markerfacecolor='none', label=f'动态最优（p={x_g_dynamic[opt_dynamic_idx]}）')
plt.xlabel('贪心概率 $p$')
plt.ylabel('总耗时（s）')
plt.title('贪心概率 $p$ 对总耗时的影响（$W=32, S=1$）')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('param_greedy.png', dpi=300)
# plt.savefig('param_greedy.pdf')  # 可选保存PDF
print("Saved param_greedy.png")

# ==================== 绘制调度数量图 ====================
s_static = sorted(schedule_static, key=lambda x: x[0])
s_dynamic = sorted(schedule_dynamic, key=lambda x: x[0])
x_s_static = [s for s, _ in s_static]
y_s_static = [t for _, t in s_static]
x_s_dynamic = [s for s, _ in s_dynamic]
y_s_dynamic = [t for _, t in s_dynamic]

plt.figure(figsize=(10, 6))
plt.plot(x_s_static, y_s_static, marker='o', label='静态', color='blue')
plt.plot(x_s_dynamic, y_s_dynamic, marker='s', label='动态', color='red')
# 标记最优值
opt_static_s_idx = np.argmin(y_s_static)
opt_dynamic_s_idx = np.argmin(y_s_dynamic)
plt.plot(x_s_static[opt_static_s_idx], y_s_static[opt_static_s_idx], 'o', markersize=10, markeredgecolor='blue', markerfacecolor='none', label=f'静态最优（S={x_s_static[opt_static_s_idx]}）')
plt.plot(x_s_dynamic[opt_dynamic_s_idx], y_s_dynamic[opt_dynamic_s_idx], 's', markersize=10, markeredgecolor='red', markerfacecolor='none', label=f'动态最优（S={x_s_dynamic[opt_dynamic_s_idx]}）')
plt.xlabel('调度数量 $S$')
plt.ylabel('总耗时（s）')
plt.title('调度数量 $S$ 对总耗时的影响（$W=32, p=1$）')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('param_schedule.png', dpi=300)
# plt.savefig('param_schedule.pdf')
print("Saved param_schedule.png")
