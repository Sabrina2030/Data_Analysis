from io import open

def cabecera():

    archivo = open("../Datos/202106/Auxiliares/salida_cabecera.txt", "w")
            #"/home/leandro/Backup/KUNAN/Proyectos/1. EnCasa/en-casa-presentaciones-pami/Leandro/Archivos/Salida/salida_cabecera.txt","w")

    archivo.write("CABECERA\n")
    archivo.write("30-71016088-7;329;15/07/2021;06-21;SAD CORDOBA S.A.;1;UP30710160887;28669\n")
    archivo.write("RED\n")
    archivo.write("30-71016088-7;;;0;CM;SAD CORDOBA S.A.;0;F SANCHEZ;3081;0;0;;3512425076\n")
    archivo.write("PROFESIONAL\n")
    archivo.write(";;;0;JARA DARIO RUBEN;1;258089;258089;DNI;22034419;23-22034419-3;F SANCHEZ;3081;0;0;;3512425076\n")
    archivo.write("PRESTADOR\n")
    archivo.write(";30-71016088-7;258089;;0;UP30710160887;96954;2;1;1;RMARCHETTO@ENCASA.COM.AR;01/01/2010;;;;0;0;0;SAD CORDOBA S.A.;OBISPO TREJO;648;;0;40130123;3512425076;28669\n")
    archivo.write("REL_PROFESIONALESXPRESTADOR\n")
    archivo.write(";30-71016088-7;258089;0;0;\n")
    archivo.write("BOCA_ATENCION\n")
    archivo.write(";30-71016088-7;;0;1;10;F SANCHEZ;3081;0;0;;3512425076\n")
    archivo.write("REL_MODULOSXPRESTADOR\n")
    archivo.write(";30-71016088-7;;0;1;\n")
    archivo.write(";30-71016088-7;;0;2;\n")
    archivo.write(";30-71016088-7;;0;3;\n")
    archivo.write(";30-71016088-7;;0;4;\n")
    archivo.write("REL_PRESTADORESXRED\n")
    archivo.write("30-71016088-7;30-71016088-7;;0;0;\n")

    archivo.close()
