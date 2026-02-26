import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(-5, 5)
ax.set_ylim(-1, 6)
ax.axis('off')

# 定义辅助函数：绘制圆柱（用于表示本地数据集）
def draw_cylinder(ax, center_x, center_y, width, height, color='lightgray', edgecolor='black', label=''):
    rect = patches.Rectangle(
        (center_x - width/2, center_y - height/2), width, height,
        linewidth=1.2, edgecolor=edgecolor, facecolor=color, alpha=0.8
    )
    ax.add_patch(rect)
    # 顶部椭圆
    top_ellipse = patches.Ellipse(
        (center_x, center_y + height/2), width, height/3,
        linewidth=1.2, edgecolor=edgecolor, facecolor=color, alpha=0.8
    )
    ax.add_patch(top_ellipse)
    # 底部椭圆
    bottom_ellipse = patches.Ellipse(
        (center_x, center_y - height/2), width, height/3,
        linewidth=1.2, edgecolor=edgecolor, facecolor=color, alpha=0.8
    )
    ax.add_patch(bottom_ellipse)
    if label:
        ax.text(center_x, center_y, label, ha='center', va='center', fontsize=9)

# ========== 参数服务器 ==========
ps_x, ps_y = 0, 4.5
ps_width, ps_height = 3.0, 1.5
ps_rect = patches.FancyBboxPatch(
    (ps_x - ps_width/2, ps_y - ps_height/2), ps_width, ps_height,
    boxstyle="round,pad=0.2", linewidth=2, edgecolor='navy', facecolor='lightblue', alpha=0.9
)
ax.add_patch(ps_rect)
ax.text(ps_x, ps_y + 0.2, '参数服务器', ha='center', va='center', fontsize=12, fontweight='bold')
ax.text(ps_x, ps_y - 0.2, '加权聚合: $W_{t+1} = \\sum_{k=1}^{N} \\frac{n_k}{n} w_{t+1}^{(k)}$', 
        ha='center', va='center', fontsize=9)
ax.text(ps_x, ps_y - 0.5, '全局更新 $W_{t+1}$', 
        ha='center', va='center', fontsize=10, fontweight='bold')

# ========== 工作节点 ==========
node_positions = [(-2.5, 2), (0, 2), (2.5, 2)]
node_colors = ['lightcoral', 'lightcoral', 'lightcoral']
node_labels = ['工作节点 1', '工作节点 2', '工作节点 3']
opt_labels = ['多步优化\n得到 $w_{t+1}^{(1)}$', '多步优化\n得到 $w_{t+1}^{(2)}$', '多步优化\n得到 $w_{t+1}^{(3)}$']
nodes = []
for i, (x, y) in enumerate(node_positions):
    rect = patches.FancyBboxPatch(
        (x - 1.2, y - 0.7), 2.4, 1.4,
        boxstyle="round,pad=0.1", linewidth=2, edgecolor='darkred', facecolor=node_colors[i], alpha=0.8
    )
    ax.add_patch(rect)
    ax.text(x, y + 0.2, node_labels[i], ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(x, y - 0.3, opt_labels[i], ha='center', va='center', fontsize=9)
    nodes.append((x, y))

# ========== 本地数据集（每个节点下方） ==========
dataset_positions = [(-2.5, 0.5), (0, 0.5), (2.5, 0.5)]
dataset_labels = ['$\\mathcal{D}_1$', '$\\mathcal{D}_2$', '$\\mathcal{D}_3$']
for i, (x, y) in enumerate(dataset_positions):
    draw_cylinder(ax, x, y, width=1.0, height=0.5, color='lightgreen', label=dataset_labels[i])

# ========== 数据集与工作节点的连接线（虚线） ==========
for i in range(len(node_positions)):
    x_ds, y_ds = dataset_positions[i]
    x_node, y_node = node_positions[i]
    # 从数据集顶部 (y_ds + height/2) 到工作节点底部 (y_node - height_node/2)
    ax.plot([x_ds, x_node], [y_ds + 0.25, y_node - 0.7],
            linestyle='--', color='gray', linewidth=1, alpha=0.7)

# ========== 步骤 1：广播全局模型和超参数 ==========
offsets = [-0.2, 0.1, 0.2]  # 箭头水平偏移以避免重叠
for i, (nx, ny) in enumerate(nodes):
    # 广播（蓝色箭头从服务器指向节点）
    ax.annotate("", xy=(nx + offsets[i], ny + 0.8), xytext=(ps_x + offsets[i], ps_y - 0.8),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    # 上传（红色箭头从节点指向服务器）
    ax.annotate("", xy=(ps_x - offsets[i], ps_y - 0.8), xytext=(nx - offsets[i], ny + 0.8),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
# 广播标注
ax.text(-1.5, 3.2, '① 广播 $W_t$, 本地轮数 $K$', fontsize=10, color='blue',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='blue'))

# ========== 步骤 2：本地多步优化（已在节点内部标注） ==========
ax.text(-3.8, 2.2, '② 本地多步优化', fontsize=10, color='darkred', fontweight='bold')

# ========== 步骤 3：上传本地模型参数 ==========
# 上传标注
ax.text(2.0, 3.5, '③ 上传 $w_{t+1}^{(k)}$', fontsize=10, color='red',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='red'))

# ========== 步骤 4：加权聚合与更新（已在服务器内部显示） ==========
ax.text(ps_x + 2.0, ps_y, '④ 加权聚合\n得到 $W_{t+1}$', fontsize=10, color='navy', fontweight='bold',
        ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='navy'))

# ========== 步骤 5：循环迭代 ==========
# 从参数服务器指向自身的弯曲虚线箭头（表示下一轮）
ax.annotate("", xy=(ps_x + 1.2, ps_y + 1.2), xytext=(ps_x + 2.5, ps_y + 0.5),
            arrowprops=dict(arrowstyle='->', color='purple', lw=2, linestyle='dashed',
                            connectionstyle="arc3,rad=0.4"))
ax.text(ps_x + 1.8, ps_y + 1., '⑤ 下一轮迭代\n直至收敛', fontsize=10, color='purple',
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='purple'))

# 停止条件标注
ax.text(ps_x + 3.0, ps_y - 1.0, '停止条件：\n目标精度 / 最大轮数', fontsize=9, color='gray',
        bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='gray'))

# 调整布局并保存
plt.tight_layout()
plt.savefig('fed_avg_training.png', dpi=150, bbox_inches='tight')
plt.show()
