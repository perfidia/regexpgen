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
przykłady poprawne: 22.1, 1.1
przykłady niepoprawne: 001.2, 012.9

FORMAT = '%0.Ylf'
opis: zera wiodące są niedowolone, po przecinku można wprowadzić dokładnie Y cyfr
przykłady poprawne: 22.1, 1.1
przykłady niepoprawne: 001.2, 012.9

FORMAT = '%.Ylf'
opis: zera wiodące są opcjonalne, po przecinku można wprowadzić dokładnie Y cyfr
przykłady poprawne: 022.1, 1.1, 001.2, 012.9

FORMAT = '%X.Ylf'
opis: X jest ignorowany (działa jak '%.Ylf')

FORMAT = '%0X.Ylf'
opis: zera wiodące są wymagane, liczba jest zapisana przy wykorzystaniu co najmniej X znaków (łącznie z kropoką),
      po przecinku można wprowadzić dokładnie Y cyfr,
      jeżeli liczba zaweira mniej niż X znaków to przestrzeń należy wypełnić zerami
przykłady poprawne dla %5.2lf: 022.1, 32431.2, 012.9
przykłady poprawne dla %5.2lf: 22.1, 111.122
'''
import builder
from regexpgen.misc import assertMinMax

SEPARATOR = '.'

def run(format, min, max):
    assertMinMax(min, max)

    b = builder.RegexBuilder()
    return  b.CreateRealRegex(format, min, max)

