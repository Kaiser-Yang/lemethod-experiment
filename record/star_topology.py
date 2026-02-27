import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.patches import FancyArrowPatch

def draw_star_topology(n_workers=6, radius=2.5, save_path='star_topology.pdf'):
    """
    绘制星型通信拓扑图
    :param n_workers: 工作节点数量
    :param radius: 工作节点分布半径
    :param save_path: 图像保存路径（支持png/pdf/svg等）
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('equal')
    ax.axis('off')  # 隐藏坐标轴

    # 中心参数服务器坐标
    center = (0, 0)

    # 绘制中心节点（使用圆角矩形或圆形，这里用圆形加阴影效果）
    center_circle = Circle(center, radius=0.5, facecolor='lightcoral', 
                           edgecolor='darkred', linewidth=2, alpha=0.9)
    ax.add_patch(center_circle)
    ax.text(center[0], center[1], '参数服务器\n(PS)', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    # 计算工作节点位置（均匀分布在圆周上）
    angles = np.linspace(0, 2*np.pi, n_workers, endpoint=False)
    worker_positions = [(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles]

    # 绘制工作节点并标注
    for i, (x, y) in enumerate(worker_positions):
        # 节点圆形
        worker_circle = Circle((x, y), radius=0.4, facecolor='skyblue',
                               edgecolor='navy', linewidth=2, alpha=0.9)
        ax.add_patch(worker_circle)
        # 节点标签
        ax.text(x, y, f'Worker {i+1}', ha='center', va='center',
                fontsize=10, fontweight='bold', color='darkblue')

        # 绘制双向箭头连接中心与工作节点
        arrow = FancyArrowPatch(center, (x, y), 
                                arrowstyle='<->',           # 双向箭头样式
                                mutation_scale=20,          # 箭头大小
                                color='gray', 
                                linewidth=1.5,
                                linestyle='-',
                                alpha=0.7,
                                connectionstyle='arc3,rad=0.0')  # 直线连接
        ax.add_patch(arrow)

    # 设置绘图范围，留出边距
    margin = 1.0
    ax.set_xlim(-radius - margin, radius + margin)
    ax.set_ylim(-radius - margin, radius + margin)

    # 保存图像（透明背景方便插入文档）
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f'saved to {save_path}')

# 调用函数生成图片
draw_star_topology(n_workers=6, radius=3.0, save_path='star_topology.png')
# 若需要PDF格式可将后缀改为.pdf
