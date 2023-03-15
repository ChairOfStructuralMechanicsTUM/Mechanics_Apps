from sympy import Symbol, integrate, Eq, Mul, Add, Float, cos, sin, Pow, Unequality, core
import sympy
import re

"""First try to read general sin or cos functions from arguments"""
def gchsnew(funct, der, leng, symbo):
    inte = 0
    inte2 = 1
    print(('in gcf'))
    if re.search("sin", str(funct)) is not None or re.search("cos", str(funct)) is not None:
        print('in f')
        funct1 = funct
        for i in range(0, der):
            funct1 = integrate(funct1, symbo)
        print('After integration: ' + str(funct1))
        try:
            int_aa = []
            for aa in range(0, funct1.args.__len__()):
                print('in aa')
                print('Length first argh: ' + str(funct1.args.__len__()))
                print('Argh erste Ebene: ' + str(funct1.args[aa]))
                print(funct1.args[aa].func)
                if funct1.args[aa] == -1 or funct1.args[aa] == 1 or funct1.args[aa].func == sin or funct1.args[aa].func == cos or funct1.args[aa].func == Pow:
                    int_aa.append(funct1.args[aa])
                elif re.search('Unequality', str(funct1.args[aa].func)) is not None or re.search('Boolean', str(funct1.args[aa].func)) is not None\
                        or re.search('Zero', str(funct1.args[aa].func)) is not None:
                    print('Unequality aa')
                    continue
                else:
                    print('In else')
                    int_aa.append(Adding_args_of_one_layer(funct1.args[aa].args, funct1.args[aa]))
            for a in int_aa:
                print(a)
            breakpoint()
            for a in int_aa:
                print('Should only be seen once')
                print(funct.func)
                if re.search('Mul', str(funct.func)) is not None:
                    inte2 = inte2 * a[0]
                else:
                    print('in else')
                    print(a)
                    inte = inte + a[0]
                    print('Inte: ' +str(inte))
                if re.search('Mul', str(funct.func)) is not None:
                    inte = inte2
            print(inte)
            inte = inte.subs(symbo, leng) - inte.subs(symbo, 0)
        except:
            print('In exception')
            return funct1
    else:
        inte = funct
        for i in range(0, der - 1):
            inte = integrate(inte, symbo)
        inte = integrate(inte, (symbo, 0, leng))

    return inte

def gchs(funct, der, leng, symbo):
    inte = 0
    inte2 = 1
    print(('in gcf'))
    if re.search("sin", str(funct)) is not None or re.search("cos", str(funct)) is not None:
        print('in f')
        funct1 = funct
        for i in range(0, der):
            funct1 = integrate(funct1, symbo)
        print('After integration: ' + str(funct1))
        try:
            int_aa = []
            for aa in range(0, funct1.args.__len__()):
                print('in aa')
                print('Length first argh: ' + str(funct1.args.__len__()))
                print('Argh erste Ebene: ' + str(funct1.args[aa]))
                print(funct1.args[aa].func)
                if funct1.args[aa] == -1 or funct1.args[aa] == 1 or funct1.args[aa].func == sin or funct1.args[aa].func == cos or funct1.args[aa].func == Pow:
                    int_aa.append(funct1.args[aa])
                elif re.search('Unequality', str(funct1.args[aa].func)) is not None or re.search('Boolean', str(funct1.args[aa].func)) is not None\
                        or re.search('Zero', str(funct1.args[aa].func)) is not None:
                    print('Unequality aa')
                    continue
                else:
                    b_parameters = []
                    for ba in range(0, funct1.args[aa].__len__()):
                        arg_ba = funct1.args[aa][ba]
                        print('in ba')
                        print(funct1.args[aa][ba].func)
                        print('Length second argh: ' + str(funct1.args[aa].__len__()))
                        print('Argh zweite Ebene: ' + str(funct1.args[aa][ba]))
                        if check_if_further(arg_ba) == False or re.search('Mul', str(funct1.args[aa][ba].func)) is not None:
                            print('if ba')
                            b_parameters.append(arg_ba)
                            print(b_parameters)
                        elif check_if_stop(arg_ba):
                            print('Unequality aa')
                            continue
                        else:
                            continue
                    print('lö')
                    int_a = 1
                    int_a2 = 0
                    for bam in b_parameters:
                        print('in bam')
                        print(bam)
                        if re.search('Mul', str(funct1.args[aa].func)) is not None:
                            int_a = int_a * bam
                        else:
                            int_a2 = int_a2 + bam

                    b_parameters.clear()
                    if re.search('Mul', str(funct1.args[aa].func)) is not None:
                        int_aa.append(int_a)
                    else:
                        int_aa.append(int_a2)
                    print('Results from second level:')
                    print(int_aa)
            for a in int_aa:
                print('Should only be seen once')
                if funct1.func == Mul:
                    inte2 = inte2 * a
                else:
                    inte = inte + a
                if funct1.args[aa].func == Mul:
                    inte = inte2

            inte = inte.subs(symbo, leng) - inte.subs(symbo, 0)
        except:
            print('Du bist doof')
    else:
        inte = funct
        for i in range(0, der - 1):
            inte = integrate(inte, symbo)
        inte = integrate(inte, (symbo, 0, leng))

    return inte

def check_if_further(funct):
    if funct == -1 or funct == 1 or re.search('sin', str(funct.func)) is not None or \
    re.search('cos', str(funct.func)) is not None or re.search('Pow', str(funct.func)) is not None:
        answer = False
    else:
        answer = True
    return answer

def check_if_stop(funct):
    if re.search('Unequality', str(funct.func)) is not None or re.search('Boolean', str(funct.func)) is not None\
                        or re.search('Zero', str(funct.func)) is not None:
        answer = True
    else:
        answer = False
    return answer

def Adding_args_of_one_layer(funct, func_prior):
    print('In extra function')
    print(func_prior)
    print(func_prior.func)
    result = []
    try:
        b_parameters = []
        for ba in range(0, funct.__len__()):
            arg_ba = funct[ba]
            print('in range')
            print('Funktion: ' + str(arg_ba.func))
            print('Fuktion value: ' + str(arg_ba))
            if check_if_further(arg_ba) == False:
                print('if ba')
                b_parameters.append(arg_ba)
                print(b_parameters)
            elif check_if_stop(arg_ba):
                print('Unequality aa')
                continue
            else:
                b_parameters = Adding_args_of_one_layer(arg_ba.args, arg_ba)
        print('lö')
        int_a = 1
        int_a2 = 0
        for bam in b_parameters:
            print('in bam')
            print(bam)
            print(func_prior.func)
            if re.search('Mul', str(func_prior.func)) is not None:
                int_a = int_a * bam
            else:
                int_a2 = int_a2 + bam

        b_parameters.clear()
        if re.search('Mul', str(func_prior.func)) is not None:
            result.append(int_a)
        else:
            result.append(int_a2)
        print('Results from second level:')
        print(result)
        return result
    except:
        return funct


