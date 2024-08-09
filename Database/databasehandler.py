import os
import sqlite3

class DatabaseHandler():
    def __init__(self, database_name : str):
        self.connect = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.connect.row_factory = sqlite3.Row

    def add_player(self, name : str, user_id : int, number : int, couple : int):
        cursor = self.connect.cursor()
        query = f"INSERT INTO Roles (name, discordId, Numero, couple) VALUES (? , ?, ?, ?);"
        cursor.execute(query, (name, user_id, number, couple, ))
        cursor.close()
        self.connect.commit()

    def add_player_role(self, name: str, role: str):
        vie = True
        cursor = self.connect.cursor()
        query = f"UPDATE Roles SET role = ?, vie = ? WHERE name = ?;"
        cursor.execute(query, (role, vie, name, ))
        cursor.close()
        self.connect.commit()

    def add_couple(self, number: str):
        cursor = self.connect.cursor()
        query = f"UPDATE Roles SET Couple = ? WHERE Numero = ?;"
        cursor.execute(query, (1, number, ))
        cursor.close()
        self.connect.commit()

    def role_for_name(self, name : str) -> str:
        cursor = self.connect.cursor()
        query = f"SELECT role FROM Roles WHERE name = ?"
        cursor.execute(query, (name, ))
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0])["role"]

    def name_for_role(self, role : str) -> str:
        cursor = self.connect.cursor()
        query = f"SELECT name FROM Roles WHERE role = ?;"
        cursor.execute(query, (role, ))
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0])["name"]

    def role_for_number(self, number : str) -> str:
        cursor = self.connect.cursor()
        query = f"SELECT role FROM Roles WHERE Numero = ?;"
        cursor.execute(query, (number, ))
        result = cursor.fetchall()
        cursor.close()
        print(result, number)
        print((result[0])["role"])
        return dict(result[0])["role"]

    def no_player(self, name : str) -> bool:
        cursor = self.connect.cursor()
        query = f"SELECT name FROM Roles WHERE name = ?;"
        cursor.execute(query, (name, ))
        result = cursor.fetchall()
        cursor.close()
        self.connect.commit()
        return len(result) > 0

    def player_list(self):
        cursor = self.connect.cursor()
        query = f"SELECT name FROM Roles;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        player_list = [row['name'] for row in result]
        return player_list

    def number_list(self):
        cursor = self.connect.cursor()
        query = f"SELECT name, Numero, vie FROM Roles;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return {name: [numero, vie] for name, numero, vie in result}

    def lg_list(self):
        role = f"Loup-Garou <:loupgarou:1075445518827798599>"
        cursor = self.connect.cursor()
        query = f"SELECT name FROM Roles WHERE role = ?;"
        cursor.execute(query, (role,))
        result = cursor.fetchall()
        cursor.close()
        player_list = [row['name'] for row in result]
        return player_list

    def discordID_for_name(self, name : str) -> str:
        cursor = self.connect.cursor()
        query = f"SELECT discordId FROM Roles WHERE name = ?;"
        cursor.execute(query, (name, ))
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0])["discordId"]

    def name_for_number(self, number : str) -> str:
        cursor = self.connect.cursor()
        query = f"SELECT name FROM Roles WHERE Numero = ?;"
        cursor.execute(query, (number, ))
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0])['name']

    def no_number(self, number: str) -> bool:
        cursor = self.connect.cursor()
        query = f"SELECT name FROM Roles WHERE Numero = ?;"
        cursor.execute(query, (number, ))
        result = cursor.fetchall()
        cursor.close()
        self.connect.commit()
        return len(result) > 0

    def death_info(self, number : str):
        cursor = self.connect.cursor()
        query = f"SELECT name, role FROM Roles WHERE Numero = ?"
        cursor.execute(query, (number, ))
        result = cursor.fetchall()
        cursor.close()
        return dict(result)

    def kill_by_name(self, name : str):
        cursor = self.connect.cursor()
        query = "UPDATE Roles SET vie = ? WHERE name = ?"
        cursor.execute(query, (0, name, ))
        cursor.close()
        self.connect.commit()

    def reset(self):
        cursor = self.connect.cursor()
        query = f"DELETE FROM Roles;"
        cursor.execute(query)
        cursor.close()
        self.connect.commit()