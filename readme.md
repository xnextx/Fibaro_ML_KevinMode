# Machine Learning KevinMode

## PL

### Opis projektu
Całe oświetlenie w domu składa się z kilkudziesięciu żarówek połączonych z systemem fibaro.

Zbieramy wszystkie zmiany stanu dla każdej żarówki i zapisujemy do bazy danych.

Następnie na podstawie tych danych, codziennie wieczorem uruchamiany jest trening, który uczy się następującego wzorca:
```{minuta po północy}, {miesiąc roku}, {dzień tygodnia} = {stan żarówki}```

System uczy się przy pomocy klasyfikatora lasów losowych, gdzie 33% danych które dostaje, traktuje jako elementy testowe, na reszcie się uczy.
Jeżeli dla procesu nauki jednej żarówki, ilość poprawnych odpowiedzi jest większa niż 51%, żarówka dodawana jest do spisu "wyuczonych".

Jeżeli użytkownik inteligentnego domu, zadecyduje się włączyć tryb KevinMode, system fibaro zacznie co minutę odpytywać o stan wszystkich żarówek, następnie na podstawie otrzymanych danych włączy/wyłączy konkretne egzemplarze.
Dzięki temu, gdy nikogo w domu nie będzie, dom wyuczając się wzorców na podstawie danych, które już były w systemie fibaro przed wprowadzeniem KevinMode (oraz powiększających się codziennie o nowe próbki) jest wstanie symulować przebywanie w nim. Jest to dodatkowe rozszerzenie już działającego systemu zabezpieczającego dom.

W planach mamy jeszcze naukę systemu konkretnego natężenia światła.

### Techniczna część
#### Docker
Całość została opakowana w 2 kontenery dockerowe:

* postgres
* api
 * flask
 * pandas
 * sklearn

#### API
##### [GET] /get_lights
###### Parametry:
* lights = id żarówki, id żarówki

###### Opis:
Zwraca stan dla każdej odpytywanej żarówki w formie tablicy JSON (0, 1 lub ERROR jeżeli żarówka nie mogła być dopisana do listy "wyuczonych")

##### [POST] /add_new_sample
###### Parametry:
* lightId - ID żarówki
* state - aktualny stan
* timestamp - timestamp zmiany
###### Opis:
Przyjmuje każdą zmianę stanu żarówki i zapisuje do bazy postgres.

##### [GET] /start_training
###### Parametry:
* brak

###### Opis:
Po wywołaniu rozpoczyna trening dla każdej z żarówek i zapisuje wyniki do katalogu models w formacie: lights_model_{id żarówki}

## [EN]
