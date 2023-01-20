from typing import List
import sys
from torch import nn
sys.path.append('./nnsnooper')
import pysnooper
import inspect

class Solution:
    def minNumber(self, nums: List[int]) -> str:
        def largerthan(a, b):
            ab = a + b
            ba = b + a
            for i in range(len(ab)):
                if ab[i] > ba[i]:
                    return True
                if ab[i] < ba[i]:
                    return False
                if ab[i] == ba[i]:
                    continue
            return False
        def merge(lsta, lstb):
            ret = list()
            i = 0
            j = 0
            while True:
                if i >= len(lsta) and j >= len(lstb):
                    return ret
                if i >= len(lsta):
                    ret.append(lstb[j])
                    j += 1
                    continue
                if j >= len(lstb):
                    ret.append(lsta[i])
                    i += 1
                    continue
                if largerthan(lsta[i], lstb[j]):
                    ret.append(lstb[j])
                    j += 1
                else:
                    ret.append(lsta[i])
                    i += 1
        def mergesort(lst, ll, rr):
            if rr - ll <= 1:
                return
            else:
                mid = (ll + rr)//2
                mergesort(lst, ll, mid)
                mergesort(lst, mid, rr)
                lst[ll:rr] = merge(lst[ll:mid], lst[mid:rr])

        zerostr = ''
        snums = list()
        for e in nums:
            if e == 0:
                zerostr += '0'
            else:
                snums.append(str(e))
        mergesort(snums, 0, len(snums))
        if len(snums) > 0:
            return zerostr+''.join(snums)
        else:
            return zerostr

solution = Solution()
# print(type(solution))
print(inspect.FrameInfo(inspect.currentframe()))
# print(Solution().minNumber([3,30,34,5,9]))