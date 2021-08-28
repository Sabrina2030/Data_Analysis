import pandas as pd
import datetime as dt
from Modules.validaciones import *


def ambulatorio():

    # import base-txt file from local proyect & copy the DatasFrames generated.
    base_txt_file = pd.read_csv('../Datos/202106/base_txt_202106.csv')
    base_txt_f_copy = base_txt_file.copy()

    # cast 'Fecha Práctica' column type to datetime type.
    base_txt_f_copy['Fecha Práctica'] = pd.to_datetime(base_txt_f_copy['Fecha Práctica'], dayfirst=True, 
                                                            format="%d/%m/%Y").dt.strftime('%d/%m/%Y')

    # add leading zeros to each value.
    base_txt_f_copy['Beneficio'] = add_zeros_to_left(base_txt_f_copy, 'Beneficio', 12)
    base_txt_f_copy['Parentesco'] = add_zeros_to_left(base_txt_f_copy, 'Parentesco', 2)

    # sort by full 'Beneficio','Parentesco','CodDiagnostico' &'Fecha Práctica'.
    base_txt_f_copy = base_txt_f_copy.sort_values(by=['Beneficio','Parentesco','Fecha Práctica']) # ,'CodDiagnostico'



    base_txt_f_copy = base_txt_f_copy.drop_duplicates(subset=['Cod Prestación', 'Fecha Práctica', 'Nro Orden'], keep='first')

    # reset index
    base_txt_f_copy = base_txt_f_copy.reset_index().drop(['index'], axis=1)

    # create the 'Ambulatorio' output file.
    with open('../Datos/202106/Auxiliares/Ambulatorio_piloto.txt', 'a', encoding='utf-8') as out_f:

        # Encabezado prestaciones.
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
                tmp = True

            if (fecha == row['Fecha Práctica']):
                out_f.write(';;;0;1;'+ str(row['Cod Prestación']) + ';' + str(row['Fecha Práctica']) + ' 00:00' + 
                            ';' + str(row['Cantidad']) + ';' + str(row['Modalidad']) + ';' + str(row['Nro Orden']) + '\n')

                if ((index < len(base_txt_f_copy.index)-1 and (fecha != base_txt_f_copy['Fecha Práctica'][index+1] or 
                     beneficio != base_txt_f_copy['Beneficio'][index+1] or
                     gp != base_txt_f_copy['Parentesco'][index+1])) or 
                     index == len(base_txt_f_copy.index)-1):
                    # Fin Ambulatorio
                    out_f.write('FIN AMBULATORIO'+'\n')
