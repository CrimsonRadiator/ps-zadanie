# Zadanie backend dla Profil Software
## Opis
Program prezentujący statystki odnośnie zdawalności [matur](https://dane.gov.pl/dataset/1567/resource/17363) od 2010 do 2018, wykorzystujący sqlite3.

W przypadku gdy skrypt znajdzie w bieżącym katalogu plik `matura.db` wykorzystuje bazę danych do obliczeń. W przeciwnym wypadku, pobiera dane w formacie `.csv` z ww. storny i tworzy na jej podstawie bazę danych.
## Wymagania
- python3.7 skompilowany z obsługą libsqlite3-dev oraz libssl-dev
## Użycie
Aby uruchomić skrypt, wstarczy wpisać
```
python3.7 matura.py [-h] [-m | -f] [--filename FILENAME] COMMAND
```
Gdzie
- `-m` specyfikuje liczenie statystyk biorąc pod uwagę tylko wyniki mężczyzn.
- `-f` specyfikuje liczenie statystyk biorąc pod uwagę tylko wyniki kobiet.
- `COMMAND` jest jedną z komend:
  - `mean`
  - `yearly`
  - `best`
  - `regressive`
  - `compare`
### Komenda `mean`
użycie: `matura.py mean VOIVODESHIP YEAR`

Oblicza średnią zdawalność matur w województwie `VOIVODESHIP` od 2010 do `YEAR`.
### Komenda `yearly`
użycie: `matura.py yearly VOIVODESHIP`

Oblicza zdawalność w województwie `VOIVODESHIP` na przestrzeni lat.
### Komenda `best`
użycie: `matura.py best`

Wypisuje województwo o najlepszej zdawalności w danym roku na przestrzeni lat.
### Komenda `regressive`
użycie: `matura.py regressive`

Wypisuje województwa w których odnotowano spadek zdawalności względem poprzedniego roku.

### Komenda `compare`
użycie: `matura.py compare VOIVODESHIP1 VOIVODESHIP2`

Porównuje zdawalność województwa `VOIVODESHIP1` z województwem `VOIVODESHIP2` na przestrzeni lat, wypisując te które miało większą zdawalność w danym roku.
