def calculate_pay(start_time, end_time, hourly_wage):
    if start_time == -1 or end_time == -1:
        return 0, 0, 0  # 表示当天未上班

    # 跨日处理
    if end_time <= start_time:
        end_time += 24

    # 普通时段：从 start_time 到 22:00（最多）
    normal_hours = max(0, min(end_time, 22.0) - start_time)

    # 深夜时段：从 22:00 到 end_time
    late_hours = max(0, end_time - max(start_time, 22.0))

    # 工资计算
    normal_pay = normal_hours * hourly_wage
    late_pay = late_hours * 1500  # 深夜固定工资

    total_pay = normal_pay + late_pay
    return normal_hours, late_hours, total_pay

def main():
    print("💼 打工工资计算器（含姓名 + 分钟输入 + 深夜工资）")

    # 输入姓名
    name = input("请输入打工者姓名：")

    # 输入基础工资
    hourly_wage = float(input(f"{name} 的普通时段每小时工资（日元）："))

    # 设置数据记录
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    total_normal = 0
    total_late = 0
    total_pay = 0

    for day in days:
        print(f"\n📅 {day}：")
        print("如果今天没打工，开始时间请输入 -1")
        start = float(input("开始时间（例：21.5 表示 21:30）："))
        if start == -1:
            print("今天未上班，跳过。")
            continue

        end = float(input("结束时间（例：2.25 表示凌晨2:15）："))

        normal, late, pay = calculate_pay(start, end, hourly_wage)

        total_normal += normal
        total_late += late
        total_pay += pay

        print(f"👉 普通时间：{normal:.2f} 小时 | 深夜时间：{late:.2f} 小时")
        print(f"💰 当天工资：{pay:.2f} 日元")

    total_hours = total_normal + total_late

    print(f"\n===== 📊 {name} 的本周工资汇总 =====")
    print(f"⏰ 普通总工时：{total_normal:.2f} 小时")
    print(f"🌙 深夜总工时：{total_late:.2f} 小时")
    print(f"🕒 总工时：{total_hours:.2f} 小时")
    print(f"💵 一周总工资：{total_pay:.2f} 日元")

main()
