import simpful as sf
import re
import numpy
from numpy import array
from simpful.rule_parsing import find_index_operator, OR, AND, AND_p, NOT

regex_clause_with_parentheses = re.compile(r"^\([a-z,_,A-Z,0-9]*\s*IS\s*[a-z,_,A-Z,0-9]*\)$")
regex_clause = re.compile(r"^[a-z,_,A-Z,0-9]*\s*IS\s*[a-z,_,A-Z,0-9]*$")


class IntervalClause(sf.Clause):
    """
    Class representing Interval Clause.
    """

    def evaluate_interval(self, IntervalFuzzySystem, verbose=False, operators=None):
        try:
            ans = IntervalFuzzySystem._lvs[self._variable].get_values(IntervalFuzzySystem._variables[self._variable])
        except KeyError:
            raise Exception("ERROR: variable '" + self._variable + "' not defined, or input value not given.\n"
                            + " ---- PROBLEMATIC CLAUSE:\n"
                            + str(self))
        if verbose:
            print("Checking if", self._variable, )
            print("whose value is", IntervalFuzzySystem._variables[self._variable], )
            print("is actually", self._term)
            print("answer:", ans[self._term])
        try:
            return ans[self._term]
        except KeyError:
            raise Exception("ERROR: term '" + self._term + "'' not defined.\n"
                            + " ---- PROBLEMATIC CLAUSE:\n"
                            + str(self))

    def __repr__(self):
        return "c.(%s IS %s)" % (self._variable, self._term)


class IntervalFunctional(sf.Functional):
    """
    Class representing Interval Functional.
    """

    def evaluate_interval(self, IntervalFuzzySystem):
        if self._A == "":
            # support for unary operators
            # print("Unary detected")
            B = self._B.evaluate_interval(IntervalFuzzySystem)
            return array(eval(self._fun + "(%s)" % B))
        else:
            A = self._A.evaluate_interval(IntervalFuzzySystem)
            B = self._B.evaluate_interval(IntervalFuzzySystem)
            # Temporary solution - start
            C = B
            if type(B) is numpy.ndarray:
                if B.size > 1:
                    C = B[0], B[1]
                else:
                    C = B
            if type(B) is tuple:
                if len(B) > 1:
                    C = B[0], B[1]
                else:
                    C = B
            if type(B) is float:
                C = B
            # Temporary solution - end
            return array(eval(self._fun + "(%s, %s)" % (A, C)))


# basic definitions of
def OR(x, y):
    """
    Definition of basic OR aggregator in rules
        :param x: first aggregated value
        :type x: tuple, float
        :param y: second aggregated value
        :type y: tuple, float
        :return: aggregated value
        :rtype: tuple, float
    """
    if type(x) is tuple and type(y) is tuple:
        return max(x[0], y[0]), max(x[1], y[1])
    else:
        return max(x, y)


def AND(x, y):
    """
    Definicja podstawowego agregatora AND w regułach jako agregacja średniej w przypadku przedziałów
    i funkcja min przy danych wejściowych typu float.
    """
    if isinstance(x, tuple) and isinstance(y, tuple):
        # Upewnij się, że obie zmienne są krotkami i operuj na każdym końcu przedziału oddzielnie
        return (min(x[0], y[0]), min(x[1], y[1]))
    elif isinstance(x, list) and isinstance(y, list):
        # Jeśli obie zmienne są listami, zamień je na krotki i wykonaj operację
        return (min(x[0], y[0]), min(x[1], y[1]))
    elif isinstance(x, list):
        # Jeśli x jest listą, zamień ją na krotkę
        x = tuple(x)
    elif isinstance(y, list):
        # Jeśli y jest listą, zamień ją na krotkę
        y = tuple(y)

    # Dla skalarnych wartości, zachowaj oryginalne zachowanie
    return min(x, y)


# def AND(x, y):
#     """
#     Definition of basic AND aggregator in rules as Mean aggregation in case intervals and min function when input data are floats
#         :param x: first aggregated value
#         :type x: tuple, float
#         :param y: second aggregated value
#         :type y: tuple, float
#         :return: aggregated value
#         :rtype: tuple, float
#     """
#     if type(x) is tuple and type(y) is tuple:
#         # return min(x[0], y[0]), min(x[1], y[1])
#         return (x[0] + y[0]) / 2.0, (x[1] + y[1]) / 2.0
#         # return pow(x[0] * y[0], 0.5), pow(x[1] * y[1], 0.5)
#         # return x[0] * y[0], x[1] * y[1]
#     else:
#         return min(x, y)
#         # return (x + y)/2.0
#         # return pow(x * y, 0.5)
#         # return x * y


def AND_p(x, y):
    """
    Definition of basic AND aggregator in rules as Product aggregation in case intervals and product function when input data are floats
        :param x: first aggregated value
        :type x: tuple, float
        :param y: second aggregated value
        :type y: tuple, float
        :return: aggregated value
        :rtype: tuple, float

    """
    if type(x) is tuple and type(y) is tuple:
        return x[0] * y[0], x[1] * y[1]
    else:
        return x * y


def NOT(x):
    """
    Negation operator in rules
        :param x: value to negation
        :type x: tuple, float
        :return: value after negation
        :rtype: tuple, float
    """
    if type(x) is tuple:
        return 1. - x[1], 1. - x[0]
    else:
        return 1. - x


def interval_preparse(STRINGA):
    """
    Function extract the antecedent
        :param STRINGA: text of rule
        :type STRINGA: str
        :return: antecedent part from rule
        :rtype: str
    """
    # extract the antecedent
    return STRINGA[STRINGA.find("IF") + 2:STRINGA.find(" THEN")].strip()


def interval_postparse(STRINGA, verbose=False):
    """
    Function extract the successor
        :param STRINGA: text of rule
        :type STRINGA: str
        :return: successor part from rule
        :rtype: str
    """
    stripped = STRINGA[STRINGA.find(" THEN") + 5:].strip("() ")
    if STRINGA.find("THEN") == -1:
        raise Exception("ERROR: badly formatted rule, please check capitalization and syntax.\n"
                        + " ---- PROBLEMATIC RULE:\n"
                        + STRINGA)
    if re.match(r"P\(", stripped) is not None:
        return tuple(re.findall(r"\w+(?=\sis)|(?<=is\s)\w+|\d\.\d\d", stripped))
    else:
        return tuple(re.findall(r"\w+(?=\sIS\s)|(?<=\sIS\s)\w+", stripped))


def interval_find_index_operator(string, verbose=False):
    """
    Function finding indexes of operators in string
        :param string: rule/part of rule
        :type string: str
        :param verbose: toggles verbose mode, default to True<
        :type verbose: bool
        :return: start and end indexes of the found operator
        :rtype: tuple
    """
    if verbose: print(" * Looking for an operator in", string)
    pos = 0
    par = 1
    while (par > 0):
        pos += 1
        # if pos>=len(string):
        # print(pos, pos2)
        # raise Exception("badly formatted rule, terminating")
        if string[pos] == ")": par -= 1
        if string[pos] == "(": par += 1
    pos2 = pos
    while (string[pos2] != "("):
        pos2 += 1
    return pos + 1, pos2


def interval_recursive_parse(text, verbose=False, operators=None, allow_empty=True):
    """
    Function for parse rules using recursive and extract each of the clauses from rule
        :param text: rule / part of rule
        :type text: str
        :param verbose: toggles verbose mode, default to False
        :type verbose: bool
        :param operators: recognized in previous calling of function aggregation operator, default to None
        :type operators: str
        :param allow_empty: toggles allow empty clause, default to True
        :type allow_empty: bool
        :return: recognized part of function with aggregators
        :rtype: IntervalFunctional
    """
    # remove useless spaces around text
    text = text.strip()

    # case 0: empty string
    if text == "" or text == "()":
        if verbose: print("WARNING: empty clause detected")
        if not allow_empty:
            raise Exception("ERROR: emtpy clauses not allowed")
        else:
            return ""

    # case 1: simple clause ("this IS that")
    if regex_clause.match(text):
        if verbose:
            print(" * Simple clause matched")

        variable = text[:text.find(" IS")].strip()
        term = text[text.find(" IS") + 3:].strip()
        ret_clause = IntervalClause(variable, term, verbose=verbose)
        if verbose:
            print(" * Rule:", ret_clause)
        return ret_clause

    elif regex_clause_with_parentheses.match(text):
        if verbose:
            print(" * Simple clause with parentheses matched")

        variable = text[1:text.find(" IS")].strip()
        term = text[text.find(" IS") + 3:-1].strip()
        ret_clause = IntervalClause(variable, term, verbose=verbose)
        if verbose:
            print(" * Rule:", ret_clause)
        return ret_clause

    else:
        if verbose:
            print(" * Regular expression is not matching with single atomic clause")

        # possible valid cases:
        # 1) atomic clause
        # 2) atomic clause OPERATOR atomic clause
        # 3) NOT atomic clause
        # 4) (clause OPERATOR clause)
        # 5) ((...)) # experimental

        if text[:3] == "NOT":
            beginindop = 0
            endindop = 3
        elif text[:4] == "(NOT":
            text = text[1:-1]
            beginindop = 0
            endindop = 3
        else:
            try:
                beginindop, endindop = find_index_operator(text, verbose=verbose)

            except IndexError:
                # last attempt: remove parentheses (if any!)
                try:
                    if text[0] == "(" and text[-1] == ")":
                        text = text[1:-1]
                        return interval_recursive_parse(text, operators=operators, verbose=verbose,
                                                        allow_empty=allow_empty)
                    else:
                        raise Exception("ERROR: badly formatted rule, please check capitalization and syntax.\n"
                                        + " ---- PROBLEMATIC RULE:\n"
                                        + text)

                except:
                    raise Exception("ERROR: badly formatted rule, please check capitalization and syntax.\n"
                                    + " ---- PROBLEMATIC RULE:\n"
                                    + text)

        firsthalf = text[:beginindop].strip()
        secondhalf = text[endindop:].strip()
        operator = text[beginindop:endindop].strip()
        if operator.find(" ") > -1:
            if verbose:
                print("WARNING: space in operator '%s' detected" % operator)
                print(" " * (28 + operator.find(" ")) + "^")
            raise Exception("ERROR: operator %s invalid: cannot use spaces in operators" % operator)

        if verbose:    print("  -- Found %s *%s* %s" % (firsthalf, operator, secondhalf))

        try:
            novel_fun = IntervalFunctional(operator,
                                           interval_recursive_parse(firsthalf, verbose=verbose, operators=operators,
                                                                    allow_empty=allow_empty),
                                           interval_recursive_parse(secondhalf, verbose=verbose, operators=operators,
                                                                    allow_empty=allow_empty),
                                           operators=operators)
        except:
            raise Exception("ERROR: badly formatted rule, please check capitalization and syntax.\n"
                            + " ---- PROBLEMATIC RULE:\n"
                            + text)
        return novel_fun
