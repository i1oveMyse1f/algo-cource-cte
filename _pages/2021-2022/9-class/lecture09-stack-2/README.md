---
layout: lecture
title:  "Дек. Устройство стека и очереди"
author: i_love_myself
categories: [ contest ]
youtube: -TplheGSsp4
toc: true
---

## Deque (дек)

Дек - это ещё более продвинутая структура, чем стек или очередь. Она умеет в 6 операций:

1. Добавить элемент в конец или в начало дека
1. Удалить элемент из конца или начала дека
1. Узнать, какие элементы лежат в конце или начале дека

Иными словами, дек - это "двусторонняя очередь".

### Зачем же нужна такая структура?

Всё ради того, чтобы решить буквально единственную, но периодически встречающуюся задачу:

> Для каждого подотрезка [l; l+k-1] (с фиксированным k, называемым размером окна) необходимо найти минимум на этом отрезке.

### Решение

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

### Код

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

## Разбор задач

### Минимальная строка

> На день рождения Пете подарили строку s длиной до 105 символов. Он взял еще две пустые строки t и u и решил сыграть в игру. По правилам в игре допускается два варианта ходов: <br> 1. Изъять символ из начала строки s и приписать его в конец строки t. <br> 2. Изъять символ из конца t и приписать его в конец строки u. <br> В результате Петя хочет, чтобы строка u была лексикографически минимальна, а s и t — пусты.

<details markdown="1">
<summary> Решение за O(n) </summary>
Жадный алгоритм: каждый раз ищем лексикографически минимальный вохможный символ, который мы можем написать в строку u. Этот символ может быть либо последним символом из строки t, либо любым из строки s. А далее лишь дело реализации: как поддерживать лексикографически минимальный сивол в строке s? Над этим советую подумать, прежде чем смотреть в раздел c кодом.
</details>

<details markdown="1">
<summary> Код </summary>

```cpp
#include <iostream>
#include <deque>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

int cnt[26];

int main() {
    string s;
    cin >> s;
    string t;

    for (char c : s)
        cnt[c - 'a']++;

    int n = s.size();

    reverse(s.begin(), s.end());

    for (int i = 0; i < n; ++i) {
        int lexmin = 27;
        for (int i = 0; i < 26; ++i)
            if (cnt[i])
                lexmin = min(lexmin, i);

        if (!t.empty() && lexmin >= t.back() - 'a') {
            cout << t.back();
            t.pop_back();
        }
        else {
            while (s.back() - 'a' != lexmin) {
                cnt[s.back() - 'a']--;
                t.push_back(s.back());
                s.pop_back();
            }
            cnt[s.back() - 'a']--;
            s.pop_back();
            cout << (char)(lexmin + 'a');
        }
    }
}
```

</details>

### Пьяница

> В игре в пьяницу карточная колода раздается поровну двум игрокам. Далее они вскрывают по одной верхней карте, и тот, чья карта старше, забирает себе обе вскрытые карты, которые кладутся под низ его колоды. Тот, кто остается без карт – проигрывает. <br> Для простоты будем считать, что все карты различны по номиналу, а также, что самая младшая карта побеждает самую старшую карту ("шестерка берет туза"). <br> Игрок, который забирает себе карты, сначала кладет под низ своей колоды карту первого игрока, затем карту второго игрока (то есть карта второго игрока оказывается внизу колоды). <br> Напишите программу, которая моделирует игру в пьяницу и определяет, кто выигрывает. В игре участвует 10 карт, имеющих значения от 0 до 9, большая карта побеждает меньшую, карта со значением 0 побеждает карту 9.

Ну тут чисто очередь. Так что главное - это написать.

## Устройство стека и очереди

В прошлый раз, когда мы обсуждали стек и очередь, мы абсолютно не задумывались, как они устроены. Пришло время поговорить о том, как же это реализовано так, чтобы все операции занимали О(1) (иначе говоря, константу) времени.

### Стек

В чём вообще проблема? Предположим, стек использует обычный массив. Тогда на каждое добавление нового элемента нам придется увеличивать массив на один элемент. К сожалению, такой операции над массивами не существует. Поэтому чтобы еёё реализовать, нам придется:

1. Создать новый массив размера n+1, это занимает О(1) по времени (да, создание массива любого размера с помощью оператора new занимает константу времени в C++)
1. Скопировать n элементов из строго массива в новый, это занимает О(n)

Таким образом, если мы добавим в стек последовательно n элементов, то это займет во премени примерно 1 + 2 + 3 + ... + n = О(n<sup>2</sup>) операций. Беда.

Как обычно в алгоритмах, нужно постараться найти "узкое место". В нашем случае - это копирование n элементов из одного массива в другой каждый раз. Значит это место нужно исправить.

Вместо того, чтобы на каждый push создавать новый массив размера n+1, будем создавать массива размера 2n, скопировав всего n элементов. Это позволит следующие n пушей не копировать старый массив. Оценим временную сложность: пусть мы добавили n элементов в стек, тогда мы потратили 1 + 2 + 0 + 4 + 0 + 0 + 0 + 8 + 0 + 0 + ... ≤ 2n = О(n) действий.

И ещё небольшое замечание, при действии pop мы не будем менять размер массива. Вместо этого будем поддерживать указатель на первый свобоный элемент в стеке. Таким образом, любой pop занимает О(1) времени.

### Очередь

#### Очередь, похожая на стек

Можно реализовать очередь абсолютно аналогично предыдущему пункту: тоже увеличивать её размер в два раза. При этом нужно поддерживать два указателя: левый указатель будет поддерживать последний элемент в очрееди и двигаться при операции pop. Правый указатель - первый свободный элемент в массиве и двигаться при операции push.

_Замечание_: при копировании массива стоит копировать, все элементы, начиная с левого указателя и заканчивая правым.

#### Кольцевая очередь

Иногда задача на очередь весьма специфичная, а именно: мы заранее знаем, что в очереди в любой момент времени будет не больше k элементов. Тогда удобнее всего реализовать очередь на кольцевом массиве:

Создадим массив размера k+1. Всё так же будем поддерживать два указателя: на первый элемент очреди и первый свободный элемент в массиве. Однако, создавать новые массивы нам не придётся. Как только любой из указателей дойдёт до конца массива, его нужно передвинуть в начало, "по кольцу". Таким образом реализация становится очень простой и удобной.
