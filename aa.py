letras = input().split(' ')

dit = {}

a = []

for i in letras:
    a.append(i.replace(',', ''))

for i in a:
    dit[i] = ''

print(dit)