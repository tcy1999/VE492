import sys
import inspect


def raise_undefined_error():
    """
    Raise not implemented error
    """
    file_name = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    print("*** Method not implemented: %s at line %s of %s" % (method, line, file_name))
    sys.exit(1)


class UnaryConstraint:
    """
    Base class for unary constraints
    """

    def __init__(self, var):
        self.var = var

    def isSatisfied(self, value):
        pass

    def affects(self, var):
        return var == self.var


class BadValueConstraint(UnaryConstraint):
    """
    Implementation of UnaryConstraint
    Satisfied if value does not match passed in parameter
    """

    def __init__(self, var, badValue):
        super().__init__(var)
        self.var = var
        self.badValue = badValue

    def isSatisfied(self, value):
        return not value == self.badValue

    def __repr__(self):
        return 'BadValueConstraint (%s) {badValue: %s}' % (str(self.var), str(self.badValue))


class GoodValueConstraint(UnaryConstraint):
    """
    Implementation of UnaryConstraint
    Satisfied if value matches passed in parameter
    """

    def __init__(self, var, goodValue):
        super().__init__(var)
        self.var = var
        self.goodValue = goodValue

    def isSatisfied(self, value):
        return value == self.goodValue

    def __repr__(self):
        return 'GoodValueConstraint (%s) {goodValue: %s}' % (str(self.var), str(self.goodValue))


class BinaryConstraint:
    """
    Base class for binary constraints
    """

    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def isSatisfied(self, value1, value2):
        pass

    def affects(self, var):
        return var == self.var1 or var == self.var2

    def otherVariable(self, var):
        return self.var2 if var == self.var1 else self.var1


class NotEqualConstraint(BinaryConstraint):
    """
    Implementation of BinaryConstraint
    Satisfied if both values assigned are different
    """

    def isSatisfied(self, value1, value2):
        return value1 != value2

    def __repr__(self):
        return 'BadValueConstraint (%s, %s)' % (str(self.var1), str(self.var2))


class ConstraintSatisfactionProblem:
    """
    Structure of a constraint satisfaction problem.
    Variables and domains should be lists of equal length that have the same order.
    varDomains is a dictionary mapping variables to possible domains.

    Args:
        variables (list<string>): a list of variable names
        domains (list<set<value>>): a list of sets of domains for each variable
        binaryConstraints (list<BinaryConstraint>): a list of binary constraints to satisfy
        unaryConstraints (list<BinaryConstraint>): a list of unary constraints to satisfy
    """

    def __init__(self, variables, domains, binaryConstraints=None, unaryConstraints=None):
        if unaryConstraints is None:
            unaryConstraints = []
        if binaryConstraints is None:
            binaryConstraints = []
        self.varDomains = {}
        for i in range(len(variables)):
            self.varDomains[variables[i]] = domains[i]
        self.binaryConstraints = binaryConstraints
        self.unaryConstraints = unaryConstraints

    def __repr__(self):
        return '---Variable Domains\n%s---Binary Constraints\n%s---Unary Constraints\n%s' % (
            ''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]),
            ''.join([str(e) + '\n' for e in self.binaryConstraints]),
            ''.join([str(e) + '\n' for e in self.binaryConstraints]))


class Assignment:
    """
    Representation of a partial assignment.
    Has the same varDomains dictionary structure as ConstraintSatisfactionProblem.
    Keeps a second dictionary from variables to assigned values, with None being no assignment.

    Args:
        csp (ConstraintSatisfactionProblem): the problem definition for this assignment
    """

    def __init__(self, csp):
        self.varDomains = {}
        for var in csp.varDomains:
            self.varDomains[var] = set(csp.varDomains[var])
        self.assignedValues = {var: None for var in self.varDomains}

    def isAssigned(self, var):
        """
        Determines whether this variable has been assigned.

        Args:
            var (string): the variable to be checked if assigned
        Returns:
            boolean
            True if var is assigned, False otherwise
        """
        return self.assignedValues[var] is not None

    def isComplete(self):
        """
        Determines whether this problem has all variables assigned.

        Returns:
            boolean
            True if assignment is complete, False otherwise
        """
        for var in self.assignedValues:
            if not self.isAssigned(var):
                return False
        return True

    def extractSolution(self):
        """
        Gets the solution in the form of a dictionary.

        Returns:
            dictionary<string, value>
            A map from variables to their assigned values.
            None if not complete.
        """
        if not self.isComplete():
            return None
        return self.assignedValues

    def __repr__(self):
        return '---Variable Domains\n%s---Assigned Values\n%s' % (
            ''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]),
            ''.join([str(e) + ':' + str(self.assignedValues[e]) + '\n' for e in self.assignedValues]))
