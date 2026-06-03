from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "amazon_products.json"
OUT = ROOT / "index.html"


OCR_LABELS = {
    "B0GWQ6SCNR": ("Do kurczaka po staropolsku", "z czarnuszką"),
    "B0GWQB6141": ("Do ryb", "ze skórką cytrynową i bazylią"),
    "B0GWQ1VXWY": ("Do szaszłyków", "z rozmarynem i czosnkiem"),
    "B0GWQC4PNQ": ("Do kurczaka", "z wędzoną papryką"),
    "B0GWPYCVN6": ("Do mięs", "z brazylijskim różowym pieprzem"),
    "B0GWPWPTHT": ("Curry", "z kurkumą i imbirem"),
    "B0GQZLRBZM": ("Zioła prowansalskie", ""),
    "B0GWQ9Z9SH": ("Skrzydełka meksykańskie", "z naturalnym pomarańczowym sokiem, tamaryndowcem i imbirem"),
    "B0GWQ6QD2K": ("Żeberka grillowane", "z naturalnymi wędzonymi pomidorami, chili i musztardą"),
    "B0GWQFM1RN": ("Sycylijska ryba", "z naturalnym sokiem z limonki, liśćmi kaffir i chili"),
    "B0GWPZKXXT": ("Stek po teksańsku", "z pieprzem syczuańskim i słodem żytnim"),
    "B0GWQ69PQ4": ("Amerykańskie", "o smaku bekonu i karmelizowanej cebuli"),
    "B0GWQ8F15V": ("Greckie", "ze skórką z cytryny i pomidorami"),
    "B0GWQ686KL": ("Włoskie", "o smaku sera i z czosnkiem"),
    "B0GWPZJZFN": ("Meksykańskie", "z wędzoną papryką i kminkiem"),
    "B0GR11MQT5": ("Zioła Grecji", "z czosnkiem i trawą cytrynową"),
    "B0GR11JSQ5": ("Zioła Włoch", "bazylia, pomidory, oregano, czosnek, chili i mięta"),
    "B0GR19CRFR": ("Zioła Francji", "z lawendą i rozmarynem"),
    "B0GR5XXM78": ("Z pieprzem kolorowym", "z dodatkiem chili ancho"),
    "B0GR5XX6B3": ("Pieprz czosnkowy", ""),
    "B0GR62J427": ("Pieprz ziołowy", ""),
    "B0GR5P4VHT": ("Do mięs", "z czosnkiem i bazylią"),
    "B0GWQ82XSS": ("Do kurczaka", "grill i piekarnik"),
    "B0GR5PP3VK": ("Do ziemniaków", "z kolendrą i cebulą"),
    "B0GR5W67KS": ("Curry", "z kurkumą i imbirem"),
    "B0GR5VR6VT": ("Do kurczaka po staropolsku", ""),
    "B0GR5SDW21": ("Do mięsa mielonego", ""),
    "B0GR5XJ3W7": ("Do mięsa wieprzowego", ""),
    "B0GR5XCWP7": ("Do ryb", "z kolendrą, kurkumą i imbirem"),
    "B0GR5SLL54": ("Do bigosu", "z nasionami gorczycy, kminkiem i borowikami"),
    "B0GR5ZBCSL": ("Do gyrosa i kebaba", ""),
    "B0GR65447J": ("WOK sauce ASIAN", "czarny pieprz i sos sojowy"),
    "B0GR5YXV1D": ("WOK sauce CHOW MEIN", "imbir i nasiona sezamu"),
    "B0GR5YXJT5": ("WOK sauce KUNG PAO", "pieprz syczuański i czosnek"),
    "B0GR634TKQ": ("WOK sauce PAD THAI", "tamarynd i imbir"),
    "B0GWD3S8BM": ("WOK sauce SPICY HOT", "pieprz Timut i chili"),
    "B0GR662B45": ("Ketchup łagodny", "z bazylią, 50% mniej cukru"),
    "B0GR61BRTY": ("Ketchup oryginalny", "z oliwkami, 50% mniej cukru"),
    "B0GR6DLCZF": ("Ketchup", "z przecierem bananowym, 50% mniej cukru"),
}

EXCLUSIVE_SALT_ONLY = {"B0GWQ6SCNR", "B0GWQ1VXWY", "B0GQZLRBZM"}
EXCLUSIVE_SALT_PERLA = {"B0GWQB6141", "B0GWQC4PNQ", "B0GWPYCVN6", "B0GWPWPTHT"}
ZIEMNIAKI_PERLA = {"B0GWQ69PQ4", "B0GWQ8F15V", "B0GWQ686KL", "B0GWPZJZFN"}
GRILL_BBQ_BADGES = {"B0GWQ9Z9SH", "B0GWQ6QD2K", "B0GWQFM1RN", "B0GWPZKXXT"}
STEAM_ZIOLA_SALT = {"B0GR11MQT5", "B0GR11JSQ5", "B0GR19CRFR"}
PEPPER_MIX_PACKS = {"B0GR5XXM78", "B0GR5XX6B3", "B0GR62J427"}
KETCHUP_APPLE_LIFEHACK = {"B0GR662B45", "B0GR61BRTY"}
STEAM_SUGAR_FOOTNOTE = {
    "B0GR11MQT5",
    "B0GR11JSQ5",
    "B0GR19CRFR",
    "B0GR5P4VHT",
    "B0GWQ82XSS",
    "B0GR5PP3VK",
    "B0GR5W67KS",
    "B0GR5VR6VT",
    "B0GR5SDW21",
    "B0GR5XJ3W7",
    "B0GR5XCWP7",
    "B0GR5SLL54",
    "B0GR5ZBCSL",
}
STEAM_HERB_QR_HEADLINE = {"B0GR11MQT5", "B0GR11JSQ5", "B0GR19CRFR"}


TERM_MAP = [
    ("Przyprawy poddane obróbce parą", "Спеції, оброблені парою"),
    ("Sterylizacja parowa", "парова стерилізація"),
    ("Sterylizowana parą", "стерилізована парою"),
    ("Naturalna przyprawa grubo mielona", "натуральна крупномелена приправа"),
    ("Naturalna przyprawa", "натуральна приправа"),
    ("Naturalna mieszanka", "натуральна суміш"),
    ("Mieszanka przyprawowa", "суміш спецій"),
    ("Mieszanka", "суміш"),
    ("Przyprawa", "приправа"),
    ("do mięsa i kurczaka", "до м'яса і курки"),
    ("Do kurczaka po staropolsku", "до курки по-старопольськи"),
    ("Do kurczaka po polsku", "до курки по-польськи"),
    ("Do kurczaka", "до курки"),
    ("Do szaszłyków", "до шашликів"),
    ("Do mięs", "до м'яса"),
    ("Do mięsa mielonego", "до фаршу"),
    ("Do mięsa wieprzowego", "до свинини"),
    ("Do ryb", "до риби"),
    ("Do ziemniaków", "до картоплі"),
    ("Do bigosu", "до бігосу"),
    ("Do gyrosa i kebaba", "до гіроса і кебаба"),
    ("Skrzydełka meksykańskie", "мексиканські крильця"),
    ("Żeberka grillowane", "реберця гриль"),
    ("Sycylijska ryba", "сицилійська риба"),
    ("Stek po teksańsku", "стейк по-техаськи"),
    ("po Grecku", "по-грецьки"),
    ("po Meksykańsku", "по-мексиканськи"),
    ("Idealna na Grill", "ідеальна на гриль"),
    ("na Grill", "на гриль"),
    ("Amerykańskie", "американські"),
    ("Greckie", "грецькі"),
    ("Włoskie", "італійські"),
    ("Meksykańskie", "мексиканські"),
    ("Zioła prowansalskie", "прованські трави"),
    ("Zioła Grecji", "трави Греції"),
    ("Zioła Włoch", "трави Італії"),
    ("Zioła Francji", "трави Франції"),
    ("Zioła Śródziemnomorskie", "середземноморські трави"),
    ("Suszone Pomidory", "сушені помідори"),
    ("Skórka z Cytryny", "лимонна цедра"),
    ("Doypack z Zamknięciem Zip", "дойпак із zip-застібкою"),
    ("Sokiem Pomarańczowym", "апельсиновим соком"),
    ("Sokiem z Limonki", "соком лайма"),
    ("Liśćmi Kaffir", "листям кафіру"),
    ("Pieprzem Syczuańskim", "сичуанським перцем"),
    ("Słodem Żytnim", "житнім солодом"),
    ("Sterylizowana Parowo", "стерилізована парою"),
    ("Sterylizowana Parą", "стерилізована парою"),
    ("Czysty Skład", "чистий склад"),
    ("Naturalny Skład", "натуральний склад"),
    ("Intensywny Smak", "інтенсивний смак"),
    ("Intensywny Aromat", "інтенсивний аромат"),
    ("Intensywna Mieszanka", "інтенсивна суміш"),
    ("Tradycyjny Smak", "традиційний смак"),
    ("Autentyczny Smak Kuchni Azjatyckiej", "автентичний смак азійської кухні"),
    ("Bez Chemii i Konserwantów", "без хімії та консервантів"),
    ("Duże Opakowanie", "велика упаковка"),
    ("Mniej Cukru", "менше цукру"),
    ("Ocet Jabłkowy", "яблучний оцет"),
    ("Octem Jabłkowym", "яблучним оцтом"),
    ("Sól Morska", "морська сіль"),
    ("Przecierem Bananowym", "банановим пюре"),
    ("Przecierem Jabłkowym", "яблучним пюре"),
    ("Zielonymi Oliwkami", "зеленими оливками"),
    ("Nasionami Gorczycy", "насінням гірчиці"),
    ("Szlachetnymi Borowikami", "добірними білими грибами"),
    ("Tradycyjnej Kapusty z Mięsem", "традиційної капусти з м'ясом"),
    ("Wyjatkowa Mieszanka Ziolowa", "виняткова трав'яна суміш"),
    ("Czyszczona Para", "очищена парою"),
    ("do Pieczenia", "для запікання"),
    ("do Smażenia", "для смаження"),
    ("do Grillowania", "для грилювання"),
    ("do Frytek", "для картоплі фрі"),
    ("do Puree", "для пюре"),
    ("do Zup", "для супів"),
    ("do Sałatek", "для салатів"),
    ("do Sosów", "для соусів"),
    ("do Mięs", "для м'яса"),
    ("do Ryb", "для риби"),
    ("do Drobiu", "для птиці"),
    ("do Wieprzowiny", "для свинини"),
    ("do Wołowiny", "для яловичини"),
    ("do Warzyw", "для овочів"),
    ("do Makaronu", "для локшини"),
    ("do Makaronu Ryżowego", "для рисової локшини"),
    ("Amerykańska", "американська"),
    ("Brazylijskim", "бразильським"),
    ("Brazylijski", "бразильський"),
    ("Różowym", "рожевим"),
    ("Bekon", "бекон"),
    ("Karmelizowana Cebula", "карамелізована цибуля"),
    ("Karmelizowanej Cebuli", "карамелізованої цибулі"),
    ("Ser i Czosnek", "сир і часник"),
    ("Jakie Ziemniaki", "яка картопля"),
    ("JAKIE ZIEMNIAKI", "ЯКА КАРТОПЛЯ"),
    ("Czarnym Pieprzem", "чорним перцем"),
    ("Sosem Sojowym", "соєвим соусом"),
    ("Pieprzem Timut", "перцем тімут"),
    ("Pieprzem Kolorowym", "кольоровим перцем"),
    ("Pieprzem", "перцем"),
    ("Pieprzu", "перцю"),
    ("Cytryną", "лимоном"),
    ("Czosnku", "часнику"),
    ("Grecku", "по-грецьки"),
    ("Meksykańsku", "по-мексиканськи"),
    ("Grill", "гриль"),
    ("grill", "гриль"),
    ("piekarnik", "духовка"),
    ("Pikantny", "пікантний"),
    ("Sezamem", "кунжутом"),
    ("Sojowym", "соєвим"),
    ("Stewią", "стевією"),
    ("Pomidorów", "помідорів"),
    ("Jabłkowym", "яблучним"),
    ("Timut", "тімут"),
    ("Wieprzowiny", "свинини"),
    ("Wołowiny", "яловичини"),
    ("Żeberek", "реберець"),
    ("Kolorowym", "кольоровим"),
    ("Wędzone Pomidory", "копчені помідори"),
    ("Dymu", "диму"),
    ("Majeranek", "майоран"),
    ("Tymianek", "тим'ян"),
    ("Oregano", "орегано"),
    ("Pomidory", "помідори"),
    ("Mięta", "м'ята"),
    ("Lawendą", "лавандою"),
    ("Trawą Cytrynową", "лемонграсом"),
    ("Liśćmi Curry", "листям карі"),
    ("Dań Orientalnych", "східних страв"),
    ("Kotletów", "котлет"),
    ("Burgerów", "бургерів"),
    ("Pulpetów", "фрикадельок"),
    ("Karkówki", "ошийка"),
    ("Pieczeni", "печені"),
    ("Pieczenia", "запікання"),
    ("Smażenia", "смаження"),
    ("Grillowania", "грилювання"),
    ("Frytek", "картоплі фрі"),
    ("Puree", "пюре"),
    ("Sałatek", "салатів"),
    ("Zup", "супів"),
    ("Sosów", "соусів"),
    ("Ryb", "риби"),
    ("Przypraw", "спецій"),
    ("Ziół", "трав"),
    ("Cukru", "цукру"),
    ("Soli", "солі"),
    ("Konserwantów", "консервантів"),
    ("Barwników", "барвників"),
    ("Chemii", "хімії"),
    ("Naturalna", "натуральна"),
    ("Naturalny", "натуральний"),
    ("Aromatyczna", "ароматна"),
    ("Aromat", "аромат"),
    ("Kompozycja", "композиція"),
    ("Idealna", "ідеальна"),
    ("Skład", "склад"),
    ("Smak", "смак"),
    ("Spicy Hot", "гострий"),
    ("Hot", "гострий"),
    ("Pieprz czosnkowy", "часниковий перець"),
    ("Pieprz ziołowy", "трав'яний перець"),
    ("Curry", "карі"),
    ("Ketchup łagodny", "кетчуп лагідний"),
    ("Ketchup oryginalny", "кетчуп оригінальний"),
    ("Ketchup", "кетчуп"),
    ("Pikantny Sos", "пікантний соус"),
    ("Sos do Dań Stir-Fry", "соус до страв Stir-Fry"),
    ("Kuchnia Azjatycka", "азійська кухня"),
    ("Bez Konserwantów i Barwników", "без консервантів і барвників"),
    ("Bez Konserwantów", "без консервантів"),
    ("Owoców Morza", "морепродуктів"),
    ("Mięsa", "м'яса"),
    ("Drobiu", "птиці"),
    ("Warzyw", "овочів"),
    ("Ryżu", "рису"),
    ("Makaronu", "локшини"),
    ("Sos", "соус"),
    ("WOK sauce", "соус WOK"),
    ("czarny pieprz", "чорний перець"),
    ("sos sojowy", "соєвий соус"),
    ("imbir", "імбир"),
    ("nasiona sezamu", "насіння кунжуту"),
    ("pieprz syczuański", "сичуанський перець"),
    ("pieprz Timut", "перець тімут"),
    ("czosnek", "часник"),
    ("czosnkiem", "часником"),
    ("bazylią", "базиліком"),
    ("bazylia", "базилік"),
    ("tamarynd", "тамаринд"),
    ("tamaryndowcem", "тамариндом"),
    ("kurkumą", "куркумою"),
    ("kurkuma", "куркума"),
    ("imbirem", "імбиром"),
    ("rozmarynem", "розмарином"),
    ("rozmaryn", "розмарин"),
    ("czarnuszką", "чорнушкою"),
    ("wędzoną papryką", "копченою паприкою"),
    ("papryką", "паприкою"),
    ("kminkiem", "кмином"),
    ("kolendrą", "коріандром"),
    ("cebulą", "цибулею"),
    ("chili ancho", "чилі анчо"),
    ("chili", "чилі"),
    ("ser", "сир"),
    ("oliwkami", "оливками"),
    ("musem bananowym", "банановим мусом"),
    ("50% mniej cukru", "на 50% менше цукру"),
    ("Zero cukru", "нуль цукру"),
    ("100% naturalny produkt", "100% натуральний продукт"),
    ("Bez dodatku soli", "без додавання солі"),
    ("Bez soli", "без солі"),
    ("Bez dodatku cukru", "без додавання цукру"),
    ("Bez dodatku konserwantów i barwników", "без додавання консервантів і барвників"),
    ("Sposoby przygotowania", "способи приготування"),
    ("7 etapów oczyszczania", "7 етапів очищення"),
    ("7 stopni oczyszczania", "7 ступенів очищення"),
    ("Światowej klasy mistrz kuchni", "майстер кухні світового класу"),
    ("Odkryj zwariowany świat Azji", "відкрий дивовижний світ Азії"),
    ("Zeskanuj kod QR", "відскануйте QR-код"),
    ("Zeskanuj QR kod", "відскануйте QR-код"),
    ("dowiedz się więcej", "дізнайтеся більше"),
]

OCR_EXACT_TRANSLATIONS = {
    "PRIPRAVKA": "PRIPRAVKA",
    "Exclusive Professional": "Exclusive Professional",
    "GRILL & BBQ": "GRILL & BBQ",
    "Przyprawy poddane obróbce parą": "Спеції, оброблені парою",
    "Naturalna przyprawa grubo mielona": "Натуральна крупномелена приправа",
    "Naturalna przyprawa do mięsa i kurczaka": "Натуральна приправа до м'яса і курки",
    "Naturalna przyprawa do ziemniaków": "Натуральна приправа до картоплі",
    "Naturalna przyprawa do ziemniaków i warzyw": "Натуральна приправа до картоплі та овочів",
    "Naturalna przyprawa do ryb i owoców morza": "Натуральна приправа до риби та морепродуктів",
    "Naturalna przyprawa": "Натуральна приправа",
    "Mieszanka przyprawowa": "Приправна суміш",
    "Bez dodatku soli": "Без додавання солі",
    "Perła Rynku 2025": "Перлина ринку 2025",
    "Zero cukru": "Нуль цукру",
    "100% naturalny produkt": "100% натуральний продукт",
    "100% naturalnych składników": "100% натуральних інгредієнтів",
    "Bez dodatku glutaminianu monosodowego, barwników i konserwantów": "Без додавання глутамату натрію, барвників і консервантів",
    "Z octem jabłkowym": "З яблучним оцтом",
    "Zobacz lifehacki o jakości ketchupu!": "Дивись лайфхаки про якість кетчупу!",
    "Patelnia": "Сковорода",
    "Kuchenka mikrofalowa": "Мікрохвильова піч",
    "Piekarnik": "Духовка",
    "Grill": "Гриль",
    "Propozycja podania": "Приклад подавання",
    "Zdjęcie symboliczne": "Символічне фото",
    "* Dodatek cukru 0% / Доданого цукру 0%": "* Доданого цукру 0%",
    "Czego dziś dowiesz o naszej przyprawie?": "Що сьогодні дізнаєшся про нашу приправу?",
    "Dlaczego sterylizujemy nasze przyprawy?": "Чому ми стерилізуємо наші приправи?",
    "Sposoby przygotowania": "Способи приготування",
    "7 etapów oczyszczania": "7 етапів очищення",
    "Do kurczaka po staropolsku": "До курки по-старопольськи",
    "z czarnuszką": "з чорнушкою",
    "Do ryb": "До риби",
    "ze skórką cytrynową i bazylią": "з лимонною цедрою та базиліком",
    "Do szaszłyków": "До шашликів",
    "z rozmarynem i czosnkiem": "з розмарином і часником",
    "Do kurczaka": "До курки",
    "z wędzoną papryką": "з копченою паприкою",
    "Do mięs": "До м'яса",
    "z brazylijskim różowym pieprzem": "з бразильським рожевим перцем",
    "Curry": "Карі",
    "z kurkumą i imbirem": "з куркумою та імбиром",
    "Zioła prowansalskie": "Прованські трави",
    "Skrzydełka meksykańskie": "Мексиканські крильця",
    "z naturalnym pomarańczowym sokiem, tamaryndowcem i imbirem": "з натуральним апельсиновим соком, тамариндом та імбиром",
    "Żeberka grillowane": "Реберця гриль",
    "z naturalnymi wędzonymi pomidorami, chili i musztardą": "з натуральними копченими помідорами, чилі та гірчицею",
    "Sycylijska ryba": "Сицилійська риба",
    "z naturalnym sokiem z limonki, liśćmi kaffir i chili": "з натуральним соком лайма, листям кафір-лайма та чилі",
    "Stek po teksańsku": "Стейк по-техаськи",
    "z pieprzem syczuańskim i słodem żytnim": "з сичуанським перцем і житнім солодом",
    "O-o-o, jakie ziemniaki": "О-о-о, яка картопля",
    "Amerykańskie": "Американські",
    "o smaku bekonu i karmelizowanej cebuli": "зі смаком бекону та карамелізованої цибулі",
    "Greckie": "Грецькі",
    "ze skórką z cytryny i pomidorami": "з лимонною цедрою та помідорами",
    "Włoskie": "Італійські",
    "o smaku sera i z czosnkiem": "зі смаком сиру та з часником",
    "Meksykańskie": "Мексиканські",
    "z wędzoną papryką i kminkiem": "з копченою паприкою та кмином",
    "Zeskanuj QR kod, dowiedz się więcej": "Відскануйте QR-код, дізнайтеся більше",
    "Zeskanuj kod QR, dowiedz się więcej": "Відскануйте QR-код, дізнайтеся більше",
    "Zeskanuj smartfonem i pysznie ugotuj": "Відскануй смартфоном і смачно приготуй",
    "Zioła Grecji": "Трави Греції",
    "z czosnkiem i trawą cytrynową": "з часником і лемонграсом",
    "Zioła Włoch": "Трави Італії",
    "bazylia, pomidory, oregano, czosnek, chili i mięta": "базилік, помідори, орегано, часник, чилі та м'ята",
    "Zioła Francji": "Трави Франції",
    "z lawendą i rozmarynem": "з лавандою та розмарином",
    "Z pieprzem kolorowym": "З кольоровим перцем",
    "z dodatkiem chili ancho": "з додаванням чилі анчо",
    "mielony z dodatkiem chili ancho": "мелений, з додаванням чилі анчо",
    "Pieprz czosnkowy": "Часниковий перець",
    "Pieprz ziołowy": "Трав'яний перець",
    "z czosnkiem i bazylią": "з часником і базиліком",
    "grill i piekarnik": "гриль і духовка",
    "Do ziemniaków": "До картоплі",
    "z kolendrą i cebulą": "з коріандром і цибулею",
    "Do kurczaka po polsku": "До курки по-польськи",
    "Do mięsa mielonego": "До фаршу",
    "Do mięsa wieprzowego": "До свинини",
    "z kolendrą, kurkumą i imbirem": "з коріандром, куркумою та імбиром",
    "Do bigosu": "До бігосу",
    "z nasionami gorczycy, kminkiem i borowikami": "з насінням гірчиці, кмином і білими грибами",
    "Do gyrosa i kebaba": "До гіроса і кебаба",
    "WOK sauce ASIAN": "Соус WOK ASIAN",
    "czarny pieprz i sos sojowy": "чорний перець і соєвий соус",
    "WOK sauce CHOW MEIN": "Соус WOK CHOW MEIN",
    "imbir i nasiona sezamu": "імбир і насіння кунжуту",
    "WOK sauce KUNG PAO": "Соус WOK KUNG PAO",
    "pieprz syczuański i czosnek": "сичуанський перець і часник",
    "WOK sauce PAD THAI": "Соус WOK PAD THAI",
    "tamarynd i imbir": "тамаринд та імбир",
    "WOK sauce SPICY HOT": "Соус WOK SPICY HOT",
    "pieprz Timut i chili": "перець Тімут і чилі",
    "Światowej klasy mistrz kuchni": "Майстер кухні світового класу",
    "Odkryj zwariowany świat Azji": "Відкрий дивовижний світ Азії",
    "Odkryj zwariowany świat AI-AZJI": "Відкрий шалений світ AI-АЗІЇ",
    "Rozmawiaj z wirtualnym szefem kuchni, generuj obrazy*": "Спілкуйся з віртуальним шеф-кухарем, генеруй зображення*",
    "* Treści na stronie zostały wygenerowane przez AI": "* Вміст на сторінці згенеровано штучним інтелектом",
    "140 g": "140 г",
    "Ketchup łagodny": "Кетчуп лагідний",
    "z bazylią, 50% mniej cukru": "з базиліком, на 50% менше цукру",
    "Ketchup oryginalny": "Кетчуп оригінальний",
    "z oliwkami, 50% mniej cukru": "з оливками, на 50% менше цукру",
    "Ketchup": "Кетчуп",
    "z musem bananowym, 50% mniej cukru": "з банановим мусом, на 50% менше цукру",
    "z przecierem bananowym, 50% mniej cukru": "з банановим пюре, на 50% менше цукру",
    "Bez dodatku konserwantów i barwników": "Без додавання консервантів і барвників",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def translate_line(line: str) -> str:
    translated = line
    for source, target in sorted(TERM_MAP, key=lambda item: len(item[0]), reverse=True):
        pattern = rf"(?<![A-Za-zÀ-ž]){re.escape(source)}(?![A-Za-zÀ-ž])"
        translated = re.sub(pattern, target, translated, flags=re.I)
    translated = re.sub(r"(?<![A-Za-zÀ-ž])ze(?![A-Za-zÀ-ž])", "з", translated, flags=re.I)
    translated = re.sub(r"(?<![A-Za-zÀ-ž])z(?![A-Za-zÀ-ž])", "з", translated, flags=re.I)
    translated = re.sub(r"(?<![A-Za-zÀ-ž])i(?![A-Za-zÀ-ž])", "і", translated, flags=re.I)
    translated = re.sub(r"(?<![A-Za-zÀ-ž])do(?![A-Za-zÀ-ž])", "до", translated, flags=re.I)
    translated = re.sub(r"(?<![A-Za-zÀ-ž])bez(?![A-Za-zÀ-ž])", "без", translated, flags=re.I)
    translated = re.sub(r"(?<![A-Za-zÀ-ž])na(?![A-Za-zÀ-ž])", "на", translated, flags=re.I)
    translated = re.sub(r"(?<![A-Za-zÀ-ž])po(?![A-Za-zÀ-ž])", "по", translated, flags=re.I)
    translated = translated.replace("по по-", "по-")
    translated = re.sub(r"\b(\d+)\s?g\b", r"\1 г", translated, flags=re.I)
    return translated


def translate_ocr_line(line: str) -> str:
    exact = OCR_EXACT_TRANSLATIONS.get(line)
    if exact:
        return exact
    return translate_line(line)


def ua_title(title: str) -> str:
    title = re.sub(r"\s+[–-]\s+", " - ", title)
    return translate_line(title)


def weight_line(product: dict) -> str:
    match = re.search(r"\b(\d+)\s*g\b", product["title"], flags=re.I)
    return f"{match.group(1)} g" if match else ""


def ocr_lines(product: dict) -> list[str]:
    asin = product["asin"]
    category = product["category"]
    label, detail = OCR_LABELS[asin]
    lines = ["PRIPRAVKA"]
    if category == "Exclusive Professional":
        lines += ["Przyprawy poddane obróbce parą", "Exclusive Professional", "Naturalna przyprawa grubo mielona", label]
        if detail:
            lines.append(detail)
        if asin in EXCLUSIVE_SALT_ONLY or asin in EXCLUSIVE_SALT_PERLA or "bez Soli" in product["title"] or "bez soli" in product["title"]:
            lines.append("Bez dodatku soli")
        if asin in EXCLUSIVE_SALT_PERLA:
            lines.append("Perła Rynku 2025")
        lines += ["7 etapów oczyszczania", "Propozycja podania"]
    elif category == "Grill & BBQ":
        target = "Naturalna przyprawa do ryb i owoców morza" if asin == "B0GWQFM1RN" else "Naturalna przyprawa do mięsa i kurczaka"
        lines += ["GRILL & BBQ", target, label]
        if detail:
            lines.append(detail)
        if asin in GRILL_BBQ_BADGES:
            lines += [
                "100% naturalnych składników",
                "Bez dodatku glutaminianu monosodowego, barwników i konserwantów",
            ]
        lines += [
            "Sposoby przygotowania",
            "Patelnia",
            "Kuchenka mikrofalowa",
            "Piekarnik",
            "Grill",
            "Zero cukru",
            "Zdjęcie symboliczne",
            "* Dodatek cukru 0% / Доданого цукру 0%",
        ]
    elif category == "O-o-o, Jakie ziemniaki":
        lines += ["O-o-o, jakie ziemniaki", label]
        if asin in ZIEMNIAKI_PERLA:
            lines.append("Perła Rynku 2025")
        if detail:
            lines.append(detail)
        target = "Naturalna przyprawa do ziemniaków i warzyw" if asin in {"B0GWQ8F15V", "B0GWQ686KL", "B0GWPZJZFN"} else "Naturalna przyprawa do ziemniaków"
        lines += [target, "Propozycja podania", "Zeskanuj smartfonem i pysznie ugotuj"]
    elif category == "Przyprawy poddane obróbce parą":
        heading = "Mieszanka przyprawowa" if asin in PEPPER_MIX_PACKS else "Naturalna przyprawa"
        lines += ["Przyprawy poddane obróbce parą", heading, label]
        if asin == "B0GR5XXM78":
            lines.append("mielony z dodatkiem chili ancho")
        elif detail:
            lines.append(detail)
        if asin in STEAM_ZIOLA_SALT:
            lines.append("Bez dodatku soli")
        if asin not in PEPPER_MIX_PACKS:
            lines.append("Zero cukru")
        lines += ["100% naturalny produkt", "Zdjęcie symboliczne"]
        if asin in STEAM_HERB_QR_HEADLINE:
            lines.append("Czego dziś dowiesz o naszej przyprawie?")
        else:
            lines.append("Dlaczego sterylizujemy nasze przyprawy?")
        lines.append("Zeskanuj kod QR, dowiedz się więcej")
        if asin in STEAM_SUGAR_FOOTNOTE:
            lines.append("* Dodatek cukru 0% / Доданого цукру 0%")
    elif category == "Sosy WOK":
        lines += [label]
        if detail:
            lines.append(detail)
        lines += [
            "Światowej klasy mistrz kuchni",
            "Odkryj zwariowany świat AI-AZJI",
            "Rozmawiaj z wirtualnym szefem kuchni, generuj obrazy*",
            "* Treści na stronie zostały wygenerowane przez AI",
            "140 g",
        ]
    elif category == "Ketchup":
        lines += [label]
        if detail:
            lines.append(detail)
        if asin in KETCHUP_APPLE_LIFEHACK:
            lines += ["Z octem jabłkowym", "Zobacz lifehacki o jakości ketchupu!"]
        lines += ["Bez dodatku konserwantów i barwników"]
    weight = weight_line(product)
    if weight and weight not in lines:
        lines.append(weight)
    return lines


def short_description(product: dict) -> str:
    title = product["title"]
    parts = re.split(r"\s+[–-]\s+", title, maxsplit=1)
    if len(parts) > 1:
        return parts[1]
    return f"Amazon-title dla ASIN {product['asin']}."


def render() -> None:
    products = json.loads(DATA.read_text(encoding="utf-8"))
    cards = []
    for product in products:
        lines = ocr_lines(product)
        translated_lines = [translate_ocr_line(line) for line in lines]
        title_ua = ua_title(product["title"])
        description = short_description(product)
        description_ua = ua_title(description)
        image = product.get("image_path", "")
        image_html = f'<img src="{esc(image)}" alt="{esc(product["title"])}" />' if image else '<div class="missing-image">Brak zdjęcia</div>'
        cards.append(
            f"""
            <article class="product-card" data-asin="{esc(product['asin'])}" data-category="{esc(product['category'])}">
              <section class="pack">
                <div class="pack-top">
                  <span class="tag">{esc(product['category'])}</span>
                  <span class="tag light">{esc(product['asin'])}</span>
                </div>
                <figure>{image_html}</figure>
                <div class="pack-meta">
                  <div><span>ASIN</span><strong>{esc(product['asin'])}</strong></div>
                  <div><span>Źródło</span><strong>Amazon.pl</strong></div>
                  <div><span>Seria</span><strong>{esc(product['category'])}</strong></div>
                  <div><span>Obraz</span><strong>{'lokalny' if image else 'do sprawdzenia'}</strong></div>
                </div>
              </section>
              <section class="translation">
                <div class="card-head">
                  <h2 class="editable">{esc(product['title'])}</h2>
                  <a class="button" href="{esc(product['url'])}">Amazon</a>
                </div>
                <table>
                  <thead><tr><th>Sekcja</th><th>Polski tekst</th><th>Український переклад</th></tr></thead>
                  <tbody>
                    <tr><td class="section-col editable">Amazon title</td><td class="editable">{esc(product['title'])}</td><td class="editable">{esc(title_ua)}</td></tr>
                    <tr><td class="section-col editable">Opis z karty</td><td class="editable">{esc(description)}</td><td class="editable">{esc(description_ua)}</td></tr>
                    <tr><td class="section-col editable">Kontrola</td><td class="editable">Sprawdzić zgodność Amazon-title, ASIN, serii i zdjęcia opakowania.</td><td class="editable">Перевірити відповідність Amazon-title, ASIN, серії та фото упаковки.</td></tr>
                  </tbody>
                </table>
                <section class="image-ocr">
                  <h3>OCR з пачки / переклад</h3>
                  <div class="ocr-grid">
                    <div class="ocr-box">
                      <span>Rozpoznany tekst z opakowania</span>
                      <p class="editable">{esc(chr(10).join(lines))}</p>
                    </div>
                    <div class="ocr-box">
                      <span>Український переклад OCR</span>
                      <p class="editable">{esc(chr(10).join(translated_lines))}</p>
                    </div>
                  </div>
                  <p class="ocr-note editable">Аудит OCR: внесено основні великі написи, видимі на головному фото Amazon. Дуже дрібні службові написи та частина QR-пояснень потребують ручної перевірки у збільшенні.</p>
                </section>
              </section>
            </article>
            """
        )

    total = len(products)
    html_doc = f"""<!doctype html>
<html lang="uk">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Pripravka Amazon PL / UA Product Cards</title>
    <style>
      :root {{ --ink:#151515; --muted:#625c54; --line:#ddd6c9; --paper:#fbfaf6; --panel:#fff; --black:#151515; --gold:#d6a51f; --red:#b94632; --green:#4f6f52; --ok:#247348; --warn:#a86612; --shadow:0 16px 38px rgba(33,28,20,.11); }}
      * {{ box-sizing:border-box; }}
      body {{ margin:0; font-family:Arial,"Arial Unicode MS",system-ui,sans-serif; background:var(--paper); color:var(--ink); }}
      a {{ color:inherit; }}
      .top-strip {{ height:12px; background:linear-gradient(90deg,var(--gold),var(--red),var(--green)); }}
      .page {{ width:min(1500px,calc(100% - 38px)); margin:0 auto; padding:26px 0 52px; }}
      header {{ display:grid; grid-template-columns:minmax(0,1fr) auto; gap:22px; align-items:end; margin-bottom:18px; }}
      h1 {{ margin:0; font-size:clamp(34px,4vw,58px); line-height:1; letter-spacing:0; }}
      .lead {{ max-width:960px; margin:10px 0 0; color:var(--muted); font-size:18px; line-height:1.45; }}
      .source {{ display:grid; gap:7px; min-width:310px; padding:14px 16px; border:1px solid var(--line); border-radius:8px; background:#fff; color:var(--muted); font-size:14px; }}
      .source strong {{ color:var(--ink); }}
      .controls {{ position:sticky; top:0; z-index:10; display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:18px; padding:12px; border:1px solid var(--line); border-radius:8px; background:rgba(255,255,255,.94); box-shadow:0 8px 20px rgba(31,26,18,.08); backdrop-filter:blur(10px); }}
      button,.button {{ display:inline-flex; align-items:center; justify-content:center; min-height:42px; padding:0 14px; border:1px solid var(--black); border-radius:8px; background:var(--black); color:#fff; font:inherit; font-size:14px; font-weight:800; text-decoration:none; cursor:pointer; }}
      button.secondary {{ border-color:var(--line); background:#fff; color:var(--ink); }}
      .status {{ margin-left:auto; color:var(--muted); font-size:14px; font-weight:800; }}
      .audit-panel {{ display:grid; gap:8px; margin-bottom:18px; padding:14px 16px; border:1px solid var(--line); border-radius:8px; background:#fff; }}
      .audit-panel h2 {{ margin:0; font-size:20px; }}
      .audit-list {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; margin:0; padding:0; list-style:none; }}
      .audit-list li {{ padding:10px 12px; border:1px solid var(--line); border-radius:8px; background:#faf8f2; color:var(--muted); font-size:14px; }}
      .ok strong {{ color:var(--ok); }} .warn strong {{ color:var(--warn); }}
      .products {{ display:grid; gap:18px; }}
      .product-card {{ display:grid; grid-template-columns:minmax(280px,32%) minmax(0,1fr); overflow:hidden; border:1px solid var(--line); border-radius:8px; background:var(--panel); box-shadow:var(--shadow); }}
      .pack {{ display:grid; grid-template-rows:auto 1fr auto; border-right:1px solid var(--line); background:linear-gradient(180deg,#fff,#f3efe8); }}
      .pack-top {{ display:flex; flex-wrap:wrap; gap:8px; padding:16px 16px 0; }}
      .tag {{ display:inline-flex; align-items:center; min-height:30px; padding:6px 10px; border-radius:999px; background:var(--black); color:#fff; font-size:12px; font-weight:900; }}
      .tag.light {{ border:1px solid var(--line); background:#fff; color:var(--ink); }}
      figure {{ display:grid; place-items:center; margin:0; padding:20px; }}
      figure img {{ width:min(100%,420px); max-height:430px; object-fit:contain; mix-blend-mode:multiply; }}
      .pack-meta {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; padding:0 16px 16px; }}
      .pack-meta div {{ min-height:58px; padding:10px; border:1px solid var(--line); border-radius:8px; background:#fff; }}
      .pack-meta span {{ display:block; margin-bottom:3px; color:var(--muted); font-size:11px; font-weight:900; text-transform:uppercase; }}
      .pack-meta strong {{ display:block; overflow-wrap:anywhere; font-size:15px; }}
      .translation {{ display:grid; min-width:0; padding:18px; }}
      .card-head {{ display:grid; grid-template-columns:minmax(0,1fr) auto; gap:12px; align-items:start; margin-bottom:14px; }}
      .card-head h2 {{ margin:0; font-size:clamp(20px,2vw,30px); line-height:1.12; letter-spacing:0; }}
      table {{ width:100%; border-collapse:collapse; table-layout:fixed; border:1px solid var(--line); }}
      th,td {{ border:1px solid var(--line); padding:11px 12px; vertical-align:top; overflow-wrap:anywhere; line-height:1.32; }}
      th {{ background:var(--black); color:var(--gold); text-align:left; font-size:13px; text-transform:uppercase; }}
      td {{ background:#fff; font-size:15px; }}
      tr:nth-child(even) td {{ background:#f8f4ec; }}
      .section-col {{ width:19%; font-weight:900; }}
      .image-ocr {{ display:grid; gap:10px; margin-top:14px; padding:14px; border:1px solid var(--line); border-radius:8px; background:#fcfaf5; }}
      .image-ocr h3 {{ margin:0; font-size:18px; line-height:1.2; }}
      .ocr-grid {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:10px; }}
      .ocr-box {{ padding:12px; border:1px solid var(--line); border-radius:8px; background:#fff; }}
      .ocr-box span {{ display:block; margin-bottom:7px; color:var(--muted); font-size:11px; font-weight:900; text-transform:uppercase; }}
      .ocr-box p {{ margin:0; line-height:1.38; white-space:pre-line; }}
      .ocr-note {{ margin:0; color:var(--muted); font-size:13px; line-height:1.35; }}
      body.editing .editable {{ outline:2px dashed rgba(214,165,31,.75); outline-offset:3px; cursor:text; }}
      body.editing .editable:focus {{ outline:3px solid var(--gold); background:#fffdf4; }}
      footer {{ margin-top:24px; color:var(--muted); font-size:13px; line-height:1.45; }}
      @media(max-width:980px){{ header,.product-card,.card-head{{grid-template-columns:1fr}} .source{{min-width:0}} .pack{{border-right:0;border-bottom:1px solid var(--line)}} .audit-list,.ocr-grid{{grid-template-columns:1fr}} }}
      @media(max-width:640px){{ .page{{width:min(100% - 28px,720px);padding-top:20px}} .controls{{position:static}} .status{{flex-basis:100%;margin-left:0}} .pack-meta{{grid-template-columns:1fr}} table,thead,tbody,tr,th,td{{display:block;width:100%}} thead{{display:none}} td::before{{display:block;margin-bottom:4px;color:var(--muted);font-size:11px;font-weight:900;text-transform:uppercase}} td:nth-child(1)::before{{content:"Sekcja"}} td:nth-child(2)::before{{content:"Polski tekst"}} td:nth-child(3)::before{{content:"Український переклад"}} }}
    </style>
  </head>
  <body>
    <div class="top-strip" aria-hidden="true"></div>
    <main class="page">
      <header>
        <div>
          <h1>Pripravka Amazon PL / UA</h1>
          <p class="lead">Картки Amazon Pripravka: фото пачки поруч із таблицею польського тексту й українського перекладу. Окремий OCR-блок містить текст, розпізнаний з головного зображення упаковки.</p>
        </div>
        <aside class="source">
          <strong>Źródło: Amazon.pl</strong>
          <span>Перевірено: 2026-06-03</span>
          <span>Карток: {total}</span>
          <span>Фото: {sum(1 for p in products if p.get('image_path'))}</span>
        </aside>
      </header>
      <section class="controls">
        <button id="editToggle" type="button">Увімкнути редагування</button>
        <button class="secondary" id="runAudit" type="button">Провести аудит</button>
        <button class="secondary" id="exportHtml" type="button">Експортувати HTML</button>
        <button class="secondary" id="resetEdits" type="button">Скинути правки</button>
        <button class="secondary" type="button" onclick="window.print()">Друк / PDF</button>
        <span class="status" id="status">Режим перегляду</span>
      </section>
      <section class="audit-panel"><h2>Аудит</h2><ul class="audit-list" id="auditList"></ul></section>
      <section class="products">{''.join(cards)}</section>
      <footer>OCR-блоки сформовані за видимими великими написами на головних фото Amazon. Дрібний службовий текст потребує ручної перевірки у збільшенні. Усі поля таблиць і OCR редагуються та можуть бути експортовані в окремий HTML.</footer>
    </main>
    <script>
      const storageKey = "pripravka-amazon-product-cards-v3";
      const editableNodes = [...document.querySelectorAll(".editable")];
      const statusNode = document.querySelector("#status");
      const editToggle = document.querySelector("#editToggle");
      function setEditing(enabled) {{
        document.body.classList.toggle("editing", enabled);
        editableNodes.forEach((node) => {{ node.contentEditable = String(enabled); node.spellcheck = true; }});
        editToggle.textContent = enabled ? "Вимкнути редагування" : "Увімкнути редагування";
        statusNode.textContent = enabled ? "Режим редагування" : "Режим перегляду";
      }}
      function saveEdits() {{
        localStorage.setItem(storageKey, JSON.stringify(editableNodes.map((node) => node.innerHTML)));
        statusNode.textContent = document.body.classList.contains("editing") ? "Правки збережено" : "Режим перегляду";
      }}
      function loadEdits() {{
        const raw = localStorage.getItem(storageKey);
        if (!raw) return;
        try {{
          const payload = JSON.parse(raw);
          editableNodes.forEach((node, index) => {{ if (typeof payload[index] === "string") node.innerHTML = payload[index]; }});
        }} catch {{ localStorage.removeItem(storageKey); }}
      }}
      function hasCyrillic(text) {{ return /[А-Яа-яІіЇїЄєҐґ]/.test(text); }}
      function hasPolishSignal(text) {{ return /[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]|\\bPripravka\\b|\\bNaturalna\\b|\\bPrzyprawa\\b|\\bKetchup\\b|\\bWOK\\b/i.test(text); }}
      function hasPolishResidue(text) {{
        const cleaned = text
          .replace(/PRIPRAVKA/g, "")
          .replace(/Exclusive Professional/g, "")
          .replace(/GRILL & BBQ/g, "")
          .replace(/WOK\\s+(ASIAN|CHOW MEIN|KUNG PAO|PAD THAI|SPICY HOT)/g, "");
        return /\\b(z|ze|i|do|bez|na|po|etapów|oczyszczania|Sposoby|przygotowania|naturalna|przyprawa|mieszanka|cukru|kod|dowiedz|więcej|sokiem|pomarańczowym|wędzonymi|pomidorami|musztardą|limonki|liśćmi|żytnim|bekonu|karmelizowanej|cebuli|czosnkiem|kolendrą|bazylią|rozmarynem|lawendą|gorczycy|borowikami|konserwantów|barwników)\\b/i.test(cleaned);
      }}
      function audit() {{
        const cards = [...document.querySelectorAll(".product-card")];
        const images = [...document.images];
        const loadedImages = images.filter((img) => img.complete && img.naturalWidth > 0);
        const tables = [...document.querySelectorAll("table")];
        const ocrSections = [...document.querySelectorAll(".image-ocr")];
        const ocrOriginals = [...document.querySelectorAll(".ocr-box:first-child p")];
        const ocrTranslations = [...document.querySelectorAll(".ocr-box:nth-child(2) p")];
        const uaCells = [...document.querySelectorAll("tbody td:nth-child(3)")];
        const empty = editableNodes.filter((node) => node.textContent.trim().length === 0);
        const missingUa = uaCells.filter((node) => !hasCyrillic(node.textContent));
        const missingOcrPl = ocrOriginals.filter((node) => !hasPolishSignal(node.textContent));
        const missingOcrUa = ocrTranslations.filter((node) => !hasCyrillic(node.textContent));
        const ocrUaWithResidue = ocrTranslations.filter((node) => hasPolishResidue(node.textContent));
        const uaCellsWithResidue = uaCells.filter((node) => hasPolishResidue(node.textContent));
        const titleWithoutBrand = [...document.querySelectorAll(".card-head h2")].filter((node) => !/Pripravka/i.test(node.textContent));
        const items = [
          ["Картки", cards.length === {total}, `Знайдено ${{cards.length}} з {total}.`],
          ["Зображення", loadedImages.length === images.length && images.length === {total}, `Завантажено ${{loadedImages.length}} з ${{images.length}} фото.`],
          ["Таблиці", tables.length === {total}, `Знайдено ${{tables.length}} таблиць PL / UA.`],
          ["OCR-блоки", ocrSections.length === {total}, `Знайдено ${{ocrSections.length}} OCR-блоків.`],
          ["OCR PL", missingOcrPl.length === 0, `OCR-блоків без польського сигналу: ${{missingOcrPl.length}}.`],
          ["OCR UA", missingOcrUa.length === 0, `OCR-перекладів без кирилиці: ${{missingOcrUa.length}}.`],
          ["OCR UA residue", ocrUaWithResidue.length === 0, `OCR-перекладів із польськими залишками: ${{ocrUaWithResidue.length}}.`],
          ["Переклад", missingUa.length === 0, `UA-комірок без кирилиці: ${{missingUa.length}}.`],
          ["Переклад residue", uaCellsWithResidue.length === 0, `UA-комірок із польськими залишками: ${{uaCellsWithResidue.length}}.`],
          ["Порожні поля", empty.length === 0, `Порожніх редагованих полів: ${{empty.length}}.`],
          ["Brand у title", titleWithoutBrand.length === 0, `Title без Pripravka: ${{titleWithoutBrand.length}}.`],
        ];
        document.querySelector("#auditList").innerHTML = items.map(([name, ok, text]) => `<li class="${{ok ? "ok" : "warn"}}"><strong>${{ok ? "OK" : "Увага"}} - ${{name}}</strong><span>${{text}}</span></li>`).join("");
        statusNode.textContent = items.every(([, ok]) => ok) ? "Аудит пройдено" : "Аудит має попередження";
      }}
      function exportHtml() {{
        const clone = document.documentElement.cloneNode(true);
        clone.querySelectorAll("[contenteditable]").forEach((node) => node.removeAttribute("contenteditable"));
        clone.querySelector("body").classList.remove("editing");
        const blob = new Blob(["<!doctype html>\\n" + clone.outerHTML], {{ type: "text/html;charset=utf-8" }});
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "pripravka-amazon-pl-ua-edited.html";
        link.click();
        URL.revokeObjectURL(link.href);
      }}
      loadEdits(); setEditing(false); audit();
      window.addEventListener("load", audit);
      document.querySelectorAll("img").forEach((img) => img.addEventListener("load", audit));
      editableNodes.forEach((node) => node.addEventListener("input", saveEdits));
      editToggle.addEventListener("click", () => setEditing(!document.body.classList.contains("editing")));
      document.querySelector("#runAudit").addEventListener("click", audit);
      document.querySelector("#exportHtml").addEventListener("click", exportHtml);
      document.querySelector("#resetEdits").addEventListener("click", () => {{ localStorage.removeItem(storageKey); location.reload(); }});
    </script>
  </body>
</html>
"""
    OUT.write_text(html_doc, encoding="utf-8")
    print(OUT)
    print(f"cards={total}")


if __name__ == "__main__":
    render()
