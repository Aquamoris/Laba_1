import sqlite3


def individual():
    con = sqlite3.connect("booking.sqlite")  # создаем базу данных и устанавливаем соединение с ней

    # инициализация бд
    f_damp = open('booking.db', 'r', encoding='utf-8-sig')  # открываем файл с дампом базой данных
    damp = f_damp.read()  # читаем данные из файла
    f_damp.close()  # закрываем файл с дампом

    con.executescript(damp)  # запускаем запросы
    con.commit()  # сохраняем информацию в базе данны

    # работа с бд
    cursor = con.cursor()  # создаем курсор

    # (1)
    # query_1 = """
    # SELECT
    #     g.guest_name,
    #     r.room_name,
    #     rb.check_in_date,
    #     rb.check_out_date,
    #     (julianday(rb.check_out_date) - julianday(rb.check_in_date) + 1) AS Количество_дней
    # FROM
    #     guest g
    # JOIN
    #     room_booking rb ON g.guest_id = rb.guest_id
    # JOIN
    #     room r ON rb.room_id = r.room_id
    # WHERE
    #     g.guest_name LIKE '%а'
    # ORDER BY
    #     g.guest_name ASC,
    #     r.room_name ASC,
    #     Количество_дней DESC;
    # """

    # # (2)
    # query_2 = """
    # SELECT
    #     s.service_name AS Услуга,
    #     COALESCE(COUNT(sb.service_booking_id), 0) AS Количество,
    #     ROUND(AVG(sb.price), 2) AS Средняя_цена,
    #     COALESCE(SUM(sb.price), 0) AS Сумма
    # FROM
    #     service s
    # LEFT JOIN
    #     service_booking sb ON s.service_id = sb.service_id
    # GROUP BY
    #     s.service_name
    # ORDER BY
    #     Сумма DESC,
    #     Услуга ASC;
    # """

    # # (3)
    # query_3 = """
    # SELECT
    #     g.guest_name AS Фамилия_И_О,
    #     COALESCE(SUM(sb.price), 0) AS Сумма_за_услуги,
    #     COALESCE(COUNT(rb.room_booking_id), 0) AS Количество_заселений
    # FROM
    #     guest g
    # JOIN
    #     room_booking rb ON g.guest_id = rb.guest_id
    # LEFT JOIN
    #     service_booking sb ON rb.room_booking_id = sb.room_booking_id
    # GROUP BY
    #     g.guest_id
    # ORDER BY
    #     Фамилия_И_О ASC;
    # """

    # (4)
    # query_4 = """
    # CREATE TEMPORARY TABLE IF NOT EXISTS temp_bill AS
    # SELECT
    #     g.guest_name AS Фамилия_гостя,
    #     r.room_name AS Название_номера,
    #     rb.check_in_date || ' / ' || rb.check_out_date AS Даты_проживания,
    #     rb.deposit_amount AS Сумма_депозита,
    #     s.service_name AS Название_услуги,
    #     GROUP_CONCAT(sb.service_start_date, ', ' ORDER BY sb.service_start_date) AS Даты_получения_услуги,
    #     SUM(sb.price) AS Общая_оплата_за_услугу
    # FROM
    #     guest g
    # JOIN
    #     room_booking rb ON g.guest_id = rb.guest_id
    # JOIN
    #     room r ON rb.room_id = r.room_id
    # LEFT JOIN
    #     service_booking sb ON rb.room_booking_id = sb.room_booking_id
    # LEFT JOIN
    #     service s ON sb.service_id = s.service_id
    # WHERE
    #     g.guest_name = 'Астахов И.И.' AND r.room_name = 'С-0206' AND rb.check_in_date = '2021-01-13'
    # GROUP BY
    #     g.guest_id, r.room_id, rb.room_booking_id, s.service_id
    # ORDER BY
    #     g.guest_name ASC, r.room_name ASC, rb.check_in_date ASC, s.service_name ASC;
    #
    # -- Создаем итоговую таблицу с отчетом
    # CREATE TEMPORARY TABLE IF NOT EXISTS bill AS
    # SELECT
    #     Фамилия_гостя || ' ' || Название_номера || ' ' || Даты_проживания AS Вид_платежа,
    #     Сумма_депозита AS Сумма
    # FROM
    #     temp_bill
    # UNION
    # SELECT
    #     Название_услуги || ' ' || Даты_получения_услуги AS Вид_платежа,
    #     Общая_оплата_за_услугу AS Сумма
    # FROM
    #     temp_bill
    # UNION
    # SELECT
    #     'Вернуть' AS Вид_платежа,
    #     Сумма_депозита - SUM(Общая_оплата_за_услугу) AS Сумма
    # FROM
    #     temp_bill;
    #
    # SELECT * FROM bill;
    # """

    # (5)
    query_5 = """
    SELECT
        g.guest_name AS Фамилия_гостя,
        COUNT(DISTINCT rb.room_booking_id) AS Количество
    FROM
        guest g
    JOIN
        room_booking rb ON g.guest_id = rb.guest_id
    WHERE
        rb.check_in_date = (SELECT MIN(check_in_date) FROM room_booking WHERE guest_id = g.guest_id)
    GROUP BY
        g.guest_id
    ORDER BY
        Количество DESC, Фамилия_гостя ASC;
    """

    cursor.execute(query_5)

    print(cursor.fetchall())
    results = cursor.fetchall()
    for i in results:
        print(i)

    # закрываем соединение с базой
    con.close()

