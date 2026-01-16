# main.py

import sys
from datetime import datetime
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data
from utils.report_generator import generate_sales_report

def main():
    try:
        print("="*50)
        print("        SALES ANALYTICS SYSTEM")
        print("="*50)
        
        # ---------------- [1/10] Read sales data ----------------
        print("\n[1/10] Reading sales data...")
        filename = 'data/sales_data.txt'
        raw_lines = read_sales_data(filename)
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # ---------------- [2/10] Parse and clean ----------------
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        valid_transactions, invalid_count, summary = validate_and_filter(transactions)
        
        # Compute filter info safely
        available_regions = sorted(set(str(tx.get('region')) for tx in transactions if tx.get('region')))
        amounts = [tx.get('amount', 0) for tx in transactions if tx.get('amount') is not None]
        min_amount = min(amounts) if amounts else 0
        max_amount = max(amounts) if amounts else 0
        
        print(f"Available Regions: {', '.join(str(r) for r in available_regions)}")
        print(f"Transaction Amount Range: {min_amount} - {max_amount}")
        print(f"✓ Parsed {len(transactions)} records")
        print(f"Valid transactions: {len(valid_transactions)}, Invalid removed: {invalid_count}")

        # ---------------- [3/10] Filtering ----------------
        print("\n[3/10] Filter Options Available:")
        print(f"Regions: {', '.join(str(r) for r in available_regions)}")
        print(f"Amount Range: ₹{min_amount} - ₹{max_amount}")
        
        user_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()
        if user_filter == 'y':
            # Region filter
            selected_regions = input(f"Enter regions to include (comma-separated, leave empty for all): ")
            selected_regions = [r.strip() for r in selected_regions.split(",") if r.strip()]
            if selected_regions:
                valid_transactions = [tx for tx in valid_transactions if str(tx.get('region')) in selected_regions]
            
            # Amount filter
            amount_min = input(f"Enter minimum amount (leave empty for {min_amount}): ").strip()
            amount_max = input(f"Enter maximum amount (leave empty for {max_amount}): ").strip()
            amount_min = float(amount_min) if amount_min else min_amount
            amount_max = float(amount_max) if amount_max else max_amount
            valid_transactions = [tx for tx in valid_transactions if tx.get('amount', 0) >= amount_min and tx.get('amount', 0) <= amount_max]

        # ---------------- [4/10] Validate ----------------
        print("\n[4/10] Validating transactions...")
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # ---------------- [5/10] Analysis ----------------
        print("\n[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_transactions)
        regions_stats = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions, n=5)
        customer_stats = customer_analysis(valid_transactions)
        daily_trends = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # ---------------- [6/10] Fetch API products ----------------
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # ---------------- [7/10] Enrich transactions ----------------
        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        matched_count = sum(1 for tx in enriched_transactions if tx.get('API_Match'))
        print(f"✓ Enriched {matched_count}/{len(enriched_transactions)} transactions")

        # ---------------- [8/10] Save enriched data ----------------
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions, output_file='data/enriched_sales_data.txt')
        print("✓ Saved to: data/enriched_sales_data.txt")

        # ---------------- [9/10] Generate report ----------------
        print("\n[9/10] Generating report...")
        generate_sales_report(
            transactions=valid_transactions,
            enriched_transactions=enriched_transactions,
            output_file='output/sales_report.txt'
        )
        print("✓ Report saved to: output/sales_report.txt")

        # ---------------- [10/10] Complete ----------------
        print("\n[10/10] Process Complete!")
        print("="*50)

    except Exception as e:
        print(f"\n✗ An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
