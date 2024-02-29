import openpyxl
import json

def parse_excel_to_json(file_path, start_row, end_row, start_column, end_column, headers, investiment_type):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    investments = []
    for row in range(start_row, end_row+1):
        investment = {}
        for col, header in zip(range(start_column, end_column+1), headers):
            investment[header] = ws.cell(row=row, column=col).value

        investment["tipo"] = investiment_type
        investments.append(investment)

    return investments

def main():
    file_path = "input/PosicaoDetalhada.xlsx"
    start_column = 1  # Column A
    end_column = 7    # Column G

    headers = ["nome", "posicaoMercado", "alocacao", "valorAplicado", "taxaMercado", "dataAplicacao", "dataVencimento"]

    investiment_types = [[9, 18, "preFixado"], [21, 30, "posFixado"], [33, 33, "inflacao"]]

    investments = []
    for investiment_type in investiment_types:
        start_row = investiment_type[0]
        end_row = investiment_type[1]

        investiment_type_description = investiment_type[2]

        investments.extend(parse_excel_to_json(file_path, start_row, end_row, start_column, end_column, headers, investiment_type_description))

    # Output investments as JSON
    with open("output/investments.json", "w") as json_file:
        json.dump(investments, json_file, indent=4)

if __name__ == "__main__":
    main()
