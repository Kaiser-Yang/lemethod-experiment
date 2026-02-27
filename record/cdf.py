#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
绘制多组实验聚合时间的累积分布函数（CDF）图，输出PNG格式。
用法: python plot_cdf.py 文件1 文件2 ... -o output.png [--skip-last] [--labels L1 L2 ...]
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']

def read_times(file_path, skip_last=True):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    if skip_last:
        lines = lines[:-1]
    return [float(line) for line in lines]

def main():
    parser = argparse.ArgumentParser(description='绘制多组实验聚合时间的CDF图')
    parser.add_argument('files', nargs='+', help='实验数据文件路径')
    parser.add_argument('-o', '--output', default='cdf.png', help='输出PNG文件名')
    parser.add_argument('--no-skip-last', dest='skip_last', action='store_false',
                        help='不跳过最后一行（若文件中无总耗时行）')
    parser.add_argument('--labels', nargs='*', help='图例标签')
    parser.add_argument('--colors', nargs='*', help='线条颜色')
    parser.add_argument('--linestyles', nargs='*', help='线条样式')
    parser.add_argument('--xlabel', default='聚合时间（秒）', help='X轴标签')
    parser.add_argument('--ylabel', default='累积概率', help='Y轴标签')
    parser.add_argument('--figsize', nargs=2, type=float, default=[8, 6], help='图表尺寸')
    parser.add_argument('--dpi', type=int, default=300, help='PNG分辨率')
    args = parser.parse_args()

    num_files = len(args.files)
    if args.labels and len(args.labels) != num_files:
        parser.error("图例标签数量必须与文件数一致")

    all_times = [read_times(f, args.skip_last) for f in args.files]

    plt.figure(figsize=args.figsize, dpi=args.dpi)
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    default_linestyles = ['-', '--', '-.', ':']

    for i, times in enumerate(all_times):
        label = args.labels[i] if args.labels else os.path.splitext(os.path.basename(args.files[i]))[0]
        color = args.colors[i] if args.colors and i < len(args.colors) else default_colors[i % len(default_colors)]
        linestyle = args.linestyles[i] if args.linestyles and i < len(args.linestyles) else default_linestyles[i % len(default_linestyles)]
        ecdf = ECDF(times)
        x = np.sort(times)
        y = ecdf(x)
        plt.plot(x, y, color=color, linestyle=linestyle, linewidth=1.5, label=label, drawstyle='steps-post')

    plt.xlabel(args.xlabel, fontsize=12)
    plt.ylabel(args.ylabel, fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(args.output, dpi=args.dpi, format='png')
    print(f"CDF图已保存至 {args.output}")

if __name__ == '__main__':
    main()
