# -*- coding: utf-8 -*-

'''
Created on Apr 27, 2011

@author: Bartosz Alchimowicz

Generowanie wyrażenie regularnego dla daty i czasu.
Data obsługuje lata przestępne.

Supported format:

%d    dzień miesiąca (01..31)
%H    godzina (00..23)
%I    godzina (00..12)
%m    numer miesiąca (01..12)
%M    minuty (00..59)
%p    AM lub PM
%P    am lub pm
%S    sekundy (00..59)
%y    dwie ostatnich cyfr roku (00..99)
%Y    rok (1997..)

Przykłady:

date "%Y-%m-%d" zakres: 2009-03-15..2009-10-15
time "%H:%M"
time "%H:%M" zakres: 11:00..12:00+01    // strefa czasowa +01 jest opcjonalna
datetime "%H:%M" zakres: 11:00..12:00+01
datetime "%Y-%m-%d %H:%M" zakres: 2009-10-10 11:15..2009-10-10 12:15 +01 // strefa czasowa +01 jest opcjonalna
datetime "%Y%m%d %H:%M"
datetime "%Y-%m-%d %H:%M:%S"

Proszę zwrócic uwagę na obecność separatorów (np. - : )
Zakresy przekazywane jako string
'''

def run(format, date_min = None, date_max = None, time_min = None, time_max = None, timezone = None):
    raise Exception('unsupported')
