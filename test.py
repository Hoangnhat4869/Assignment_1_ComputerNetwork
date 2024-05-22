from math import comb

class Solution:
    def numOfWays(self, nums: list[int]) -> int:
        return (self.numOfWaysRec(nums) - 1)%1000000007

    def numOfWaysRec(self, nums: list[int]) -> int:
        if len(nums) < 3:
            return 1
        left = list()
        right = list()
        for i in range(1, len(nums)):
            if (nums[i] < nums[0]):
                left.append(nums[i])
            elif (nums[i] > nums[0]):
                right.append(nums[i])

        return (self.numOfWaysRec(left) * self.numOfWaysRec(right) * comb(len(left) + len(right), len(left)))


if __name__ == '__main__':
    sol = Solution()
    nums = [10,23,12,18,4,29,2,8,41,31,25,21,14,35,26,5,19,43,22,37,9,20,44,28,1,39,30,38,36,6,13,16,27,17,34,7,15,3,11,24,42,33,40,32]
    print(sol.numOfWays(nums))