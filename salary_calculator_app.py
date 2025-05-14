import streamlit as st
import pandas as pd
from datetime import datetime

def to_decimal(hour, minute):
    return hour + minute / 60

def calculate_pay(start, end, rest, hourly_wage, bonus_count, bonus_per_item=500):
    if end <= start:
        end += 24
    total_hours = end - start - rest

    normal_hours = max(0, min(end, 22.0) - start)
    late_hours = max(0, end - max(start, 22.0))

    normal_pay = normal_hours * hourly_wage
    late_pay = late_hours * 1500
    bonus = bonus_count * bonus_per_item
    total_pay = normal_pay + late_pay + bonus

    return round(normal_hours, 2), round(late_hours, 2), round(total_hours, 2), bonus, round(total_pay, 2)

st.set_page_config(page_title="工资计算器 / 給与計算機", page_icon="💼")

# 语言切换
lang = st.selectbox("🌐 言語を選択してください / 请选择语言", ["日本語", "中文"])

# 翻译函数
def T(jp, zh):
    return jp if lang == "日本語" else zh

st.title(T("💼 アルバイト給与計算機（月別）", "💼 打工工资计算器（月度版）"))
name = st.text_input(T("お名前を入力してください", "请输入🐂🐎的姓名"))

hourly_wage = st.number_input(T("通常時給（円）", "普通时薪（日元）"), min_value=0, value=1200, step=100)
bonus_per_item = 500
st.markdown("---")

records = []

for day in range(1, 32):
    with st.expander(f"{T('📅', '📅')} {day} {T('日', '日')}"):
        worked = st.checkbox(T("勤務しましたか？", "是否上班"), value=True, key=f"worked_{day}")
        if not worked:
            continue

        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input(T("出勤時間", "上班时间"), value=datetime.strptime("18:00", "%H:%M").time(), key=f"start_{day}")
        with col2:
            end_time = st.time_input(T("退勤時間", "下班时间"), value=datetime.strptime("01:00", "%H:%M").time(), key=f"end_{day}")

        rcol1, rcol2 = st.columns(2)
        with rcol1:
            rest_hour = st.number_input(T("休憩 - 時間", "休息时长 - 小时"), min_value=0, max_value=5, value=0, key=f"rest_h_{day}")
        with rcol2:
            rest_min = st.number_input(T("休憩 - 分", "休息时长 - 分钟"), min_value=0, max_value=59, value=30, key=f"rest_m_{day}")

        bonus_count = st.number_input(T("ステーキ販売数（1個 ¥500）", "今天卖出牛排数量（每份¥500）"), min_value=0, value=0, step=1, key=f"bonus_{day}")

        start = to_decimal(start_time.hour, start_time.minute)
        end = to_decimal(end_time.hour, end_time.minute)
        rest = to_decimal(rest_hour, rest_min)

        normal, late, total, bonus, pay = calculate_pay(start, end, rest, hourly_wage, bonus_count)
        records.append({
            T("日付", "日期"): f"{day}{T('日', '日')}",
            T("通常時間", "普通工时"): normal,
            T("深夜時間", "深夜工时"): late,
            T("合計労働時間", "总工时"): total,
            T("ボーナス", "奖金"): bonus,
            T("日給合計", "工资合计"): pay
        })

st.markdown(f"## {T('📊 月次給与サマリー', '📊 月度工资汇总')}")

if records:
    df = pd.DataFrame(records)
    st.dataframe(df, use_container_width=True)

    total_row = pd.DataFrame([{
        T("日付", "日期"): T("合計", "总计"),
        T("通常時間", "普通工时"): df[T("通常時間", "普通工时")].sum(),
        T("深夜時間", "深夜工时"): df[T("深夜時間", "深夜工时")].sum(),
        T("合計労働時間", "总工时"): df[T("合計労働時間", "总工时")].sum(),
        T("ボーナス", "奖金"): df[T("ボーナス", "奖金")].sum(),
        T("日給合計", "工资合计"): df[T("日給合計", "工资合计")].sum()
    }])
    st.dataframe(total_row)

    if name:
        st.success(T(f"🎉 {name} の給与計算が完了しました！", f"🎉 {name} 的工资已计算完成！"))
else:
    st.info(T("少なくとも1日の勤務記録を入力してください。", "请先填写至少一天的工作记录。"))
