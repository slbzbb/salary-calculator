def calculate_daily_pay(start_hour, end_hour, hourly_wage):
    if end_hour <= start_hour:
        end_hour += 24

    normal_hours = max(0, min(end_hour, 22) - start_hour)
    late_hours = max(0, end_hour - max(start_hour, 22))

    pay = (normal_hours * hourly_wage) + (late_hours * hourly_wage * 1.2)
    return normal_hours, late_hours, pay

def main():
    print("💼 打工工资计算器（支持深夜加班 + 跨午夜 + 没打工跳过）")
    hourly_wage = float(input("请输入每小时工资（日元）："))

    total_normal_hours = 0
    total_late_hours = 0
    total_pay = 0

    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    for day in days:
        print(f"\n🕒 {day}")
        print("如果今天没打工，请输入 -1")
        start = int(input("请输入打工开始时间（0~23 或 -1 跳过）："))

        if start == -1:
            print("该天未打工，已跳过。")
            continue

        end = int(input("请输入打工结束时间（0~23）："))
        
        normal, late, pay = calculate_daily_pay(start, end, hourly_wage)
        
        total_normal_hours += normal
        total_late_hours += late
        total_pay += pay

    print("\n📊 一周打工汇总")
    print(f"普通时段工时：{total_normal_hours:.1f} 小时")
    print(f"深夜时段工时：{total_late_hours:.1f} 小时")
    print(f"💰 总工资：{total_pay:.2f} 日元")

main()
