import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# تحميل البيانات
df = pd.read_csv("USA_cars_datasets.csv")

# إعداد الصفحة
st.set_page_config(page_title="Cars Market Dashboard", page_icon="🚗", layout="wide")

# إضافة العنوان الرئيسي
st.title("🚗 **Cars Market Analysis Dashboard**")
st.markdown("""
    This dashboard allows you to interact with car market data including car prices, mileage, and more.
    Use the filters on the sidebar to analyze the data in more detail.
""")

# --- إعداد الفلاتر ---
st.sidebar.header("**Filter Data**")
brand_filter = st.sidebar.selectbox("Select Car Brand", options=df['brand'].unique())
year_filter = st.sidebar.slider("Select Year Range", min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=(int(df['year'].min()), int(df['year'].max())))
price_filter = st.sidebar.slider("Select Price Range", min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(int(df['price'].min()), int(df['price'].max())))

# تصفية البيانات بناءً على الفلاتر
filtered_df = df[(df['brand'] == brand_filter) & 
                 (df['year'].between(year_filter[0], year_filter[1])) & 
                 (df['price'].between(price_filter[0], price_filter[1]))]

# --- عرض البيانات ---
st.subheader("Data Overview")
st.write(f"Displaying {filtered_df.shape[0]} records.")
st.dataframe(filtered_df.head(), use_container_width=True)

# --- الرسم البياني 1: متوسط الأسعار حسب الماركة ---
st.subheader(f"Average Car Prices by Brand ({brand_filter})")
brand_price_avg = filtered_df.groupby('brand')['price'].mean().sort_values(ascending=False)
fig1 = px.bar(brand_price_avg, 
              x=brand_price_avg.index, 
              y=brand_price_avg.values, 
              labels={'x': 'Car Brand', 'y': 'Average Price ($)'}, 
              title="Average Price by Brand", 
              color=brand_price_avg.values, 
              color_continuous_scale='Viridis')
st.plotly_chart(fig1, use_container_width=True)

# --- الرسم البياني 2: توزيع الأسعار حسب السنة ---
st.subheader("Price Distribution by Year")
fig2 = px.box(filtered_df, 
              x="year", 
              y="price", 
              title="Price Distribution by Year", 
              labels={"year": "Car Year", "price": "Price ($)"}, 
              color="year")  # تم إزالة color_continuous_scale
st.plotly_chart(fig2, use_container_width=True)

# --- الرسم البياني 3: العلاقة بين السعر والمسافة المقطوعة ---
st.subheader("Price vs Mileage")
fig3 = px.scatter(filtered_df, 
                  x="mileage", 
                  y="price", 
                  color="condition", 
                  title="Price vs Mileage", 
                  labels={"mileage": "Mileage (in miles)", "price": "Price ($)"}, 
                  hover_data=['brand', 'year'], 
                  color_continuous_scale='RdBu')
st.plotly_chart(fig3, use_container_width=True)

# --- الرسم البياني 4: مقارنة بين الحالة والسعر ---
st.subheader("Price Comparison by Condition")
fig4 = px.violin(filtered_df, 
                 y="price", 
                 x="condition", 
                 box=True, 
                 points="all", 
                 title="Price Comparison by Condition",
                 labels={"condition": "Car Condition", "price": "Price ($)"}, 
                 color="condition", 
                 color_discrete_sequence=["#FF6347", "#FFD700", "#90EE90"])
st.plotly_chart(fig4, use_container_width=True)

# --- رسم بياني تفاعلي مع خاصية التصفية ---
st.subheader("Interactive Dashboard with Filters")
fig5 = go.Figure(data=go.Scatter(
    x=filtered_df['mileage'], 
    y=filtered_df['price'], 
    mode='markers', 
    marker=dict(color=filtered_df['year'], colorscale='Viridis', showscale=True, size=8)
))
fig5.update_layout(title="Interactive Price vs Mileage",
                  xaxis_title="Mileage (in miles)",
                  yaxis_title="Price ($)",
                  template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# --- إضافة نصوص تفاعلية ---
st.markdown("""
    **Key Insights:**
    - **Top Brands**: Brands like Tesla and BMW tend to have higher average prices.
    - **Price Trends**: Older cars typically have a lower price, while new models hold better value.
    - **Mileage Impact**: Higher mileage cars tend to have a lower price.
    - **Condition**: Cars in good condition generally sell for more money, even with higher mileage.
""")

# --- عرض المزيد من التفاصيل ---
st.subheader("Additional Insights and Suggestions")
st.markdown("""
    - You can use this dashboard to better understand the car market trends.
    - Experiment with filters to find the best deals for specific car brands, years, and price ranges.
""")
