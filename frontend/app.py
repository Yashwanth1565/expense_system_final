import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import io
from datetime import date

# ================= CONFIG =================
#BASE_URL = "http://127.0.0.1:8000"  # 🔥 change after deployment
BASE_URL = "https://expense-backend-61vh.onrender.com"


#BASE_URL = "https://your-backend.onrender.com"  # 👈 replace after deploy


def safe_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

st.set_page_config(page_title="Expense System", layout="wide")

# ================= BEAUTIFUL UI =================
st.markdown("""
<style>
.stApp { background-color: #0e1117; color: #ffffff; }
[data-testid="stSidebar"] { background-color: #161b22; }
h1 { color: #58a6ff; }

.stButton button {
    background: linear-gradient(135deg, #238636, #2ea043);
    color: white;
    border-radius: 8px;
}

.stDownloadButton button {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white;
    border-radius: 8px;
}

[data-testid="metric-container"] {
    background-color: #161b22;
    border-radius: 10px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Expense Management System")

menu = st.sidebar.radio("Menu", [
    "📊 Dashboard",
    "📈 Analytics",
    "➕ Add Expense",
    "📋 View Expenses",
    "📌 Expense Status",
    "📤 Export"
])

# ================= SAFE API =================
def safe_get(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"API Error: {res.status_code}")
            st.write(res.text)
            return None
    except Exception as e:
        st.error("Backend not running or wrong URL")
        st.write(e)
        return None

# ================= DASHBOARD =================
if menu == "📊 Dashboard":
    data = safe_get(f"{BASE_URL}/dashboard/")

    if data:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", data["total"])
        c2.metric("Approved", data["approved"])
        c3.metric("Rejected", data["rejected"])
        c4.metric("Pending", data["pending"])

# ================= ADD =================
elif menu == " Add Expense":
    st.subheader("Add New Expense")

    name = st.text_input("Employee Name")
    amt = st.number_input("Amount", min_value=1)
    cat = st.selectbox("Category", ["Travel", "Food", "Office", "Other"])
    desc = st.text_input("Description")

    if st.button("Submit"):
        try:
            res = requests.post(f"{BASE_URL}/expenses/", json={
                "employee_name": name,
                "amount": amt,
                "category": cat,
                "description": desc
            })

            if res.status_code == 200:
                st.success("✅ Expense Added")
            else:
                st.error("Failed to add")
                st.write(res.text)

        except Exception as e:
            st.error("Backend not reachable")
            st.write(e)

# ================= VIEW =================
elif menu == "📋 View Expenses":
    st.subheader("All Expenses")

    data = safe_get(f"{BASE_URL}/expenses/")

    if data:
        df = pd.DataFrame(data)

        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No expenses found")

# ================= ANALYTICS =================
elif menu == "📈 Analytics":
    st.subheader("Analytics Dashboard")

    data = safe_get(f"{BASE_URL}/expenses/")

    if data:
        df = pd.DataFrame(data)

        if not df.empty:

            col1, col2 = st.columns(2)

            # Pie chart
            with col1:
                fig = px.pie(
                    df,
                    names="status",
                    title="Status Distribution",
                    color_discrete_map={
                        "Pending": "#d29922",
                        "Approved": "#3fb950",
                        "Rejected": "#f85149"
                    }
                )
                st.plotly_chart(fig, use_container_width=True)

            # Bar chart
            with col2:
                fig2 = px.bar(
                    df,
                    x="category",
                    y="amount",
                    title="Category Spending",
                    color="category"
                )
                st.plotly_chart(fig2, use_container_width=True)

            # Line chart
            df["date"] = pd.to_datetime(df["date"])
            trend = df.groupby("date")["amount"].sum().reset_index()

            fig3 = px.line(
                trend,
                x="date",
                y="amount",
                title="Spending Over Time"
            )
            st.plotly_chart(fig3, use_container_width=True)

# ================= EXPENSE STATUS =================
elif menu == "📌 Expense Status":
    st.subheader("📌 Expense Decision Panel")

    st.info("Review pending expenses and update their status (Approved / Rejected)")

    data = safe_get(f"{BASE_URL}/expenses/")

    if data:
        df = pd.DataFrame(data)

        pending_df = df[df["status"] == "Pending"]

        if pending_df.empty:
            st.success("🎉 No pending expenses!")
        else:
            st.dataframe(pending_df, use_container_width=True)

            st.markdown("---")

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                exp_id = st.number_input("Expense ID", min_value=1)

            with col2:
                action = st.selectbox("Update Status", ["Approved", "Rejected"])

            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Submit", use_container_width=True):
                    try:
                        res = requests.put(
                            f"{BASE_URL}/expenses/{exp_id}/status",
                            json={"status": action}
                        )

                        if res.status_code == 200:
                            if action == "Approved":
                                st.success(f"✅ Expense {exp_id} Approved")
                            else:
                                st.warning(f"❌ Expense {exp_id} Rejected")
                        else:
                            st.error("Update failed")
                            st.write(res.text)

                    except Exception as e:
                        st.error("Backend not reachable")
                        st.write(e)

# ================= EXPORT =================
elif menu == "📤 Export":
    st.subheader("Export Data")

    data = safe_get(f"{BASE_URL}/expenses/")

    if data:
        df = pd.DataFrame(data)

        # Excel
        def to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        st.download_button(
            label="📥 Download Excel",
            data=to_excel(df),
            file_name=f"expenses_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # CSV
        st.download_button(
            label="📄 Download CSV",
            data=df.to_csv(index=False),
            file_name="expenses.csv",
            mime="text/csv"
        )


