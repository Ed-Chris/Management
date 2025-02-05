import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Chore Management", page_icon="✅", layout="wide")

# Main Title
st.title("✅ Chore Management App")
st.write("Welcome to the Chore Management App! Easily **track, assign, and update chores** to keep everything organized.")

# Features Section
st.subheader("📌 Features")
st.markdown("- 📂 **Upload Chores** from an Excel file.")
st.markdown("- 📊 **View Chores** assigned to each person.")
st.markdown("- ✅ **Update Chores** when completed.")

# Bin Collection Info
st.subheader("🗑️ Bin Collection Schedule")
st.info("🟢🔵 **Green & Blue Bins:** Every **Tuesday**")
st.info("⚫ **Black Bins:** Every **Alternate Wednesday**")

# Cleaning Reminder
st.subheader("🧹 Cleanliness Reminder")
st.warning("⚠️ **Please clean up after yourself if you make a mess!**")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
st.sidebar.success("Select a page above to continue.")

# Footer
st.markdown("---")
st.caption("UNO or counter-strike, come let's play")
