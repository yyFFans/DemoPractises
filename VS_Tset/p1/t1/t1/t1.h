#pragma once
#include <vector>
#include <iostream>

using std::vector;

class Solution
{ 
    public:
        vector<int> twoSum(vector<int>& nums, int target)
        {
            int i = 0;int j = 0;

            bool found = false;

            vector<int> ret(2);

            vector<int>::iterator pd1;
            vector<int>::iterator pd2;

            for (pd1 = nums.begin(); pd1 != nums.end(); pd1++)
            {
                i++;
                if (target <= i)
                {
                    continue;
                }

                for (pd2 = pd1; pd2 != nums.end(); pd2++)
                {
                    if (target == (*pd1 + *pd2))
                    {
                        found = true;
                        break;
                    }
                    j++;
                }

                if (true == found)
                {
                    break;
                }

                j = 0;
                
            }
            ret[0] = i;
            ret[1] = j;
            return ret;
        }
};