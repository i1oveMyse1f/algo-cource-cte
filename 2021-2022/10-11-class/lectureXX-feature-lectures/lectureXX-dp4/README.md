# Интересные задачи на ДП

## Задача (гирьки: три кучки равной массы)

Дан набор гирек массой m<sub>1</sub>,…,m<sub>N</sub>. Можно ли их разложить на три кучки равной массы?

### Решение

Здесь опять же очень легко можно модифицировать рюкзак. Пусть dp[i][w1][w2] - это можем ли мы собрать кучки размера w1 и w2, используя только первые i предметов. Тогда ответ будет лежать в dp[i][W/3][W/3]. Переходы тривиальные.

### Бонус

> Подумайте над этой задачкой, но с разделением кучек на n равных по весу частей (быстрее чем решение, аналогичное решению выше).

### Код

```cpp
// code will be here
```