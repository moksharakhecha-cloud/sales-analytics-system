def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
            continue

        try:
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': parts[3].replace(',', '').strip(),
                'Quantity': int(parts[4].replace(',', '').strip()),
                'UnitPrice': float(parts[5].replace(',', '').strip()),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            transactions.append(transaction)
        except ValueError:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    for tx in transactions:
        if (
            tx['Quantity'] <= 0 or
            tx['UnitPrice'] <= 0 or
            not tx['TransactionID'].startswith('T') or
            not tx['ProductID'].startswith('P') or
            not tx['CustomerID'].startswith('C')
        ):
            invalid_count += 1
            continue

        amount = tx['Quantity'] * tx['UnitPrice']
        tx['Amount'] = amount

        regions.add(tx['Region'])
        amounts.append(amount)
        valid_transactions.append(tx)

    print(f"Available Regions: {', '.join(sorted(regions))}")
    if amounts:
        print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    filtered = []
    filtered_by_region = 0
    filtered_by_amount = 0

    for tx in valid_transactions:
        if region and tx['Region'] != region:
            filtered_by_region += 1
            continue
        if min_amount and tx['Amount'] < min_amount:
            filtered_by_amount += 1
            continue
        if max_amount and tx['Amount'] > max_amount:
            filtered_by_amount += 1
            continue
        filtered.append(tx)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered)
    }

    return filtered, invalid_count, summary
# utils/data_processor.py

# ---------------- Part 1 ----------------
def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        if len(parts) != 8:
            continue

        try:
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': parts[3].replace(',', '').strip(),
                'Quantity': int(parts[4].replace(',', '').strip()),
                'UnitPrice': float(parts[5].replace(',', '').strip()),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            transactions.append(transaction)
        except ValueError:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    for tx in transactions:
        if (
            tx['Quantity'] <= 0 or
            tx['UnitPrice'] <= 0 or
            not tx['TransactionID'].startswith('T') or
            not tx['ProductID'].startswith('P') or
            not tx['CustomerID'].startswith('C')
        ):
            invalid_count += 1
            continue

        amount = tx['Quantity'] * tx['UnitPrice']
        tx['Amount'] = amount

        regions.add(tx['Region'])
        amounts.append(amount)
        valid_transactions.append(tx)

    print(f"Available Regions: {', '.join(sorted(regions))}")
    if amounts:
        print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    filtered = []
    filtered_by_region = 0
    filtered_by_amount = 0

    for tx in valid_transactions:
        if region and tx['Region'] != region:
            filtered_by_region += 1
            continue
        if min_amount and tx['Amount'] < min_amount:
            filtered_by_amount += 1
            continue
        if max_amount and tx['Amount'] > max_amount:
            filtered_by_amount += 1
            continue
        filtered.append(tx)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered)
    }

    return filtered, invalid_count, summary

# ---------------- Part 2 ----------------
def calculate_total_revenue(transactions):
    return sum(tx['Quantity'] * tx['UnitPrice'] for tx in transactions)


def region_wise_sales(transactions):
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        r = tx['Region']
        amt = tx['Quantity'] * tx['UnitPrice']
        if r not in region_stats:
            region_stats[r] = {'total_sales': 0.0, 'transaction_count': 0}
        region_stats[r]['total_sales'] += amt
        region_stats[r]['transaction_count'] += 1

    for r in region_stats:
        region_stats[r]['percentage'] = round(region_stats[r]['total_sales'] / total_revenue * 100, 2)

    region_stats = dict(sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    return region_stats


def top_selling_products(transactions, n=5):
    product_stats = {}
    for tx in transactions:
        p = tx['ProductName']
        qty = tx['Quantity']
        amt = tx['Quantity'] * tx['UnitPrice']
        if p not in product_stats:
            product_stats[p] = {'total_quantity': 0, 'total_revenue': 0.0}
        product_stats[p]['total_quantity'] += qty
        product_stats[p]['total_revenue'] += amt

    products = [(p, product_stats[p]['total_quantity'], product_stats[p]['total_revenue']) for p in product_stats]
    products.sort(key=lambda x: x[1], reverse=True)
    return products[:n]


def customer_analysis(transactions):
    customer_stats = {}
    for tx in transactions:
        c = tx['CustomerID']
        amt = tx['Quantity'] * tx['UnitPrice']
        p = tx['ProductName']
        if c not in customer_stats:
            customer_stats[c] = {'total_spent': 0.0, 'purchase_count': 0, 'products_bought': set()}
        customer_stats[c]['total_spent'] += amt
        customer_stats[c]['purchase_count'] += 1
        customer_stats[c]['products_bought'].add(p)

    for c in customer_stats:
        stats = customer_stats[c]
        stats['avg_order_value'] = round(stats['total_spent'] / stats['purchase_count'], 2)
        stats['products_bought'] = list(stats['products_bought'])

    customer_stats = dict(sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    return customer_stats


def daily_sales_trend(transactions):
    daily_stats = {}
    for tx in transactions:
        d = tx['Date']
        amt = tx['Quantity'] * tx['UnitPrice']
        cust = tx['CustomerID']
        if d not in daily_stats:
            daily_stats[d] = {'revenue': 0.0, 'transaction_count': 0, 'unique_customers': set()}
        daily_stats[d]['revenue'] += amt
        daily_stats[d]['transaction_count'] += 1
        daily_stats[d]['unique_customers'].add(cust)

    for d in daily_stats:
        daily_stats[d]['unique_customers'] = len(daily_stats[d]['unique_customers'])

    return dict(sorted(daily_stats.items()))


def find_peak_sales_day(transactions):
    daily_stats = daily_sales_trend(transactions)
    peak_day = max(daily_stats.items(), key=lambda x: x[1]['revenue'])
    date = peak_day[0]
    revenue = peak_day[1]['revenue']
    transaction_count = peak_day[1]['transaction_count']
    return date, revenue, transaction_count


def low_performing_products(transactions, threshold=10):
    product_stats = {}
    for tx in transactions:
        p = tx['ProductName']
        qty = tx['Quantity']
        amt = qty * tx['UnitPrice']
        if p not in product_stats:
            product_stats[p] = {'total_quantity': 0, 'total_revenue': 0.0}
        product_stats[p]['total_quantity'] += qty
        product_stats[p]['total_revenue'] += amt

    low_products = [(p, product_stats[p]['total_quantity'], product_stats[p]['total_revenue'])
                    for p in product_stats if product_stats[p]['total_quantity'] < threshold]
    low_products.sort(key=lambda x: x[1])
    return low_products

