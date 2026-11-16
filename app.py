import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- 页面配置 ----------
st.set_page_config(
    page_title="电商销售数据看板",
    page_icon="📊",
    layout="wide",
)

st.title("📊 电商销售数据看板")
st.caption("实验2 · 数据看板的设计与实现")

# ---------- 读取数据 ----------
# 老版本使用 st.cache 替代 st.cache_data
@st.cache
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ---------- 侧边栏筛选 ----------
with st.sidebar:
    st.header("筛选条件")
    selected_cats = st.multiselect(
        "选择品类",
        options=df["category"].unique(),
        default=df["category"].unique(),
    )
    date_range = st.date_input(
        "日期范围",
        value=(df["date"].min(), df["date"].max()),
        min_value=df["date"].min(),
        max_value=df["date"].max(),
    )

filtered = df[df["category"].isin(selected_cats)].copy()
if len(date_range) == 2:
    filtered = filtered[
        (filtered["date"] >= pd.Timestamp(date_range[0]))
        & (filtered["date"] <= pd.Timestamp(date_range[1]))
    ]

# ---------- 数据概览区 ----------
total_amount = filtered["amount"].sum()
avg_amount = filtered["amount"].mean()
order_count = len(filtered)

# 去掉可能引起兼容性问题的 delta 参数
col1, col2, col3 = st.columns(3)
col1.metric("总销售额", f"¥{total_amount:,.0f}")
col2.metric("平均订单金额", f"¥{avg_amount:,.0f}")
col3.metric("订单总数", f"{order_count:,}")

# ---------- 维度统计区（基础柱状图） ----------
st.subheader("品类销售额对比")
cat_sales = filtered.groupby("category")["amount"].sum().reset_index()
# 使用最基础的柱状图，去掉复杂参数
fig_bar = px.bar(
    cat_sales, x="category", y="amount",
    title="各品类销售额",
    color="category"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ---------- 趋势分析区（基础折线图） ----------
st.subheader("月度销售趋势")
monthly = filtered.groupby("month")["amount"].sum().reset_index()
fig_line = px.line(monthly, x="month", y="amount", markers=True,
                   title="月度销售额变化")
st.plotly_chart(fig_line, use_container_width=True)

# ---------- 占比结构区（基础饼图） ----------
st.subheader("品类占比结构")
# 去掉 hole 参数，画标准的饼图
fig_pie = px.pie(cat_sales, names="category", values="amount",
                 title="品类销售额占比")
st.plotly_chart(fig_pie, use_container_width=True)

# ---------- 明细数据区 ----------
st.subheader("明细数据")
st.dataframe(
    filtered[["order_id", "date", "category", "price", "quantity", "amount"]].sort_values("date", ascending=False),
    use_container_width=True,
)