import tagui as r
import UI_Constants
import pytesseract
import openpyxl
import pandas as pd
from Mapping_loader import MappingFileLoader

try:
    #***********  Reading Mapping file - Product mapping and Parse Param mapping  ****************#
    mf1 = MappingFileLoader.fetch_Parse_param_mapping()
    mf2 = MappingFileLoader.fetch_Product_Mapping()
    count_mf2 = len(mf2)

    name_retail = mf1.__getitem__(0)
    date_of_sale = mf1.__getitem__(1)
    existing_file_record_range = mf1.__getitem__(2)
    new_file_record_range = mf1.__getitem__(3)
    purchase_record_range = mf1.__getitem__(4)

    name_retail_rows = name_retail.get('name.retail')
    date_of_sale_rows = date_of_sale.get('date.of.sale')
    existing_file_record_range_rows = existing_file_record_range.get('existing.file.record.range')
    new_file_record_range_rows = new_file_record_range.get('new.file.record.range')
    purchase_record_range_rows = purchase_record_range.get('purchase.record.range')

    name_retail__st_row = name_retail_rows.split(',')[0]
    name_retail__end_col = name_retail_rows.split(',')[1]
    date_of_sale__st_row = date_of_sale_rows.split(',')[0]
    date_of_sale__end_col = date_of_sale_rows.split(',')[1]
    existing_file_record_range__st_row = existing_file_record_range_rows.split(',')[0]
    existing_file_record_range__end_row = existing_file_record_range_rows.split(',')[1]
    new_file_record_range__st_row = new_file_record_range_rows.split(',')[0]
    new_file_record_range__end_row = new_file_record_range_rows.split(',')[1]
    purchase_record_range__st_row = purchase_record_range_rows.split(',')[0]
    purchase_record_range__end_row = purchase_record_range_rows.split(',')[1]

    #************     Reading Main excel sheet    ***************#
    ExcelFile_Path = r'D:\SMWSED\config\SMWSED.xlsx'
    Data_file = openpyxl.load_workbook(ExcelFile_Path)
    Data_sheet = Data_file['SMWSED']

    #************     Reading Date from excel sheet    ***************#
    Retailer_name = Data_sheet.cell(row=2, column=2).value
    Date_of_sale = Data_sheet.cell(row=3, column=2).value
    Date_of_sale_str = Date_of_sale.split(':')[0]
    Date_of_sale_date = Date_of_sale.split(':')[1]

    #************    Creating three lists    ***************#
    existing_file_list = []
    new_file_record_list = []
    purchase_record_list = []

    #************    iterate through excel    ***************#
    for i in range(int(existing_file_record_range__st_row), int(existing_file_record_range__end_row)+1):
        existing_file_list_col = []
        for j in range(1, Data_sheet.max_column+1):
            cell_obj = Data_sheet.cell(row=i, column=j)
            existing_file_list_col.append(cell_obj.value)
        existing_file_list.append(existing_file_list_col)

    for i in range(int(new_file_record_range__st_row), int(new_file_record_range__end_row)+1):
        new_file_record_list_col = []
        for j in range(1, Data_sheet.max_column+1):
            cell_obj = Data_sheet.cell(row=i, column=j)
            new_file_record_list_col.append(cell_obj.value)
        new_file_record_list.append(new_file_record_list_col)

    for i in range(int(purchase_record_range__st_row), int(purchase_record_range__end_row)+1):
        purchase_record_list_col = []
        for j in range(1, Data_sheet.max_column+1):
            cell_obj = Data_sheet.cell(row=i, column=j)
            purchase_record_list_col.append(cell_obj.value)
        purchase_record_list.append(purchase_record_list_col)

    #************    Getting lenth os three lists    ***************#
    count_pur = len(purchase_record_list)
    count_ex = len(existing_file_list)
    count_new = len(new_file_record_list)
    

    #************    creating three lists with PackSize   ***************#
    brandName_packsize_ex = []
    brandName_packsize_new = []
    brandName_packsize_pur = [] 

    #************    iterate through excel     ***************# 
    for i in range(int(existing_file_record_range__st_row), int(existing_file_record_range__end_row)+1):
        if not (Data_sheet.cell(row=i, column=2).value == None) or not  (Data_sheet.cell(row=i, column=3).value == None):
            brand_name = Data_sheet.cell(row=i, column=2).value
            pack_size = Data_sheet.cell(row=i, column=3).value
            brand_pack_ex = brand_name + "_" + pack_size
            brandName_packsize_ex.append(brand_pack_ex)            


    for i in range(int(new_file_record_range__st_row), int(new_file_record_range__end_row)+1):
        if not (Data_sheet.cell(row=i, column=2).value == None) or not (Data_sheet.cell(row=i, column=3).value == None):
            brand_name = Data_sheet.cell(row=i, column=2).value
            pack_size = Data_sheet.cell(row=i, column=3).value
            brand_pack_new = brand_name + "_" + pack_size
            brandName_packsize_new.append(brand_pack_new)
            

    for i in range(int(purchase_record_range__st_row), int(purchase_record_range__end_row)+1):
        if not (Data_sheet.cell(row=i, column=2).value == None) or not (Data_sheet.cell(row=i, column=3).value == None):
            brand_name = Data_sheet.cell(row=i, column=2).value
            pack_size = Data_sheet.cell(row=i, column=3).value
            brand_pack_pur = brand_name + "_" + pack_size
            brandName_packsize_pur.append(brand_pack_pur)            


    #************    Creating class UI ACTIONS    ***************#
    class UI_Actions:
        def __init__(self):

            r.init(visual_automation = True)
            r.url(UI_Constants.LOGIN_URL)
            r.wait(5)

        def login(self):
            print("its inside login method")
            if r.popup(UI_Constants.LOGIN_URL) == True:
                r.wait(5)
                r.type(UI_Constants.XPATH_USERNAME, UI_Constants.USER_NAME)
                print('user name')
                r.wait(5)
                r.type(UI_Constants.XPATH_PASSWORD, UI_Constants.PASSWORD)
                print('pass ward')
                r.wait(5)
                r.snap(UI_Constants.XPATH_CAPTCHA_IMG,UI_Constants.IMG_CAPTCHA_CAPTUREIMAGE_NAME)
                TextFromImage = pytesseract.image_to_string(UI_Constants.IMG_CAPTCHA_CAPTUREIMAGE_NAME)
                r.wait(5)
                r.type(UI_Constants.XPATH_CAPTCHA_TEXT,
                    TextFromImage)
                r.wait(5)
                r.click(UI_Constants.XPATH_LOGIN_BTN)
                r.wait(5)
                if r.exist(UI_Constants.IMG_OK_BTN):
                   r.click(UI_Constants.IMG_OK_BTN)
                r.wait(3)
                isLoginSuccess =  (r.click(UI_Constants.XPATH_LOGIN_BTN) == False)
                return isLoginSuccess

        
        def manualLogin(self):
            
            user_name = r.ask("Enter User Name ")            
            r.type(UI_Constants.XPATH_USERNAME, user_name)
            r.wait(3)

            pass_word = r.ask("Enter Pass word ")            
            r.type(UI_Constants.XPATH_PASSWORD, pass_word)
            r.wait(3)

            captcha_text = r.ask("Enter Captcha Text ")
            r.type(UI_Constants.XPATH_CAPTCHA_TEXT, captcha_text) 
            r.wait(3)  

            r.click(UI_Constants.XPATH_LOGIN_BTN) 
            r.wait(5)


        def performAction(self):
            r.wait(2)
            r.click(UI_Constants.XPATH_PERMITS_LINK)
            r.wait(1)
            r.click(UI_Constants.XPATH_DEALER_LINK)


        def dateAndFL2reatailSelection(self):
            r.wait(5)
            r.type(UI_Constants.XPATH_DATE_OF_SALE,Date_of_sale_date)
            r.wait(2)
            r.type(UI_Constants.XPATH_FL2_REATAIL_SALE,UI_Constants.FL2_REATAIL_SALE)
            r.wait(2)  


        def fillingBrandnamePacksizeAndBottles(self): 
            for x in range(0, count_pur):
                Brand_name_pur = purchase_record_list[x][1]
                Pack_Size_pur = purchase_record_list[x][2]
                Bottle_count_pur = purchase_record_list[x][3]
                for y in range(0, count_ex):
                    Brand_name_ex = existing_file_list[y][1]
                    Pack_Size_ex = existing_file_list[y][2]
                    Bottle_count_ex = existing_file_list[y][3]
                    if not existing_file_list[y][1] == None:        
                        for i in range(0, count_mf2):
                            if existing_file_list[y][1] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                existing_file_list[y][1] = (str(mf2[i]).split(':')[1][2:-2]).strip()
                                r.wait(3)
                                r.click(UI_Constants.XPATH_BRAND_NAME)
                                r.wait(3)
                                r.type(UI_Constants.XPATH_BRAND_NAME,str(existing_file_list[y][1]))
                                r.wait(3)
                                r.click(UI_Constants.XPATH_CLICK) 
                                r.wait(2)
                                r.type(UI_Constants.XPATH_PACK_SIZE,str(existing_file_list[y][2]))                                     
                                r.wait(3)
                                r.type(UI_Constants.XPATH_EXISTING_STOCK, '[clear]')
                                r.wait(3)
                                r.type(UI_Constants.XPATH_EXISTING_STOCK,str(existing_file_list[y][3]))
                                r.wait(3)                               
                                r.click(UI_Constants.XPATH_CLICK) 
                                r.wait(2)
                            else :
                                if brandName_packsize_ex[y] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                    brandName_packsize_ex[y] = (str(mf2[i]).split(':')[1][2:-2]).strip()
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_BRAND_NAME)
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_BRAND_NAME,str(brandName_packsize_ex[y]))
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_PACK_SIZE,str(existing_file_list[y][2]))
                                    print(str(existing_file_list[y][2]))       
                                    r.wait(3)
                                    r.type(UI_Constants.XPATH_EXISTING_STOCK, '[clear]')
                                    r.wait(3)
                                    r.type(UI_Constants.XPATH_EXISTING_STOCK,str(existing_file_list[y][3]))
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2) 
                    else:
                        pass                                          
                for z in range(0, count_new):
                    Brand_name_new = new_file_record_list[z][1]
                    Pack_Size_new = new_file_record_list[z][2]
                    Bottle_count_new = new_file_record_list[z][3]
                    if not purchase_record_list[x][1] == None :               
                        if ((str(purchase_record_list[x][1].strip()) == str(new_file_record_list[z][1].strip())) and (str(purchase_record_list[x][2]).strip() == str(new_file_record_list[z][2]).strip())):
                            for i in range(0, count_mf2):
                                if new_file_record_list[z][1] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                    new_file_record_list[z][1] = (str(mf2[i]).split(':')[1][2:-1])
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_BRAND_NAME)
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_BRAND_NAME,str(new_file_record_list[z][1]))
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_PACK_SIZE,str(new_file_record_list[z][2]))
                                    r.wait(5)
                                    r.type(UI_Constants.XPATH_NEW_STOCK, '[clear]')
                                    r.wait(3)
                                    r.type(UI_Constants.XPATH_NEW_STOCK,str(new_file_record_list[z][3]))
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)                    
                                    r.type(UI_Constants.XPATH_NEW_STOCK_PURCHASED, '[clear]')
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_NEW_STOCK_PURCHASED,str(purchase_record_list[x][3]))
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)                             
                                else :
                                    if brandName_packsize_new[z] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                        brandName_packsize_new[z] = (str(mf2[i]).split(':')[1][2:-2])
                                        r.wait(3)
                                        r.click(UI_Constants.XPATH_BRAND_NAME)
                                        r.wait(2)
                                        r.type(UI_Constants.XPATH_BRAND_NAME,str( brandName_packsize_new[z]))
                                        r.wait(3)
                                        r.click(UI_Constants.XPATH_CLICK) 
                                        r.wait(2)
                                        r.type(UI_Constants.XPATH_PACK_SIZE,str(new_file_record_list[z][2]))
                                        r.wait(5)
                                        r.type(UI_Constants.XPATH_NEW_STOCK, '[clear]')
                                        r.wait(3)
                                        r.type(UI_Constants.XPATH_NEW_STOCK,str(new_file_record_list[z][3]))
                                        r.wait(3) 
                                        r.click(UI_Constants.XPATH_CLICK) 
                                        r.wait(2)                   
                                        r.type(UI_Constants.XPATH_NEW_STOCK_PURCHASED, '[clear]')
                                        r.wait(2)
                                        r.type(UI_Constants.XPATH_NEW_STOCK_PURCHASED,str(purchase_record_list[x][3]))
                                        r.wait(3) 
                                        r.click(UI_Constants.XPATH_CLICK) 
                                        r.wait(2)  
                                    
                        else:
                            for i in range(0, count_mf2):                        
                                if new_file_record_list[z][1] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                    new_file_record_list[z][1] = (str(mf2[i]).split(':')[1][2:-1])
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_BRAND_NAME)
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_BRAND_NAME,str(new_file_record_list[z][1]))                    
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_PACK_SIZE,str(new_file_record_list[z][2]))
                                    r.wait(3)
                                    r.type(UI_Constants.XPATH_NEW_STOCK, '[clear]')
                                    r.wait(3)
                                    r.type(UI_Constants.XPATH_NEW_STOCK,str(new_file_record_list[z][3]))
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)
                                else :
                                    if brandName_packsize_new[z] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                        brandName_packsize_new[z] = (str(mf2[i]).split(':')[1][2:-2])
                                        r.wait(3)
                                        r.click(UI_Constants.XPATH_BRAND_NAME)
                                        r.wait(2)
                                        r.type(UI_Constants.XPATH_BRAND_NAME,str(brandName_packsize_new[z]))                    
                                        r.wait(3)
                                        r.click(UI_Constants.XPATH_CLICK) 
                                        r.wait(2)
                                        r.type(UI_Constants.XPATH_PACK_SIZE,str(new_file_record_list[z][2]))
                                        r.wait(3)
                                        r.type(UI_Constants.XPATH_NEW_STOCK, '[clear]')
                                        r.wait(3)
                                        r.type(UI_Constants.XPATH_NEW_STOCK,str(new_file_record_list[z][3]))
                                        r.wait(3)
                                        r.click(UI_Constants.XPATH_CLICK) 
                                        r.wait(2)
                    else:  
                        for i in range(0, count_mf2):
                            if new_file_record_list[z][1] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                new_file_record_list[z][1] = (str(mf2[i]).split(':')[1][2:-2])
                                r.wait(3)
                                r.click(UI_Constants.XPATH_BRAND_NAME)
                                r.wait(2)
                                r.type(UI_Constants.XPATH_BRAND_NAME,str(new_file_record_list[z][1]))                    
                                r.wait(3) 
                                r.click(UI_Constants.XPATH_CLICK) 
                                r.wait(2)                               
                                r.type(UI_Constants.XPATH_PACK_SIZE,str(new_file_record_list[z][2]))
                                r.wait(3)
                                r.type(UI_Constants.XPATH_NEW_STOCK, '[clear]')
                                r.wait(3)
                                r.type(UI_Constants.XPATH_NEW_STOCK,str(new_file_record_list[z][3]))
                                r.wait(3)
                                r.click(UI_Constants.XPATH_CLICK) 
                                r.wait(2)
                            else :
                               if brandName_packsize_new[z] == ((str(mf2[i]).split(':')[0])[2:-1]):
                                    brandName_packsize_new[z] = (str(mf2[i]).split(':')[1][2:-2]) 
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_BRAND_NAME)
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_BRAND_NAME,str(brandName_packsize_new[z]))                    
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)
                                    r.type(UI_Constants.XPATH_PACK_SIZE,str(new_file_record_list[z][2]))
                                    r.wait(3)
                                    r.type(UI_Constants.XPATH_NEW_STOCK, '[clear]')
                                    r.wait(3)
                                    r.type(UI_Constants.XPATH_NEW_STOCK,str(new_file_record_list[z][3]))
                                    r.wait(3)
                                    r.click(UI_Constants.XPATH_CLICK) 
                                    r.wait(2)
                                                                           
        def loginOut(self):
            r.wait(2)
            r.click(UI_Constants.XPATH_LOG_OUT)
            r.wait(2)
            r.close()


except ImportError:
    print(ImportError)                                
