from datetime import datetime

def get_date_from_input():
    while True:
        try:
            date_str = input('Введите дату в формате ГГГГ-ММ-ДД: ')
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return selected_date
        except ValueError:
            print('Некорректный формат даты. Повторите ввод.')

def get_time_from_input():
    while True:
        try:
            time_str = input('Введите время в формате ЧЧ:ММ: ')
            selected_time = datetime.strptime(time_str, '%H:%M').time()
            return selected_time
        except ValueError:
            print('Некорректный формат времени. Повторите ввод.')

def main_menu():
    print('Выберите опцию:')
    print('1. Выбрать дату')
    print('2. Выбрать время')
    print('3. Выход')

    while True:
        choice = input('Введите номер опции: ')
        
        if choice == '1':
            selected_date = get_date_from_input()
            print('Выбранная дата:', selected_date)
            break
        elif choice == '2':
            selected_time = get_time_from_input()
            print('Выбранное время:', selected_time)
            break
        elif choice == '3':
            break
        else:
            print('Некорректный номер опции. Повторите ввод.')

if __name__ == '__main__':
    main_menu()
