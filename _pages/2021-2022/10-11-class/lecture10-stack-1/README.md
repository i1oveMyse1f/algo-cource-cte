---
layout: lecture
title:  "Стеки, очереди и деки - 1"
author: i_love_myself
categories: [ useful ]
youtube: s_KS9AvCYJA
toc: true
---

## Стек

### ПСП
> Скобочная последовательность называется правильной в одном из трёх случаев: <br> 1. Пустая последовательность является ПСП. <br> 2. Если A - ПСП, то (A), [A] и {A} - ПСП. <br> 3. Если A и B - ПСП, то их конкатенация AB - тоже ПСП <br> По данной последовательности скобок s необходимо понять, является ли она ПСП.

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

Дек - это ещё более продвинутая структура, чем стек или очередь. Она умеет в 6 операций:

1. Добавить элемент в конец или в начало дека
1. Удалить элемент из конца или начала дека
1. Узнать, какие элементы лежат в конце или начале дека

Иными словами, дек - это "двусторонняя очередь".

### Зачем же нужна такая структура?

Всё ради того, чтобы решить буквально единственную, но периодически встречающуюся задачу:

> Для каждого подотрезка [l; l+k-1] (с фиксированным k, называемым размером окна) необходимо найти минимум на этом отрезке.

### Решение

<details markdown="1">

Будем хранить в деке наибольшую возрастающую последовательность элементов на отрезке [r-k+1; r], которая начинается с минимального элемента на отрезке [r-k+1; r] и оканчивается в r-м. Например, если k=3, массив равен [1, 3, 2, 4, 1]. Тогда мы должны научиться вычислять следующее:

* r=1: [1]
* r=2: [1, 3]
* r=3: [1, 2]
* r=4: [2, 4]
* r=5: [1]

По определению нашего инварианта минимальный элемент находится в начале  поддерживаемого дека. Осталось, собственно понять, как его поддерживать.

1. Пусть мы знаем, чему равен дек для отрезка [r-k; r-1]. Как его обновить для отрезка [r-l+1; r]?
1. Надо удалить с конца дека все элементы, которые меньше a[r].
1. Если в начале дека стоит элемент, который стоит в исходом массиве на позиции r-k, то его надо удалить (так как он больше не в окне размера k). Соответственно, в деке надо хранить не значения элементов, а их индексы в исходом массиве.

</details>

### Код

<details markdown="1">

```cpp
#include <iostream>
#include <deque>
#include <vector>

using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (int& x : a) {
        cin >> x;
    }
    deque<int> d; // [indexes]
    for (int r = 0; r < n; ++r) {
        if (!d.empty() && d.front() == r - k)
            d.pop_front();
        while (!d.empty() && a[d.back()] > a[r])
            d.pop_back();
        d.push_back(r);

        if (r >= k - 1)
            cout << a[d.front()] << '\n';
    }
}
```

</details>
