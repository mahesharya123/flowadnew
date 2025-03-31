import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.express as px
import plotly.graph_objects as go
import uuid

class PaymentSystem:
    """
    Class to manage payments for both drivers and advertisers
    """
    
    def __init__(self):
        """Initialize the payment system"""
        # Initialize payment records in session state if not already present
        if "payment_records" not in st.session_state:
            st.session_state.payment_records = []
        
        # Initialize invoice records in session state
        if "invoices" not in st.session_state:
            st.session_state.invoices = []
            
        # Initialize payment methods in session state
        if "payment_methods" not in st.session_state:
            st.session_state.payment_methods = []
    
    def add_payment(self, payment_data):
        """
        Add a new payment record
        
        Parameters:
        - payment_data: Dictionary containing payment information
        """
        # Add payment ID and timestamp
        payment_data["payment_id"] = str(uuid.uuid4())
        payment_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.session_state.payment_records.append(payment_data)
        return payment_data
    
    def get_payments(self, user_id=None, payment_type=None, date_from=None, date_to=None, status=None):
        """
        Get payment records with optional filters
        
        Parameters:
        - user_id: Filter by user ID
        - payment_type: Filter by payment type (driver_payment, advertiser_payment)
        - date_from: Filter by start date (YYYY-MM-DD)
        - date_to: Filter by end date (YYYY-MM-DD)
        - status: Filter by payment status (pending, completed, failed)
        """
        if "payment_records" not in st.session_state:
            st.session_state.payment_records = []  # Initialize if missing
            
        payments = st.session_state.payment_records
        
        # Apply filters
        if user_id:
            payments = [p for p in payments if p.get("user_id") == user_id]
        
        if payment_type:
            payments = [p for p in payments if p.get("payment_type") == payment_type]
        
        if date_from:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            payments = [p for p in payments if datetime.strptime(p.get("timestamp").split()[0], "%Y-%m-%d") >= date_from_obj]
        
        if date_to:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            payments = [p for p in payments if datetime.strptime(p.get("timestamp").split()[0], "%Y-%m-%d") <= date_to_obj]
        
        if status:
            payments = [p for p in payments if p.get("status") == status]
        
        return payments
    
    def create_driver_payment(self, driver_id, amount, description="Driver payment"):
        """
        Create a payment for a driver
        
        Parameters:
        - driver_id: ID of the driver
        - amount: Payment amount
        - description: Payment description
        """
        payment_data = {
            "user_id": driver_id,
            "payment_type": "driver_payment",
            "amount": amount,
            "description": description,
            "status": "pending"
        }
        
        return self.add_payment(payment_data)
    
    def process_advertiser_payment(self, advertiser_id, campaign_id, amount, payment_method="credit_card"):
        """
        Process a payment from an advertiser
        
        Parameters:
        - advertiser_id: ID of the advertiser
        - campaign_id: ID of the campaign
        - amount: Payment amount
        - payment_method: Payment method (credit_card, bank_transfer, upi)
        """
        payment_data = {
            "user_id": advertiser_id,
            "campaign_id": campaign_id,
            "payment_type": "advertiser_payment",
            "amount": amount,
            "payment_method": payment_method,
            "status": "completed",  # Assume immediate completion for the demo
            "transaction_id": f"TXN-{str(uuid.uuid4())[:8].upper()}"
        }
        
        return self.add_payment(payment_data)
    
    def create_invoice(self, user_id, user_type, amount, items, due_date=None):
        """
        Create an invoice
        
        Parameters:
        - user_id: ID of the user (advertiser or driver)
        - user_type: Type of user (advertiser, driver)
        - amount: Total invoice amount
        - items: List of invoice items
        - due_date: Invoice due date (defaults to 15 days from now)
        """
        if due_date is None:
            due_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        
        invoice_data = {
            "invoice_id": f"INV-{str(uuid.uuid4())[:8].upper()}",
            "user_id": user_id,
            "user_type": user_type,
            "amount": amount,
            "items": items,
            "issue_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date,
            "status": "pending"
        }
        
        st.session_state.invoices.append(invoice_data)
        return invoice_data
    
    def get_invoices(self, user_id=None, status=None):
        """
        Get invoices with optional filters
        
        Parameters:
        - user_id: Filter by user ID
        - status: Filter by invoice status (pending, paid, overdue)
        """
        # Initialize invoices in session state if not already present
        if "invoices" not in st.session_state:
            st.session_state.invoices = []
            
        invoices = st.session_state.invoices
        
        # Apply filters
        if user_id:
            invoices = [inv for inv in invoices if inv.get("user_id") == user_id]
        
        if status:
            invoices = [inv for inv in invoices if inv.get("status") == status]
        
        return invoices
    
    def add_payment_method(self, user_id, method_data):
        """
        Add a payment method for a user
        
        Parameters:
        - user_id: ID of the user
        - method_data: Dictionary containing payment method details
        """
        # Add method ID
        method_data["method_id"] = str(uuid.uuid4())
        method_data["user_id"] = user_id
        method_data["added_date"] = datetime.now().strftime("%Y-%m-%d")
        
        # Add to session state
        st.session_state.payment_methods.append(method_data)
        return method_data
    
    def get_payment_methods(self, user_id):
        """
        Get payment methods for a user
        
        Parameters:
        - user_id: ID of the user
        """
        if "payment_methods" not in st.session_state:
            st.session_state.payment_methods = []
            
        filtered_methods = [method for method in st.session_state.payment_methods if method.get("user_id") == user_id]
        return filtered_methods
    
    def display_payment_form(self, user_id, user_type, amount=None, description=None):
        """
        Display a payment form
        
        Parameters:
        - user_id: ID of the user making the payment
        - user_type: Type of user (advertiser, driver)
        - amount: Pre-filled amount (optional)
        - description: Pre-filled description (optional)
        """
        st.subheader("Payment Details")
        
        with st.form("payment_form"):
            # Payment amount
            if amount is None:
                amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
            else:
                st.metric("Amount to Pay", f"₹{amount:.2f}")
            
            # Payment description
            if description is None:
                description = st.text_area("Description", placeholder="Payment description")
            else:
                st.write(f"**Description:** {description}")
            
            # Payment method selection
            payment_methods = [
                "Credit/Debit Card",
                "UPI",
                "Bank Transfer",
                "Net Banking"
            ]
            
            selected_method = st.selectbox("Select Payment Method", payment_methods)
            
            # Different input fields based on payment method
            if selected_method == "Credit/Debit Card":
                card_number = st.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
                col1, col2 = st.columns(2)
                with col1:
                    expiry = st.text_input("Expiry (MM/YY)", placeholder="MM/YY")
                with col2:
                    cvv = st.text_input("CVV", placeholder="XXX", type="password")
                name_on_card = st.text_input("Name on Card")
            
            elif selected_method == "UPI":
                upi_id = st.text_input("UPI ID", placeholder="username@upi")
            
            elif selected_method == "Bank Transfer":
                st.info("You will be redirected to your bank's website to complete the transaction.")
            
            elif selected_method == "Net Banking":
                banks = ["HDFC Bank", "ICICI Bank", "State Bank of India", "Axis Bank", "Kotak Mahindra Bank"]
                selected_bank = st.selectbox("Select Bank", banks)
            
            # Terms acceptance
            terms_accepted = st.checkbox("I accept the terms and conditions")
            
            # Submit button
            submit_button = st.form_submit_button("Make Payment")
            
            if submit_button:
                if not terms_accepted:
                    st.error("Please accept the terms and conditions to proceed.")
                    return None
                
                if amount <= 0:
                    st.error("Please enter a valid amount.")
                    return None
                
                # Validate payment method inputs
                if selected_method == "Credit/Debit Card":
                    if not card_number or not expiry or not cvv or not name_on_card:
                        st.error("Please fill in all card details.")
                        return None
                    
                    # Basic validation
                    if not card_number.replace(" ", "").isdigit() or len(card_number.replace(" ", "")) != 16:
                        st.error("Please enter a valid 16-digit card number.")
                        return None
                
                elif selected_method == "UPI":
                    if not upi_id or "@" not in upi_id:
                        st.error("Please enter a valid UPI ID.")
                        return None
                
                # Create a payment record
                payment_data = {
                    "user_id": user_id,
                    "payment_type": f"{user_type}_payment",
                    "amount": amount,
                    "description": description,
                    "payment_method": selected_method.lower().replace("/", "_"),
                    "status": "completed"  # Assume success for demo
                }
                
                payment = self.add_payment(payment_data)
                
                # Show success message
                st.success(f"Payment of ₹{amount:.2f} processed successfully. Transaction ID: {payment['payment_id'][:8]}")
                return payment
        
        return None
    
    def display_payment_summary(self, user_id=None, payment_type=None):
        """
        Display a summary of payments
        
        Parameters:
        - user_id: ID of the user (optional)
        - payment_type: Type of payment (optional)
        """
        payments = self.get_payments(user_id=user_id, payment_type=payment_type)
        
        if not payments:
            st.info("No payment records found.")
            return
        
        # Create summary statistics
        total_amount = sum(p.get("amount", 0) for p in payments)
        completed_payments = [p for p in payments if p.get("status") == "completed"]
        pending_payments = [p for p in payments if p.get("status") == "pending"]
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Transactions", len(payments))
        
        with col2:
            st.metric("Total Amount", f"₹{total_amount:.2f}")
        
        with col3:
            st.metric("Pending Payments", len(pending_payments))
        
        # Recent transactions
        st.subheader("Recent Transactions")
        
        # Create a DataFrame for display
        payment_data = []
        for payment in sorted(payments, key=lambda p: p.get("timestamp", ""), reverse=True)[:10]:
            payment_data.append({
                "Date": payment.get("timestamp", "").split()[0],
                "Description": payment.get("description", "Payment"),
                "Amount": f"₹{payment.get('amount', 0):.2f}",
                "Status": payment.get("status", "unknown").title(),
                "Method": payment.get("payment_method", "unknown").replace("_", " ").title()
            })
        
        # Display as table
        if payment_data:
            st.dataframe(pd.DataFrame(payment_data), use_container_width=True)
        
        # Payment trend over time
        st.subheader("Payment Trend")
        
        # Group payments by date
        payment_by_date = {}
        for payment in payments:
            date = payment.get("timestamp", "").split()[0]
            amount = payment.get("amount", 0)
            
            if date in payment_by_date:
                payment_by_date[date] += amount
            else:
                payment_by_date[date] = amount
        
        # Sort dates
        dates = sorted(payment_by_date.keys())
        amounts = [payment_by_date[date] for date in dates]
        
        # Create line chart
        if dates and amounts:
            fig = px.line(
                x=dates,
                y=amounts,
                title="Payment Trend Over Time",
                labels={"x": "Date", "y": "Amount (₹)"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def display_invoice(self, invoice_id):
        """
        Display an invoice
        
        Parameters:
        - invoice_id: ID of the invoice to display
        """
        # Find the invoice
        invoice = None
        for inv in st.session_state.invoices:
            if inv.get("invoice_id") == invoice_id:
                invoice = inv
                break
        
        if not invoice:
            st.error("Invoice not found.")
            return
        
        # Display invoice header
        st.markdown(f"### Invoice #{invoice['invoice_id']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Issue Date:** {invoice['issue_date']}")
            st.markdown(f"**Due Date:** {invoice['due_date']}")
        
        with col2:
            st.markdown(f"**Status:** {invoice['status'].title()}")
            st.markdown(f"**Total Amount:** ₹{invoice['amount']:.2f}")
        
        st.divider()
        
        # Display invoice items
        st.subheader("Invoice Items")
        
        items_data = []
        for item in invoice.get("items", []):
            items_data.append({
                "Description": item.get("description", ""),
                "Amount": f"₹{item.get('amount', 0):.2f}"
            })
        
        if items_data:
            st.dataframe(pd.DataFrame(items_data), use_container_width=True)
        else:
            st.info("No items in this invoice.")
        
        st.divider()
        
        # Display payment options if invoice is pending
        if invoice["status"] == "pending":
            st.subheader("Pay This Invoice")
            
            if st.button("Proceed to Payment"):
                st.session_state.paying_invoice = invoice_id