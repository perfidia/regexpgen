# -*- coding: utf-8 -*-

'''
Set of functions to generate regular expressions from a pattern similar to printf function.
'''

import builder
import re
#import mdate, mtime, mdatetime

def integer(frmt, minV = None, maxV = None):
    """

    Generating regular expression for integer numbers.

    :param frmt: format similar to C printf function (description below)
    :param minV: optional minimum value
    :param maxV: optional maximum value
    :return: regular expression for a given format

    Generating regular expressions for integers (-2, -1, 0, 1, 2, 3...).

    Supported formats:

    FORMAT = '%d'
    description: leading zeros are optional,
    correct examples: -1, -005, 0, 1, 001, 012
    incorrect examples: N/A

    FORMAT = '%0d'
    description: leading zeros are forbidden
    correct examples: -2, -2123, 0, 1, 255
    incorrect examples: 001, 012

    FORMAT = '%0Xd'
    description: number written with X characters, in case of number lesser than int('9'*X) it should be leaded with zeros,
    correct examples for %04d: 0001, 5678
    incorrect examples for %04d: 00011, 111

    Examples of use:

    print regexpgen.integer("%0d", -10, 10)
    ^(-?([0-9]|10))$

    print regexpgen.integer("%04d", -10, 10)
    ^(-?(000[0-9]|0010))$

    """

    b = builder.RegexBuilder()
    return b.createIntegerRegex(frmt, minV, maxV)

def nnint(frmt, minV = None, maxV = None):
    """

    Generating regular expression for a non negative integer numbers.

    :param frmt: format similar to C printf function (description below)
    :param minV: optional minimum value
    :param maxV: optional maximum value
    :return: regular expression for a given format

    Generating regular expressions for non-negative integers (0, 1, 2, 3...).


    Supported formats:

    the same as for integers


    Examples of use:

    print regexpgen.nnint("%0d")
    ^([1-9][0-9]*|0)$

    print regexpgen.nnint("%04d", 71, 85)
    ^(007[1-9]|008[0-5])$

    """

    b = builder.RegexBuilder()
    return b.createNNIntegerRegex(frmt, minV, maxV)

def real(format, min = None, max = None):
    """
    Generating regular expressions for real numbers with accuracy of float() function.

    :param format: format similar to C printf function (description below)
    :param min: optional minimum value
    :param max: optional maximum value
    :return: regular expression for a given format

    Supported formats:

    FORMAT = '%lf'
    description: leading zeros are optional
    correct examples: 0.1, 1.32, 001.21, 012.123

    FORMAT = '%0lf'
    description: leading zeros are forbidden
    correct examples: 22.1, 1.1
    incorrect examples: 001.2, 012.9

    FORMAT = '%0.Ylf'
    description: leading zeros are forbidden, after the comma exactly Y characters are expected
    correct examples for %0.1lf: 22.1, 1.1
    incorrect examples for %0.1lf: 001.2, 012.9

    FORMAT = '%.Ylf'
    description: leading zeros are optional, after the comma exactly Y characters are expected
    correct examples for %0.1lf: 022.1, 1.1, 001.2, 012.9
    incorrect examples for %0.1lf: 3.222, 0.22

    FORMAT = '%X.Ylf'
    description: X  is ignored (works like '%.Ylf')

    FORMAT = '%0X.Ylf'
    description: leading zeros are required, number written with at least X characters (including dot),
          after the comma exactly Y characters are expected,
          if number of characters is lesser than X, it should be leaded with zeros
    correct examples for %5.1lf: 002.1, 32431.2, 022.9
    incorrect examples for %5.2lf: 22.111, 1.1


    Examples of use:

    print regexpgen.real("%lf", -1.5, 2.5)
    ^(-?(0*((0)\.0|(0)(\.(([0-9])[0-9]*))|(1)(\.(([0-3]|4)[0-9]*))|(1)\.50*))|0*((1)\.5|(1)(\.(5|([5-9])[0-9]*))|(2)(\.(([0-3]|4)[0-9]*))|(2)\.50*))$

    print regexpgen.real("%0.1lf", -1.0, 2.0)
    ^(-?(((0)\.(([0-9]))|(1)\.0))|((1)\.(([0-9]))|(2)\.0))$

    """

    b = builder.RegexBuilder()
    return b.createRealRegex(format, min, max)

def time(format, min = None, max = None):
    """
    Generating regular expressions for time.

    :param format: format similar to C printf function (description below)
    :param min: optional minimum value
    :param max: optional maximum value
    :return: regular expression for a given format

    Supported formats consists following syntaxes:

    %H    hours (00..23)
    %I    hours (00..12)
    %M    minutes (00..59)
    %S    seconds (00..59)
    %p    AM or PM
    %P    am or pm

    Additional information:

    :%I must come with %p or %P
    :%H can not come with %I, %p or %P
    :%P and %p can not come together
    :%H can not come with %S without %M
    :%P and %p can not be only syntaxes


    Examples of use:
    print regexpgen.time("%H:%M", "12:24", "17:59")
    ^(12\:(2[4-9]|[3-4][0-9]|5[0-9])|(1[3-5]|16)\:[0-5][0-9]|17\:[0-5][0-9])$

    print regexpgen.time("%I-%M-%S %P", "01-00-00 AM", None)
    ^(11\-00\-[0-5][0-9]\ PM|11\-(0[1-9]|1[0-9]|[2-4][0-9]|5[0-8])\-[0-5][0-9]\ PM|11\-59\-[0-5][0-9]\ PM)$

    """
    b = builder.RegexBuilder()
    return b.createTimeRegex(format, min, max)


def concatenate(concatenationList):
    result = ""
    for element in concatenationList:
        if len(element) == 1:
            result += element[0]
        elif len(element) == 4:
            if element[0] == "int":
                b = builder.RegexBuilder()
                result += b.createIntegerRegex(element[1], int(element[2]), int(element[3])).replace("^", "")
            elif element[0] == "real":
                result += b.createRealRegex(element[1], int(element[2]), int(element[3])).replace("^", "")
            else:
                raise ValueError("Bad input")
        else:
            raise ValueError("Bad input")
    return "^({0})$".format(result.replace("^", "").replace("$", ""))

#def date(format, min = None, max = None, timezone = None, matchStartEnd = True):
#    return startEndMatcher(mdate.run(format, min, max, timezone), matchStartEnd)
#
#def datetime(format, date_min = None, date_max = None, time_min = None, time_max = None, timezone = None, matchStartEnd = True):
#    return startEndMatcher(mdatetime.run(format, date_min, date_max, time_min, time_max, timezone), matchStartEnd)