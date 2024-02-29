import json
from collections import defaultdict

def scale(original_value, original_lower_bound, original_upper_bound):
    return ((original_value - original_lower_bound) / (original_upper_bound - original_lower_bound)) * 10

def readYearlyAllocationFromFile():
    with open('output/investments.json', 'r') as file:
        objects = json.load(file)

    # Dictionary that provides a default value (0, in this case) for a key that doesn't exist.
    yearly_allocation = defaultdict(float)

    # Parse each object and calculate the allocation for each year
    for obj in objects:
        valor_aplicado = float(obj["posicaoMercado"].replace("R$", "").replace(".", "").replace(",", "."))
        data_aplicacao = obj["dataVencimento"]
        year = int(data_aplicacao.split("/")[-1])
        yearly_allocation[year] += valor_aplicado

    return {key: yearly_allocation[key] for key in sorted(yearly_allocation.keys(), reverse=True)}


def printYearlyAllocationPercentage(yearly_allocation: dict):
    # Calculate the percentage allocation for each year
    total_allocation = sum(yearly_allocation.values())

    percentage_allocation = {}
    for year, value in yearly_allocation.items():
        percentage_allocation[year] = (value / total_allocation) * 100

    for year, percentage in percentage_allocation.items():
        print(f"{year}: {percentage:.2f}% with R$ {yearly_allocation[year]:.2f}")


def printDistributionGrade(yearly_allocation: dict):
    total_allocation = sum(yearly_allocation.values())

    ideal_distribution = total_allocation / len(yearly_allocation)
    
    total_difference = 0

    for allocation in yearly_allocation.values():
        difference = ideal_distribution - allocation  

        total_difference += abs(difference)

    average_difference_graded = scale(total_difference / len(yearly_allocation), total_allocation / len(yearly_allocation), 0)
    print(f"Graded distribution: {average_difference_graded:.2f} out of 10")


def main():
    yearly_allocation = readYearlyAllocationFromFile()

    printYearlyAllocationPercentage(yearly_allocation)

    print("----------------------------------")

    print(f"Total amount: R$ {sum(yearly_allocation.values()):.2f}")
    
    printDistributionGrade(yearly_allocation)


if __name__ == "__main__":
    main()