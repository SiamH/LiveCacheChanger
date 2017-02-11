import re
import string
import time

# Replacing 'TODAY' token with YYYY-MM-DD format
def ConvertToday(sExpr):
    token = "${TODAY}"
    if sExpr.find(token) == -1:
        return sExpr

    value = time.strftime("%Y-%m-%d")
    sExpr = sExpr.replace(token, value)
    return sExpr

# Fidning tokens specific to four operations.
# Returning id of operations, key, value, full expression, criticalOrNot
def ParseExpr(sExpr):
    sExpr = ConvertToday(sExpr)

    SetExpr = r"SET ([a-zA-Z]+.*)=([a-zA-Z]+.*)";
    matches = re.findall(SetExpr, sExpr)
    if len(matches) > 0:
        return 1, matches[0][0], matches[0][1], sExpr, True

    ExpandExpr = r"EXPAND ([a-zA-Z]+.*) \${([a-zA-Z]+.*)}";
    matches = re.findall(ExpandExpr, sExpr)
    if len(matches) > 0:
        return 2, matches[0][1], "", sExpr, False

    DelExpr = r"DEL ([a-zA-Z]+.*)";
    matches = re.findall(DelExpr, sExpr)
    if len(matches) > 0:
        return 3, matches[0], "", sExpr, True

    ListExpr = r"LIST";
    matches = re.findall(ListExpr, sExpr)
    if len(matches) > 0:
        return 4, "", "", sExpr, False

    return -1, "", "", sExpr, False


def UnitTesting_Expr():
    sExpr = 'SET NAME=John'
    ids, key, value, data, needlock = ParseExpr(sExpr)
    assert (ids == 1)
    assert (key == 'NAME')
    assert (value == 'John')
    assert (needlock == True)

    sExpr = 'DEL NAME'
    ids, key, value, data, needlock = ParseExpr(sExpr)
    assert (ids == 3)
    assert (key == 'NAME')
    assert (value == '')
    assert (needlock == True)

    sExpr = 'LIST'
    ids, key, value, data, needlock = ParseExpr(sExpr)
    assert (ids == 4)
    assert (key == '')
    assert (value == '')
    assert (needlock == False)

    sExpr = 'EXPAND Hello, ${NAME}'
    ids, key, value, data, needlock = ParseExpr(sExpr)
    assert (ids == 2)
    assert (key == 'NAME')
    assert (value == '')
    assert (needlock == False)
