#!/usr/bin/env python

class Person(object):
    attrs = ['citizen', 'age', 'disability', 'selfprescribed']
    def __init__(self,
                citizen=False,
                age=0,
                disability=None,
                clinicaltrial=False,
                selfprescribed=False):
        """
        Keyword Arguments:
            citizen (bool): whether the person is a united states citizen
            age (int): age in years of the person
            disability (str): the person's disability as a string* (default: None)
            clinicaltrial (bool): whether the person is participating
                in a clinical trial
            selfprescribed (bool): whether the person is a physician
                with the right to self-prescribe off-label
        """
        assert isinstance(citizen, bool)
        assert isinstance(age, int)
        assert disability == None or isinstance(disability, str)
        assert isinstance(clinicaltrial, bool)
        assert isinstance(selfprescribed, bool)
        self.citizen = citizen
        self.age = age
        self.disability = disability
        self.clinicaltrial = clinicaltrial
        self.selfprescribed = selfprescribed

    def __str__(self):
        strs = []
        for attr in self.attrs:
            strs.append("{}: {}".format(attr, getattr(self, attr)))
        return "\n".join(strs)


def has_right__cannabis(person):
    """
    Arguments:
        person (Person): a given person

    Returns:
        bool: whether a person has the right to use cannabis
    """
    if person.clinicaltrial:
        return True
    return False


def has_right__thc(person):
    """
    Arguments:
        person (Person): a given person

    Returns:
        bool: whether a person has the right to use cannabis
    """
    if person.disability:
        return True
    if person.clinicaltrial:
        return True
    if person.selfprescribed:
        return True
    return False


def have_equal_rights(person1, person2):
    if has_right__thc(person1) == has_right__thc(person2):
        if has_right__cannabis(person1) == has_right__cannabis(person2):
            return True
    return False


import difflib
def diff_objects(obj1, obj2):
    return '\n'.join(
        difflib.unified_diff(
            str(obj1).split('\n'),
            str(obj2).split('\n'),
            'Person 1',
            'Person 2',
            lineterm=''))


import unittest
class TestHasRight_statusquo(unittest.TestCase):
    def test_has_right__disability(self):
        p = Person(disability=False)
        assert has_right__thc(p) == False
        assert has_right__cannabis(p) == False
        p = Person(disability=True)
        assert has_right__thc(p) == True
        assert has_right__cannabis(p) == False

    def test_has_right__clinicaltrial(self):
        p = Person(clinicaltrial=True)
        assert has_right__cannabis(p) == True
        assert has_right__thc(p) == True
        p = Person(clinicaltrial=False)
        assert has_right__cannabis(p) == False
        assert has_right__thc(p) == False

    def test_has_right__selfprescribed(self):
        p = Person(selfprescribed=True)
        assert has_right__thc(p) == True
        p = Person(selfprescribed=False)
        assert has_right__thc(p) == False


class TestHaveEqualRights(unittest.TestCase):
    def test_have_equal_rights(self):
        persons = [
            Person(disability=False),
            Person(disability=True),
            Person(clinicaltrial=True),
            Person(clinicaltrial=False),
            Person(selfprescribed=False),
            Person(selfprescribed=True)
        ]
        import itertools
        errors = []
        for p1, p2 in itertools.combinations(persons, 2):
            try:
                assert have_equal_rights(p1, p2) == True
            except AssertionError as e:
                print("")
                print("NOT EQUAL")
                print(diff_objects(p1, p2))
                errors.append(e)
        if len(errors):
            raise AssertionError(errors)

         # Therefore, persons do not have equal rights under the current law.

###

# CSA: Schedule I Criteria

def substance_helps_with(condition):
    results = []
    for person in all_persons:
        output = check_helps_with(substance, person, condition)
        results.append(output)
    return results


def is_medically_useful(substance):
    for person in all_persons:
        for condition in all_conditions:
            if substance_helps_with(condition):
                return True
    return False

###

# Constitutionality


class AmendmentTest(object):
    def __init__(self, law):
        self.do_test(law)

    def do_test(self):
        raise NotImplemented


import collections

class Amendment(object):
    text = None

    @classmethod
    def violated_by(cls, law):
        has_test = False
        outputs = collections.OrderedDict()
        for key, value in cls.__dict__:
            if isinstance(value, AmendmentTest):
                has_test = True
                _AmendmentTest = value
                _output = _AmendmentTest(law)
                outputs[key] = _output

        if not has_test:
            raise NotImplementedError()

        errors = collections.OrderedDict()
        for key, value in outputs.items():
            if value is not None:
                print(key, value)
                errors[key] = value
        return errors


class QuestionResponse(collections.namedtuple(
    ('question', 'answer', 'raw_response')):
    pass


def prompt_user(question):
    response = raw_input("{}:\n".format(question))
    return QuestionResponse(question, response, response)


import enum
class ResponseEnum(enum.ENUM):
    YES = 'Yes'
    NO = 'No'
    IDK = "I don't know"
    ICR = "I can't remember"


def prompt_user_yesno(question):
    result = None
    while result is None:
        raw_response = raw_input(
            "{}: (Y/N/IDK (q)):\n".format(question))
        response = raw_response.lower()
        if response.startswith('y'):
            result = ResponseEnum.YES
        elif response.startswith('n'):
            result = ResponseEnum.NO
        elif response.startswith('idk'):
            result = ResponseEnum.IDK
        elif response.startswith('q'):
            result = None
        else:
            print('(yes, no, idk, q to quit')
    return QuestionResponse(question, result, response)


class US_Constitution(object):
    def __init__(self):
        self.amendments = [
            self.Amendment_5,
            self.Amendment_9,
            self.Amendment_14)

    class Amendment_9(Amendment):

        class UnenumeratedRights(AmendmentTest):
            """
            Persons have natural rights not specified in the Constitution
            e.g. "Life, Liberty, and the pursuit of Happiness"
            (Declaration of Independence)
            """
            @classmethod
            def do_test_law(cls, law):
                raise NotImplemented

            @classmethod
            def do_test_charge(self, charge, law):
                raise NotImplemented

    class Amendment_5(Amendment):

        class Self_Incrimination(AmendmentTest):
            """
            - Applies when asked to testify against oneself in a criminal trial
            - "I plead the 5th"
            """

            def do_test(self, law):
                results = []
                response = prompt_user_yesno(
                    "Does the law require defandants to testify against themselves "
                    "in order to prove intent?")
                results.append(response)
                if response.answer != ResponseEnum.YES:



        class Due_Process_Clause(AmendmentTest):
            """
            All persons have equal right to substantive,
                procedural due process
            """

        class Due_Process_Equal_Rights(AmendmentTest):
            """
            All persons have equal right to due process (and thus equal rights)

            TODO: Bolling Sharpe

            The front of the Supreme Court reads:

                "Equal Justice Under Law"
            """

    class Amendment_14(Amendment):
        class Equal_Protection_Clause(AmendmentTest):
            """
            - applies to State Laws
            """


US_CONSTITUTION = US_Constitution()


class LawTester(object):
    def is_unconstitutional(law, constitution):
        # ...
        results = []
        for i, amendment in enumerate(constitution.amendments):
            output = amendment.violated_by(law)
            if output:
                results.append(output)
        return results


class Law(object):
    pass


class FederalLaw(Law):

    def is_unconstitutional(law, constitution):
        return is_federally_unconstitutional(law, US_CONSTITUTION)


class StateLaw(Law):

    # state_constitution = Constitution()

    def is_unconstitutional(law, state_constitution=None):
        """
        Returns:
            list:
        """
        if state_constitution is None:
            state_constitution = self.state_constitution
        federally = LawTester.is_unconstitutional(law, US_CONSTITUTION)
        stately = LawTester.is_unconstitutional(law, state_constitution)
        results = []
        if federally:
            results.extend(federally)
        if stately:
            results.extend(stately)
        return results


class LocalLaw(Law):
    def is_unconstitutional(law,
                            state_constitution=None,
                            local_constitution=None):
        """
        Returns:
            list:
        """
        if state_constitution is None:
            state_constitution = self.state_constitution
        if local_constitution is None:
            local_constitution = self.local_constitution
        federally = LawTester.is_unconstitutional(law, US_CONSTITUTION)
        stately = LawTester.is_unconstitutional(law, state_constitution)
        locally = LawTester.is_unconstitutional(law, local_constitution)
        results = []
        if federally:
            results.extend(federally)
        if stately:
            results.extend(stately)
        if locally:
            results.extend(locally)
        return results


if __name__ == "__main__":
    unittest.main()
