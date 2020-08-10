import argparse
import BinaryCSP
import traceback
from Testing import csp_parse, assignment_parse


questionValues = {
    'q1': 4,
    'q2': 2,
    'q3': 2,
    'q4': 4,
    'q5': 4,
    'q6': 2
}


def run_test(test_file_name):
    """
    Runs a single test. Either prints correct or a failure message.
    Returns True if the test passes. ValueError if test does not exist.
    """
    args = []
    hint = None

    try:
        with open(test_file_name) as test_file:
            test_function = getattr(BinaryCSP, test_file.readline().strip())
            for line in test_file:
                line = line.split()
                line_type = line[0]

                if line_type == 'csp':
                    with open(line[1]) as csp_file:
                        args.append(csp_parse(csp_file.readlines()))
                elif line_type == 'assignment':
                    with open(line[1]) as assignment_file:
                        args.append(assignment_parse(assignment_file.readlines()))
                elif line_type == 'function':
                    args.append(getattr(BinaryCSP, line[1]))
                elif line_type == 'constraint':
                    args.append(getattr(BinaryCSP, line[1])(*line[2:]))
                elif line_type == 'boolean':
                    args.append(line[1] == 'True')
                elif line_type == 'hint':
                    hint = ' '.join(line[1:])
                else:
                    args.append(line[1])

    except IOError:
        raise ValueError('Invalid test: %s\n'
                         '(Tests should normally be specified as \'test_cases\[question]\[test].test\')'
                         % test_file_name)
    except Exception as e:
        print('An error occurred within the autograder: ')
        print(e)

    try:
        result = test_function(*args)
    except Exception as e:
        print()
        print('FAIL:', test_file_name)
        print('Something broke:')
        print(traceback.format_exc())
        return False

    try:
        test_local = {'success': False, 'result': result, 'args': args, 'correct': None}
        exec(
            compile(
                open(test_file_name.replace('.test', '.solution')).read(),
                test_file_name.replace('.test', '.solution'), 'exec'
            ), {}, test_local
        )
        correct = test_local['correct']
        success = test_local['success']

    except IOError as e:
        raise ValueError('Invalid solution file: %s' % test_file_name.replace('.test', '.solution'))
    except Exception as e:
        print()
        print('FAIL:', test_file_name)
        print('Solution check failed. Check your return type.')
        print()
        return False

    if success:
        print('PASS:', test_file_name)
    else:
        print()
        print('FAIL:', test_file_name)
        print('Your answer:', str(result))
        print('Correct answer:', str(correct))
        if hint is not None:
            print('Hint:', hint)
        print()

    return success


def run_tests(tests):
    """
    Runs every test in a list of tests.
    Prints an error message for invalid tests.
    """
    print('____________________________________________________________________')
    print()
    all_pass = True
    for test in tests:
        try:
            all_pass = run_test(test) and all_pass
        except ValueError as e:
            print(e)
    if all_pass:
        print()
        print('--------------------------------------------------------------------')
        print('All tests passed')
        print('--------------------------------------------------------------------')
        print()
    else:
        print()
        print('--------------------------------------------------------------------')
        print('Not all tests passed')
        print('--------------------------------------------------------------------')
        print()


def main():
    """
    Parses command line arguments.
    Can run a list of questions and a list of tests.
    Defaults to running all questions and printing the total score.
    """
    print()
    parser = argparse.ArgumentParser(description='Constraint satisfaction problem autograder')
    parser.add_argument('-t', '--test', action='append', dest='tests')
    args = vars(parser.parse_args())
    if args['tests'] is not None:
        run_tests(args['tests'])


if __name__ == '__main__':
    main()
