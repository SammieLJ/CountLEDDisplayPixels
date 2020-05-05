#!/usr/bin/env python3
from os.path import abspath, exists
import os.path, sys

"""
Hackatlon test - Preračunavanje zasedenosti teksta na poljubnem zaslonu

Program prikaže koliko znakov se bo prikazalo in 
koliko znakov se še lahko prikaže, če je še prostor na zaslonu.

Author: Samir Subašić
Last modified: 25 March 2020
Website: www.github.com/samirsub
"""

STARTING_FONT_SIZE = 1 # default naj bo 1


def find_longest_word(word_list):  
    longest_word =  max(word_list, key=len)
    return longest_word

def string_len(s):
    return len(s)

def check_text_size_on_screen(font_size, besede, sirina_zaslona, visina_zaslona):
    # razrežemo (prelomimo) besede, glede širine zaslona
    vrstice = []; vrstica = []
    from_index = 0; to_index = 0
    besede = sorted(besede, key=string_len)
    vrstice = besede
    for beseda in besede:
        vrstica.append(beseda)
        temp_vrstica = ' '.join(vrstica)

        if font_size * len(temp_vrstica) >= int(sirina_zaslona) :
            vrstica = []
            # vrstice = [" ".join(vrstice[from_index:to_index])]+vrstice[to_index:]
            if from_index == 0:
                vrstice = [" ".join(vrstice[from_index:to_index])]+vrstice[to_index:]
            else:
                vrstice = vrstice[:from_index]+[" ".join(vrstice[from_index:to_index])]+vrstice[to_index:]
            to_index=to_index+1
            from_index = to_index
        else:
            to_index=to_index+1

    # pripravimo še širino najdajšega prelomljenega teksta
    if len(vrstice) != 0:
        najdaljsa_vrstica = find_longest_word(vrstice)
    else:
        najdaljsa_vrstica = ""

    # preverimo višino in širino teksta, ki se bi prikazal za določeno višino fonta
    if (font_size * len(vrstice)) <=  int(visina_zaslona) and (font_size * len(najdaljsa_vrstica)) <= int(sirina_zaslona) :
        return True
    else:
        return False


def calculate_display_pixels(line):
    # Izpiše Prikazano: Neprikazano: Rezerva:

    # razdeli (z uporabo presledka) samo prva dva podatka, 
    # tako da bosta v tabeli [širina, višina, tekst]
    one_line = line.split(' ', 2)

    # izračunaj velikost poljubnega zaslona iz podatkov posamezne vrstice iz datoteke vhodi.txt
    #display_pixel_size = int(one_line[0]) * int(one_line[1])
    sirina_zaslona = one_line[0]
    visina_zaslona = one_line[1]
    print("Velikost zaslona širina " + sirina_zaslona + ", višina " + visina_zaslona)
    
    # nastavi, koliko znakov naj se prikaže na poljubnem zaslonu
    num_of_letters_to_display = len(one_line[2])
    print("Tekst: " + one_line[2])
    print("Št. znakov za prikazat: " + str(num_of_letters_to_display))

    # najdi najdaljšo besedo
    besede = one_line[2].split()
    najdaljsa_beseda = find_longest_word(besede)
    print("Najdaljša beseda je: " + najdaljsa_beseda + " šr. črk: " + str(len(najdaljsa_beseda)))

    najvecja_velikost_fonta = 0
    # povečujemo velikost fonta, meja je višina zaslona
    for font_size in range(STARTING_FONT_SIZE, int(visina_zaslona)) :
        # preverimo, če najdaljša beseda lahko se izpise na zaslonu
        if ((font_size * len(najdaljsa_beseda)) < int(sirina_zaslona)):
            # prelomimo tekst, da vidimo, če gre lahko celoten na ekran
            if check_text_size_on_screen(font_size, besede, sirina_zaslona, visina_zaslona):
                najvecja_velikost_fonta = font_size
        else:
            print(".....................")
            break
        
    print() #nova vrstica
    return najvecja_velikost_fonta

def main():

    # Preberi datoteko vhodi.txt, lines je tabela, ki za vrednost vsebuje vsako vrstico
    #f_path = abspath('vhodi.txt')
    #f_path = os.path.join(sys.path[0], 'some file.txt')
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f_path = os.path.join(__location__, 'vhodi.txt')
    print(f_path)

    if exists(f_path):
        with open(f_path) as f:
            lines = [line.rstrip() for line in f]
        
        izhod = []
        # tukaj sprožimo zanko, ki se sprehodi skozi vse vrstice v vhodi.txt
        for line in lines:
            izhod.append(calculate_display_pixels(line))

        # izpis rezultatov v izhod.txt
        f = open('izhod.txt', 'w')
        for izhodna_vrstica in izhod:
            f.write(str(izhodna_vrstica) + '\n')
        f.close()
    else:
        print("Ne najdem datoteke za branje vhodnih podatkov!")

# nastavimo, katera funkcija bo main, torej glavna funkcija programa
if __name__ == '__main__':
    main()
