import xlrd

def get_data():
    data_sheet = xlrd.open_workbook(r"./datas/since.xls").sheet_by_index(0)
    results = []
    for row in range(1,data_sheet.nrows):
        result = ""
        SUstr = data_sheet.cell(row,0).value
        KYstr = data_sheet.cell(row,1).value
        AUstr = data_sheet.cell(row,2).value
        AFstr = data_sheet.cell(row,3).value
        FUstr = data_sheet.cell(row,4).value
        if(SUstr != "*"):
            result = "SU=" + SUstr
        if(KYstr != "*"):
            if(result != ""):
                result = result + " AND KY=" + KYstr
            else:
                result = "KY=" + KYstr
        if(AUstr != "*"):
            if(result != ""):
                result = result + " AND AU=" + AUstr
            else:
                result = "AU=" + AUstr
        if(AFstr != "*"):
            if(result != ""):
                result = result + " AND AF=" + AFstr
            else:
                result = "AF=" + AFstr
        if(FUstr != "*"):
            if(result != ""):
                result = result + " AND FU=" + FUstr
            else:
                result = "FU=" + FUstr
        results.append(result)
        print(result)
    return results
'''
SU=主题,TKA=篇关摘,KY=关键词,TI=篇名,FT=全文,AU=作者,FI=第一作者,RP=通讯作者,AF=作者单位,FU=基金,AB=摘要,CO=小标题, RF=参考文献,CLC=分类号,LY=文献来源, DOI=DOI,CF=被引频次
'''