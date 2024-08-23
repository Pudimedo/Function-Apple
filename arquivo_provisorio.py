class formated_funcs:

    def __init__(self) -> None:

        self.funcs = []

    @staticmethod

    def format_func(func : list) -> str:

        parameter = func[0][func[0].rfind('(') + 1]
        formated_func = '' #funcao formatada
        for i, letter in enumerate(func[1]):

            if letter == parameter and func[1][i - 1].isnumeric():
                formated_func += '*'
            
            formated_func += letter
        
        return formated_func

fredo = formated_funcs()

for i in range(3):

    func = input().split('=')

    fredo.funcs.append(fredo.format_func(func))

print(fredo.funcs)




