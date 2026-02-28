import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.lines as mlines

def draw_full_sequence_diagram(save_path='sequence_diagram.pdf'):
    """
    绘制聚合与分发阶段的完整控制消息时序图
    :param save_path: 保存路径（支持png/pdf/svg等）
    """
    fig, ax = plt.subplots(figsize=(14, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(-14, 2)  # y轴向下增长
    ax.axis('off')

    # 定义参与者及其x坐标
    participants = {
        '工作节点A': 2,
        '工作节点B': 4,
        '工作节点C': 6,
        '调度器': 8,
        '参数服务器': 10
    }

    # 绘制垂直生命线
    for name, x in participants.items():
        ax.plot([x, x], [0, -16], color='gray', linestyle='-', linewidth=1, alpha=0.5)
        ax.text(x, 0.8, name, ha='center', va='bottom', fontsize=11, fontweight='bold')

    # 定义消息序列 (每个元组: (源, 目标, 标签, y坐标))
    messages = [
        # 聚合阶段
        ('工作节点A', '调度器', 'ASK_LOCAL_AGGREGATION', -1),
        ('调度器', '工作节点B', 'ASK_AS_RECEIVER', -2),
        ('工作节点B', '调度器', 'ASK_AS_RECEIVER_REPLY (accept)', -3),
        ('调度器', '工作节点A', 'ASK_LOCAL_AGGREGATION_REPLY (receiver=工作节点B)', -4),
        ('工作节点A', '工作节点B', 'LOCAL_AGGREGATION', -5),
        ('工作节点B', '调度器', 'FINISH_RECEIVING_LOCAL_AGGREGATION', -6),

        # 服务器广播迭代完成（聚合结束，分发开始）
        ('参数服务器', '工作节点A', 'NOTIFY_WORKER_ONE_ITERATION_FINISH', -7.4),
        ('参数服务器', '工作节点B', 'NOTIFY_WORKER_ONE_ITERATION_FINISH', -7.8),  # 略微偏移避免重叠
        ('参数服务器', '工作节点C', 'NOTIFY_WORKER_ONE_ITERATION_FINISH', -8.2),

        # 分发阶段（以工作节点A为例发起分发请求）
        ('工作节点A', '调度器', 'ASK_MODEL_RECEIVER', -9),
        ('调度器', '工作节点A', 'ASK_MODEL_RECEIVER_REPLY (target=工作节点C)', -11),
        ('工作节点A', '工作节点C', 'MODEL_DISTRIBUTION', -12),
        ('工作节点C', '工作节点A', 'MODEL_DISTRIBUTION_REPLY', -13)
    ]

    # 绘制消息箭头
    for src, dst, label, y in messages:
        x_start = participants[src]
        x_end = participants[dst]
        # 画水平箭头（略微弯曲避免重叠）
        arrow = FancyArrowPatch(
            (x_start, y), (x_end, y),
            arrowstyle='->',
            mutation_scale=20,
            color='black',
            linewidth=1.5,
            alpha=0.9,
            connectionstyle='arc3,rad=0.1'
        )
        ax.add_patch(arrow)
        # 在箭头中间上方添加消息标签
        mid_x = (x_start + x_end) / 2
        ax.text(mid_x, y + 0.1, label, ha='center', va='bottom',
                fontsize=8, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # 添加阶段分隔线及标注
    ax.axhline(y=-8, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax.text(1, -8.3, '聚合阶段结束 /\n分发阶段开始', ha='left', va='top', fontsize=10, style='italic', color='gray')

    # 保存图像
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f'saved to {save_path}')


# 调用生成
draw_full_sequence_diagram('sequence_diagram.png')
