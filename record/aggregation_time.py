#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
绘制多组实验的每轮聚合时间折线图，输出PNG格式。
用法: python plot_aggregation_times.py 文件1 文件2 ... -o output.png [--num-rounds N] [--skip-last] [--labels L1 L2 ...]
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
def read_times(file_path, num_rounds=None, skip_last=True):
    """
    读取文件中的每轮耗时。
    参数:
        file_path: 文件路径
        num_rounds: 指定轮数，若为None则自动推断
        skip_last: 是否跳过最后一行（总耗时）
    返回:
        list of float, 每轮耗时
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    if skip_last:
        lines = lines[:-1]
    if num_rounds is not None:
        lines = lines[:num_rounds]
    return [float(line) for line in lines]

def main():
    parser = argparse.ArgumentParser(description='绘制多组实验聚合时间折线图')
    parser.add_argument('files', nargs='+', help='实验数据文件路径')
    parser.add_argument('-o', '--output', default='aggregation_times.png', help='输出PNG文件名')
    parser.add_argument('--num-rounds', type=int, default=100, help='总轮数（默认100）')
    parser.add_argument('--no-skip-last', dest='skip_last', action='store_false',
                        help='不跳过最后一行（若文件中无总耗时行）')
    parser.add_argument('--labels', nargs='*', help='图例标签，数量需与文件数一致')
    parser.add_argument('--colors', nargs='*', help='线条颜色')
    parser.add_argument('--linestyles', nargs='*', help='线条样式')
    parser.add_argument('--xlabel', default='训练轮次', help='X轴标签')
    parser.add_argument('--ylabel', default='聚合时间（秒）', help='Y轴标签')
    parser.add_argument('--figsize', nargs=2, type=float, default=[10, 6], help='图表尺寸 (宽 高)')
    parser.add_argument('--dpi', type=int, default=300, help='输出PNG的分辨率')
    args = parser.parse_args()

    num_files = len(args.files)
    if args.labels and len(args.labels) != num_files:
        parser.error("图例标签数量必须与文件数一致")

    # 读取数据
    all_times = [read_times(f, args.num_rounds, args.skip_last) for f in args.files]
    max_rounds = max(len(t) for t in all_times)
    x = np.arange(1, max_rounds + 1)

    plt.figure(figsize=args.figsize, dpi=args.dpi)
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    default_linestyles = ['-', '--', '-.', ':']

    for i, times in enumerate(all_times):
        label = args.labels[i] if args.labels else os.path.splitext(os.path.basename(args.files[i]))[0]
        color = args.colors[i] if args.colors and i < len(args.colors) else default_colors[i % len(default_colors)]
        linestyle = args.linestyles[i] if args.linestyles and i < len(args.linestyles) else default_linestyles[i % len(default_linestyles)]
        plt.plot(x[:len(times)], times, color=color, linestyle=linestyle, linewidth=1.5, label=label)

    plt.xlabel(args.xlabel, fontsize=12)
    plt.ylabel(args.ylabel, fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(args.output, dpi=args.dpi, format='png')
    print(f"PNG图已保存至 {args.output}")

if __name__ == '__main__':
    main()
