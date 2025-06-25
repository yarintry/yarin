import pandas as pd

filename = "tofesneshek.xlsx"

def getExel(filename):
    filename = pd.read_excel(filename)
    excelrows = len(filename)
    return excelrows

print(getExel(filename))

def readExcel(df, index, part):
    try:
        first_value = df.iloc[index, part+1]
        print(first_value)
        first_word = str(first_value).split()[0]
        return first_word
    except Exception as e:
        print(f"שגיאה בקריאת נתון מהאקסל: {e}")
        return ''

