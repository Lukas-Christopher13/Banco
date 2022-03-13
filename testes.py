<<<<<<< HEAD
=======
def insereOrdenado(lista1,lista2):

    if len(lista1) != 10:
        return 'Insira uma lista com dez termos!'
    if len(lista2) > 10:
        return 'Insira uma lista com até dez termos!'

    #ordenar
    for i in range(len(lista2)):
        if lista1[0] > lista2[i]:
            tuplaAux = lista1[0], lista2[i]

            lista1[0] = tuplaAux[1]
            lista2[i] = tuplaAux[0]
    
    for i in range(len(lista1)-1):
        for e in range(len(lista2)):
            if (lista2[e] >= lista1[i]) and (lista2[e] <= lista1[i+1]):
                tuplaAux = lista1[i+1], lista2[e]

                lista1[i+1] = tuplaAux[1]
                lista2[e] = tuplaAux[0]
    
    lista2.sort()
    
    for i in lista2:
        lista1.append(i)

    return lista1

print(insereOrdenado([1,3,5,6,7,8,12,31,54,60],[2,23,56,12,0,13,0,2]))
>>>>>>> 0cab383a8195788952e00a1bb440832d1fc9aa68
