import pandas as pd
import plotly.express as px
import streamlit as st

# تحميل البيانات
df = pd.read_csv("USA_cars_datasets.csv")

st.set_page_config(page_title="Cars Market Dashboard", layout="wide")
st.title("🚗 Cars Market Analysis Dashboard")
st.markdown("This dashboard allows you to interact with car market data including car prices, mileage, and more.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Brand filter
brands = sorted(df["brand"].unique())
selected_brand = st.sidebar.selectbox("Select Car Brand:", brands)

# Year range filter
min_year = int(df["year"].min())
max_year = int(df["year"].max())
year_range = st.sidebar.slider("Select Year Range:", min_year, max_year, (min_year, max_year))

# Price range filter
min_price = int(df["price"].min())
max_price = int(df["price"].max())
price_range = st.sidebar.slider("Select Price Range ($):", min_price, max_price, (min_price, max_price), step=1000)

# تصفية البيانات
filtered_df = df[
    (df["brand"] == selected_brand) &
    (df["year"].between(year_range[0], year_range[1])) &
    (df["price"].between(price_range[0], price_range[1]))
]

st.markdown(f"### 📊 Displaying {filtered_df.shape[0]} records for brand: **{selected_brand}**")

# عرض الجدول
st.dataframe(filtered_df.head(10), use_container_width=True)

# رسم 1: متوسط السعر حسب الحالة
st.subheader("Average Price by Condition")
avg_price_condition = filtered_df.groupby("condition")["price"].mean().sort_values()
fig1 = px.bar(avg_price_condition,
              x=avg_price_condition.index,
              y=avg_price_condition.values,
              labels={"x": "Condition", "y": "Average Price ($)"},
              color=avg_price_condition.values,
              color_continuous_scale="Blues")
st.plotly_chart(fig1, use_container_width=True)

# رسم 2: عدد السيارات حسب الموديل
st.subheader("Top 10 Models by Count")
model_count = filtered_df["model"].value_counts().nlargest(10)
fig2 = px.bar(x=model_count.index, y=model_count.values,
              labels={"x": "Model", "y": "Number of Cars"},
              title="Top 10 Models",
              color=model_count.values,
              color_continuous_scale="Purples")
st.plotly_chart(fig2, use_container_width=True)

# رسم 3: السعر مقابل الأميال
st.subheader("Price vs Mileage")
fig3 = px.scatter(filtered_df, x="mileage", y="price",
                  title="Price vs Mileage",
                  labels={"mileage": "Mileage", "price": "Price ($)"},
                  opacity=0.6)
st.plotly_chart(fig3, use_container_width=True)

# رسم 4: توزيع الأسعار
st.subheader("Price Distribution")
fig4 = px.histogram(filtered_df, x="price",
                    nbins=30,
                    labels={"price": "Price ($)"},
                    title="Price Distribution",
                    color_discrete_sequence=["#4C78A8"])
st.plotly_chart(fig4, use_container_width=True)

# Insights
st.markdown("### 🔎 Key Insights")
st.markdown("""
- **Top Brands**: Brands like Tesla and BMW tend to have higher average prices.
- **Price Trends**: Older cars typically have a lower price.
- **Mileage Impact**: Higher mileage cars tend to have lower prices.
- **Condition**: Cars in good condition usually sell for more.
""")

st.markdown("### 💡 Suggestions")
st.markdown("""
- Use filters to explore the best deals.
- Compare models and prices within each brand.
""")
