import os
import pandas as pd
import matplotlib.pyplot as plt

def create_period(df: pd.DataFrame, start_date: str, end_date: str):
    
    """Функция для построения графика изменения курса за весь период.
    Args:
        df: DataFrame, содержащий столбцы 'date' и 'value'.
        start_date: Начальная дата для графика.
        end_date: Конечная дата для графика.
    """
    # Формируем заголовок с учетом выбранного периода
    plt.figure(figsize=(12, 7))
    plt.plot(df['date'], df['value'], marker='o', linestyle='-', color='#1f77b4', label='Курс', markersize=6)
    title = f'Изменение курса за период с {start_date} по {end_date}' if start_date and end_date else 'Изменение курса за весь период'
    plt.title(title, fontsize=18)
    plt.xlabel('Дата', fontsize=14)
    plt.ylabel('Курс', fontsize=14)
    plt.xticks(rotation=45)

    # Аннотируем значения на графике
    for i, value in enumerate(df['value']):
        plt.text(df['date'].iloc[i], value, f'{value:.2f}', fontsize=9, ha='right', va='bottom')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left', fontsize=12)
    
    plt.tight_layout()
    plt.show(block=True)

def create_month(df: pd.DataFrame, month: str):
    """Функция для построения графика изменения курса за указанный месяц с медианой и средним значением.
    Args:
        df: DataFrame, содержащий столбцы 'date' и 'value'.
        month: Месяц в формате 'YYYY-MM' для фильтрации данных.
    """
    df = df.copy()  # Создаем копию DataFrame
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    filtered_df = df[df['date'].dt.to_period('M') == month]

    if filtered_df.empty:
        print(f"Данных за месяц {month} нет.")
        return

    median_value = filtered_df['value'].median()
    mean_value = filtered_df['value'].mean()

    plt.figure(figsize=(12, 7))
    plt.plot(filtered_df['date'], filtered_df['value'], marker='o', linestyle='-', color='#1f77b4', label='Курс')
    plt.axhline(y=median_value, color='g', linestyle='--', label='Медиана')
    plt.axhline(y=mean_value, color='r', linestyle='--', label='Среднее значение')

    plt.title(f'Изменение курса за месяц {month}', fontsize=18)
    plt.xlabel('Дата', fontsize=14)
    plt.ylabel('Курс', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left', fontsize=12)

    plt.tight_layout()
    plt.show(block=True)

def calculate_month(df: pd.DataFrame):
    """Функция для вычисления среднего значения курса за месяц.
    Args:
        df: DataFrame, содержащий столбцы 'date' и 'value'.
    Returns:
        DataFrame, сгруппированный по месяцу, с рассчитанным средним значением курса.
    """
    df['month'] = df['date'].dt.to_period('M')
    monthly_mean = df.groupby('month')['value'].mean().reset_index()
    return monthly_mean

def filter_by_deviation(df: pd.DataFrame, threshold: float):
    """Функция для фильтрации DataFrame по отклонению от среднего значения курса.
    Args:
        df: DataFrame
        threshold: Значение отклонения от среднего значения
    Returns:
        Отфильтрованный DataFrame.
    """
    if 'deviation_from_mean' not in df.columns:
        raise ValueError("DataFrame должен содержать столбец 'deviation_from_mean'.")
    filtered_df = df[df['deviation_from_mean'] >= threshold]
    return filtered_df

def filter_date(df: pd.DataFrame, start_date: str, end_date: str):
    """Функция для фильтрации DataFrame по диапазону дат.
    Args:
        df: DataFrame
        start_date: Начальная дата в формате 'YYYY-MM-DD'.
        end_date: Конечная дата в формате 'YYYY-MM-DD'.
    Returns:
        Отфильтрованный DataFrame.
    """
    df = df.copy()  # Создаем копию DataFrame
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Если даты не указаны, возвращаем все данные
    if not start_date and not end_date:
        return df

    # Фильтрация строк, где дата находится в заданном диапазоне
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    return filtered_df

def main():
    print("Введите путь до файла (./dataset.csv): ", end="")
    filename = input().strip()
    if not filename:
        filename = "./dataset.csv"
    
    # Проверяем, существует ли указанный файл
    if not os.path.exists(filename):
        print(f"Ошибка: Файл '{filename}' не найден.")
        return
    
    # Загружаем данные
    df = pd.read_csv(filename, sep=";")
    df.columns = ["date", "value"]
    df.dropna(subset=["date"], inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.fillna({"value": df["value"].mean()}, inplace=True)

    # Подсчет отклонений
    median_value = df['value'].median()
    mean_value = df['value'].mean()
    df['deviation_from_median'] = df['value'] - median_value
    df['deviation_from_mean'] = df['value'] - mean_value

    while True:
        print("\nВыберите действие:")
        print("1 - Построить график за указанный период")
        print("2 - Построить график за указанный месяц")
        print("3 - Вычислить средние значения по месяцам")
        print("4 - Фильтровать данные по отклонению от среднего")
        print("5 - Выйти из программы")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            # Ввод периода
            print("Введите начальную дату (YYYY-MM-DD, по умолчанию весь период): ", end="")
            start_date = input().strip()
            print("Введите конечную дату (YYYY-MM-DD, по умолчанию весь период): ", end="")
            end_date = input().strip()
            start_date = start_date if start_date else None
            end_date = end_date if end_date else None
            filtered_df = filter_date(df, start_date, end_date)
            if filtered_df.empty:
                print("Нет данных для отображения в выбранном диапазоне дат.")
            else:
                create_period(filtered_df, start_date, end_date)

        elif choice == "2":
            # Ввод месяца
            month = input("Введите месяц (YYYY-MM в формате): ").strip()
            if not month:
                print("Месяц обязателен для ввода.")
                continue
            create_month(df, month)

        elif choice == "3":
            # Вывод средней информации по месяцам
            monthly_data = calculate_month(df)
            print(monthly_data)

        elif choice == "4":
        # Фильтрация по отклонению
            try:
                threshold_input = input("Введите порог отклонения (например, 5.0): ").strip()
                threshold = float(threshold_input) if threshold_input else 5.0  # По умолчанию 5.0
            except ValueError:
                print("Ошибка: необходимо ввести число.")
                continue

            filtered_df = filter_by_deviation(df, threshold)
            if filtered_df.empty:
                print("Нет данных с таким отклонением.")
            else:
                print(filtered_df)

        elif choice == "5":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main()