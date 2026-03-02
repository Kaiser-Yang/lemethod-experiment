import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def draw_full_sequence_diagram(save_path='sequence_diagram.pdf'):
    """
    绘制聚合与分发阶段的完整控制消息时序图
    :param save_path: 保存路径（支持png/pdf/svg等）
    """
    _, ax = plt.subplots(figsize=(14, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(-17, 2)  # y轴向下增长，扩展一点以容纳更多消息
    ax.axis('off')

    # 定义参与者及其x坐标
    participants = {
        '工作节点A': 2,
        '工作节点B': 4,
        '工作节点C': 6,
        '调度器': 8,
        '参数服务器': 10
    }

    # 绘制垂直生命线（延长至 -16.5）
    for name, x in participants.items():
        ax.plot([x, x], [0, -16.5], color='gray', linestyle='-', linewidth=1, alpha=0.5)
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

        # 调度器通知所有工作节点迭代完成（原为参数服务器，现改为调度器）
        ('调度器', '工作节点A', 'NOTIFY_WORKER_ONE_ITERATION_FINISH', -7.2),
        ('调度器', '工作节点B', 'NOTIFY_WORKER_ONE_ITERATION_FINISH', -7.6),
        ('调度器', '工作节点C', 'NOTIFY_WORKER_ONE_ITERATION_FINISH', -8.0),

        # 分发阶段：服务器首先询问调度器并发送
        ('参数服务器', '调度器', 'ASK_MODEL_RECEIVER', -9.2),
        ('调度器', '参数服务器', 'ASK_MODEL_RECEIVER_REPLY (target=工作节点C)', -10.2),
        ('参数服务器', '工作节点C', 'MODEL_DISTRIBUTION', -11.2),
        ('工作节点C', '参数服务器', 'MODEL_DISTRIBUTION_REPLY', -12.2),

        # 工作节点C也进行分发（可视为与服务器同时进行，此处顺序绘制）
        ('工作节点C', '调度器', 'ASK_MODEL_RECEIVER', -13.2),
        ('参数服务器', '调度器', 'ASK_MODEL_RECEIVER', -13.4),
        ('调度器', '工作节点C', 'ASK_MODEL_RECEIVER_REPLY (target=工作节点A)', -14.2),
        ('调度器', '参数服务器', 'ASK_MODEL_RECEIVER_REPLY (target=工作节点B)', -14.6),
        ('工作节点C', '工作节点A', 'MODEL_DISTRIBUTION', -15.2),
        ('参数服务器', '工作节点B', 'MODEL_DISTRIBUTION', -15.4),
        ('工作节点A', '工作节点C', 'MODEL_DISTRIBUTION_REPLY', -16.2),
        ('工作节点B', '参数服务器', 'MODEL_DISTRIBUTION_REPLY', -16.4),
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
        ax.text(mid_x, y + 0.15, label, ha='center', va='bottom',
                fontsize=8, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # 添加阶段分隔线及标注（调整位置）
    ax.axhline(y=-8.5, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax.text(1, -8.8, '聚合阶段结束 /\n分发阶段开始', ha='left', va='top', fontsize=10, style='italic', color='gray')

    # 保存图像
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f'saved to {save_path}')

# 调用生成
draw_full_sequence_diagram('sequence_diagram.png')
