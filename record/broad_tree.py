import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np

def draw_broadcast_tree(save_path='broadcast_tree.png'):
    """
    绘制动态并发分发树（广播树）
    特点：
    1. 按调度轮次分层：PS和第一轮节点在同一层（y坐标相同），第二轮节点在下层，依此类推
    2. 每条边上标注调度序号（①, ②, ...），表示第几次调度产生的传输
    """
    # 缩小画布尺寸
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_aspect('equal')
    ax.axis('off')

    # ========== 定义扩散过程 ==========
    # 调度记录: (源节点, 目标节点, 调度轮次)
    schedule = [
        (1, 'PS', 'W4'),
        (2, 'PS', 'W6'),
        (2, 'W4', 'W1'),
        (3, 'PS', 'W7'),
        (3, 'W6', 'W3'),
        (3, 'W1', 'W2'),
        (3, 'W4', 'W5'),
        (4, 'W5', 'W8'),
    ]

    # ========== 分层布局 ==========
    layer = {'PS': 0}
    for _, src, dst in schedule:
        layer[dst] = layer[src] + 1

    nodes_by_layer = {}
    for node, l in layer.items():
        nodes_by_layer.setdefault(l, []).append(node)

    # 减小节点间距
    y_spacing = 1.0   # 原 1.5
    x_spacing = 0.8   # 原 1.2
    pos = {}
    for l, nodes in nodes_by_layer.items():
        nodes_sorted = sorted(nodes)
        n = len(nodes_sorted)
        start_x = - (n - 1) * x_spacing / 2
        for i, node in enumerate(nodes_sorted):
            pos[node] = (start_x + i * x_spacing, -l * y_spacing)

    # ========== 绘制节点（半径缩小） ==========
    # PS
    ps_circle = Circle(pos['PS'], radius=0.35, facecolor='lightcoral',
                       edgecolor='darkred', linewidth=2, alpha=0.9)
    ax.add_patch(ps_circle)
    ax.text(pos['PS'][0], pos['PS'][1], 'PS', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    # 工作节点
    for node in pos:
        if node == 'PS':
            continue
        circle = Circle(pos[node], radius=0.28, facecolor='skyblue',
                        edgecolor='navy', linewidth=2, alpha=0.9)
        ax.add_patch(circle)
        ax.text(pos[node][0], pos[node][1], node, ha='center', va='center',
                fontsize=10, fontweight='bold', color='darkblue')

    # ========== 绘制带序号标注的边 ==========
    round_colors = {1: 'red', 2: 'orange', 3: 'green', 4: 'blue'}

    for round_num, src, dst in schedule:
        arrow = FancyArrowPatch(
            pos[src], pos[dst],
            arrowstyle='->',
            mutation_scale=18,
            color=round_colors.get(round_num, 'gray'),
            linewidth=1.8,
            alpha=0.9,
            connectionstyle='arc3,rad=0.0'
        )
        ax.add_patch(arrow)

        # 边的中点
        mid_x = (pos[src][0] + pos[dst][0]) / 2
        mid_y = (pos[src][1] + pos[dst][1]) / 2
        offset = 0.08
        dx = pos[dst][0] - pos[src][0]
        dy = pos[dst][1] - pos[src][1]
        norm = np.hypot(dx, dy)
        if norm > 0:
            dx /= norm
            dy /= norm
        perp_x = -dy * offset
        perp_y = dx * offset
        label_x = mid_x + perp_x
        label_y = mid_y + perp_y

        # 标注序号（带圆圈）
        # ax.text(label_x, label_y, f'{round_num}', ha='center', va='center',
        #         fontsize=9, fontweight='bold',
        #         bbox=dict(boxstyle='circle,pad=0.15', facecolor='white',
        #                   edgecolor=round_colors.get(round_num, 'black')))

    # ========== 图例 ==========
    legend_elements = []
    for r in range(1, 5):
        legend_elements.append(plt.Line2D([0], [0], color=round_colors[r], lw=2,
                                          label=f'第{r}次调度'))
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
              frameon=True, facecolor='white', edgecolor='gray')

    # 缩小坐标边距
    x_vals = [p[0] for p in pos.values()]
    y_vals = [p[1] for p in pos.values()]
    x_margin = 0.8
    y_margin = 0.6
    ax.set_xlim(min(x_vals) - x_margin, max(x_vals) + x_margin)
    ax.set_ylim(min(y_vals) - y_margin, max(y_vals) + y_margin)

    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=False)
    print(f'saved to {save_path}')

# 调用生成广播树
draw_broadcast_tree('broadcast_tree.png')
