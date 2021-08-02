"""
测试工具集: 
"""

from __future__ import absolute_import, division, print_function, annotations

import os
import sys
from typing import List

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.extend([SRC_DIR])

from leetcode.commons.quick_sort import partition2


class Solution:

    def findKthLargest(self, nums: List[int], k: int) -> int:
        N = len(nums)

        # 使用正向排序的思路, 需要将 "第 k 大" 问题转换为 "第 k 小" 问题
        # 这里需要特别注意边界条件
        k = N - k

        l, r = 0, N - 1
        while True:
            p = partition2(nums, l, r)
            if p == k:
                return nums[p]
            elif p > k:
                r = p - 1
            else:
                l = p + 1


if __name__ == "__main__":
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    exp_r = 5

    sol = Solution()
    result = sol.findKthLargest(nums, k)

    print(f"expect: {exp_r}, result: {result}")

    assert result == exp_r, f"{result} != {exp_r}"
