import streamlit as st

st.set_page_config(page_title="打工工资计算器", page_icon="💼")

st.title("💼 打工工资计算器（含姓名 + 分钟输入 + 深夜加成）")
name = st.text_input("请输入打工者姓名：")

wage = st.number_input("普通时段每小时工资（日元）", min_value=0.0, step=50.0, value=1200.0)

days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
total_normal = 0
total_late = 0
total_pay = 0

st.markdown("### 每天上班时间（支持分钟输入，例如 21.5 表示 21:30）")
for day in days:
    with st.expander(f"{day}"):
        start = st.number_input(f"{day} 开始时间", min_value=-1.0, max_value=23.99, value=-1.0, key=f"{day}_start")
        end = st.number_input(f"{day} 结束时间", min_value=0.0, max_value=23.99, value=0.0, key=f"{day}_end")

        if start == -1.0:
            st.info(f"{day} 未上班")
            continue

        if end <= start:
            end += 24.0

        normal = max(0, min(end, 22.0) - start)
        late = max(0, end - max(start, 22.0))

        pay = normal * wage + late * 1500
        total_normal += normal
        total_late += late
        total_pay += pay

        st.write(f"普通时间：{normal:.2f} 小时 | 深夜时间：{late:.2f} 小时")
        st.write(f"当天工资：{pay:.2f} 日元")

total_hours = total_normal + total_late

st.markdown("---")
st.subheader(f"📊 {name} 的本周汇总")
st.write(f"⏰ 普通工时：{total_normal:.2f} 小时")
st.write(f"🌙 深夜工时：{total_late:.2f} 小时")
st.write(f"🕒 总工时：{total_hours:.2f} 小时")
st.write(f"💰 总工资：{total_pay:.2f} 日元")
