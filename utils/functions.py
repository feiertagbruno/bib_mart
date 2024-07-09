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

def get_ordem_alfabetica_lista():
    return ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
                              "q","r","s","t","u","v","w","x","y","z","0-9..."]

def get_queryset_filtro_letra(filtro_letra, queryset, campo_para_filtro):

    mapa_da_regex = {
        'a': r"^[AaÁáÀàÂâÃãÄäÅå]",
        'e': r"^[EeÈèÉéÊêËë]",
        'i': r"^[IiÌìÍíÎîÏï]",
        'o': r"^[OoÒòÓóÔôÕõÖö]",
        'u': r"^[UuÙùÚúÛûÜü]",
        'c': r"^[cCçÇ]",
        '0-9...': r"^[^A-Za-zÀ-ÿ]",
    }

    if filtro_letra.lower() in mapa_da_regex:
        regex = mapa_da_regex[filtro_letra.lower()]
        queryset = queryset.filter(**{f"{campo_para_filtro}__regex": regex})
    else:
        queryset = queryset.filter(**{f"{campo_para_filtro}__istartswith": filtro_letra})

    return queryset