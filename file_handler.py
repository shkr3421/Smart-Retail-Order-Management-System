def show_daily_report():
    import csv
    total_sales = 0

    try:
        with open("orders.csv", "r") as file:
            reader = csv.DictReader(file)

            print("\n--- DAILY SALES REPORT ---")
            for row in reader:
                print(
                    f"Order ID: {row['order_id']} | "
                    f"Product: {row['product_name']} | "
                    f"Qty: {row['quantity']} | "
                    f"Total: {row['total']}"
                )
                total_sales += float(row["total"])

            print("Total Revenue:", total_sales)

    except FileNotFoundError:
        print("No orders found yet.")
