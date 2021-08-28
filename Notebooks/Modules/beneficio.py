import pandas as pd
import numpy as np
import datetime
from io import open

def beneficio():
    
    base = pd.read_csv('../Datos/202106/base_txt_202106.csv')
    
    result = base.groupby('Beneficio').agg({'Fecha Práctica': ['min']})
    result = result['Fecha Práctica']
    result=result.reset_index()
    
    #cambiar nombre de columna min
    result = result.rename(columns = {'min': 'Fecha_prestacion'})
    
    #cambiar el formato de la fecha 
    result['Fecha_prestacion'] = pd.to_datetime(result['Fecha_prestacion'], dayfirst=True, format="%d/%m/%Y").dt.strftime('%d/%m/%Y')
    
    #paso a str 
    result ['Beneficio'] = result ['Beneficio'].astype(str)
    
    #agregar 0 
    def agregar0(df, col: str, d: int):
        if (df[col].dtype == object):
            c = 0
            for i in df[col]:
                df.at[c,col] = i.zfill(d)
                c +=1
        return df[col]
    
    result ['Beneficio'] = agregar0(result, 'Beneficio', 12)
    
    archivo = open("../Datos/202106/Auxiliares/Beneficio.txt", "w")
            #"/home/leandro/Backup/KUNAN/Proyectos/1. EnCasa/en-casa-presentaciones-pami/Leandro/Archivos/Salida/Beneficio.txt","w")
    archivo.write("BENEFICIO\n")
    for i,j in zip(result.Beneficio, result.Fecha_prestacion):
        archivo.write("{}{}{}{}{}{}{}{}{}{}{}".format(";",";",";",i,";",";",";","1",";",j,"\n")) 
    #for i in dataSet.BENEFICIO:
    #archivo.write(str(i + "\n"))
    archivo.close()
