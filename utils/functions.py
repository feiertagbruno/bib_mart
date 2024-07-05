def is_integer(variable):
    try:
        int(variable)
        return True
    except (ValueError, TypeError):
        return False

def list_para_string(lista, delimitador_lista, delimitador_tupla = None):
    
    string_de_retorno = ""

    if delimitador_tupla:
        for l1, l2 in lista:
            if not string_de_retorno:
                string_de_retorno = str(l1) + str(delimitador_tupla) + str(l2)
            else:
                string_de_retorno += str(delimitador_lista) + str(l1) + str(delimitador_tupla) + str(l2)
    else:
        for li in lista:
            if not string_de_retorno:
                string_de_retorno = str(li)
            else:
                string_de_retorno += str(delimitador_lista) + str(li)
    
    return string_de_retorno