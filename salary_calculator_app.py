def to_decimal_time(hour, minute):
    return hour + minute / 60

def parse_time_input(prompt):
    try:
        time_str = input(prompt).strip()
        if time_str.upper() == "NO":
            return "NO", "NO"
        h, m = map(int, time_str.split(":"))
        return h, m
    except:
        print("❌ 输入格式错误，请用 HH:MM 形式，例如 18:30，或输入 NO 跳过")
        return parse_time_input(prompt)

def calculate_pay(start_h, start_m, end_h, end_m,
                  rest_h, rest_m,
                  hourly_wage, bonus_count, bonus_per_item=500):
    start = to_decimal_time(start_h, start_m)
    end = to_decimal_time(end_h, end_m)
    if end <= start:
        end += 24

    rest = to_decimal_time(rest_h, rest_m)

    normal_hours = max(0, min(end, 22.0) - start)
    late_hours = max(0, end - max(start, 22.0))
    total_hours = (end - start) - rest

    normal_pay = normal_hours * hourly_wage
    late_pay = late_hours * 1500
    bonus = bonus_count * bonus_per_item
    total_pay = normal_pay + late_pay + bonus

    return round(normal_hours, 2), round(late_hours, 2), round(total_hours, 2), bonus, round(total_pay, 2)

def run_calculator():
    print("💼 打工工资计算器（支持 NO / 姓名 / HH:MM 格式）")
    name = input("请输入🐂🐎的姓名：")
    hourly_wage = float(input("请输入普通时薪（日元）："))
    bonus_per_item = 500

    total_normal = total_late = total_hours = total_bonus = total_pay = 0

    for day in range(1, 32):
        print(f"\n📅 {day}日（如未打工，输入 NO）")

        start_h, start_m = parse_time_input("上班时间（HH:MM 或 NO）：")
        if start_h == "NO":
            print("今天未打工，已跳过。")
            continue

        end_h, end_m = parse_time_input("下班时间（HH:MM）：")
        rest_h, rest_m = parse_time_input("休息时间总长（HH:MM）：")
        bonus_count = int(input("今天卖出牛排几份？："))

        normal, late, total, bonus, pay = calculate_pay(
            start_h, start_m, end_h, end_m,
            rest_h, rest_m,
            hourly_wage, bonus_count, bonus_per_item
        )

        total_normal += normal
        total_late += late
        total_hours += total
        total_bonus += bonus
        total_pay += pay

        print(f"普通时间：{normal} h，深夜时间：{late} h，总工时：{total} h")
        print(f"🍖 奖金：¥{bonus}，💰 当天工资：¥{pay}")

    print(f"\n===== 📊 {name} 的工资汇总 =====")
    print(f"普通时段总工时：{total_normal} 小时")
    print(f"深夜时段总工时：{total_late} 小时")
    print(f"总工时（已扣休息）：{total_hours} 小时")
    print(f"奖金总额：¥{total_bonus}")
    print(f"工资总额：¥{total_pay}")

# 程序入口
run_calculator()
