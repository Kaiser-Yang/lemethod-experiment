import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(-5, 5)
ax.set_ylim(-1, 8)
ax.axis('off')  # 隐藏坐标轴

# 定义辅助函数：绘制圆柱（数据源）
def draw_cylinder(ax, center_x, center_y, width, height, color='gray', edgecolor='black'):
    """绘制一个简单的圆柱，由矩形和两个半椭圆组成"""
    rect = patches.Rectangle(
        (center_x - width/2, center_y - height/2), width, height,
        linewidth=1.5, edgecolor=edgecolor, facecolor=color, alpha=0.8
    )
    ax.add_patch(rect)
    # 顶部椭圆
    top_ellipse = patches.Ellipse(
        (center_x, center_y + height/2), width, height/3,
        linewidth=1.5, edgecolor=edgecolor, facecolor=color, alpha=0.8
    )
    ax.add_patch(top_ellipse)
    # 底部椭圆
    bottom_ellipse = patches.Ellipse(
        (center_x, center_y - height/2), width, height/3,
        linewidth=1.5, edgecolor=edgecolor, facecolor=color, alpha=0.8
    )
    ax.add_patch(bottom_ellipse)

# ========== 1. 数据准备与划分 ==========
data_x, data_y = 0, 7
draw_cylinder(ax, data_x, data_y, width=2.5, height=1.2, color='lightgray')

# 三个数据分片（矩形）
shard_positions = [(-2, 5), (0, 5), (2, 5)]
shard_colors = ['lightgreen', 'lightgreen', 'lightgreen']
shard_labels = ['分片 1', '分片 2', '分片 3']
shards = []
for i, (x, y) in enumerate(shard_positions):
    rect = patches.Rectangle(
        (x-0.8, y-0.5), 1.6, 1.0,
        linewidth=1.5, edgecolor='black', facecolor=shard_colors[i], alpha=0.8
    )
    ax.add_patch(rect)
    ax.text(x, y, shard_labels[i], ha='center', va='center', fontsize=14)
    shards.append((x, y))

# 从数据源到分片的箭头
for (x, y) in shard_positions:
    ax.annotate("", xy=(x, y+0.5), xytext=(data_x, data_y-0.6),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# 步骤标签 (1) —— 向左移动，避免与方框重叠
ax.text(-3.2, 5.7, '(1) 数据准备与划分', fontsize=14, fontweight='bold', color='darkgreen')

# ========== 2. 局部计算 ==========
node_positions = [(-2, 3), (0, 3), (2, 3)]
node_colors = ['orange', 'orange', 'orange']
node_labels = ['节点 1\n前向/反向', '节点 2\n前向/反向', '节点 3\n前向/反向']
nodes = []
for i, (x, y) in enumerate(node_positions):
    # 圆角矩形
    rect = patches.FancyBboxPatch(
        (x-0.9, y-0.6), 1.8, 1.2,
        boxstyle="round,pad=0.1", linewidth=1.5, edgecolor='black',
        facecolor=node_colors[i], alpha=0.8
    )
    ax.add_patch(rect)
    ax.text(x, y, node_labels[i], ha='center', va='center', fontsize=14)
    nodes.append((x, y))

# 分片到节点的箭头
for (sx, sy), (nx, ny) in zip(shard_positions, node_positions):
    ax.annotate("", xy=(nx, ny+0.6), xytext=(sx, sy-0.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# 步骤标签 (2) —— 向左移动，避免与方框重叠
ax.text(-3.2, 3.9, '(2) 局部计算', fontsize=14, fontweight='bold', color='darkorange')

# ========== 3. 跨节点通信与聚合 ==========
ps_x, ps_y = 0, 0.8
ps_width, ps_height = 2.2, 1.4
ps_rect = patches.Rectangle(
    (ps_x - ps_width/2, ps_y - ps_height/2), ps_width, ps_height,
    linewidth=1.5, edgecolor='black', facecolor='lightblue', alpha=0.8
)
ax.add_patch(ps_rect)
ax.text(ps_x, ps_y, '参数服务器\n聚合全局梯度', ha='center', va='center', fontsize=14)

# 上传梯度箭头（从节点到参数服务器）
offsets = [-0.2, 0.1, 0.2]  # 左右偏移以显示平行箭头
for i, (nx, ny) in enumerate(nodes):
    # 上传（实线箭头，方向向下）
    ax.annotate("", xy=(ps_x + offsets[i], ps_y + ps_height/2),
                xytext=(nx + offsets[i], ny - 0.7),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    # 下发（虚线箭头，方向向上），用不同的偏移避免重叠
    ax.annotate("", xy=(nx - offsets[i], ny - 0.7),
                xytext=(ps_x - offsets[i], ps_y + ps_height/2),
                arrowprops=dict(arrowstyle='->', color='blue', lw=1.5, linestyle='dashed'))

# 在第一个箭头旁边添加文字标注
ax.text(-2.2, 2.0, '梯度', fontsize=14, color='red')
ax.text(-0.6, 1.85, '更新', fontsize=14, color='blue')

# 步骤标签 (3)
ax.text(-2.2, 1.6, '(3) 跨节点通信与聚合', fontsize=14, fontweight='bold', color='darkblue', ha='left')

# ========== 4. 模型更新与迭代 ==========
# 从参数服务器指向数据源的虚线曲线箭头
ax.annotate("", xy=(data_x, data_y-0.8), xytext=(ps_x, ps_y+ps_height/2),
            arrowprops=dict(arrowstyle='->', color='purple', lw=2, linestyle='dashed',
                            connectionstyle="arc3,rad=0.3"))
ax.text(0.5, 4.0, '下一轮迭代', fontsize=14, color='purple', rotation=20)

# 步骤标签
ax.text(1.2, 0.75, '(4) 模型更新与迭代', fontsize=14, fontweight='bold', color='purple')

# 全局模型标注
ax.text(ps_x, ps_y-0.9, '全局模型', fontsize=14, color='gray', ha='center')

# 调整图形并保存
plt.tight_layout()
plt.savefig('distributed_training.png', dpi=150, bbox_inches='tight')
print('saved to distributed_training.png')
