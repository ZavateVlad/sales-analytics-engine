import json

# Exercise 1

sales = [
    {"product": "laptop", "amount": 1200, "region": "North"},
    {"product": "mouse", "amount": 25, "region": "South"},
    {"product": "keyboard", "amount": 75, "region": "East"},
    {"product": "monitor", "amount": 450, "region": "West"},
    {"product": "laptop", "amount": 1100, "region": "South"}
]

task1 = [row["amount"] for row in sales if row["amount"] > 100]
# print(task1)

task2 = set([row["product"] for row in sales])
# I added set to be unique values,
# since the products don't have a name and would be easier to understand what products we have
# print(task2)

task3 = [row for row in sales if row["region"] == "South"]
# print(task3)

task4 = [(row["amount"] + row["amount"] / 10) for row in sales]
# print(task4)

# Exercise 2
task5 = {row["product"]: row["amount"] for row in sales}
# print(task5)

task6 = {row["region"]: row["amount"] for row in sales}
# print(task6)

task7 = {row["product"]: row["amount"] for row in sales if row["amount"] > 100}
# print(task7)

task8 = {row["product"].upper(): row["amount"] for row in sales}
# print(task8)

task9 = sorted(sales, key=lambda x: x["amount"], reverse=True)
# print(task9)

task10 = max(sales, key=lambda x: x["amount"])
# print(task10)

task11 = list(filter(lambda x: x["amount"] > 100, sales))
# print(task11)

task12 = list(map(lambda x: x["amount"], sales))


# How is this working really? map does apply the x["amount"] function on sales? why i would ever use map with lambda?
# print(task12)


def load_and_clean_sales(filename):
    data = []
    with open(filename, "r") as f:
        header = f.readline().strip().split(",")
        for line in f:
            rows = line.strip().split(',')
            data.append(dict(zip(header, rows)))

    cleaned_data = [
        {
            **element,
            'quantity': int(element['quantity']),
            'unit_price': float(element['unit_price']),
            'revenue': int(element['quantity']) * float(element['unit_price'])
        }
        for element in data
        if element['quantity'].isdigit()
    ]

    return cleaned_data


print(load_and_clean_sales("sales_q1.csv"))


def calculate_basic_metrics(sales_data):
    with open("analytics_config.json", "r") as f:
        config_data = json.load(f)
        basic_metrics = {
            "total_revenue": sum([row["revenue"] for row in sales_data]),
            "average_order_value": sum([row["revenue"] for row in sales_data]) / len(sales_data),
            "high_value_orders": [row for row in sales_data if
                                  row["revenue"] > config_data["high_value_threshold"]]
        }
    return basic_metrics


print(calculate_basic_metrics(load_and_clean_sales("sales_q1.csv")))


def calculate_revenue_by_category(sales_data):
    revenues = {
        "revenue_by_region": {region: sum(row["revenue"] for row in sales_data if row["region"] == region)
                              for region in set(row["region"] for row in sales_data)},
        "revenue_by_product": {product: sum(row["revenue"] for row in sales_data if row["product"] == product)
                               for product in set(row["product"] for row in sales_data)}
    }
    return revenues


print(calculate_revenue_by_category(load_and_clean_sales("sales_q1.csv")))


def get_top_performers(sales_data, config):
    # Read JSON file
    with open(config, "r") as f:
        config_data = json.load(f)

    # Calculate top_product
    pairs = list(calculate_revenue_by_category(sales_data)["revenue_by_product"].items())
    product_rank = sorted(pairs, key=lambda x: x[1], reverse=True)

    # Calculate top_person
    revenue_by_salesperson = {
        sale_person: (sum(person["revenue"] for person in sales_data if person["salesperson"] == sale_person))
        for sale_person in set(person["salesperson"] for person in sales_data)}

    top_data = {
        "top_products": [list(element) for element in product_rank[0:config_data["top_n_products"]]],
        "top_salesperson": max(revenue_by_salesperson.items(), key=lambda x: x[1])[0]

    }
    return top_data


print(get_top_performers(load_and_clean_sales("sales_q1.csv"), "analytics_config.json"))


def generate_analytics_report(filename, config_file):
    sales_data = load_and_clean_sales(filename)

    basic_metrics = calculate_basic_metrics(sales_data)
    category_revenue = calculate_revenue_by_category(sales_data)
    top_performers = get_top_performers(sales_data, config_file)

    output_dictionary = {**basic_metrics, **category_revenue, **top_performers}

    with open("analytics_report.json", "w") as r:
        json.dump(output_dictionary, r, indent=2)

    return output_dictionary

print(generate_analytics_report("sales_q1.csv", "analytics_config.json"))
