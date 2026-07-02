import streamlit as st
import sqlite3

# --- BACKEND DATABASE OPERATIONS ---


def save_transaction(desc, amt, cat):
    """Inserts a new transaction record into the SQL database."""
    conn = sqlite3.connect('fintech_vault.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (description, amount, category) VALUES (?, ?, ?)",
        (desc, amt, cat)
    )
    conn.commit()
    conn.close()


def fetch_transactions():
    """Retrieves all stored transactions from the database."""
    conn = sqlite3.connect('fintech_vault.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT description, amount, category, date FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_all_transactions():
    """Completely empties the transactions table in the SQL database."""
    conn = sqlite3.connect('fintech_vault.db')
    cursor = conn.cursor()
    # TRUNCATE / DELETE command removes all rows from the table
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()

# --- SMART AUTOMATIC CATEGORISATION ---


def auto_categorise(description):
    """Automatically categorises expenses based on common UK keywords."""
    desc = description.lower()
    if any(keyword in desc for keyword in ['pret', 'costa', 'tesco', 'sainsbury', 'eat', 'food', 'mcdonalds']):
        return "Food & Drink"
    elif any(keyword in desc for keyword in ['tfl', 'tube', 'uber', 'train', 'bus']):
        return "London Commute"
    elif any(keyword in desc for keyword in ['aws', 'github', 'openai', 'laptop', 'monitor', 'software']):
        return "Tech & Software Allowance"
    else:
        return "General Expense"


# --- USER INTERFACE DESIGN ---
st.set_page_config(page_title="UK Fintech Ledger",
                   page_icon="💷", layout="wide")
st.title("💷 Smart UK Fintech Expense Ledger")
st.write("A robust backend data store tracking expenses against UK HMRC tax allowance guidelines.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Log New Transaction")
    description_input = st.text_input(
        "Transaction Description (e.g., TFL Tube journey or Pret Coffee)")
    amount_input = st.number_input("Amount (£)", min_value=0.01, step=0.01)

    if st.button("Submit to Database", use_container_width=True):
        if description_input and amount_input:
            detected_category = auto_categorise(description_input)
            save_transaction(description_input,
                             amount_input, detected_category)
            st.success(
                f"Successfully committed to SQL under category: **{detected_category}**")
        else:
            st.error("Please enter both a description and an amount.")

with col2:
    st.subheader("📊 Live SQL Database Ledger")
    data = fetch_transactions()

    if data:
        total_spent = sum(row[1] for row in data)
        tax_free_remaining = max(12570.00 - total_spent, 0.0)

        m1, m2 = st.columns(2)
        m1.metric("Total Logged Outgoings", f"£{total_spent:,.2f}")
        m2.metric("Est. Tax-Free Allowance Remaining",
                  f"£{tax_free_remaining:,.2f}")

        st.write("### Raw Database Rows")
        for row in data:
            st.info(f"📝 **{row[0]}** | 💰 **£{row[1]:.2f}** | 🏷️ *{row[2]}*")
    else:
        st.info(
            "The SQL database is currently empty. Add your first transaction on the left!")
# --- DANGER ZONE SECTION ---
st.markdown("---")
st.subheader("⚠️ Danger Zone")

# We use a unique key name so Streamlit treats it as a distinct action
if st.button("🚨 Clear All Ledger Data", use_container_width=True, key="clear_data"):
    clear_all_transactions()
    st.success("The database ledger has been completely wiped clean!")
    # Force the app to rerun and refresh the screen instantly
    st.rerun()
