# Карта фотографий сайта

## Где что лежит

| Папка | Что это |
|---|---|
| `photo/new/` | ваши исходники как есть (только на диске, в git не входят) |
| `assets/images/products/<коллекция>/` | фото товаров на сайте (webp) |
| `assets/images/portfolio/` | интерьеры из раздела «Интерьеры» |
| `data/products.json` | список фото каждой коллекции = порядок в галерее |

Коллекции: `cloud`, `curve`, `nordic`, `camaleonda` (это Bellini), `daybed`, `cube`, `verde`, `graphite`.

## Откуда какое фото взято (photo/new → сайт)

### Cube Lounge
cube-01 ← IG692 (белый модуль + пёс, терраса) · cube-02 ← IG524 · cube-03 ← IG281 ·
cube-04 ← photo_46 · cube-05 ← photo_50 · cube-06 ← photo_51 · cube-07 ← photo_57 · cube-08 ← photo_15

### Verde Tufted (зелёная)
verde-01 ← photo_53 · verde-02 ← photo_54 · verde-03 ← photo_55 · verde-04 ← photo_56 (кресло) ·
verde-05 ← IG299 (жалюзи) · verde-06 ← photo_1 · verde-07 ← photo_10 · verde-08 ← photo_15

### Graphite Loft (тёмный)
graphite-01 ← photo_5 · graphite-02 ← photo_6 · graphite-03 ← photo_31 · graphite-04 ← photo_32 · graphite-05 ← photo_33

### Bellini / camaleonda (добавленные)
camaleonda-03..06 ← photo_34, photo_35, photo_36, photo_37 (решётка/лайтбокс)

### Daybed (добавленные)
daybed-04 ← photo_7 (белая кровать) · daybed-05 ← IG689 · daybed-06 ← photo_8 · daybed-07 ← photo_9

### Cloud (добавленные)
cloud-12 ← photo_19 · cloud-13 ← photo_20 · cloud-14 ← photo_21 · cloud-15 ← photo_22 ·
cloud-16 ← photo_23 · cloud-17 ← photo_24 · cloud-18 ← photo_30 (оранжевая) · cloud-19 ← photo_2 · cloud-20 ← photo_27

### Curve (добавленные)
curve-12 ← IG179 · curve-13 ← photo_29 (пуф-кресло) · curve-14 ← photo_42 · curve-15 ← photo_48 · curve-16 ← photo_49

### Portfolio (интерьеры)
interior-07 ← photo_12 (терраса) · interior-08 ← photo_17 (деревянные панели) ·
interior-09 ← photo_28 (классика) · interior-10 ← photo_4 (мама с ребёнком)

### Не использованы (можно куда-нибудь добавить)
photo_3 (библиотека) · photo_13, photo_14 (терраса, крупный план) · photo_18, photo_25, photo_26 ·
photo_38–45 (пёсики/котики крупным планом) · видео 207806549....mp4

## Как самому поправить

**Обрезать/отретушировать:** правьте файл прямо в `assets/images/products/...`,
сохраняя то же имя (например `verde-03.webp`). Сайт сам показывает фото в
любой пропорции целиком, так что резать можно как угодно. Сохранилось не в
webp, а в jpg? Положите рядом и скажите мне — конвертирую.

**Пересортировать по коллекциям / поменять порядок в галерее:** порядок
задаётся списком `images` в `data/products.json` (первый элемент = главное
фото на карточке и странице). Скажите, что куда — перенесу; или сами
поменяйте строки местами в json.

**После любых правок:** `git add -A && git commit -m "photos" && git push` —
сайт обновится сам через 1–2 минуты.
