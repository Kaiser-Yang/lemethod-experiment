import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle


def draw_architecture(save_path='architecture.pdf'):
    """
    绘制整体架构图：参数服务器节点（内嵌调度器）与工作节点，展示控制流与数据流
    :param save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # ========== 绘制节点 ==========
    # 参数服务器节点（大矩形，代表物理节点）
    ps_rect = Rectangle((1, 2.5), 2.5, 2, facecolor='lightcoral', edgecolor='darkred', linewidth=2, alpha=0.7)
    ax.add_patch(ps_rect)
    ax.text(2.25, 4.2, '参数服务器节点', ha='center', fontsize=12, fontweight='bold')

    # 参数服务器内部组件（主进程）
    ps_main = Rectangle((1.2, 3.0), 1.4, 0.8, facecolor='white', edgecolor='darkred', linewidth=1.5)
    ax.add_patch(ps_main)
    ax.text(1.7, 3.4, '参数服务器', ha='center', fontsize=10, va='center')

    # 调度器进程（小矩形，位于参数服务器节点内）
    scheduler = Rectangle((2.2, 3.0), 1.0, 0.8, facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5)
    ax.add_patch(scheduler)
    ax.text(2.5, 3.4, '调度器', ha='center', fontsize=10, va='center', color='darkgreen')

    # 工作节点（四个圆形，分布在右侧）
    worker_pos = [(6, 4.5), (6, 3.5), (6, 2.5), (6, 1.5)]
    for i, (x, y) in enumerate(worker_pos):
        circle = Circle((x, y), 0.5, facecolor='skyblue', edgecolor='navy', linewidth=2, alpha=0.8)
        ax.add_patch(circle)
        ax.text(x, y, f'Worker {i+1}', ha='center', va='center', fontsize=10, fontweight='bold', color='darkblue')

    # ========== 绘制连线 ==========
    # 控制消息（虚线箭头）：每个工作节点 -> 调度器
    for (x_w, y_w) in worker_pos:
        arrow = FancyArrowPatch(
            (x_w-0.5, y_w), (2.5 + 0.5, 3.4),  # 指向调度器中心
            arrowstyle='->',
            linestyle='dashed',
            mutation_scale=15,
            color='gray',
            linewidth=1.5,
            alpha=0.7,
            connectionstyle='arc3,rad=0.1'
        )
        ax.add_patch(arrow)
    arrow = FancyArrowPatch(
        (2.7, 3.5), (1.7, 3.5),
        arrowstyle='->',
        linestyle='dashed',
        mutation_scale=15,
        color='gray',
        linewidth=1.5,
        alpha=0.7,
        connectionstyle='arc3,rad=0.1'
    )
    ax.add_patch(arrow)
    arrow = FancyArrowPatch(
        (1.7, 3.2), (2.7, 3.2),
        arrowstyle='->',
        linestyle='dashed',
        mutation_scale=15,
        color='gray',
        linewidth=1.5,
        alpha=0.7,
        connectionstyle='arc3,rad=0.1'
    )
    ax.add_patch(arrow)

    # 调度器到工作节点的虚线箭头（双向控制，但为简洁可加反向箭头，或直接用双头？用单向示意双向需要两条线）
    # 为简化，我们加一条从调度器指向工作节点的虚线，表示控制回复
    for (x_w, y_w) in worker_pos:
        arrow = FancyArrowPatch(
            (2.5 + 0.5, 3.4), (x_w-0.5, y_w),
            arrowstyle='->',
            linestyle='dashed',
            mutation_scale=15,
            color='gray',
            linewidth=1.5,
            alpha=0.7,
            connectionstyle='arc3,rad=0.1'
        )
        ax.add_patch(arrow)

    # 数据流（实线）：工作节点之间的数据交换（局部聚合）
    # 连接Worker1-Work2, Worker2-Work3, Worker3-Work4 示例
    data_edges = [(0,1), (1,2), (2,3)]
    for i, j in data_edges:
        arrow = FancyArrowPatch(
            worker_pos[i], worker_pos[j],
            arrowstyle='<->',  # 双向数据交换
            linestyle='solid',
            mutation_scale=15,
            color='darkblue',
            linewidth=1.8,
            alpha=0.8,
            connectionstyle='arc3,rad=0.2'
        )
        ax.add_patch(arrow)

    # 数据流：工作节点与参数服务器之间的数据交换（最终聚合结果上传 / 模型广播）
    for (x_w, y_w) in worker_pos:
        arrow = FancyArrowPatch(
            (x_w-0.5, y_w), (2.0, 3.4),  # 指向参数服务器主进程
            arrowstyle='<->',
            linestyle='solid',
            mutation_scale=15,
            color='darkred',
            linewidth=1.8,
            alpha=0.8,
            connectionstyle='arc3,rad=0.1'
        )
        ax.add_patch(arrow)

    # 添加图例（手动构造）
    # 控制消息样例
    ax.plot([], [], linestyle='dashed', color='gray', linewidth=1.5, label='控制消息')
    # 工作节点间数据流
    ax.plot([], [], linestyle='solid', color='darkblue', linewidth=1.8, label='节点间数据')
    # 节点-服务器数据流
    ax.plot([], [], linestyle='solid', color='darkred', linewidth=1.8, label='节点-服务器数据')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

    # 保存图像
    plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
    print(f'saved to {save_path}')

# 调用生成
draw_architecture('architecture.png')
