import pandas as pd
import numpy as np
import re
from Modules.validaciones import *
from datetime import datetime, date
    
    
def detalle_op(periodo, auxiliar_periodo, codigos_txt):

    
    # DEFINICIONES LOCALES.
    
    # Some patterns.
    module_pattern = r'\d+|SEMANAL|MENSUAL'
    fragments_pattern = r'\s\s--\s|\s\s--'
    benef_gp_pattern = r'\s[/]\s'
    cleaning_pattern = r'SEMANALES|CLINICO 1|CLINICO 2|SESION SEMANAL|20 MG|40 MG|60 MG|80 MG|CONCENTRADOR DE O2|T6 M3|2 RECARGAS'

    # Some functions.
    # Divide a string & concatenate the parts without '/' caracter.
    def concat_b_p(string: str):
        xs = re.split(benef_gp_pattern, string)
        concat = xs[0] + xs[1]
        return concat

    # Clean data according to some patterns.
    def clean(string: str):
        xs = re.split(cleaning_pattern, string)
        string2 = ''.join(xs)
        return string2

    # Add as items into a list the 'CODIGO DE PRACTICA OP', 'Periodo' and 'QPeriodo' values, that are on 'ESTADO DE PRACTICA: APROBADA'.
    def parsear(string: str):
        parts = re.findall(module_pattern, string)
        return parts


    # create a new df with some data of 'auxiliar_periodo'.
    auxiliar_periodo_filtered = pd.DataFrame(auxiliar_periodo, columns=['NRO. OP', 'NRO. BENEFICIO/GP', 'ESTADO DE PRACTICA: APROBADA'])

    # create a list for 'NRO. BENEFICIO' and another for 'GP'
    zs = list(map(lambda x: re.split(benef_gp_pattern, x), auxiliar_periodo_filtered['NRO. BENEFICIO/GP']))
    beneficios = list(map(lambda x: x[0], zs))
    grados_parentesco = list(map(lambda x: x[1], zs))
    beneficios = list(map(lambda x: x.zfill(12), beneficios))

    # concatenate 'NRO. BENEFICIO' & 'GP' without the '/' caracter.
    auxiliar_periodo_filtered['NRO. BENEFICIO/GP'] = auxiliar_periodo_filtered['NRO. BENEFICIO/GP'].apply(concat_b_p)

    # add leading zeros to each value.
    auxiliar_periodo_filtered['NRO. BENEFICIO/GP'] = add_zeros_to_left(auxiliar_periodo_filtered, 'NRO. BENEFICIO/GP', 14)

    # insert some columns into 'base_op_pami' df.
    auxiliar_periodo_filtered.insert(2, 'CODIGO DE PRACTICA OP', '')
    auxiliar_periodo_filtered.insert(3, 'Periodo', '')
    auxiliar_periodo_filtered.insert(4, 'QPeriodo', '')



    # create: 
    # - a list of the description of the modules and submodules.
    # - a list of the number of modules and submodules of each OP.
    # - a list of the modules and submodules, period and period amount values.

    description = []
    q_beneficio_list = []
    parts = []
    tmp_ls = ''
    tmp_ls_2 = ''
    for i, string in auxiliar_periodo_filtered['ESTADO DE PRACTICA: APROBADA'].iteritems():
        tmp_ls = re.split(fragments_pattern, string)
        tmp_ls.pop(len(tmp_ls)-1)
        description = description + tmp_ls

        tmp_ls_2 = parsear(clean(string))
        q_beneficio_list.append(len(tmp_ls_2)//3)
        parts = parts + tmp_ls_2

    # create:
    # - a list of the number of OP according to the number of their modules.
    # - a list of the number of BENEFICIO-GP according to the number of their modules.
    # - a list of 'NRO. BENEFICIO' full values.
    # - a list of 'GP' full values.
    op_list = []
    benef_gp_list = []
    full_beneficios = []
    full_grados_parentesco = []
    for i, size in enumerate(q_beneficio_list):
        op = auxiliar_periodo_filtered['NRO. OP'][i]
        benef_gp = auxiliar_periodo_filtered['NRO. BENEFICIO/GP'][i]
        benef = beneficios[i]
        gp = grados_parentesco[i]
        for j in range(size):
            op_list.append(op)
            benef_gp_list.append(benef_gp)
            full_beneficios.append(benef)
            full_grados_parentesco.append(gp)

    # create different lists by the modules or submodules, period & period amount
    modules = parts[::3]
    period = parts[1::3]
    amount = parts[2::3]

    # create a list for the days amount of practices.
    dias = []
    for i, p in enumerate(period):
        if (p == 'MENSUAL'):
            qdias = 30 * int(amount[i])
            dias.append(qdias)
        elif (p == 'SEMANAL'):
            qdias = 7 * int(amount[i])
            dias.append(qdias)
        else:
            dias.append('El periodo ingresado no es válido')



    # create a new df with filtered data
    auxiliar_periodo_filtered_2 = pd.DataFrame({'NRO. OP': op_list, 'NRO. BENEFICIO-GP': benef_gp_list, 'BENEFICIO': full_beneficios, 
                                          'GP': full_grados_parentesco, 'CODIGO DE PRACTICA OP': modules, 'PERIODO': period, 
                                          'QPERIODO': amount, 'QDIAS': dias, 'ESTADO DE PRACTICA: APROBADA': description})

    #agrego columnas
    auxiliar_periodo_filtered_2[['Fecha Fin','Visita','Modulo']] = ''

    #Reordeno las columnas 
    auxiliar_periodo_filtered_2 = auxiliar_periodo_filtered_2[['NRO. OP', 'NRO. BENEFICIO-GP', 'BENEFICIO', 'GP',
           'CODIGO DE PRACTICA OP', 'PERIODO', 'QPERIODO', 'QDIAS', 'Fecha Fin', 'Visita', 'Modulo', 'ESTADO DE PRACTICA: APROBADA'  ]].copy()

    #Paso a int para poder comparar
    auxiliar_periodo_filtered_2['CODIGO DE PRACTICA OP'] = auxiliar_periodo_filtered_2['CODIGO DE PRACTICA OP'].astype(int)
    codigos_txt['CODIGO DE PRACTICA OP'] = codigos_txt['CODIGO DE PRACTICA OP'].convert_dtypes()

    #renombro los datos nulos de la tabla de codigos en el campo tipo servicio prestador 
    codigos_txt['Tipo servicio prestador'] = codigos_txt['Tipo servicio prestador'].fillna('nulos')



    def validar_visita(prestador):
        #filtrar 
        df = codigos_txt[codigos_txt['CODIGO DE PRACTICA TXT'] == prestador]
        #print(df)
        var = df['Tipo servicio prestador'].min()
        #print(var)

        if var == 'nulos':
            return 'NO'
        else:
            return 'SI'

    auxiliar_periodo_filtered_2['Visita'] = auxiliar_periodo_filtered_2['CODIGO DE PRACTICA OP'].apply(validar_visita)



    Detalle_op = auxiliar_periodo_filtered_2.copy()

    def modulo(codigo_op):
        codigos_op_modulos = codigos_txt.loc[codigos_txt['CODIGO DE PRACTICA OP'] == codigo_op, 'MODULO']
        modulo = codigos_op_modulos.reset_index(drop=True)[0]
        if (modulo == 'SI'):
            return 'SI'
        else:
            return 'NO'

    #Aplico la funcion
    Detalle_op['Modulo'] = [ modulo(x[1]) for x in Detalle_op['CODIGO DE PRACTICA OP'].items() ]



    mes = str(periodo.month).zfill(2)
    periodo_string = str(periodo.year) + mes
    url = '../Datos/' + periodo_string + '/detalle_op_' + periodo_string +'.csv'

    Detalle_op.to_csv(url, index=False, encoding='utf-8')
