import openpyxl


def get_codes(file_path):
    skip_words = ['ETF・ETN', 'PRO Market']
    codes = []

    wb = openpyxl.load_workbook(file_path)
    ws = wb["Sheet1"]
    for row in ws.iter_rows(min_row=2):
        market = str(row[3].value)
        if (not exist_words(market, skip_words)):
            codes.append(str(row[1].value))
    return codes


def exist_words(text, words):
    exist = False
    for word in words:
        if (word in text):
            exist = True
    return exist


codes = get_codes("kabu.xlsx")
