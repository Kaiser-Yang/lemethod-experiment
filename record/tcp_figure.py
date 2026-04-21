import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# 设置中文字体（如果需要中文标注，请确保系统有中文字体）
plt.rcParams["font.sans-serif"] = [ "WenQuanYi Zen Hei" ]


# 图1：TCP拥塞控制在FL中的问题示意图
def fig_tcp_problems():
    _, axes = plt.subplots(2, 2, figsize=(12, 10))

    # (a) 理想情况：节点交错完成
    ax1 = axes[0, 0]
    ax1.set_title("(a) 理想情况：节点交错完成", fontsize=14)
    workers = ["W1", "W2", "W3", "W4", "W5"]
    times = [0.2, 0.5, 0.8, 1.1, 1.4]
    ax1.barh(workers, times, color="lightgreen", edgecolor="black")
    ax1.set_xlabel("完成时间 (s)")
    ax1.set_xlim(0, 1.8)
    ax1.axvline(x=1.4, linestyle="--", color="red", label="聚合等待时间")
    ax1.legend()

    # (b) 拥塞情况：节点同时完成
    ax2 = axes[0, 1]
    ax2.set_title("(b) 拥塞情况：节点同时完成", fontsize=14)
    workers = ["W1", "W2", "W3", "W4", "W5"]
    times = [1.0, 1.0, 1.0, 1.0, 1.0]
    ax2.barh(workers, times, color="salmon", edgecolor="black")
    ax2.set_xlabel("完成时间 (s)")
    ax2.set_xlim(0, 1.5)
    ax2.axvline(x=1.0, linestyle="--", color="red", label="聚合等待时间")
    ax2.legend()

    # (c) TCP窗口震荡
    ax3 = axes[1, 0]
    ax3.set_title("(c) TCP窗口震荡现象", fontsize=14)
    rounds = list(range(1, 21))
    # 模拟窗口震荡
    window = []
    w = 10
    for i in range(20):
        if i % 5 == 0 and i > 0:
            w = max(2, w // 2)  # 模拟拥塞减半
        else:
            w = min(20, w + 1)
        window.append(w)
    ax3.plot(rounds, window, "b-o", markersize=4, linewidth=1.5)
    ax3.set_xlabel("通信轮次")
    ax3.set_ylabel("TCP拥塞窗口 (MSS)")
    ax3.set_ylim(0, 25)
    ax3.grid(True, linestyle="--", alpha=0.5)
    ax3.axhline(y=10, linestyle=":", color="gray", label="理想稳定窗口")
    ax3.legend()

    # (d) 聚合时间波动
    ax4 = axes[1, 1]
    ax4.set_title("(d) 聚合时间剧烈波动", fontsize=14)
    rounds = list(range(1, 21))
    # 模拟聚合时间波动
    agg_time = [
        0.5,
        0.6,
        0.55,
        0.8,
        1.2,
        0.9,
        1.5,
        0.7,
        0.65,
        1.1,
        1.3,
        0.85,
        0.9,
        1.4,
        1.6,
        1.0,
        0.95,
        1.2,
        1.1,
        1.3,
    ]
    ax4.plot(rounds, agg_time, "r-s", markersize=4, linewidth=1.5)
    ax4.set_xlabel("通信轮次")
    ax4.set_ylabel("聚合时间 (s)")
    ax4.grid(True, linestyle="--", alpha=0.5)
    ax4.axhline(y=np.mean(agg_time), linestyle="--", color="blue", label="平均时间")
    ax4.legend()

    plt.tight_layout()
    plt.savefig("tcp_problems.pdf", format="pdf", dpi=300, bbox_inches="tight")
    print("已生成 tcp_problems.pdf")


# 图2：算法总体框架图
def fig_algorithm_framework():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # 定义模块位置和大小
    modules = {
        "time_meas": (1, 6, 2.5, 1.2),
        "stat_maintain": (4, 6, 2.5, 1.2),
        "anomaly_detect": (7, 6, 2.5, 1.2),
        "dynamic_thresh": (10, 6, 2.5, 1.2),
        "adjust": (5.5, 3, 3, 1.2),
        "output": (5.5, 0.5, 3, 1),
    }

    # 绘制模块
    colors = {
        "time_meas": "#A8D5E5",
        "stat_maintain": "#FFD966",
        "anomaly_detect": "#F4A582",
        "dynamic_thresh": "#92C5DE",
        "adjust": "#B5E3B5",
        "output": "#D3D3D3",
    }

    for name, (x, y, w, h) in modules.items():
        rect = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.1",
            facecolor=colors[name],
            edgecolor="black",
            linewidth=1.5,
        )
        ax.add_patch(rect)

    # 定义每个模块对应的文字
    text_blocks = {
        "time_meas": "时间测量模块\n记录聚合开始/结束时间\n计算 T_cur",
        "stat_maintain": "统计维护模块\n滑动窗口存储历史耗时\nEMA更新 E[T], 计算σ",
        "anomaly_detect": "异常检测模块\n3-sigma原则\n|T_cur - E[T]| > 3σ",
        "dynamic_thresh": "动态阈值模块\n阈值 = δ·(E[T]²/T_init)\n判断是否显著变化",
        "adjust": "调节决策模块\nAIAD策略: ΔR = ±1",
        "output": "输出模块\n输出: 更新后的并发接收数 R",
    }

    for name, (x, y, w, h) in modules.items():
        text = text_blocks[name]
        ax.text(
            x + w / 2,
            y + h / 2,
            text,
            ha="center",  # 水平居中
            va="center",  # 垂直居中
            fontsize=12,
            fontweight="bold" if "模块" in text else "normal",
        )

    # 绘制箭头（调整箭头大小、起止位置和弧度）
    def draw_arrow(start_rect, end_rect, ax, direction="right", rad=0.0):
        """绘制箭头，起点从一个矩形的边缘出发，到目标矩形的边缘结束"""
        x1, y1, w1, h1 = start_rect
        x2, y2, w2, h2 = end_rect

        # 增大箭头和箭头头部的大小
        props = dict(
            arrowstyle="->,head_width=0.5,head_length=0.8",
            lw=2,
            color="black",
            shrinkA=10,
            shrinkB=10,
        )

        if direction == "right":  # 从右边缘到左边缘
            start = (x1 + w1, y1 + h1 / 2)  # 起点：矩形右边缘中点
            end = (x2, y2 + h2 / 2)  # 终点：矩形左边缘中点
        elif direction == "down":  # 从下边缘到上边缘
            start = (x1 + w1 / 2, y1)  # 起点：矩形下边缘中点
            end = (x2 + w2 / 2, y2 + h2)  # 终点：矩形上边缘中点
        elif direction == "skip1": 
            start = (x1 + w1 / 2, y1)
            end = (x2+w2, y2 + h2 / 2)
            props["connectionstyle"] = f"arc3,rad={rad}"
        elif direction == 'skip2':
            start = (x1 + w1 / 2, y1)
            end = (x2, y2 + h2 / 2)
            props["connectionstyle"] = f"arc3,rad={rad}"
        else:
            start, end = 0, 0

        ax.annotate("", xy=end, xytext=start, arrowprops=props)

    # 时间测量 -> 统计维护
    draw_arrow(modules["time_meas"], modules["stat_maintain"], ax, direction="right")
    # 统计维护 -> 异常检测
    draw_arrow(
        modules["stat_maintain"], modules["anomaly_detect"], ax, direction="right"
    )
    # 异常检测 -> 动态阈值
    draw_arrow(
        modules["anomaly_detect"], modules["dynamic_thresh"], ax, direction="right"
    )
    # 动态阈值 -> 调节决策
    draw_arrow(
        modules["dynamic_thresh"], modules["adjust"], ax, direction="skip1", rad=-0.3
    )
    # 异常检测 -> 输出
    draw_arrow(
        modules["anomaly_detect"], modules["output"], ax, direction="skip2", rad=0.6
    )
    # 调节决策 -> 输出
    draw_arrow(modules["adjust"], modules["output"], ax, direction="down")

    # 标注异常跳过分支
    ax.text(4.8, 4.8, "异常值则跳过", fontsize=14, color="black")

    plt.tight_layout()
    plt.savefig(
        "algorithm_overview.pdf",
        format="pdf",
        dpi=300,
        bbox_inches="tight",
    )
    print("已生成 algorithm_overview.pdf")


if __name__ == "__main__":
    fig_tcp_problems()
    fig_algorithm_framework()
