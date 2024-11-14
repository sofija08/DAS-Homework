import requests
from bs4 import BeautifulSoup as Bs
import pandas as pd
from datetime import datetime, timedelta
import time
import locale
import os
import openpyxl
from openpyxl.styles import Alignment, Font, Border, Side
from concurrent.futures import ThreadPoolExecutor

locale.setlocale(locale.LC_ALL, 'mk_MK.UTF-8')

def generate_date_ranges(start_date, end_date, days=364):
    start = datetime.strptime(start_date, "%d.%m.%Y")
    end = datetime.strptime(end_date, "%d.%m.%Y")
    while start < end:
        next_end = min(start + timedelta(days=days), end)
        yield start.strftime("%d.%m.%Y"), next_end.strftime("%d.%m.%Y")
        start = next_end + timedelta(days=1)

def fetch_all_issuer_symbols():
    url = "https://www.mse.mk/mk/stats/symbolhistory/REPL"
    response = requests.get(url)
    symbols = []

    if response.status_code == 200:
        soup = Bs(response.text, "html.parser")
        dropdown = soup.find("select", {"name": "Code"})
        options = dropdown.find_all("option")

        for option in options:
            symbol = option['value']
            if not any(char.isdigit() for char in symbol):
                symbols.append(symbol)

    return symbols

def load_previous_data():
    filename = "mse.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename, dayfirst=True)
        df['Датум'] = pd.to_datetime(df['Датум'], errors='coerce', format='%d.%m.%Y')
        df = df.dropna(subset=['Датум'])
        return df
    else:
        return pd.DataFrame()

def extract_data_for_issuer(symbol, start_date, end_date):
    base_url = "https://www.mse.mk/mk/stats/symbolhistory/REPL"
    all_data = []

    for from_date, to_date in generate_date_ranges(start_date, end_date):
        payload = {
            "FromDate": from_date,
            "ToDate": to_date,
            "Code": symbol
        }
        response = requests.post(base_url, data=payload)
        if response.status_code == 200:
            soup = Bs(response.text, "html.parser")
            table = soup.find('table', {'id': 'resultsTable'})
            if table:
                for row in table.find_all('tr')[1:]:
                    cols = [col.text.strip() for col in row.find_all('td')]
                    all_data.append([symbol] + cols)
                time.sleep(1)
        else:
            print(f"Failed for {from_date} to {to_date}. Status code: {response.status_code}")

    return all_data


def format_column_value(x):
    if isinstance(x, str) and '.' in x:
        return locale.format_string('%.2f', float(x.replace('.', '')), grouping=True)
    elif isinstance(x, str):
        return locale.format_string('%d', int(x.replace('.', '')), grouping=True)
    return x

def save_as_excel(df, filename):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Stock Data')
        workbook = writer.book
        worksheet = workbook['Stock Data']

        header_font = Font(bold=True)
        header_alignment = Alignment(horizontal='center', vertical='center')
        header_fill = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        for cell in worksheet[1]:
            cell.font = header_font
            cell.alignment = header_alignment
            cell.fill = header_fill

        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column].width = adjusted_width

        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))
        for row in worksheet.iter_rows():
            for cell in row:
                cell.border = thin_border

        workbook.save(filename)

def store_collected_data(all_data, existing_df):
    df_new = pd.DataFrame(all_data, columns=[
        'Код на издавач', 'Датум', 'Цена на последна трансакција', 'Мак.', 'Мин.',
        'Просечна цена', '%пром.', 'Количина', 'Промет во БЕСТ во денари',
        'Вкупен промет во денари'
    ])
    df_new['Датум'] = pd.to_datetime(df_new['Датум'], format='%d.%m.%Y')
    combined_df = pd.concat([existing_df, df_new], ignore_index=True).drop_duplicates(
        subset=['Код на издавач', 'Датум']).sort_values(['Код на издавач', 'Датум'])

    for col in ['Промет во БЕСТ во денари', 'Вкупен промет во денари']:
        combined_df[col] = combined_df[col].apply(format_column_value)

    combined_df.to_csv("mse.csv", index=False, encoding='utf-8-sig')
    print("Data saved to mse.csv")

    save_as_excel(combined_df, "mse_formatted.xlsx")
    print("Formatted data saved to mse_formatted.xlsx")

def save_run_date(date):
    with open("LASTDATE.txt", "w") as file:
        file.write(date)

def load_run_date():
    if os.path.exists("LASTDATE.txt"):
        with open("LASTDATE.txt", "r") as file:
            return file.read().strip()
    return None

start_time = time.time()

last_run_date = load_run_date()
start_date = last_run_date if last_run_date else "03.11.2014"
end_date = datetime.today().strftime("%d.%m.%Y")
symbols = fetch_all_issuer_symbols()
existing_df = load_previous_data()

if 'Код на издавач' not in existing_df.columns:
    print("Warning: 'Код на издавач' column is missing from the existing data. Please check your CSV file.")

def process_symbol(symbol):
    symbol_data = existing_df[existing_df['Код на издавач'] == symbol] if 'Код на издавач' in existing_df.columns else pd.DataFrame()

    if not symbol_data.empty:
        last_date = symbol_data['Датум'].max().strftime("%d.%m.%Y")
        start_date_for_symbol = (datetime.strptime(last_date, "%d.%m.%Y") + timedelta(days=1)).strftime("%d.%m.%Y")
    else:
        start_date_for_symbol = start_date

    new_data = extract_data_for_issuer(symbol, start_date_for_symbol, end_date)
    return new_data

all_data = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(process_symbol, symbols)

    for result in results:
        if result:
            all_data.extend(result)

if all_data:
    store_collected_data(all_data, existing_df)

save_run_date(datetime.today().strftime("%d.%m.%Y"))

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
