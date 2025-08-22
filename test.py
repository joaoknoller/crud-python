def contador():
    print("Iniciando")
    yield 1
    print("Continuando")
    yield 2
    print("Quase no fim")
    yield 3
    print("Fim")


gen = contador()

for numero in gen:
    print("Recebi:", numero)