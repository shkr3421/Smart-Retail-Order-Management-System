import csv
from datetime import datetime
from typing import Dict, List, Optional
import os


class BillItem:
    """Represents a single item in the bill"""
    
    def __init__(self, product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.unit_price = product.price
        self.subtotal = self.unit_price * quantity
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity} @ ₹{self.unit_price} = ₹{self.subtotal}"


class Bill:
    """Handles billing calculations, discounts, taxes and bill generation"""
    
    def __init__(self, customer_name: str = "Walk-in Customer"):
        self.customer_name = customer_name
        self.items: List[BillItem] = []
        self.discount_percent = 0.0
        self.tax_percent = 5.0  # Default GST
        self.bill_number = self._generate_bill_number()
        self.timestamp = datetime.now()
        self.payment_method = ""
        self.payment_status = "Pending"
    
    def _generate_bill_number(self) -> str:
        """Generate unique bill number based on timestamp"""
        return f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def add_item(self, product, quantity: int) -> bool:
        """Add item to bill if stock is available"""
        if product.is_stock_available(quantity):
            # Check if product already exists in bill
            for item in self.items:
                if item.product.pid == product.pid:
                    item.quantity += quantity
                    item.subtotal = item.unit_price * item.quantity
                    product.reduce_stock(quantity)
                    return True
            
            # Add new item
            bill_item = BillItem(product, quantity)
            self.items.append(bill_item)
            product.reduce_stock(quantity)
            return True
        else:
            print(f"❌ Insufficient stock for {product.name}. Available: {product.stock}")
            return False
    
    def remove_item(self, product_id: int) -> bool:
        """Remove item from bill and restore stock"""
        for i, item in enumerate(self.items):
            if item.product.pid == product_id:
                # Restore stock
                item.product.stock += item.quantity
                self.items.pop(i)
                return True
        return False
    
    def apply_discount(self, discount_percent: float):
        """Apply percentage discount to the bill"""
        if 0 <= discount_percent <= 100:
            self.discount_percent = discount_percent
        else:
            raise ValueError("Discount must be between 0 and 100")
    
    def set_tax_rate(self, tax_percent: float):
        """Set tax percentage"""
        if tax_percent >= 0:
            self.tax_percent = tax_percent
        else:
            raise ValueError("Tax rate cannot be negative")
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal before discount and tax"""
        return sum(item.subtotal for item in self.items)
    
    def calculate_discount_amount(self) -> float:
        """Calculate discount amount"""
        return (self.calculate_subtotal() * self.discount_percent) / 100
    
    def calculate_tax_amount(self) -> float:
        """Calculate tax on discounted amount"""
        discounted_amount = self.calculate_subtotal() - self.calculate_discount_amount()
        return (discounted_amount * self.tax_percent) / 100
    
    def calculate_total(self) -> float:
        """Calculate final total amount"""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount_amount()
        tax = self.calculate_tax_amount()
        return subtotal - discount + tax
    
    def is_empty(self) -> bool:
        """Check if bill has any items"""
        return len(self.items) == 0
    
    def display_bill(self):
        """Display formatted bill"""
        if self.is_empty():
            print("⚠ No items in the bill")
            return
        
        print("\n" + "="*50)
        print("           SMART RETAIL STORE")
        print("="*50)
        print(f"Bill No: {self.bill_number}")
        print(f"Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Customer: {self.customer_name}")
        print("-"*50)
        print(f"{'Item':<20} {'Qty':<5} {'Rate':<8} {'Amount':<10}")
        print("-"*50)
        
        for item in self.items:
            print(f"{item.product.name:<20} {item.quantity:<5} ₹{item.unit_price:<7} ₹{item.subtotal:<9}")
        
        print("-"*50)
        subtotal = self.calculate_subtotal()
        discount_amount = self.calculate_discount_amount()
        tax_amount = self.calculate_tax_amount()
        total = self.calculate_total()
        
        print(f"{'Subtotal:':<35} ₹{subtotal:.2f}")
        
        if self.discount_percent > 0:
            print(f"{'Discount (' + str(self.discount_percent) + '%):':<35} -₹{discount_amount:.2f}")
        
        if self.tax_percent > 0:
            print(f"{'Tax (' + str(self.tax_percent) + '%):':<35} +₹{tax_amount:.2f}")
        
        print("-"*50)
        print(f"{'TOTAL AMOUNT:':<35} ₹{total:.2f}")
        print("="*50)
        print("        Thank you for shopping!")
        print("="*50)
    
    def set_payment_info(self, method: str, status: str = "Completed"):
        """Set payment method and status"""
        self.payment_method = method
        self.payment_status = status
    
    def save_to_csv(self, filename: str = "daily_sales.csv"):
        """Save bill details to CSV file"""
        try:
            with open(filename, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                
                # Write header if file is empty
                if file.tell() == 0:
                    writer.writerow([
                        "Date", "Bill_Number", "Customer", "Product_ID", 
                        "Product_Name", "Quantity", "Unit_Price", "Subtotal",
                        "Discount_Percent", "Tax_Percent", "Total_Amount",
                        "Payment_Method", "Payment_Status"
                    ])
                
                total_amount = self.calculate_total()
                
                for item in self.items:
                    writer.writerow([
                        self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        self.bill_number,
                        self.customer_name,
                        item.product.pid,
                        item.product.name,
                        item.quantity,
                        item.unit_price,
                        item.subtotal,
                        self.discount_percent,
                        self.tax_percent,
                        total_amount,
                        self.payment_method,
                        self.payment_status
                    ])
            
            print(f"💾 Bill saved to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving bill: {e}")
            return False


class PaymentProcessor:
    """Handles different payment methods"""
    
    @staticmethod
    def process_cash_payment(bill_amount: float) -> Dict:
        """Process cash payment with change calculation"""
        try:
            cash_received = float(input(f"Enter cash received (Bill Amount: ₹{bill_amount:.2f}): ₹"))
            
            if cash_received < bill_amount:
                return {
                    "success": False,
                    "method": "Cash",
                    "message": f"Insufficient cash. Need ₹{bill_amount - cash_received:.2f} more."
                }
            
            change = cash_received - bill_amount
            return {
                "success": True,
                "method": "Cash",
                "amount_received": cash_received,
                "change": change,
                "message": f"Payment successful. Change: ₹{change:.2f}"
            }
            
        except ValueError:
            return {
                "success": False,
                "method": "Cash",
                "message": "Invalid cash amount entered."
            }
    
    @staticmethod
    def process_card_payment(bill_amount: float) -> Dict:
        """Process card payment (simulation)"""
        print(f"Processing card payment of ₹{bill_amount:.2f}...")
        print("Please swipe/insert your card...")
        
        # Simulate card processing
        import time
        time.sleep(1)
        
        return {
            "success": True,
            "method": "Card",
            "amount_received": bill_amount,
            "change": 0,
            "message": "Card payment successful!"
        }
    
    @staticmethod
    def process_upi_payment(bill_amount: float) -> Dict:
        """Process UPI payment (simulation)"""
        print(f"UPI Payment: ₹{bill_amount:.2f}")
        print("Scan QR code or enter UPI ID...")
        
        # Simulate UPI processing
        import time
        time.sleep(1)
        
        return {
            "success": True,
            "method": "UPI",
            "amount_received": bill_amount,
            "change": 0,
            "message": "UPI payment successful!"
        }


class ReportGenerator:
    """Generates various reports from sales data"""
    
    @staticmethod
    def generate_payment_summary(filename: str = "daily_sales.csv") -> Dict:
        """Generate payment method summary"""
        if not os.path.exists(filename):
            return {"error": "No sales data found"}
        
        payment_summary = {
            "Cash": {"count": 0, "amount": 0.0},
            "Card": {"count": 0, "amount": 0.0},
            "UPI": {"count": 0, "amount": 0.0},
            "total_transactions": 0,
            "total_amount": 0.0
        }
        
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                processed_bills = set()
                
                for row in reader:
                    bill_number = row.get("Bill_Number", "")
                    if bill_number in processed_bills:
                        continue
                    
                    processed_bills.add(bill_number)
                    payment_method = row.get("Payment_Method", "Cash")
                    total_amount_str = row.get("Total_Amount", "0")
                    
                    try:
                        total_amount = float(total_amount_str) if total_amount_str else 0.0
                    except (ValueError, TypeError):
                        total_amount = 0.0
                    
                    if payment_method in payment_summary:
                        payment_summary[payment_method]["count"] += 1
                        payment_summary[payment_method]["amount"] += total_amount
                    
                    payment_summary["total_transactions"] += 1
                    payment_summary["total_amount"] += total_amount
            
            return payment_summary
            
        except Exception as e:
            return {"error": f"Error reading sales data: {e}"}
    
    @staticmethod
    def generate_daily_summary(date: str = None, filename: str = "daily_sales.csv") -> Dict:
        """Generate daily sales summary"""
        if not os.path.exists(filename):
            return {"error": "No sales data found"}
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        daily_summary = {
            "date": date,
            "total_bills": 0,
            "total_items_sold": 0,
            "total_revenue": 0.0,
            "total_discount": 0.0,
            "total_tax": 0.0,
            "top_products": {},
            "customer_count": 0
        }
        
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                processed_bills = set()
                customers = set()
                
                for row in reader:
                    row_date = row.get("Date", "").split(" ")[0]
                    if row_date != date:
                        continue
                    
                    bill_number = row.get("Bill_Number", "")
                    customer = row.get("Customer", "")
                    product_name = row.get("Product_Name", "")
                    
                    try:
                        quantity = int(row.get("Quantity", "0")) if row.get("Quantity") else 0
                        total_amount = float(row.get("Total_Amount", "0")) if row.get("Total_Amount") else 0.0
                        discount_percent = float(row.get("Discount_Percent", "0")) if row.get("Discount_Percent") else 0.0
                    except (ValueError, TypeError):
                        quantity = 0
                        total_amount = 0.0
                        discount_percent = 0.0
                    
                    # Count unique bills
                    if bill_number not in processed_bills:
                        processed_bills.add(bill_number)
                        daily_summary["total_bills"] += 1
                        daily_summary["total_revenue"] += total_amount
                        daily_summary["total_discount"] += (total_amount * discount_percent) / (100 - discount_percent) if discount_percent > 0 else 0
                    
                    # Count customers
                    if customer:
                        customers.add(customer)
                    
                    # Count items
                    daily_summary["total_items_sold"] += quantity
                    
                    # Track top products
                    if product_name in daily_summary["top_products"]:
                        daily_summary["top_products"][product_name] += quantity
                    else:
                        daily_summary["top_products"][product_name] = quantity
                
                daily_summary["customer_count"] = len(customers)
                
                # Sort top products
                daily_summary["top_products"] = dict(
                    sorted(daily_summary["top_products"].items(), 
                           key=lambda x: x[1], reverse=True)[:5]
                )
            
            return daily_summary
            
        except Exception as e:
            return {"error": f"Error reading sales data: {e}"}
    
    @staticmethod
    def display_payment_summary():
        """Display payment summary in formatted way"""
        summary = ReportGenerator.generate_payment_summary()
        
        if "error" in summary:
            print(f"❌ {summary['error']}")
            return
        
        print("\n" + "="*40)
        print("       PAYMENT METHOD SUMMARY")
        print("="*40)
        print(f"{'Method':<10} {'Count':<8} {'Amount':<12}")
        print("-"*40)
        
        for method in ["Cash", "Card", "UPI"]:
            count = summary[method]["count"]
            amount = summary[method]["amount"]
            print(f"{method:<10} {count:<8} ₹{amount:<11.2f}")
        
        print("-"*40)
        print(f"{'TOTAL':<10} {summary['total_transactions']:<8} ₹{summary['total_amount']:<11.2f}")
        print("="*40)
    
    @staticmethod
    def display_daily_summary(date: str = None):
        """Display daily summary in formatted way"""
        summary = ReportGenerator.generate_daily_summary(date)
        
        if "error" in summary:
            print(f"❌ {summary['error']}")
            return
        
        print("\n" + "="*50)
        print(f"       DAILY SALES SUMMARY - {summary['date']}")
        print("="*50)
        print(f"Total Bills: {summary['total_bills']}")
        print(f"Total Customers: {summary['customer_count']}")
        print(f"Total Items Sold: {summary['total_items_sold']}")
        print(f"Total Revenue: ₹{summary['total_revenue']:.2f}")
        print(f"Total Discount Given: ₹{summary['total_discount']:.2f}")
        print("-"*50)
        print("TOP SELLING PRODUCTS:")
        
        if summary['top_products']:
            for product, qty in summary['top_products'].items():
                print(f"  {product}: {qty} units")
        else:
            print("  No sales data available")
        
        print("="*50)


def create_sample_bill():
    """Create a sample bill for testing"""
    from product import load_inventory
    
    inventory = load_inventory()
    bill = Bill("John Doe")
    
    # Add some items
    rice = inventory.get_product(101)
    oil = inventory.get_product(103)
    
    if rice and oil:
        bill.add_item(rice, 2)
        bill.add_item(oil, 1)
        bill.apply_discount(10)  # 10% discount
        
        bill.display_bill()
        return bill
    
    return None


if __name__ == "__main__":
    # Test the billing system
    print("Testing Billing System...")
    sample_bill = create_sample_bill()
    
    if sample_bill:
        # Test payment processing
        print("\n--- Payment Processing ---")
        payment_result = PaymentProcessor.process_cash_payment(sample_bill.calculate_total())
        print(payment_result["message"])
        
        # Test reporting
        print("\n--- Testing Reports ---")
        ReportGenerator.display_payment_summary()
        ReportGenerator.display_daily_summary()