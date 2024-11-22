from fastapi import HTTPException, UploadFile, File, Query
import pandas as pd
import os
from .. import app

DATA_DIR = "data/csv_files" # тут будуть зберігатись 
os.makedirs(DATA_DIR, exist_ok=True)

# енд поінти
@app.get("/")
def root():
    return {"message": "Welcome to API!"}

# ендпоінт з можливістю завантажити таблицю ексель і отримати у папці data/csv_files csv файли з місяцями
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        # зчитатання файлу безпосередньо за допомогою pandas ExcelFile
        excel_data = pd.ExcelFile(file.file)

        # розділення Excel на CSV
        sheet_names = []
        for sheet_name in excel_data.sheet_names:
            df = excel_data.parse(sheet_name)
            csv_path = os.path.join(DATA_DIR, f"{sheet_name}.csv")
            df.to_csv(csv_path, index=False)
            sheet_names.append(sheet_name)
        
        # якщо все правильно то виведе File uploaded and processed successfully", "sheets" і покаже які саме місяці уло створенно і додано

        return {"message": "File uploaded and processed successfully", "sheets": sheet_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/monthly_summary/")
async def get_monthly_summary(month: str = Query(..., description="Назва місяця (наприклад березень)")):
    # список усіх файлів у каталозі
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

    # пошук потрібного файлу
    matching_file = None
    for file in csv_files:
        if month.lower() in file.lower():
            matching_file = file
            break

    # якщо пошук не вдався то ми пишемо що місяць із такою назвою не знайденно, це може бути зумовленно не правильним написанням але ніяк не капсом
    if not matching_file:
        raise HTTPException(status_code=404, detail=f"Файл для місяця '{month}' не знайдено.")

    # завантаження файлу
    df = pd.read_csv(os.path.join(DATA_DIR, matching_file))

    # тут вам представленний код де змінні заповнюються, від ДОХОДЫ і до Earn у нас доходи, і від Видатки і до УСЬОГО у нас витрати
    # якщо ні то виводить Не знайдено необхідних секцій у файлі.
    try:
        income_start = df[df.iloc[:, 0].str.contains("ДОХОДЫ", na=False)].index[0]
        income_end = df[df.iloc[:, 0].str.contains("Earn", na=False)].index[0]
        expenses_start = df[df.iloc[:, 0].str.contains("Видатки", na=False)].index[0]
        expenses_end = df[df.iloc[:, 0].str.contains("УСЬОГО", na=False)].index[0]
    except IndexError:
        raise HTTPException(status_code=400, detail="Не знайдено необхідних секцій у файлі.")

    # функція для деталізації по секціях
    def calculate_details(start, end):
        section = df.iloc[start:end + 1]  # вибір секції
        section = section.set_index(section.columns[0])  # перший стовпець як назви категорій
        section_numeric = section.apply(pd.to_numeric, errors="coerce").fillna(0)  # тільки числові дані)
        section_totals = section_numeric.sum(axis=1)  # сума для кожної категорії 
        return section_totals.to_dict()

    # деталізація виводу доходів та витрат
    income_details = calculate_details(income_start, income_end)
    expenses_details = calculate_details(expenses_start, expenses_end)

    return {
        "місяць": month,
        "усі_дохіди": sum(income_details.values()),
        "усі_витрати": sum(expenses_details.values()),
        "деталі_доходів": income_details,
        "деталі_витрат": expenses_details,
    }


@app.get("/yearly_summary/")
async def get_yearly_summary():
    # список усіх файлів у каталозі
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

    # якщо нема жодного загруженого файлу csv, тобто ви пропустили ендпоінт з загрузкою, тоооооо виведе Не знайдено жодного файлу для підрахунку.
    if not csv_files:
        raise HTTPException(status_code=404, detail="Не знайдено жодного файлу для підрахунку.")

    yearly_income = 0
    yearly_expenses = 0

    # підрахунок для всіх файлів
    for file in csv_files:
        df = pd.read_csv(os.path.join(DATA_DIR, file))

        # тут вам представленний код де змінні заповнюються, від ДОХОДЫ і до Earn у нас доходи, і від Видатки і до УСЬОГО у нас витрати
        try:
            income_start = df[df.iloc[:, 0].str.contains("ДОХОДЫ", na=False)].index[0]
            income_end = df[df.iloc[:, 0].str.contains("Earn", na=False)].index[0]
            expenses_start = df[df.iloc[:, 0].str.contains("Видатки", na=False)].index[0]
            expenses_end = df[df.iloc[:, 0].str.contains("УСЬОГО", na=False)].index[0]
        except IndexError:
            continue  # пропустити файл якщо секцію не було знайденно

        # функція для підрахунку сум за рік
        def calculate_sum(start, end):
            section = df.iloc[start:end + 1, 1:]  # вибор сектору пропускаючи перший стовпець
            section = section.apply(pd.to_numeric, errors="coerce")  # перетворення на числа
            return section.sum().sum()  # сума всіх чисел

        # витрати і доходи за рік   
        yearly_income += calculate_sum(income_start, income_end)
        yearly_expenses += calculate_sum(expenses_start, expenses_end)
    # вивід цих значень вище ^
    return {
        "усі_дохіди": yearly_income,
        "усі_витрати": yearly_expenses,
    }