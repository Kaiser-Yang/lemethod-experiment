import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
import matplotlib.pyplot as plt
import numpy as np

# 数据（按比例升序排列）
ratios = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
static = [4240.682, 3538.090, 3291.103, 3472.937, 3552.370,
          3329.377, 3601.908, 3239.656, 3431.546, 3290.089]
dynamic = [4488.734, 3498.226, 3503.869, 3606.440, 3547.754,
           3429.589, 3559.462, 3312.365, 3433.623, 3495.003]
base_static = 14098.513
base_dynamic = 14085.684

plt.figure(figsize=(8,5))
plt.plot(ratios, static, 'o-', color='blue', label='静态')
plt.plot(ratios, dynamic, 's-', color='red', label='动态')
plt.axhline(y=base_static, color='blue', linestyle='--', alpha=0.7, label='静态基准')
plt.axhline(y=base_dynamic, color='red', linestyle='--', alpha=0.7, label='动态基准')
plt.xlabel('链接扩展比率（%）')
plt.ylabel('总耗时（s）')
plt.title('总耗时随链接扩展比率变化图（W=50）')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('sparse.png', dpi=300)
# plt.savefig('sparse.pdf')
print('sparse.png generated')
