---
layout: lecture
title:  "ДП по поддеревьям"
author: i_love_myself
categories: [ useful ]
youtube: VN6c12AIPP4
toc: true
---

## Максимальное паросочетание в дереве [neerc](https://neerc.ifmo.ru/wiki/index.php?title=Динамика_по_поддеревьям)

> Необходимо найти максимальное паросочетание в дереве за линейное время.

Паросочетание (англ. matсhing) M в двудольном графе - произвольное множество рёбер графа такое, что никакие два ребра не имеют общей вершины.

<details markdown="1">

<summary>
Решение
</summary>
dp[v][0/1] = размеру максимального паросочетания в поддереве вершины v, если 0 - не взяли v, 1 - взяли v.

Окей, тогда придумаем переходы:

<p align="center">
dp[v][0] = ∑max(dp[u][0], dp[u][1]) по всем u - детям v
</p>

Т.е. из поддерева каждого сына мы выбираем оптимальное паросочетание. А вот в случае, когда мы хотим покрыть v паросочетанием, всё несколько сложнее. Мы должны выбрать сына u, который не был бы покрыт паросочетанием, взять ребро v-u и ещё из остальных поддеревьев взять по оптимальному ответу, т.е. формула будет иметь вид:

dp[v][1] = max<sub>u - сын</sub> dp[u][0] + 1 + ∑<sub>w - cын, u != w</sub>max(dp[w][0], dp[w][1])

Замечаем, что пока это квадрат, но прибавим и вычтем к сумме max(dp[u][0], dp[u][1]). Тогда под суммой окажется значение, равное dp[v][0]. Т.е. получили итоговую формулу вида:

<p align="center">
dp[v][1] = max<sub>u - сын v</sub> dp[v][0] - max(dp[u][0], dp[u][1]) + dp[u][0] + 1
</p>
</details>

<details markdown="1">
<summary>
Код
</summary>

```cpp
void dfs(int v, int p = -1) {
    for (int u : gr[v]) {
        if (u != p) {
            dfs(u, v);
            dp[v][0] += max(dp)
        }
    }
    for (int u : gr[v]) {
        if (u != p) {
            dp[v][1] = max(dp[v][1], dp[v][0] - max(dp[u][0], dp[u][1]) + dp[u][0] + 1);
        }
    }
}
```

</details>

## Диаметр через каждую вершину

> В дереве для каждой вершины необходимо найти самый длинный путь, проходящий через неё за линейное время.

<details markdown="1">
<summary>
Решение
</summary>
Пусть dp[v] - обозначает самый длинный путь в поддереве. Тогда самый длинный путь, проходящий через v строго в поддереве - это dp[u<sub>1</sub>] + dp[u<sub>2</sub>] + 2, где u<sub>1</sub> и u<sub>2</sub> - это максимум и второй максимум по сыновьям v. Главная проблема в том, что пути, проходящие через веришину v могут уходить в наддерево v. Но сейчас разберем и такой случай!

Чтобы решить проблему заметим, что у корня дерева наддерева нет. А ещё заметим, что мы можем выбрать поддерево u корня v, и при переходе в поддерево передать в него значение самого длинного пути в наддереве - dp[w] + 2, где w - это какая-то вершина, отличная от u и имеющая при этом максимальное значение динамики. Ок. То есть, начав с корня, мы можем начитывать пути в наддеревья. Остался один маленький нюанс. Нужно уметь считать dp[w] за $O(1)$, то есть для всех детей искать максимум по сыновьям кроме u.

Для этого трюк: запомним максимум и второй максимум. Если u - это позиция максимума, то ответ - второй максимум, для остальных - позиция максимума. Всё, теперь, собирая решение воедино, мы сможем за линию считать диаметр дерева через каждую вершину.
</details>

<details markdown="1"><summary>Код за $O(n^2)$</summary>

```cpp
#include <iostream>
#include <vector>

using namespace std;

const int N = 1e5;
vector<int> gr[N];
int dp[N];
int h[N];
int ans[N];

void dfs1(int v, int p = -1) {
    h[v] = 0;

    int max1 = 0;
    int max2 = -1;
    for (int u : gr[v]) {
        if (u != p) {
            dfs1(u, v);
            h[v] = max(h[v], h[u] + 1);

            if (h[u] >= max1) {
                max2 = max1;
                max1 = h[u];
            }
            else if (h[u] > max2) {
                max2 = h[u];
            }
        }
    }

    if (max2 == -1) {
        dp[v] = max1 + 1;
    }
    else {
        dp[v] = max1 + max2 + 2;
    }
}

void dfs2(int v, int p = -1, int max_supertree = 0) {
    ans[v] = max(ans[v], h[v] + max_supertree);
    for (int u : gr[v]) {
        if (u != p) {
            int new_max_supertree = max_supertree + 1;
            for (int w : gr[v]) {
                if (w != p && w != u) {
                    new_max_supertree = max(new_max_supertree, h[w] + 2);
                }
            }
            dfs2(u, v, new_max_supertree);
        }
    }
}

int main() {
    int n;
    cin >> n;
    for (int i = 1; i < n; ++i) {
        int a, b;
        cin >> a >> b;
        --a, --b;
        gr[a].push_back(b);
        gr[b].push_back(a);
    }

    dfs1(0);
    dfs2(0);

    for (int i = 0; i < n; ++i) {
        cout << ans[i] << ' ';
    }
}

```

</details>

<details markdown="1"><summary>Код за $O(n)$</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int N = 1e5;
vector<int> gr[N];
int dp[N];
int h[N];
int ans[N];

void dfs1(int v, int p = -1) {
    h[v] = 0;

    int max1 = 0;
    int max2 = -1;
    for (int u : gr[v]) {
        if (u != p) {
            dfs1(u, v);
            h[v] = max(h[v], h[u] + 1);

            if (h[u] >= max1) {
                max2 = max1;
                max1 = h[u];
            }
            else if (h[u] > max2) {
                max2 = h[u];
            }
        }
    }

    if (max2 == -1) {
        dp[v] = max1 + 1;
    }
    else {
        dp[v] = max1 + max2 + 2;
    }
}

void dfs2(int v, int p = -1, int max_supertree = 0) {
    ans[v] = max(ans[v], h[v] + max_supertree);
    vector<int> pref, suf;
    for (int u : gr[v]) {
        if (u != p) {
            pref.push_back(h[u]);
            suf.push_back(h[u]);
        }
    }
    for (int i = 1; i < pref.size(); ++i) {
        pref[i] = max(pref[i - 1], pref[i]);
    }
    for (int i = int(pref.size()) - 2; i >= 0; --i) {
        suf[i] = max(suf[i + 1], suf[i]);
    }

    int i = 0;
    for (int u : gr[v]) {
        if (u != p) {
            int new_max_supertree = max({ max_supertree + 1,
                                          i == 0 ? 0 : pref[i - 1] + 2,
                                          i + 1 == suf.size() ? 0 : suf[i + 1] + 2 });
            dfs2(u, v, new_max_supertree);
            i++;
        }
    }
}

int main() {
    int n;
    cin >> n;
    for (int i = 1; i < n; ++i) {
        int a, b;
        cin >> a >> b;
        --a, --b;
        gr[a].push_back(b);
        gr[b].push_back(a);
    }

    dfs1(0);
    dfs2(0);

    for (int i = 0; i < n; ++i) {
        cout << ans[i] << ' ';
    }
}

```

</details>

## Количество связных подграфов на K вершинах [cf post](https://codeforces.com/blog/entry/63257)

> Дано дерево. Необходимо вычислить количество связных подграфов размера K в нём за время:
> [a] $O(nk^2)$
> [b] $O(nk)$

dp[v][k] - это количество связных подграфов размера k в поддереве v, если v - корень. Тогда научимся считать динамику трюком: сразу считать всю дп сложно и непонятно. Вместо этого будем добавлять по одному поддереву. То есть у нас будут промежуточные состояния: dp[v][k][t], которое означает количество связных подграфов размера k в поддереве v, если v - корень и мы рассмотрели первые t детей v. Переходы будет проще описать кодом:

```cpp
void solve(int v, int p = -1)
{
    dp[v][0] = 1;
    dp[v][1] = 1;

    for (int u : gr[v]) {
        if (u == p) continue;
        solve(u, v);
        
        fill(tmp , tmp + k + 1 , 0);
        for (int i = 1; i <= k; i++)
            for (int j = 0; i + j <= K; j++)
                tmp[i + j] += dp[v][i] * dp[u][j];

        for(int i = 0; i <= min(K , Sub[v]); i++)
            dp[v][i] = tmp[i];
    }
}
```

Это решение за чистый квадрат по k. Оказывается, что если идти до min(k, размера поддерева u), то асимптотика превратится в O(nk). Доказательства я не знаю. Т.е. Решение превратится в такое:

```cpp
void solve(int v, int p = -1)
{
    Sub[v] = 1;
    dp[v][0] = 1;
    dp[v][1] = 1;

    for (int u : gr[v]) {
        if (u == p) continue;
        solve(u, v);

        fill(tmp , tmp + k + 1 , 0);
        for(int i = 1; i <= min(Sub[v] , k); i++)
            for(int j = 0; j <= Sub[u] && i + j <= K; j++)
                tmp[i + j] += dp[v][i] * dp[u][j];
        
        Sub[v] += Sub[u];

        for(int i = 0; i <= min(K , Sub[v]); i++)
            dp[v][i] = tmp[i];
    }
}
```

## Сумма длин всех путей в дереве [neerc](https://neerc.ifmo.ru/wiki/index.php?title=Динамика_по_поддеревьям)

> Найти сумму длин всех путей в дереве.

## Коровы в стойла на дереве [informatics](https://informatics.msk.ru/mod/statements/view.php?id=16806&chapterid=3381#1)

> Дано дерево на $n$ вершинах и число $k$. В каждой вершине дерева находится по одной корове. Необходимо выбрать в каких вершинах построить $k$ стойл так, чтобы максимальный путь от коровы до ближайшего стойла был как можно меньше.
