# This class loads the mapping file, which has customer side
# ERP Product name mapped to the equavalent name in Govt Portal
from numpy import maximum
import pandas as pd
from pandas.core.indexes.base import Index


class MappingFileLoader:
    data = None
    data1 = None
    data2 = None

    def __init__(self):
        global data,data1,data2        
        xls = pd.ExcelFile('C:\SMWSED\config\mapping_file.xlsx')
        xls2 = pd.ExcelFile('C:\SMWSED\config\MAPPING LIQUOR NAME new.xlsx')
        
        data = xls2.parse(xls2.sheet_names[0])
        data1 = xls.parse(xls.sheet_names[1])
        data2 = xls.parse(xls.sheet_names[2])

        
    @staticmethod
    def fetch_Product_Mapping():
        global data
        mappedData = {}
        df = pd.DataFrame(data)
        for index, row in df.iterrows():
            mappedData[row['BRAND']] = row['UI_NAME']
            # print(mappedData)
        return mappedData

    @staticmethod    
    def fetch_Parse_param_mapping():
        global data1
        mappedData1 = []
        df1 = pd.DataFrame(data1)
        for index, row in df1.iterrows():
            rowData1 = {row['param.name']: row['param.value']}
            mappedData1.append(rowData1)
            #print(rowData1)
        return mappedData1

    @staticmethod
    def user_Credentials():
        global data2
        mappedData2 = {}
        df2 = pd.DataFrame(data2)
        for index, row in df2.iterrows():
            mappedData2[row['Name']] = row['Value']
            #print(rowData2)
        return mappedData2    
        
        

mfl = MappingFileLoader()
mfl.fetch_Product_Mapping()
mfl.fetch_Parse_param_mapping()
mfl.user_Credentials()

