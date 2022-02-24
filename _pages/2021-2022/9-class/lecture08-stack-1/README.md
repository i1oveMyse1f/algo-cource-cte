---
layout: lecture
title:  "Стеки, очереди"
author: i_love_myself
categories: [ contest ]
youtube: -TplheGSsp4
toc: true
---

## Стек

### ПСП
> Скобочная последовательность называется правильной в одном из трёх случаев: <br> 1. Пустая последовательность является ПСП. <br> 2. Если A - ПСП, то (A), [A] и {A} - ПСП. <br> 3. Если A и B - ПСП, то их конкатенация AB - тоже ПСП <br> По данной посдеодовательности скобок s необходимо понять, является ли она ПСП.

Когда речь заходит о скобочных последовательностях, то вы сразу должны вспоминать о _балансе_ (нет, не о балансе вселенной).

<details markdown="1">
<summary>Решение</summary>
</details>

<details markdown="1">
<summary>Код</summary>

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

    vector<char> st;
    for (char c : s) {
        if (c == '(' || c == '[')
            st.push_back(c);
        else {
            if (!st.empty() && is_match(st.back(), c)) {
                st.pop_back();
            }
            else {
                cout << "NO";
                return 0;
            }
        }
    }

    if (st.empty())
        cout << "YES";
    else
        cout << "NO";
}
```

</details>

### Про воду
> Дана последовательность a длины n, задающаяя высоту стены в позиции i. Потом полил дождь. Необходимо понять, сколько воды осталось на стенах (её площадь). Здесь будет картинка, но пока её нет.

<details markdown="1">
<summary>Код</summary>

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a)
        cin >> x;

    int ans = 0;
    vector<int> st; // indexes
    for (int i = 0; i < n; ++i) {
        if (st.empty()) {
            st.push_back(i);
            continue;
        }

        while (!st.empty() && a[i] > a[st.back()]) {
            int h0 = a[st.back()];
            st.pop_back();
            if (!st.empty()) {
                int hor = i - st.back() - 1;
                int vert = min(a[st.back()], a[i]) - h0;
                ans += hor * vert;
            }
        }
        st.push_back(i);
    }

    cout << ans;
}
```

</details>

### Ещё одна задача, которая часто встречается

> Дан массив целых чисел a. Для каждоо элемента a[i] необходимо найти ближайший элемент слева, который не превосходит i-го.

## Очередь

> Дана шахматная доска и шахматный конь, который на ней стоит. Необходимо найти минимальное количество ходов для того, чтобы добраться из стартовой клетки в данную.

<details markdown="1">
<summary>Код</summary>

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <queue>

using namespace std;

void check(int i, int j, queue<pair<int, int>>& q, vector<vector<bool>>& used, vector<vector<int>>& f, int d) {
    if (i >= 0 && i < 8 && j >= 0 && j < 8 && !used[i][j]) {
        q.push({ i, j });
        used[i][j] = true;
        f[i][j] = d + 1;
    }
}

int main() {
    char a1;
    int b1;
    char a2;
    int b2;

    cin >> a1 >> b1 >> a2 >> b2; // A8 E3
    a1 -= 'A';
    a2 -= 'A';
    b1 -= 1;
    b2 -= 1;
    // [0; 7], [0; 7]

    queue<pair<int, int>> q;
    q.push({ a1, b1 });
    vector<vector<bool>> used(8, vector<bool>(8));
    used[a1][b1] = true;
    vector<vector<int>> f(8, vector<int>(8));
    f[a1][b1] = 0;

    while (!q.empty()) {
        auto [i, j] = q.front();
        q.pop();

        check(i - 2, j - 1, q, used, f, f[i][j]);
        check(i + 2, j - 1, q, used, f, f[i][j]);
        check(i - 2, j + 1, q, used, f, f[i][j]);
        check(i + 2, j + 1, q, used, f, f[i][j]);
        check(i - 1, j - 2, q, used, f, f[i][j]);
        check(i + 1, j - 2, q, used, f, f[i][j]);
        check(i - 1, j + 2, q, used, f, f[i][j]);
        check(i + 1, j + 2, q, used, f, f[i][j]);
    }

    cout << f[a2][b2];
}
```

</details>

## Дек

1. Минимум в окне
