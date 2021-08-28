# import libraries
import numpy as np
import pandas as pd
import datetime as dt
from Modules.validaciones import *
from Modules.df_local_functions import *


def afiliado():
        
    # insert an header into a file
    t_DataFrame = type(pd.DataFrame())
    def add_header(file_url, header: str):
        with open(file_url, 'r+', encoding='utf-8') as outf:
            content = outf.read()
            outf.seek(0, 0)
            outf.write(header.strip() + '\n' + content)
            
    # import PAMI & base_sql file from local proyect.
    t = pd.read_csv("../Datos/202106/base_txt_202106.csv")
#            '/home/leandro/Backup/KUNAN/Proyectos/1. EnCasa/en-casa-presentaciones-pami/Leandro/Archivos/Entrada/Base-txt .csv')
    
    # copy the DatasFrames
    base_txt_file = t.copy()
    
    # build output file with 'afiliados' data
    # columns of interest
    interest_col = ['Apellido y Nombre', 'Tipo Documento', 'Nro Documento', 'Estado Civil', 'Nacionalidad', 'Calle',
                'Puerta', 'Piso', 'Dpto', 'CP', 'Telefono', 'Fecha Nacimiento', 'Sexo', 'CUIT', 'CUIL',
                'Beneficio', 'Parentesco', 'Sucursal', 'Agencia', 'Corresponsalia', 'Afip', 'Afiliacion', 
                'Formulario', 'Fecha Baja', 'Codigo Baja'
               ]

    full_interest_col = ['Apellido y Nombre', 'Tipo Documento', 'Nro Documento', 'Estado Civil', 'Nacionalidad', 'Pais', 'Calle',
                     'Puerta', 'Piso', 'Dpto', 'CP', 'Telefono', 'Fecha Nacimiento', 'Sexo', 'CUIT', 'CUIL',
                     'Beneficio', 'Parentesco', 'Sucursal', 'Agencia', 'Corresponsalia', 'Afip', 'Afiliacion', 
                     'Formulario', 'Fecha Baja', 'Codigo Baja'
                    ]
    
    # create a copy of 'base_txt_file' df
    base_txt_file_copy = base_txt_file.copy()
    
    # cast 'Fecha Nacimiento' column type to datetime type
    base_txt_file_copy['Fecha Nacimiento'] = pd.to_datetime(base_txt_file_copy['Fecha Nacimiento'], dayfirst=True, 
                                                        format="%d/%m/%Y").dt.strftime('%d/%m/%Y')
    
    # add leading zeros to each value.
    base_txt_file_copy['Beneficio'] = add_zeros_to_left(base_txt_file_copy, 'Beneficio', 12)
    base_txt_file_copy['Parentesco'] = add_zeros_to_left(base_txt_file_copy, 'Parentesco', 2)
    
    # sort by full name & date
    base_txt_file_copy = base_txt_file_copy.sort_values(by=['Beneficio'])
    
    # create a new DataFrame only with interest columns
    afiliado_df = base_txt_file_copy.loc[:, interest_col]
    
    # add a column called 'pais'
    afiliado_df.insert(5, 'Pais', '')
    
    # aplicar filtro y eliminar registros repetidos.
    final_afiliado_df = afiliado_df.drop_duplicates(subset='Apellido y Nombre', keep='first')
    final_afiliado_df = final_afiliado_df.reset_index().drop(['index'], axis=1)
    
    # check the validity of 'Tipo Documento' in each register.
    final_afiliado_df['Tipo Documento'] = replace_Series_values(final_afiliado_df, 'Tipo Documento', 'DI', 'DNI')

    # change the order of the 'CP' column.
    col_new_order = ['Apellido y Nombre', 'Tipo Documento', 'Nro Documento', 'Estado Civil', 'Nacionalidad', 'Pais', 'Calle', 
                 'Puerta', 'Piso', 'CP', 'Dpto', 'Telefono', 'Fecha Nacimiento', 'Sexo', 'CUIT', 'CUIL', 'Beneficio', 
                 'Parentesco', 'Sucursal', 'Agencia', 'Corresponsalia', 'Afip', 'Afiliacion', 'Formulario', 'Fecha Baja', 
                 'Codigo Baja']
    final_afiliado_df = final_afiliado_df.reindex(columns=col_new_order)
    
    # export 'final_afiliado_df' to a txt file
    final_afiliado_df.to_csv("../Datos/202106/Auxiliares/afiliado_piloto.txt", sep=';', header=False, index=False, encoding='utf-8')
            #'/home/leandro/Backup/KUNAN/Proyectos/1. EnCasa/en-casa-presentaciones-pami/Leandro/Archivos/Salida/afiliado_piloto.txt', sep=';', header=False, index=False, encoding='utf-8')
    
    # add 'AFILIADO', as an header, into the 'afiliado_piloto.txt' file
    afiliado_piloto_url = "../Datos/202106/Auxiliares/afiliado_piloto.txt"
    #"/home/leandro/Backup/KUNAN/Proyectos/1. EnCasa/en-casa-presentaciones-pami/Leandro/Archivos/Salida/afiliado_piloto.txt"
    add_header(afiliado_piloto_url, 'AFILIADO')
