# Аудит HTML-ресурсу Pripravka Amazon PL / UA Product Cards

Файл: `/Users/viacheslavdubovyk/Desktop/AI/Codex/pripravka-products/amazon-audit/index.html`

URL локального перегляду: `http://localhost:3000/amazon-audit/`

Дата перевірки: 2026-06-03

## 1. Джерело

- Дані зібрані зі сторінок Amazon.pl, які були надані користувачем.
- Усього в списку: 39 Amazon URL.
- Групи:
  - Exclusive Professional: 7
  - Grill & BBQ: 4
  - O-o-o, Jakie ziemniaki: 4
  - Przyprawy poddane obróbce parą: 16
  - Sosy WOK: 5
  - Ketchup: 3

## 2. Аудит структури HTML

- HTML згенеровано як окремий ресурс у папці `amazon-audit`.
- На сторінці є 39 карток товарів у форматі: фото пачки зліва, таблиця PL / UA справа.
- На сторінці є 39 Amazon-посилань.
- На сторінці є 39 локальних зображень товарів.
- На сторінці є 39 таблиць `Sekcja / Polski tekst / Український переклад`.
- На сторінці є 39 окремих блоків `OCR з пачки / переклад`.
- Загальна кількість редагованих полів у браузері: 507.
- Порожніх редагованих полів не виявлено.

## 3. Аудит зображень

- Усі 39 головних фото товарів завантажені локально в `amazon-audit/assets`.
- HTML використовує локальні копії фото, а не гарячі Amazon-посилання.
- Розмір папки з фото: приблизно 4.4 MB.
- Кеш HTML-сторінок Amazon збережений у `amazon-audit/pages` для повторної перевірки без повторного навантаження на Amazon.

## 4. Аудит title / brand

- 38 із 39 Amazon-title містять бренд `Pripravka`.
- 1 картка має попередження: title на Amazon не містить `Pripravka`.
- Попередження:
  - ASIN `B0GWQ82XSS`
  - Група: `Przyprawy poddane obróbce parą`
  - Title: `Przyprawa do kurczaka grill i piekarnik – mieszanka przypraw do mięsa, kurkuma czosnek naturalna przyprawa bez cukru i soli, do pieczenia smażenia grillowania, przyprawa do kurczaka i mięsa`
  - Дія: вручну перевірити на Amazon, чи це справді картка Pripravka, чи title потребує виправлення.

## 5. Аудит перекладу

- Для кожної з 39 карток додано український переклад Amazon-title.
- Усі 39 українських перекладів містять кирилицю.
- Для кожної картки додано таблицю з польським текстом Amazon-картки та українським перекладом.
- Переклади зроблені як робочі поля для аудиту й редагування: кулінарні терміни та смакові варіанти потрібно фінально звірити вручну.
- Проведено повторний аудит на змішані польсько-українські фрагменти в українських комірках.
- Виправлено залишки польських службових слів і фраз у перекладах: `z`, `ze`, `i`, `do`, `bez`, `Sokiem`, `Konserwantów`, `Pieprzem`, `Liśćmi`, `Sterylizowana Parowo` та інші.
- Додатково після ручної перевірки виправлено короткі польські залишки, які попередній regex не ловив:
  - `na` -> `на`
  - `po Grecku` -> `по-грецьки`
  - `po Meksykańsku` -> `по-мексиканськи`
  - `Idealna na Grill` -> `ідеальна на гриль`
- Перевірені ASIN після корекції: `B0GWQ1VXWY`, `B0GWQ8F15V`, `B0GWPZJZFN`, `B0GR662B45`, `B0GR6DLCZF`.
- Після коригування: `UA-комірок із польськими залишками: 0`.

## 6. Аудит OCR-тексту з упаковок

- Для кожної з 39 карток додано окремий OCR-блок.
- OCR-блок містить:
  - `Rozpoznany tekst z opakowania`
  - `Український переклад OCR`
  - примітку аудиту щодо надійності розпізнавання.
- Усі 39 OCR-блоків мають польський мовний сигнал.
- Усі 39 OCR-переклади містять українську кирилицю.
- Проведено додатковий аудит OCR-перекладів на залишки польського тексту.
- Виправлено приклади змішаного перекладу:
  - `z kurkumą i imbirem` -> `з куркумою та імбиром`
  - `z czarnuszką` -> `з чорнушкою`
  - `7 etapów oczyszczania` -> `7 етапів очищення`
- Після ручного звірення з фото виправлено OCR для `B0GR5VR6VT`:
  - `Do kurczaka po polsku` -> `Do kurczaka po staropolsku`
  - `До курки по-польськи` -> `До курки по-старопольськи`
- Додано пріоритетні OCR-блоки, звірені вручну користувачем:
  - WOK: `B0GR65447J`, `B0GR5YXV1D`, `B0GR5YXJT5`, `B0GR634TKQ`, `B0GWD3S8BM` - виправлено `Azji` на `AI-AZJI`, додано рядки про віртуального AI-шефа, AI-контент і `140 g`.
  - Grill & BBQ `B0GWQFM1RN` - виправлено `Naturalna przyprawa do mięsa i kurczaka` на `Naturalna przyprawa do ryb i owoców morza`.
  - Ziemniaki `B0GWQ8F15V`, `B0GWQ686KL`, `B0GWPZJZFN` - додано `i warzyw` та QR-підпис `Zeskanuj smartfonem i pysznie ugotuj`.
  - Ziemniaki `B0GWQ69PQ4` - оновлено QR-підпис на `Zeskanuj smartfonem i pysznie ugotuj`.
  - Ketchup `B0GR6DLCZF` - виправлено `z musem bananowym` на `z przecierem bananowym`.
- Додано OCR-бейджі пріоритету 2 з українським перекладом:
  - Exclusive `B0GWQ6SCNR`, `B0GWQ1VXWY`, `B0GQZLRBZM` - додано `Bez dodatku soli` / `Без додавання солі`.
  - Exclusive `B0GWQB6141`, `B0GWQC4PNQ`, `B0GWPYCVN6`, `B0GWPWPTHT` - додано `Bez dodatku soli` / `Без додавання солі` та `Perła Rynku 2025` / `Перлина ринку 2025`.
  - Ziemniaki `B0GWQ69PQ4`, `B0GWQ8F15V`, `B0GWQ686KL`, `B0GWPZJZFN` - додано `Perła Rynku 2025` / `Перлина ринку 2025`.
  - Grill & BBQ `B0GWQ9Z9SH`, `B0GWQ6QD2K`, `B0GWQFM1RN`, `B0GWPZKXXT` - додано `100% naturalnych składników` / `100% натуральних інгредієнтів` та `Bez dodatku glutaminianu monosodowego, barwników i konserwantów` / `Без додавання глутамату натрію, барвників і консервантів`.
  - Парова серія Zioła `B0GR11MQT5`, `B0GR11JSQ5`, `B0GR19CRFR` - додано окремий бейдж `Bez dodatku soli` / `Без додавання солі`.
  - Ketchup `B0GR662B45`, `B0GR61BRTY` - додано `Z octem jabłkowym` / `З яблучним оцтом` та `Zobacz lifehacki o jakości ketchupu!` / `Дивись лайфхаки про якість кетчупу!`.
- Внесено уточнення пріоритету 3:
  - `B0GR5XXM78`, `B0GR5XX6B3`, `B0GR62J427` - замінено `Naturalna przyprawa` на `Mieszanka przyprawowa` / `Приправна суміш`.
  - `B0GR5XXM78` - уточнено `z dodatkiem chili ancho` на `mielony z dodatkiem chili ancho` / `мелений, з додаванням чилі анчо`.
  - Для трьох чорних паків `B0GR5XXM78`, `B0GR5XX6B3`, `B0GR62J427` прибрано фронтовий OCR-рядок `Zero cukru`, бо на головному фото пачки він не підтверджений.
- Після додаткової перевірки за скриншотами користувача додано дрібні та бокові написи, які раніше не були включені в OCR-блоки:
  - Для всіх `Grill & BBQ` додано підписи способів приготування: `Patelnia`, `Kuchenka mikrofalowa`, `Piekarnik`, `Grill` / `Сковорода`, `Мікрохвильова піч`, `Духовка`, `Гриль`.
  - Для всіх `Grill & BBQ` додано `Zdjęcie symboliczne` / `Символічне фото`, `* Dodatek cukru 0% / Доданого цукру 0%` / `* Доданого цукру 0%` та вагу `30 g` / `30 г`.
  - Для всіх `O-o-o, Jakie ziemniaki` додано боковий напис `Propozycja podania` / `Приклад подавання` та вагу `25 g` / `25 г`.
  - Для всіх `Exclusive Professional` додано боковий напис `Propozycja podania` / `Приклад подавання` та вагу з пачки.
  - Для парової серії додано `Zdjęcie symboliczne` / `Символічне фото`, QR-заголовки `Czego dziś dowiesz o naszej przyprawie?` або `Dlaczego sterylizujemy nasze przyprawy?` з українським перекладом, а також вагу з пачки.
  - Для зелених і основних парових паків додано нижній рядок `* Dodatek cukru 0% / Доданого цукру 0%` / `* Доданого цукру 0%`.
  - Для чорних паків `B0GR5XXM78`, `B0GR5XX6B3`, `B0GR62J427` не додавалися `Zero cukru` і нижній цукровий footnote, бо на фронтальному фото вони не підтверджені.
  - Для всіх інших карток додано вагу з пачки, якщо вона присутня в Amazon-title і відповідає видимому формату пакування.
- Після коригування: `OCR-перекладів із польськими залишками: 0`.
- OCR зроблено по основних великих написах, видимих на головному фото Amazon: бренд, серія, назва продукту, смакові компоненти, claim-плашки на кшталт `Zero cukru`, `100% naturalny produkt`, `Przyprawy poddane obróbce parą`.
- Дрібний службовий текст, QR-пояснення малого розміру та вертикальні бокові написи не вважаються підтвердженим OCR, якщо їх не можна надійно прочитати з доступного зображення.

## 7. Функції ресурсу

- `Увімкнути редагування` - дозволяє редагувати title, таблиці PL / UA та OCR-блоки.
- `Провести аудит` - перевіряє кількість карток, фото, таблиць, OCR-блоків, перекладів і порожніх полів.
- `Експортувати HTML` - створює HTML із поточними правками.
- `Скинути правки` - очищає localStorage для цього ресурсу.
- `Друк / PDF` - дозволяє зберегти сторінку як PDF.
- Після оновлення OCR-бейджів ключ localStorage змінено на `pripravka-amazon-product-cards-v3`, щоб старі локальні правки не перекривали нову базову версію HTML.

## 8. Висновок

Ресурс готовий до ручної перевірки Amazon-карток. Критичних технічних помилок не виявлено: 39/39 карток, 39/39 фото, 39/39 таблиць і 39/39 OCR-блоків завантажені. Повторна перевірка на `localhost:3000/amazon-audit/` підтвердила: `OCR-перекладів із польськими залишками: 0`, `UA-комірок із польськими залишками: 0`, `Порожніх редагованих полів: 0`. Є одне очікуване змістове попередження щодо Amazon-title без бренду `Pripravka` для `B0GWQ82XSS`.
