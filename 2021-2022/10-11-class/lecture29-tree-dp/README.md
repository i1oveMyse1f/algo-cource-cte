# ДП по поддеревьям

## Максимальное паросочетание в дереве [neerc](https://neerc.ifmo.ru/wiki/index.php?title=Динамика_по_поддеревьям)

> Необходимо найти максимальное паросочетание в дереве за линейное время.

Паросочетание (англ. matсhing) M в двудольном графе - произвольное множество рёбер графа такое, что никакие два ребра не имеют общей вершины.

<details>

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

<details>
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

<details>
<summary>
Решение
</summary>
Пусть dp[v] - обозначает самый длинный путь в поддереве. Тогда самый длинный путь, проходящий через v строго в поддереве - это dp[u<sub>1</sub>] + dp[u<sub>2</sub>] + 2, где u<sub>1</sub> и u<sub>2</sub> - это максимум и второй максимум по сыновьям v. Главная проблема в том, что пути, проходящие через веришину v могут уходить в наддерево v. Но сейчас разберем и такой случай!

Чтобы решить проблему заметим, что у корня дерева наддерева нет. А ещё заметим, что мы можем выбрать поддерево u корня v, и при переходе в поддерево передать в него значение самого длинного пути в наддереве - dp[w] + 2, где w - это какая-то вершина, отличная от u и имеющая при этом максимальное значение динамики. Ок. То есть, начав с корня, мы можем начитывать пути в наддеревья. Остался один маленький нюанс. Нужно уметь считать dp[w] за O(1), то есть для всех детей искать максимум по сыновьям кроме u.

Для этого трюк: запомним максимум и второй максимум. Если u - это позиция максимума, то ответ - второй максимум, для остальных - позиция максимума. Всё, теперь, собирая решение воедино, мы сможем за линию считать диаметр дерева через каждую вершину.
</details>

## Количество связных подграфов на K вершинах [cf post](https://codeforces.com/blog/entry/63257)

> Дано дерево. Необходимо вычислить количество связных подграфов размера K в нём за время: <br> [a] O(nk<sup>2</sup>) </br> [b] O(nk)

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

## Коровы в стойла на дереве [informatics](https://informatics.msk.ru/mod/statements/view.php?id=16806&chapterid=3381#1)