// t1.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "t1.h"

int main()
{
    using std::cout;
    using std::cin;
    int i = 0;
    int input = 0;
    vector<int> testnums(10);

    for (i = 0; i < 10; i++)
    {
        testnums[i] = i + 2;

    }

    cout << "input a number\n";
    cin >> input;    Solution sol;
    vector<int> ret(2);

    ret = sol.twoSum(testnums, input);

    cout << ret[0] << "," << ret[1] << "\n";

    return 0;
}

