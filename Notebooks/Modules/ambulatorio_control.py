import pandas as pd
import datetime as dt
import numpy as np
from Modules.validaciones import *
from Modules.df_local_functions import *


def ambulatorio_control():
    # import the file
    Beneficio_list_file = pd.read_csv('../Datos/202106/Auxiliares/full_Beneficio_list.txt')
    Beneficio_list_df = Beneficio_list_file.copy()

    Beneficio_list_df = Beneficio_list_df.drop_duplicates(subset='AFILIACION', keep='first')
    Beneficio_list_df = Beneficio_list_df.reset_index().drop(['index'], axis=1)

    Beneficio_list_df['AFILIACION'] = add_zeros_to_left(Beneficio_list_df, 'AFILIACION', 14)

    Beneficio_list = list(Beneficio_list_df['AFILIACION'])

    # import base-txt file from local proyect & copy the DatasFrames generated.
    base_txt_file = pd.read_csv('../Datos/202106/base_txt_202106.csv')
    base_txt_f_copy = base_txt_file.copy()

    # cast 'Fecha Práctica' column type to datetime type.
    base_txt_f_copy['Fecha Práctica'] = pd.to_datetime(base_txt_f_copy['Fecha Práctica'], dayfirst=True, 
                                                            format="%d/%m/%Y").dt.strftime('%d/%m/%Y')

    # add leading zeros to each value.
    base_txt_f_copy['Beneficio'] = add_zeros_to_left(base_txt_f_copy, 'Beneficio', 12)
    base_txt_f_copy['Parentesco'] = add_zeros_to_left(base_txt_f_copy, 'Parentesco', 2)

    # insert 'AFILIACION' column into 'base_txt_f_copy' with the values of 'Beneficio_list'.
    base_txt_f_copy.insert(0, 'AFILIACION', '')
    base_txt_f_copy['AFILIACION'] = base_txt_f_copy[['Beneficio', 'Parentesco']].apply(''.join, axis=1)

    for i, n in enumerate(Beneficio_list):
        base_txt_f_copy['AFILIACION'] = replace_Series_values(base_txt_f_copy, 'AFILIACION', n, i)

    # sort by full 'Beneficio','Parentesco','CodDiagnostico' &'Fecha Práctica'.
    base_txt_f_copy = base_txt_f_copy.sort_values(by=['AFILIACION', 'Fecha Práctica', 'Cod Prestación', 'Nro Orden'])

    # drop duplicates rows
    base_txt_f_copy = base_txt_f_copy.drop_duplicates(subset=['Cod Prestación', 'Fecha Práctica', 
                                                              'AFILIACION'], keep='first') 

    base_txt_f_copy = base_txt_f_copy.reset_index().drop(['index'], axis=1)

    for i, n in enumerate(Beneficio_list):
        base_txt_f_copy['AFILIACION'] = replace_Series_values(base_txt_f_copy, 'Beneficio', i, n)

    base_txt_f_copy = base_txt_f_copy.drop(['AFILIACION'], axis=1)


    # create the 'Ambulatorio' output file.
    with open('../Datos/202106/Auxiliares/Ambulatorio_piloto.txt', 'w', encoding='utf-8') as out_f:

        # Encabezado prestaciones
        out_f.write('PRESTACIONES'+'\n')

        fecha = ''
        beneficio = ''
        gp = ''
        for index, row in base_txt_f_copy.iterrows():

            if (fecha != row['Fecha Práctica'] or beneficio != row['Beneficio'] or gp != row['Parentesco']):

                # Ambulatorio
                out_f.write('AMBULATORIO'+'\n')

                out_f.write('30-71016088-7;;258089;0;0;0;1;0;' + str(row['Fecha Práctica']) + ';;;2;' +
                            str(row['Nro Orden']) + ';1;' + row['Beneficio'] + ';' + row['Parentesco'] + '\n')

                # REL_DIAGNOSTICOSXAMBULATORIO
                out_f.write('REL_DIAGNOSTICOSXAMBULATORIO'+'\n')
                out_f.write(';;;0;1;'+ str(row['CodDiagnostico']) + ';' + str(row['Tipo Diagnostico']) + '\n')


                # REL_PRACTICASREALIZADASXAMBULATORIO
                out_f.write('REL_PRACTICASREALIZADASXAMBULATORIO'+'\n')

                fecha = row['Fecha Práctica']
                beneficio = row['Beneficio']
                gp = row['Parentesco']

            if (fecha == row['Fecha Práctica']):
                out_f.write(';;;0;1;'+ str(row['Cod Prestación']) + ';' + str(row['Fecha Práctica']) + ' 00:00' + 
                            ';' + str(row['Cantidad']) + ';' + str(row['Modalidad']) + ';' + str(row['Nro Orden']) + '\n')

                if ((index < len(base_txt_f_copy.index)-1 and (fecha != base_txt_f_copy['Fecha Práctica'][index+1] or 
                     beneficio != base_txt_f_copy['Beneficio'][index+1] or
                     gp != base_txt_f_copy['Parentesco'][index+1])) or 
                     index == len(base_txt_f_copy.index)-1):
                    # Fin Ambulatorio
                    out_f.write('FIN AMBULATORIO'+'\n')


