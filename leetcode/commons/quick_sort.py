"""
测试工具集: 快速排序算法
"""

from __future__ import absolute_import, division, print_function, annotations

import os
import sys
from typing import List, Optional
from queue import Queue
from random import randint

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.extend([SRC_DIR])


def partition(nums: List[int], l: int = 0, r: int = -1) -> int:
    """快排分段算法

    该算法代码来源于算法导论给出的伪代码. 

    该算法的核心是, 在内部的 For 循环中, 将数组分成四个部分:
    * l <= k < i: A[k] <= pivot
    * i <= k < j: A[k] > pivot
    * j : 当前正在处理的变量
    * j + 1 <= k < r: 待处理区域

    Args:
        nums (List[int]): 原始数组
        l (int, optional): 正在处理的数组的左边界(含). Defaults to 0.
        r (int, optional): 正在处理的数组的右边界(含). Defaults to -1.

    Returns:
        int: 枢纽元素对应的索引, 满足枢纽元素左边的元素全部小于枢纽元素, 右边元素全部大于枢纽元素
    """
    pivot = nums[r]

    i = l - 1
    for j in range(l, r):
        if nums[j] <= pivot:
            i += 1
            if i != j:
                nums[i], nums[j] = nums[j], nums[i]

    nums[i + 1], nums[r] = nums[r], nums[i + 1]
    return i + 1


def partition2(nums: List[int], l: int = 0, r: int = -1) -> int:
    """快排分段算法

    该算法思想来源于 知乎 [深入理解快速排序（quciksort）](https://zhuanlan.zhihu.com/p/63202860).

    其核心思想是: 设置两个指针 i 和 j, 分别 向右 和 向左 扫描. 
    
    理解该算法, 重点需要理解里面存在 "空置" 的概念, 而且 "空置" 位置还在来回的切换. 举例而言:
    * 当从左往右扫描时, A[j] 位置是空置的, 所以可以通过 A[j] = A[i] 将大于枢纽值的元素移动到右边, 当放置完成时, A[i] 位置又被 "空置" 了
    * 当从右往左扫描时, A[i] 位置是空置的, 所以可以通过 A[i] = A[j] 来将小于枢纽值的元素移到左边 (同理, 新的 A[j] 位置又被 "空置")

    Args:
        nums (List[int]): 原始数组
        l (int, optional): 正在处理的数组的左边界(含). Defaults to 0.
        r (int, optional): 正在处理的数组的右边界(含). Defaults to -1.

    Returns:
        int: 枢纽元素对应的索引, 满足枢纽元素左边的元素全部小于枢纽元素, 右边元素全部大于枢纽元素
    """
    # nums[r] 元素被当做枢纽元素, 其值已暂存, 对应位置可以理解为空置
    pivot = nums[r]

    i, j = l, r

    while i < j:
        # 1. 从左往右扫描, 找到大于枢纽元素的值
        while i < j and nums[i] <= pivot:
            i += 1

        # 1-1. 从左向右扫描时, j 位置相当于已经空置(首次循环对应枢纽元素的位置)
        # 当 nums[i] 放置到 j 位置后, i 位置已空置, 可用于后续处理
        nums[j] = nums[i]

        # 2. 从右往左扫描, 找到小于枢纽元素的值
        while i < j and nums[j] > pivot:
            j -= 1

        # 2.1 如前面描述, i 位置已经空置, 可以用于保存比枢纽值小的元素
        # 当 nums[j] 放置到 i 位置后, j 位置空置, 可用于后续处理
        nums[i] = nums[j]

    nums[i] = pivot
    return i


def quick_sort(nums: List[int], l: Optional[int] = 0, r: Optional[int] = None):
    if r is None:
        r = len(nums)

    if l >= r:
        return nums

    p = partition2(nums, l, r)

    print(p, nums)

    quick_sort(nums, l, p - 1)
    quick_sort(nums, p + 1, r)

    return nums


def quick_sort_iter(
    nums: List[int],
    l: Optional[int] = 0,
    r: Optional[int] = None,
) -> List[int]:
    """迭代方式实现快速排序

    原始的快速排序使用了递归调用的方式, 可能造成栈空间溢出.
    此处修改为迭代方式, 迭代方式使用了队列来记录每次迭代的参数, 避免了递归调用时需要将复杂的程序现场压栈带来的栈空间浪费
    Args:
        nums (List[int]): 原始待排序数组
        l (int, optional): 数组的左边界. Defaults to 0.
        r (int, optional): 数组的右边届. Defaults to -1.

    Returns:
        List[int]: 排序后的数组

    **注意**:
    * 该算法使用了本地排序方式, 直接对原数组进行修改
    """
    if r is None:
        r = len(nums)

    if l >= r:
        return nums

    q = Queue()
    q.put((l, r))

    while not q.empty():
        print(list(q.queue))

        l, r = q.get()

        # 每次确定一个数的位置
        p = partition2(nums, l, r)

        # print(p, nums)

        if p - 1 > l:
            q.put((l, p - 1))
        if p + 1 < r:
            q.put((p + 1, r))

    return nums


if __name__ == "__main__":
    # 1. 示例数组
    # nums = [3, 2, 1, 5, 6, 4]

    # 2. 随机数组
    nums = [randint(0, 100) for _ in range(30)]

    # 3. 极端情况, 递增数组
    # nums = sorted(nums)

    # 4. 极端情况, 递减数组
    # nums = sorted(nums, reverse=True)

    print(f"before sorted: {nums}")

    exp_r = sorted(nums)

    result = quick_sort_iter(nums, 0, len(nums) - 1)

    print(f"after sorted: {result}")

    assert exp_r == result, f"{exp_r} != {result}"
