import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

def draw_aggregation_tree_one_leaf_per_m(save_path='aggregation_tree.pdf', reversed = False):
    """
    绘制每个中间节点恰好有一个叶子节点的局部聚合树（叶子深度不等）
    :param save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    # 节点坐标（手工布局，保证层次清晰）
    pos = {
        'PS': (0, 0),          # 参数服务器
        'W6': (-2, -1.5),       # 中间节点1
        'W7': (2, -1.5),        # 中间节点2
        'W8': (2.5, -2.5),      # 中间节点3（位于M2下层）
        'W1': (-2, -2.5),         # M1的叶子
        'W2': (1.5, -2.5),          # M2的叶子
        'W3': (3, -3.5),      # M3的叶子
        'W5': (2, -3.5),
        'W4': (0, -1.5)           # 直接连PS的叶子（深度1）
    }

    # 边（子 -> 父），每个M节点只有一个直接叶子
    edges = [
        ('W1', 'W6'),
        ('W6', 'PS'),
        ('W2', 'W7'),
        ('W7', 'PS'),
        ('W3', 'W8'),
        ('W8', 'W7'),
        ('W4', 'PS'),
        ('W5', 'W8'),
    ]

    # 绘制节点
    # 参数服务器（红色）
    ps_circle = Circle(pos['PS'], radius=0.45, facecolor='lightcoral',
                       edgecolor='darkred', linewidth=2, alpha=0.9)
    ax.add_patch(ps_circle)
    ax.text(pos['PS'][0], pos['PS'][1], 'PS', ha='center', va='center',
            fontsize=14, fontweight='bold', color='white')

    # 中间聚合节点（绿色）
    for node in ['W6', 'W7', 'W8']:
        circle = Circle(pos[node], radius=0.4, facecolor='lightgreen',
                        edgecolor='darkgreen', linewidth=2, alpha=0.9)
        ax.add_patch(circle)
        ax.text(pos[node][0], pos[node][1], node, ha='center', va='center',
                fontsize=12, fontweight='bold', color='darkgreen')

    # 叶子节点（蓝色）
    for node in ['W1', 'W2', 'W3', 'W4', 'W5']:
        circle = Circle(pos[node], radius=0.35, facecolor='skyblue',
                        edgecolor='navy', linewidth=2, alpha=0.9)
        ax.add_patch(circle)
        ax.text(pos[node][0], pos[node][1], node, ha='center', va='center',
                fontsize=11, fontweight='bold', color='darkblue')

    # 绘制带箭头的边
    for child, parent in edges:
        if reversed:
            parent, child = child, parent
        arrow = FancyArrowPatch(
            pos[child], pos[parent],
            arrowstyle='->',
            mutation_scale=20,
            color='gray',
            linewidth=1.8,
            alpha=0.8,
            connectionstyle='arc3,rad=0.0'  # 直线连接
        )
        ax.add_patch(arrow)

    # 设置绘图范围
    x_vals = [p[0] for p in pos.values()]
    y_vals = [p[1] for p in pos.values()]
    x_margin = 1.2
    y_margin = 1.0
    ax.set_xlim(min(x_vals) - x_margin, max(x_vals) + x_margin)
    ax.set_ylim(min(y_vals) - y_margin, max(y_vals) + y_margin)

    # 保存图像（透明背景）
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f'saved to {save_path}')

# 调用生成
draw_aggregation_tree_one_leaf_per_m('aggregation_tree.png')
draw_aggregation_tree_one_leaf_per_m('broadcast_tree.png', True)
