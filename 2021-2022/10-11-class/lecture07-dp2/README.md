# ДП по подотрезкам

## Получи ПСП

> Дана последовательсность из скобок длины n. Необходимо удалить как можно меньше скобок так, чтобы получилась правильная скобочная последовательность.

<details>
<summary> Код </summary>

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

bool is_match(char a, char b) {
    return a == '(' && b == ')' || a == '[' && b == ']';
}

int main() {
    string s;
    cin >> s;
    int n = s.size();
    vector<vector<int>> dp(n + 1, vector<int>(n + 1));

    // ()[]

    for (int len = 1; len <= n; ++len) {
        for (int i = 0, j = len - 1; j < n; ++i, ++j) {
            if (len == 1) {
                dp[i][j] = 0;
            }
            else if (len == 2) {
                if (is_match(s[i], s[j])) {
                    dp[i][j] = 2;
                }
                else {
                    dp[i][j] = 0;
                }
            }
            else {
                dp[i][j] = 0;
                if (is_match(s[i], s[j]))
                    dp[i][j] = dp[i + 1][j - 1] + 2;
                for (int m = i + 1; m <= j - 1; ++m)
                    dp[i][j] = max(dp[i][j], dp[i][m] + dp[m + 1][j]);
            }
        }
    }

    cout << dp[0][n - 1];
}
```

</details>

## Количество бинарных деревьев поиска

> Дан набор целых чисел a длины n. Необходимо вычислить, какое количество различных бинарных деревьев поиска можно построить, используя все числа из набора. <br> Напомню, что _бинарным деревом поиска_ может называеться дерево, у которого удовлетворяющее двум ограничениям: <br> 1. У каждой вершины не больше двух детей <br> 2. Если в вершине стоит число x, то в левом поддереве все числа должны быть строго меньше x, а в правом - не меньше x.

<details>
<summary> Код </summary>

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

const int INF = 2e9;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a)
        cin >> x;

    vector<int> p(n, -1);
    vector<int> dp(n + 1, INF);
    vector<int> ind_dp(n + 1, -1);
    dp[0] = -INF;

    for (int i = 0; i < n; ++i) {
        int l = 0, r = n + 1;
        // dp[l]: dp[l] < a[i] и l - max

        while (r - l > 1) { // [l; r)
            int m = (r + l) / 2;
            if (dp[m] < a[i])
                l = m;
            else
                r = m;
        }

        dp[l + 1] = a[i];
        ind_dp[l + 1] = i;
        p[i] = ind_dp[l];
    }

    int i = 1;
    while (dp[i + 1] != INF)
        ++i;

    i = ind_dp[i]; // индекс ( из a) последнего элемента самой длинной ВП
    vector<int> ans;
    ans.push_back(a[i]);
    while (p[i] != -1) {
        i = p[i];
        ans.push_back(a[i]);
    }

    reverse(ans.begin(), ans.end());
    for (int x : ans)
        cout << x << ' ';
}
```

</details>