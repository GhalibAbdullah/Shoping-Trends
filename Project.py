import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import math
import numpy as np

# Load the dataset
st.image("Shoopingtrends.jpg")
st.title("🛒 Shopping Trends Analysis")
st.write("---")
st.write("Welcome to the **Shopping Trends Analysis** dashboard! 🛍️ Explore customer behaviors, sales trends, and more with interactive visualizations and insights.")

# Sidebar Header
st.sidebar.title("📊 Navigation")
st.sidebar.write("Use the options below to explore different analyses.")

# Upload the CSV
uploaded_file = "shopping_trends_with_regions.csv"
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Sidebar Analysis Options
    option = st.sidebar.radio(
        "🔍 Choose an Analysis:",
        [
            "Exploratory Data Analysis",
            "Customer Segment Prediction",
            "Seasonal Purchase Prediction",
            "Consumer Behavior",
        ],
    )

    # Categories Filtering
    product_categories = df["Category"].dropna().unique()
    st.sidebar.write("### 🛍️ Filter by Category")
    category_checkboxes = {"Select All Categories": st.sidebar.checkbox("Select All Categories", value=True)}

    for category in product_categories:
        category_checkboxes[category] = st.sidebar.checkbox(category, value=True if category_checkboxes["Select All Categories"] else False)

    if category_checkboxes["Select All Categories"]:
        selected_category = product_categories
    else:
        selected_category = [category for category, selected in category_checkboxes.items() if selected and category != "Select All Categories"]

    # Seasons Filtering
    seasons = df["Season"].dropna().unique()
    st.sidebar.write("### 🌸☀️🍂❄️ Filter by Season")
    season_checkboxes = {"Select All Seasons": st.sidebar.checkbox("Select All Seasons", value=True)}

    for season in seasons:
        season_checkboxes[season] = st.sidebar.checkbox(season, value=True if season_checkboxes["Select All Seasons"] else False)

    if season_checkboxes["Select All Seasons"]:
        selected_season = seasons
    else:
        selected_season = [season for season, selected in season_checkboxes.items() if selected and season != "Select All Seasons"]

    # Apply Filters
    filtered_df = df[(df["Category"].isin(selected_category)) & (df["Season"].isin(selected_season))]

    # Analysis Logic
    if option == "Exploratory Data Analysis":
        st.header("📊 Exploratory Data Analysis")
        st.write("Get an in-depth overview of the dataset and uncover key trends that drive customer behavior! ✨")

        # Data Preview
        st.subheader("1️⃣ **Data Preview** 📄")
        st.write("Here's a quick look at the data after applying the selected filters:")
        st.write(filtered_df)

        # Missing Values
        st.subheader("2️⃣ **Missing Value Information** ⚠️")
        st.write("Below is a summary of missing values in the dataset:")
        st.write(df.isnull().sum())

        # Summary Statistics
        st.subheader("3️⃣ **Summary Statistics** 📊")
        st.write("Explore the statistical overview of the dataset:")
        st.write(df.describe().round(2))

        # Revenue Metrics
        total_revenue = filtered_df["Purchase Amount (USD)"].sum()
        total_customers = len(filtered_df)
        average_revenue = total_revenue / total_customers if total_customers else 0

        st.subheader("4️⃣ **Revenue Metrics** 💰")
        st.markdown(f"- **Total Revenue:** ${total_revenue:,.2f}")
        st.markdown(f"- **Total Customers:** {total_customers}")
        st.markdown(f"- **Average Revenue per Customer:** ${average_revenue:,.2f}")

        # Visualizations
        st.subheader("5️⃣ **Visualizations** 📈")

        # Total sales by category
        st.write("**Total Sales by Category** 🛒")
        total_sales = filtered_df.groupby("Category")["Purchase Amount (USD)"].sum().reset_index()
        fig, ax = plt.subplots()
        ax.bar(total_sales["Category"], total_sales["Purchase Amount (USD)"], color="skyblue")
        ax.set_ylabel("Purchase Amount (USD)")
        ax.set_xlabel("Category")
        ax.set_title("Total Sales by Category")

        for i, v in enumerate(total_sales["Purchase Amount (USD)"]):
            ax.text(i, v + 500, f"${v:,.0f}", ha='center', va='bottom')

        st.pyplot(fig)

        # Average purchase amount by gender
        st.write("**Average Purchase Amount by Gender** 👩‍🦰👨")
        avg_purchase_gender = filtered_df.groupby("Gender")["Purchase Amount (USD)"].mean().reset_index()
        fig, ax = plt.subplots()
        ax.bar(avg_purchase_gender["Gender"], avg_purchase_gender["Purchase Amount (USD)"], color="lightblue")
        ax.set_ylabel("Average Purchase Amount (USD)")
        ax.set_xlabel("Gender")
        ax.set_title("Average Purchase by Gender")

        for i, v in enumerate(avg_purchase_gender["Purchase Amount (USD)"]):
            ax.text(i, v + 5, f"${v:,.2f}", ha='center', va='bottom')

        st.pyplot(fig)

        st.write("🔎 **Key Takeaway:** These insights help track overall performance and customer behaviors effectively.")

    elif option == "Customer Segment Prediction":
        st.header("🧑‍🤝‍🧑 Customer Segment Prediction")
        st.write("🎯 Identify and predict customer segments based on age groups, enabling targeted marketing strategies.")

        def predict_customer_segment(age):
            if age < 18:
                return "Teenager"
            elif age < 25:
                return "Young Adult"
            elif age < 40:
                return "Adult"
            elif age < 60:
                return "Middle Aged"
            else:
                return "Senior"

        df["Predicted Segment"] = df["Age"].apply(predict_customer_segment)
        st.dataframe(df[["Customer ID", "Age", "Predicted Segment"]])

        st.write("📊 **Segment Distribution**")
        segment_distribution = df["Predicted Segment"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(segment_distribution, labels=segment_distribution.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("Customer Segment Distribution")
        st.pyplot(fig)

        st.write("📋 **Insight:** This segmentation helps tailor marketing campaigns to different age groups.")

    elif option == "Seasonal Purchase Prediction":
        st.header("🌸 Seasonal Purchase Prediction")
        st.write("🔮 Analyze seasonal sales trends and forecast future purchasing behavior.")

        season_sales = filtered_df.groupby(["Season", "Item Purchased"])["Purchase Amount (USD)"].sum().reset_index()
        pivot_table = season_sales.pivot(index="Season", columns="Item Purchased", values="Purchase Amount (USD)").fillna(0)
        st.write("📊 **Seasonal Sales Data (Pivot Table):**")
        st.dataframe(pivot_table)

        avg_sales_season = season_sales.groupby("Season")["Purchase Amount (USD)"].mean()
        predicted_sales = avg_sales_season.mean()
        st.write(f"💡 **Predicted Average Sales for Next Season:** ${predicted_sales:,.2f}")

        fig, ax = plt.subplots()
        pivot_table.plot(ax=ax, kind="line", marker="o", colormap="Blues")
        ax.set_title("Sales Trends Across Seasons")
        ax.set_ylabel("Purchase Amount (USD)")
        ax.set_xlabel("Season")
        st.pyplot(fig)

        st.write("📈 **Takeaway:** Predicting trends helps businesses prepare for peak seasons efficiently.")

    elif option == "Consumer Behavior":
        st.header("🌍 Consumer Behavior")
        st.write("🔍 Analyze consumer trends across different regions and categories.")

        regions = df["Region"].dropna().unique()
        for region in regions:
            st.subheader(f"📍 Consumer Trends in {region} Region")
            region_data = filtered_df[filtered_df["Region"] == region]

            region_sales = region_data.groupby(["Season", "Category"])["Purchase Amount (USD)"].sum().reset_index()
            region_pivot = region_sales.pivot(index="Season", columns="Category", values="Purchase Amount (USD)").fillna(0)

            fig, ax = plt.subplots()
            region_pivot.plot(kind='line', ax=ax, figsize=(10, 6))
            ax.set_title(f"Seasonal Sales by Category in {region} Region")
            ax.set_xlabel("Season")
            ax.set_ylabel("Total Purchase Amount (USD)")
            ax.grid(True)
            st.pyplot(fig)

        st.write("📋 **Insight:** Understanding consumer behavior across regions helps optimize regional strategies.")

# Footer
st.write("---")
st.write("👨‍💻 **Powered by Abdullah bin Ghalib (BSDSF22M047)** 🚀")
