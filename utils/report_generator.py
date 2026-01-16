# utils/report_generator.py

from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report safely handling None values.
    """

    def safe_str(val):
        return str(val) if val is not None else "N/A"

    # Overall summary
    total_revenue = sum(tx.get('amount', 0) for tx in transactions)
    total_transactions = len(transactions)
    avg_order = total_revenue / total_transactions if total_transactions else 0
    dates = [tx.get('date') for tx in transactions if tx.get('date')]
    start_date = min(dates) if dates else "N/A"
    end_date = max(dates) if dates else "N/A"

    # Region-wise
    region_summary = {}
    for tx in transactions:
        region = safe_str(tx.get('region'))
        amt = tx.get('amount', 0)
        if region not in region_summary:
            region_summary[region] = {'total_sales': 0, 'transactions': 0}
        region_summary[region]['total_sales'] += amt
        region_summary[region]['transactions'] += 1

    # Top products
    product_totals = {}
    for tx in transactions:
        products = tx.get('products_bought') or []
        for p in products:
            pname = safe_str(p)
            if pname not in product_totals:
                product_totals[pname] = {'quantity': 0, 'revenue': 0}
            product_totals[pname]['quantity'] += 1
            product_totals[pname]['revenue'] += tx.get('amount', 0)
    top_products = sorted(product_totals.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]

    # Top customers
    customer_totals = {}
    for tx in transactions:
        cust = safe_str(tx.get('customer_id'))
        amt = tx.get('amount', 0)
        if cust not in customer_totals:
            customer_totals[cust] = {'total_spent': 0, 'orders': 0}
        customer_totals[cust]['total_spent'] += amt
        customer_totals[cust]['orders'] += 1
    top_customers = sorted(customer_totals.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]

    # Daily trends
    daily_stats = {}
    for tx in transactions:
        date = safe_str(tx.get('date'))
        if date not in daily_stats:
            daily_stats[date] = {'revenue': 0, 'transactions': 0, 'customers': set()}
        daily_stats[date]['revenue'] += tx.get('amount', 0)
        daily_stats[date]['transactions'] += 1
        daily_stats[date]['customers'].add(safe_str(tx.get('customer_id')))
    
    # API enrichment
    total_enriched = sum(1 for tx in enriched_transactions if tx.get('API_Match'))
    success_rate = (total_enriched / len(enriched_transactions) * 100) if enriched_transactions else 0
    unmatched_products = [tx.get('product_name', 'N/A') for tx in enriched_transactions if not tx.get('API_Match')]

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*40 + "\n")
        f.write("       SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("="*40 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-"*40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order:,.2f}\n")
        f.write(f"Date Range: {start_date} to {end_date}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Region':<10} {'Sales':>15} {'Transactions':>15}\n")
        for region, stats in sorted(region_summary.items(), key=lambda x: x[1]['total_sales'], reverse=True):
            f.write(f"{region:<10} ₹{stats['total_sales']:>14,.2f} {stats['transactions']:>15}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Rank':<5} {'Product':<20} {'Qty':>5} {'Revenue':>15}\n")
        for idx, (pname, data) in enumerate(top_products, 1):
            f.write(f"{idx:<5} {pname:<20} {data['quantity']:>5} ₹{data['revenue']:>14,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Rank':<5} {'Customer':<15} {'Total Spent':>15} {'Orders':>10}\n")
        for idx, (cust, data) in enumerate(top_customers, 1):
            f.write(f"{idx:<5} {cust:<15} ₹{data['total_spent']:>14,.2f} {data['orders']:>10}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Date':<12} {'Revenue':>15} {'Transactions':>12} {'Unique Customers':>18}\n")
        for date, stats in sorted(daily_stats.items()):
            f.write(f"{date:<12} ₹{stats['revenue']:>14,.2f} {stats['transactions']:>12} {len(stats['customers']):>18}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-"*40 + "\n")
        f.write(f"Total products enriched: {total_enriched}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n")
        f.write(f"Unmatched products: {', '.join(safe_str(p) for p in unmatched_products)}\n")
        f.write("\n")
        f.write("=== END OF REPORT ===\n")
