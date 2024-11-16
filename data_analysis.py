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
