import streamlit as st
import pandas as pd
import altair as alt
import random

st.set_page_config(page_title="掷骰子统计", layout="wide")

st.title("掷骰子结果统计")
st.write("模拟多次掷骰子，统计 1~6 点出现的次数和频率。")

n = st.slider("掷骰子次数", min_value=1, max_value=10000, value=600, step=100)

if "dice_results" not in st.session_state:
    st.session_state.dice_results = []

if st.button("重新掷骰子") or len(st.session_state.dice_results) != n:
    st.session_state.dice_results = [random.randint(1, 6) for _ in range(n)]

results = st.session_state.dice_results

counts = [0] * 6
for p in results:
    counts[p - 1] += 1

total = len(results)

df = pd.DataFrame({
    "点数": [1, 2, 3, 4, 5, 6],
    "次数": counts,
    "频率": [c / total for c in counts],
})

display_df = df.copy()
display_df["频率"] = display_df["频率"].map(lambda x: f"{x:.2%}")

st.subheader("统计表")
st.dataframe(display_df, hide_index=True)
st.caption(f"总掷骰次数：{total}")

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("点数:N", title="点数"),
    y=alt.Y("次数:Q", title="出现次数"),
    tooltip=[alt.Tooltip("点数:N"), alt.Tooltip("次数:Q")],
).properties(height=350)

st.subheader("柱状图")
st.altair_chart(chart, use_container_width=True)

most_face = df.loc[df["次数"].idxmax(), "点数"]
st.metric("出现次数最多的点数", f"{most_face} 点")