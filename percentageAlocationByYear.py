import json
import csv
from collections import defaultdict


def main():
    with open('output/investments.json', 'r') as file:
        objects = json.load(file)

    # Dictionary that provides a default value (0, in this case) for a key that doesn't exist.
    yearly_allocation = defaultdict(float)

    total_allocation = 0

    # Parse each object and calculate the allocation for each year
    for obj in objects:
        valor_aplicado = float(obj["posicaoMercado"].replace("R$", "").replace(".", "").replace(",", "."))
        data_aplicacao = obj["dataVencimento"]
        year = int(data_aplicacao.split("/")[-1])
        yearly_allocation[year] += valor_aplicado
        total_allocation += valor_aplicado

    # Calculate the percentage allocation for each year
    percentage_allocation = {}
    for year, value in yearly_allocation.items():
        percentage_allocation[year] = (value / total_allocation) * 100

    for year in sorted(percentage_allocation.keys(), reverse=True):
        percentage = percentage_allocation[year]
        print(f"Year {year}: {percentage:.2f}% with R$ {yearly_allocation[year]:.2f}")


    with open('output/allocation_results_percentage.csv', 'w', newline='') as csvfile:
        fieldnames = ['Year', 'Percentage', 'Allocation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for year in sorted(percentage_allocation.keys(), reverse=True):
            percentage = percentage_allocation[year]
            allocation = yearly_allocation[year]
            writer.writerow({'Year': year, 'Percentage': f"{percentage:.2f}%", 'Allocation': f"R$ {allocation:.2f}"})


if __name__ == "__main__":
    main()