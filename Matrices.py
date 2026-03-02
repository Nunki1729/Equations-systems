def str_num(txt):
    # Se declaran estas variables para averiguar mediante una operación lógica que tipo de cadena ha sido introducida
    caracter = list(txt)
    entero = False
    decimal = False
    frase = False

    if len(caracter) > 1:  # Se comprueba si es un número negativo para que luego no de error
        if caracter[0] == '-':
            caracter.pop(0)

    for letra in caracter:  # Se comprueba que tipo de entrada es (entero, decimal o texto)
        if letra in '0123456789':
            entero = True
        elif letra in '.,\'':
            decimal = True
        else:
            frase = True
            break

    if caracter[0] in '.,\'':  # Asegura que un supuesto decimal tenga parte entera (que no sea ,654)
        raise SystemExit('El dato introducido no es un número, vuelva a rellenar los campor por favor')
    else:
        if frase:  # Mediante operaciones lógicas se comprueba si es un entero un float o un str
            raise SystemExit('El dato introducido no es un número, vuelva a rellenar los campor por favor')
        elif entero and decimal and not frase:
            return float(txt)
        elif entero and not decimal and not frase:
            return int(txt)


def obtener_sub_matriz(matriz, fila, columna):
    sub_matriz = []
    # pasa por todas las filas y quando llega a la que se desea eliminar no la giuarda en la sub_matriz
    for i in range(len(matriz)):
        if i == fila:
            continue
        nueva_fila = []
        # En cada fila lee todos los valores y cuando llega al que esta en la columna deseada elimina en nueva_fila
        for j in range(len(matriz[i])):
            if j == columna:
                continue
            nueva_fila.append(matriz[i][j])
        sub_matriz.append(nueva_fila)
    return sub_matriz


def determinante(matriz):
    if len(matriz) == 1:  # Usa fórmula para calcular determinante de un término
        return matriz[0][0]
    elif len(matriz) == 2:  # Usa fórmula para calcular determinante de un término
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        return det
    else:
        det = 0
        for i in range(len(matriz)):  # Calcula el determinante usando los menores complemetarios
            det += matriz[0][i] * determinante(obtener_sub_matriz(matriz, 0, i)) * (-1) ** i
        return det


def op_filas(a, fila1, b, fila2):
    fila3 = [0] * len(fila1)  # Se crea el array que guardara la nueva fila
    for i in range(len(fila1)):
        fila3[i] = a * fila1[i] + b * fila2[i]  # Va sumando término a termino generando la nueva fila
    return fila3


def matriz_triangular(matriz):
    matriz_copia = [fila[:] for fila in matriz]  # Evitamos la mutabilidad de python
    for i in range(len(matriz_copia)):
        for j in range(i+1, len(matriz_copia)):
            # Al empezar por i + 1 no modificamos filas en las que ya hemos conseguido suficientes ceros
            if i == j:
                continue
            if isinstance(matriz_copia[i], list) and isinstance(matriz_copia[j], list):
                # Asegura que se esta trabajando con arrays
                matriz_copia[j] = op_filas(matriz_copia[j][i], matriz_copia[i], -matriz_copia[i][i], matriz_copia[j])
                # Calculo de la fila con los ceros requeridos
            else:
                raise SystemExit('El dato introducido no es un número, vuelva a rellenar los campor por favor')
    return matriz_copia


def sol_ecuacion(ecuacion):
    a = 0
    for i in ecuacion:
        if i == 0:
            continue
        else:
            a = i  # Guarda el valor del primer coeficiente
            break
    b = a + 2 * ecuacion[-1]
    # Permite que al restarle a b todos los coeficientes se quede el verdadero valor de b en ax = b
    for j in ecuacion:
        b -= j
    return b/a


def obtener_solucion(matriz):
    sol = [0] * len(matriz)  # Se crea un array donde se guardan las soluciones
    for i in range(len(matriz)):
        if i == 0:  # Queremos resolver las ecuaciones inverso por lo que la primera se ignora y se hace al final
            continue
        else:
            sol[-i] = sol_ecuacion(matriz[-i])  # Se resuelve las ecuaciones en orden inverso
            for j in range(len(matriz)):
                matriz[j][-(i+1)] *= sol[-i]
                # Los valores que ya se han hallado se sustituyen en las siguientes ecuaciones
    sol[0] = sol_ecuacion(matriz[0])  # Se resuelve la primera ecuación ya que antes había sido ignorada
    return sol


n = str_num(input('Ingrese la cantidad de incógnitas que tiene el sistema de cuaciones que desea resolver: '))

print('A continuación se le pedira que vaya escribiendo los coeficientes del sistema de ecuaciones de forma que'
      ' esten ordenados por columnas: suponga que desea resolver el sistema 5x + 3y = 8, 6x - y = 23,'
      ' en este caso debería introducir 5, 3, 8, 6, -1, 23')

coeficiente = [[0] * (n + 1) for _ in range(n)]  # Genera el array donde se almacenarán los coeficientes

for num_linea, linea in enumerate(coeficiente):  # Pide al usuario que introduzca los coeficientes de forma ordenada
    for num_coeficiente, _ in enumerate(linea):
        coeficiente[num_linea][num_coeficiente] = str_num(input('Introduzca el coeficiente de la ecuación '
                                                                + str(num_linea + 1) + ' y el término '
                                                                + str(num_coeficiente + 1) + ': '))


if determinante(coeficiente) == 0:  # Se comprueba si el sistema es resoluble
    print('No es posible encontrar solución a este sistema')
else:
    coeficiente = matriz_triangular(coeficiente)
    soluciones = obtener_solucion(coeficiente)

    for num_solucion, solucion in enumerate(soluciones):  # Imprime los valores de las incógnitas de forma ordenada
        print('El valor de la variable número ' + str(num_solucion+1) + ' es ' + str(solucion))
