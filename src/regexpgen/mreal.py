# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla liczba reczywistych.

Supported format:

FORMAT = '%lf'
opis: zera wiodące są dozwolone,
przykłady poprawne: 0.1, 1.32, 001.21, 012.123

FORMAT = '%0lf'
opis: zera wiodące są niedowolone
przykłady poprawne: 022.1, 1.1
przykłady niepoprawne: 001.2, 012.9

FORMAT = '%0.Ylf'
opis: zera wiodące są niedowolone, po przecinku można wprowadzić maksymalnie Y cyfr
przykłady poprawne: 022.1, 1.1
przykłady niepoprawne: 001.2, 012.9

FORMAT = '%.Ylf'
opis: zera wiodące są opcjonalne, po przecinku można wprowadzić maksymalnie Y cyfr
przykłady poprawne: 022.1, 1.1, 001.2, 012.9

FORMAT = '%X.Ylf'
opis: zera wiodące są opcjonalne, liczba jest zapisana przy wykorzystaniu X znaków (łącznie z kropoką),
      po przecinku można wprowadzić maksymalnie Y cyfr
przykłady poprawne dla %5.2lf: 022.1, 111.1, 001.2, 012.9
przykłady poprawne dla %5.2lf: 22.1, 111.122

FORMAT = '%0X.Ylf'
opis: zera wiodące są wymagane, liczba jest zapisana przy wykorzystaniu X znaków (łącznie z kropoką),
      po przecinku można wprowadzić maksymalnie Y cyfr, jeżeli liczba zaweira mniej niż X znaków to
      przestrzeń należy wypełnić zerami
przykłady poprawne dla %5.2lf: 022.1, 32431.2, 012.9
przykłady poprawne dla %5.2lf: 22.1, 111.122
'''

SEPARATOR = '.'

def run(format, min, max):
	raise Exception('unsupported')
