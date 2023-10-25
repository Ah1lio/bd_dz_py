import psycopg2

def create_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone(
    id SERIAL PRIMARY KEY,
    id_client INTEGER NOT NULL REFERENCES client(id),
    phone CHAR(11) 
    );
    """)

def add_new_client(cur, name, surname, email):
    cur.execute("""
    INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);
    """, (name, surname, email))
    
def add_new_phone(cur, id_client, phone):
    ("""
    INSERT INTO phone(id_client, phone) VALUES(%s, %s)
    """, (id_client, phone))

def change_client():
    print("Для изменения информации, введите нужную вам цифру.\n"
          "1 - изменить имя; 2 - изменить фамилию; 3 - изменить e-mail; 4 - изменить номер телефона")
    while True:
        command = int(input())
        if command == 1:
            input_id = input("Введите id клиента имя которого хотите изменить: ")
            input_name_change = input("Введите новое имя:")
            cur.execute("""
            UPDATE client SET name = %s where id = %s;
            """, (input_name_change, input_id))
            break
        elif command == 2:
            input_id = input("Введите id клиента имя которого хотите изменить: ")
            input_surname_change = input("Введите новую фамилию:")
            cur.execute("""
            UPDATE client SET surname = %s where id = %s;
            """, (input_surname_change, input_id))
            break
        elif command == 3:
            input_id = input("Введите id клиента имя которого хотите изменить: ")
            input_email_change = input("Введите новый email:")
            cur.execute("""
            UPDATE client SET email = %s where id = %s;
            """, (input_email_change, input_id))
            break
        elif command == 4:
            input_phone = input("Введите номер телефона который хотите изменить: ")
            input_phone_change = input("Введите новый номер телефона: ")
            cur.execute("""
            UPDATE phone SET phone = %s where phone = %s;
            """, (input_phone_change, input_phone))
            break
        else:
            print("Данной команды нет")

def delete_phone():
    input_id_client = input("Введите id клиента номер телефона которого хотите удалить: ")
    input_phone_client = input("Введите номер телефона который хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone WHERE id_client=%s AND phone=%s
        """, (input_id_client, input_phone_client))

def delete_client():
    '''Удаление имеющейся информации о клиенте'''
    input_id_client = input("Введите id клиента которого хотите удалить: ")
    input_client_name = input("Введите фамилию клиента которого хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone WHERE id_client=%s
        """, (input_id_client,))
        cur.execute("""
        DELETE FROM client WHERE id=%s AND name=%s
        """, (input_id_client, input_client_name))

def find_client():
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n "
          "1 - найти по имени; 2 - найти по фамилии; 3 - найти по e-mail; 4 - найти по номеру телефона")
    while True:
        command_find = int(input("Введите команду для поиска клиента: "))
        if command_find == 1:
            input_name_find = input("Введите имя для поиска клиента: ")
            cur.execute("""
            SELECT * FROM client as cl
            LEFT JOIN phone AS ph ON ph.id = cl.id
            WHERE name = %s
            """, (input_name_find))
            print(cur.fetchall())
        elif command_find == 2:
            input_surname_find = input("Введите фамилию для поиска клиента: ")
            cur.execute("""
            SELECT * FROM client as cl
            LEFT JOIN phone AS ph ON ph.id = cl.id
            WHERE surname = %s
            """, (input_surname_find))
            print(cur.fetchall())
        elif command_find == 3:
            input_email_find = input("Введите email для поиска клиента: ")
            cur.execute("""
            SELECT * FROM client as cl
            LEFT JOIN phone AS ph ON ph.id = cl.id
            WHERE email = %s
            """, (input_email_find))
            print(cur.fetchall())
        elif command_find == 4:
            input_phone_find = input("Введите номер телефона для поиска клиента: ")
            cur.execute("""
            SELECT * FROM client as cl
            LEFT JOIN phone AS ph ON ph.id = cl.id
            WHERE phone = %s
            """, (input_phone_find))
            print(cur.fetchall())
        else:
            print("Данной команды нет")

with psycopg2.connect(database = 'test', user = 'postgres', password = '10012003') as conn:
    with conn.cursor() as cur:
        create_table(cur)
        add_new_client(cur, "Polina", "Drozdova", "pol.drozd@mail.ru")
        add_new_client(cur, "Pasha", "Begunov", "begun@mail.ru")
        add_new_client(cur, "Dima", "Volkov", "volk@mail.ru")
        add_new_phone(cur, 1, "12345678910")
        add_new_phone(cur, 2, "59623587412")
        add_new_phone(cur, 3, "23410679319")
        change_client()
        delete_phone()
        delete_client()
        find_client()
               
conn.close()