from pathlib import Path
import json
import random
import string
import streamlit as st

# --- Your Bank Class (Integrated for Streamlit) ---
class Bank:
    # Use 'bank_database.json' to ensure persistence across sessions/restarts
    # In a real app, you would use a proper database, but JSON file simulates persistence.
    database = 'bank_database.json'
    data = []

    # Initialize data load when class is defined
    try: 
        db_path = Path(database)
        if db_path.exists():
            with open(db_path, 'r') as fs:
                content = fs.read()
                if content:
                    data = json.loads(content)
                else:
                    data = []
        else:
            with open(db_path, 'w') as fs:
                fs.write("[]")
            # print(f"Database file '{database}' created.")

    except Exception as err:
        st.error(f"An error occurred while loading database: {err}")

    @classmethod
    def __update(cls):
        """Saves the current data list to the JSON file."""
        try:
            with open(cls.database, 'w') as fs:
                json.dump(cls.data, fs, indent=4)
        except Exception as err:
            st.error(f"An error occurred during database update: {err}")
    
    @staticmethod
    def __accountno():
        """Generates a 9-character alphanumeric account number."""
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id_list = alpha + digits
        random.shuffle(id_list)
        return "".join(id_list)
    
    def get_user(self, accNo, pin):
        """Helper to find user data by account number and pin."""
        try:
            pin = int(pin)
        except ValueError:
            return None 

        user_data = [i for i in Bank.data if i.get('Account no.') == accNo and i.get('pin') == pin]
        return user_data[0] if user_data else None

    # --- Methods for the GUI ---
    def create_account(self, name, email, phone_no_str, pin_str):
        try:
            phone_no = int(phone_no_str)
            pin = int(pin_str)
        except ValueError:
            return "Error: Phone number and Pin must be valid numbers."

        if len(str(pin)) != 4:
            return "Error: Pin must be 4 digits."
        
        if len(str(phone_no)) != 10:
            return "Error: Phone number must be 10 digits."

        d = {
            "name": name,
            "email": email,
            "phone no.": phone_no,
            "pin": pin,
            "Account no.": Bank.__accountno(),
            "Balance": 0
        }

        Bank.data.append(d)
        Bank.__update()
        return f"Success! Account created. Your Account no. is: **{d['Account no.']}**. Please remember it."

    def deposit_money(self, accNo, pin, amount_str):
        user_data = self.get_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect Account no./Pin."
        
        try:
            amount = int(amount_str)
        except ValueError:
            return "Error: Deposit amount must be a number."
            
        if amount <= 0:
            return "Error: Invalid amount."
        elif amount > 10000:
            return "Error: Deposit limit is 10000."
        else:
            user_data['Balance'] += amount
            Bank.__update()
            return f"Success! Amount credited. New Balance: **${user_data['Balance']:,}**"

    def withdraw_money(self, accNo, pin, amount_str):
        user_data = self.get_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect Account no./Pin."

        try:
            amount = int(amount_str)
        except ValueError:
            return "Error: Withdrawal amount must be a number."

        if amount <= 0:
            return "Error: Invalid amount."
        elif amount > 10000:
            return "Error: Withdrawal limit is 10000."
        elif amount > user_data['Balance']:
            return "Error: Insufficient balance. Current balance is **${user_data['Balance']:,}**."
        else:
            user_data['Balance'] -= amount
            Bank.__update()
            return f"Success! Amount debited. New Balance: **${user_data['Balance']:,}**"

    def get_details(self, accNo, pin):
        user_data = self.get_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect Account no./Pin."
        else:
            details_str = "\n".join([f"- **{k}:** {v}" for k, v in user_data.items()])
            return details_str
            
    def update_details(self, accNo, pin, new_name, new_email, new_phone_str, new_pin_str):
        user_data = self.get_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect Account no./Pin."
        
        # Logic to update fields if not empty/invalid
        if new_name:
            user_data['name'] = new_name
        
        if new_email:
            user_data['email'] = new_email
            
        if new_phone_str:
            try:
                phone_no = int(new_phone_str)
                if len(str(phone_no)) == 10:
                    user_data['phone no.'] = phone_no
                else:
                    return "Error: New phone number must be 10 digits."
            except ValueError:
                return "Error: New phone number must be a number."
        
        if new_pin_str:
            try:
                new_pin = int(new_pin_str)
                if len(str(new_pin)) == 4:
                    user_data['pin'] = new_pin
                else:
                    return "Error: New pin must be 4 digits."
            except ValueError:
                return "Error: New pin must be a number."

        Bank.__update()
        return "Success! Details updated."

    def delete_account(self, accNo, pin):
        user_data = self.get_user(accNo, pin)
        if not user_data:
            return "Error: User not found or incorrect Account no./Pin."
        
        # Find the index of the dictionary in the list and remove it
        for i, account in enumerate(Bank.data):
            if account.get("Account no.") == accNo and account.get("pin") == pin:
                del Bank.data[i]
                Bank.__update()
                return "Success! Account deleted successfully."
        
        return "Error: Account deletion failed."

# --- Streamlit Application Functions ---

# Initialize Bank class
bank = Bank()

def main_app():
    st.set_page_config(page_title="Gemini Bank App", layout="centered")
    
    st.title("🏦 Gemini Bank Application")
    st.subheader("Web Interface for Basic Banking Operations")
    
    # Use a selectbox in the sidebar for navigation
    operation = st.sidebar.selectbox(
        "Select Operation",
        ("Create Account", "Deposit Money", "Withdraw Money", "Account Details", "Update Details", "Delete Account")
    )
    
    st.markdown("---")

    # --- Operation Handlers ---

    if operation == "Create Account":
        handle_create_account()
    elif operation == "Deposit Money":
        handle_deposit_withdraw("Deposit Money", bank.deposit_money)
    elif operation == "Withdraw Money":
        handle_deposit_withdraw("Withdraw Money", bank.withdraw_money)
    elif operation == "Account Details":
        handle_details()
    elif operation == "Update Details":
        handle_update_details()
    elif operation == "Delete Account":
        handle_delete_account()

# --- Component Functions ---

def display_result(result):
    if result.startswith("Error"):
        st.error(result.replace("Error: ", ""))
    elif result.startswith("Success"):
        st.success(result.replace("Success! ", ""))
    else:
        st.info(result)

def handle_create_account():
    st.header("Create New Account")
    
    with st.form("create_form"):
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        phone = st.text_input("Phone No. (10 digits):")
        pin = st.text_input("PIN (4 digits):", type="password", max_chars=4)
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            result = bank.create_account(name, email, phone, pin)
            display_result(result)


def handle_deposit_withdraw(title, operation_func):
    st.header(title)
    
    with st.form(f"{title.lower().replace(' ', '_')}_form"):
        accNo = st.text_input("Account No:")
        pin = st.text_input("PIN:", type="password", max_chars=4)
        amount = st.text_input("Amount (Max 10000):")
        
        submitted = st.form_submit_button(title)
        
        if submitted:
            result = operation_func(accNo, pin, amount)
            display_result(result)


def handle_details():
    st.header("Account Details")
    
    with st.form("details_form"):
        accNo = st.text_input("Account No:")
        pin = st.text_input("PIN:", type="password", max_chars=4)
        
        submitted = st.form_submit_button("Show Details")
        
        if submitted:
            result = bank.get_details(accNo, pin)
            display_result(result)


def handle_update_details():
    st.header("Update Details")
    
    st.info("Enter your current details for verification, and new details (leave blank to skip/keep old value).")
    
    with st.form("update_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### **Current Details (Verification)**")
            accNo = st.text_input("Account No. (Current):")
            pin = st.text_input("Current PIN:", type="password", max_chars=4)
            
        with col2:
            st.markdown("##### **New Details (Optional)**")
            new_name = st.text_input("New Name:")
            new_email = st.text_input("New Email:")
            new_phone = st.text_input("New Phone No (10 digits):")
            new_pin = st.text_input("New PIN (4 digits):", type="password", max_chars=4)
        
        submitted = st.form_submit_button("Update Details")
        
        if submitted:
            result = bank.update_details(accNo, pin, new_name, new_email, new_phone, new_pin)
            display_result(result)


def handle_delete_account():
    st.header("Delete Account")
    
    with st.form("delete_form"):
        accNo = st.text_input("Account No:")
        pin = st.text_input("PIN:", type="password", max_chars=4)
        
        st.warning("This action cannot be undone.")
        
        submitted = st.form_submit_button("Delete Account")
        
        if submitted:
            # Add a confirmation step
            if st.checkbox("I confirm I want to delete this account."):
                result = bank.delete_account(accNo, pin)
                display_result(result)
            else:
                st.error("Please confirm the deletion.")


if __name__ == "__main__":
    main_app()