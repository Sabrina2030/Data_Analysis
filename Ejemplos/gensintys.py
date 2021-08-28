import pandas 
import cx_Oracle
import numpy as np

sql =       "select s.spo_id spo_id,  "
sql = sql + "      replace (s.spo_cuit,'-') spo_cuit, "
sql = sql + "      pf.pfa_tipo_documento tipo_doc, "
sql = sql + "      pf.pfa_numero_de_documento nro_doc, "
sql = sql + "      s.spo_denominacion spo_denominacion, "
sql = sql + "      s.spo_tipo_sujeto_pasivo, "
sql = sql + "      NULL nro_cta, "
sql = sql + "      NULL dominio, "
sql = sql + "      NULL ins_id, "
sql = sql + "      '1' AS nro_lote "
sql = sql + "FROM    tax.sujetos_pasivos@tax s "
sql = sql + "join tax.personas_fisicas@tax pf on s.SPO_ID = pf.PFA_SPO_ID "
sql = sql + "WHERE      spo_fecha_baja IS NULL "
sql = sql + "AND PCK_PARAMETRICAS.FC_VALIDA_CUIT(s.spo_cuit) =1 "
sql = sql + "AND not exists ( SELECT 1 "
sql = sql + "                    FROM migracion.Padron_Sintys_Datos_PFJ pa "
sql = sql + "                    WHERE pa.CUIT_OTAX = s.spo_cuit "
sql = sql + "                    and pa.GRADO_CONFIAB >75 "
sql = sql + "                 ) "

sql = sql + "UNION "
sql = sql + "select spo_id, "
sql = sql + "      replace (s.spo_cuit,'-') spo_cuit, "
sql = sql + "      pf.pfa_tipo_documento tipo_doc, "
sql = sql + "      pf.pfa_numero_de_documento nro_doc, "
sql = sql + "      s.spo_denominacion spo_denominacion, "
sql = sql + "      s.spo_tipo_sujeto_pasivo , "
sql = sql + "      NULL nro_cta, "
sql = sql + "      NULL dominio, "
sql = sql + "      NULL ins_id, "
sql = sql + "      '1' AS nro_lote "
sql = sql + "FROM   tax.sujetos_pasivos@tax s "
sql = sql + "join tax.personas_fisicas@tax pf on pf.pfa_spo_id= s.spo_id "
sql = sql + "join  migracion.padron_sintys_datos_pfj pd on s.spo_cuit = cuit_otax  AND grado_confiab >= 50 "
sql = sql + "WHERE NOT  ((utl_match.jaro_winkler_similarity(fc_normalizar_denom(s.spo_denominacion),fc_normalizar_denom(deno)) >= 50 OR "
sql = sql + "            (utl_match.jaro_winkler_similarity(REGEXP_SUBSTR(fc_normalizar_denom(s.spo_denominacion), '^([A-Za-z]+)(\s+)', 1, 1, 'i'), REGEXP_SUBSTR(fc_normalizar_denom(pd.deno), '^([A-Za-z]+)(\s+)', 1, 1, 'i')) >= 50 "
sql = sql + "                          AND "
sql = sql + "             utl_match.jaro_winkler_similarity(REGEXP_SUBSTR(fc_normalizar_denom(s.spo_denominacion), '(\s+)([A-Za-z]+)$', 1, 1, 'i'),  REGEXP_SUBSTR(fc_normalizar_denom(pd.deno), '(\s+)([A-Za-z]+)$', 1, 1, 'i')) >= 50))) "


sql = sql + "UNION   "
sql = sql + "select s.spo_id spo_id, "
sql = sql + "     replace (s.spo_cuit,'-') spo_cuit, "
sql = sql + "      NULL tipo_doc, "
sql = sql + "      NULL nro_doc, "
sql = sql + "      s.spo_denominacion spo_denominacion, "
sql = sql + "      s.spo_tipo_sujeto_pasivo spo_tipo_sujeto_pasivo, "
sql = sql + "      NULL nro_cta, "
sql = sql + "      NULL dominio, "
sql = sql + "      NULL ins_id, "
sql = sql + "      '1' AS nro_lote "
sql = sql + "FROM    tax.sujetos_pasivos@tax s "
sql = sql + "join tax.personas_juridicas@tax pj on s.SPO_ID = pj.PJA_SPO_ID "
sql = sql + "WHERE      spo_fecha_baja IS NULL "
sql = sql + "AND PCK_PARAMETRICAS.FC_VALIDA_CUIT(s.spo_cuit) =1 "
sql = sql + "AND not exists ( SELECT 1 "
sql = sql + "                    FROM migracion.Padron_Sintys_Datos_PFJ pa "
sql = sql + "                    WHERE pa.CUIT_OTAX = s.spo_cuit "
sql = sql + "                    and pa.GRADO_CONFIAB >75 "
sql = sql + "                 ) "

sql = sql + "UNION  "
sql = sql + "select s.spo_id spo_id, "
sql = sql + "     replace (s.spo_cuit,'-') spo_cuit, "
sql = sql + "      NULL tipo_doc, "
sql = sql + "      NULL nro_doc, "
sql = sql + "      s.spo_denominacion spo_denominacion, "
sql = sql + "      s.spo_tipo_sujeto_pasivo spo_tipo_sujeto_pasivo, "
sql = sql + "      NULL nro_cta, "
sql = sql + "      NULL dominio, "
sql = sql + "      NULL ins_id,  "
sql = sql + "      '1' AS nro_lote "
sql = sql + "FROM   tax.sujetos_pasivos@tax s "
sql = sql + "join tax.personas_juridicas@tax pj on pj.pja_spo_id= s.spo_id "
sql = sql + "join  migracion.padron_sintys_datos_pfj pd on s.spo_cuit = cuit_otax  AND grado_confiab >= 50 "
sql = sql + "WHERE NOT  ((utl_match.jaro_winkler_similarity(fc_normalizar_denom(s.spo_denominacion),fc_normalizar_denom(deno)) >= 50 OR "
sql = sql + "            (utl_match.jaro_winkler_similarity(REGEXP_SUBSTR(fc_normalizar_denom(s.spo_denominacion), '^([A-Za-z]+)(\s+)', 1, 1, 'i'), REGEXP_SUBSTR(fc_normalizar_denom(pd.deno), '^([A-Za-z]+)(\s+)', 1, 1, 'i')) >= 50 "
sql = sql + "                          AND "
sql = sql + "             utl_match.jaro_winkler_similarity(REGEXP_SUBSTR(fc_normalizar_denom(s.spo_denominacion), '(\s+)([A-Za-z]+)$', 1, 1, 'i'),  REGEXP_SUBSTR(fc_normalizar_denom(pd.deno), '(\s+)([A-Za-z]+)$', 1, 1, 'i')) >= 50))) "

con = cx_Oracle.connect('nivel1/MIGRADORES@10.250.2.147:1521/moremigd')
dataset = pandas.read_sql(sql , con)
con.close()


dataset["NRO_DOC"] = dataset["NRO_DOC"].replace(np.nan, 0)
dataset["NRO_DOC"] = dataset['NRO_DOC'].astype(np.int64)

dataset.to_csv('sujetos_sintys.csv', encoding='utf-8', index=False, sep='\t')



