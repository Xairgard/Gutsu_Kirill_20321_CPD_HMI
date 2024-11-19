## Задание
Руководство компании целыми днями не знает куда себя деть. Поэтому они решили дать задание своим программистам написать программу игры "Морской бой". Но эта игра будет немного отличаться от классической. Для тех, кто не знаком с этой древней, как мир, игрой, напомню ее краткое описание.
Каждый игрок у себя на бумаге рисует игровое поле 10 х 10 клеток и расставляет на нем десять кораблей: однопалубных - 4; двухпалубных - 3; трехпалубных - 2; четырехпалубный - 1.

![alt text](https://github.com/Zhastik/Zhaslan_Dusaev_20321_HMI_CPD/blob/main/CPD/Task_2/download.png)

Корабли расставляются случайным образом, но так, чтобы не выходили за пределы игрового поля и не соприкасались друг с другом (в том числе и по диагонали).

Затем, игроки по очереди называют клетки, куда производят выстрелы. И отмечают эти выстрелы на другом таком же поле в 10 х 10 клеток, которое представляет поле соперника. Соперник при этом должен честно отвечать: "промах", если ни один корабль не был задет и "попал", если произошло попадание. Выигрывает тот игрок, который первым поразит все корабли соперника.

Но это была игра из глубокого прошлого. Теперь же, в компьютерную эру, корабли на игровом поле могут перемещаться в направлении своей ориентации на одну клетку после каждого хода соперника, если в них не было ни одного попадания.

Итак, лично вам поручается сделать важный фрагмент этой игры - расстановку и управление кораблями в этой игре. А само задание звучит так.

В программе необходимо объявить два класса:
Ship - для представления кораблей;
GamePole - для описания игрового поля.

Класс Ship должен описывать корабли набором следующих параметров:
x, y - координаты начала расположения корабля (целые числа);
length - длина корабля (число палуб: целое значение: 1, 2, 3 или 4);
tp - ориентация корабля (1 - горизонтальная; 2 - вертикальная).

![alt text](https://github.com/Zhastik/Zhaslan_Dusaev_20321_HMI_CPD/blob/main/CPD/Task_2/4231.png)

Объекты класса Ship должны создаваться командами:

ship = Ship(length)
ship = Ship(length, tp)
ship = Ship(length, tp, x, y)

По умолчанию (если не указывается) параметр tp = 1, а координаты x, y равны None.
В каждом объекте класса Ship должны формироваться следующие локальные атрибуты:

_x, _y - координаты корабля (целые значения в диапазоне [0; size), где size - размер игрового поля);
_length - длина корабля (число палуб);
_tp - ориентация корабля;
_is_move - возможно ли перемещение корабля (изначально равно True);
_cells - изначально список длиной length, состоящий из единиц (например, при length=3, _cells = [1, 1, 1]).

Список _cells будет сигнализировать о попадании соперником в какую-либо палубу корабля. Если стоит 1, то попадания не было, а если стоит значение 2, то произошло попадание в соответствующую палубу.
При попадании в корабль (хотя бы одну его палубу), флаг _is_move устанавливается в False и перемещение корабля по игровому полю прекращается.

В самом классе Ship должны быть реализованы следующие методы (конечно, возможны и другие, дополнительные):
set_start_coords(x, y) - установка начальных координат (запись значений в локальные атрибуты _x, _y);
get_start_coords() - получение начальных координат корабля в виде кортежа x, y;

move(go) - перемещение корабля в направлении его ориентации на go клеток (go = 1 - движение в одну сторону на клетку; go = -1 - движение в другую сторону на одну клетку); движение возможно только если флаг _is_move = True;

is_collide(ship) - проверка на столкновение с другим кораблем ship (столкновением считается, если другой корабль или пересекается с текущим или просто соприкасается, в том числе и по диагонали); метод возвращает True, если столкновение есть и False - в противном случае;

is_out_pole(size) - проверка на выход корабля за пределы игрового поля (size - размер игрового поля, обычно, size = 10); возвращается булево значение True, если корабль вышел из игрового поля и False - в противном случае;

С помощью магических методов ```__getitem__()``` и ```__setitem__()``` обеспечить доступ к коллекции _cells следующим образом:
```Py
value = ship[indx] # считывание значения из _cells по индексу indx (индекс отсчитывается от 0)
ship[indx] = value # запись нового значения в коллекцию _cells
```
init() - начальная инициализация игрового поля; здесь создается список из кораблей (объектов класса Ship): однопалубных - 4; двухпалубных - 3; трехпалубных - 2; четырехпалубный - 1 (ориентация этих кораблей должна быть случайной).

Корабли формируются в коллекции _ships следующим образом: однопалубных - 4; двухпалубных - 3; трехпалубных - 2; четырехпалубный - 1. Ориентация этих кораблей должна быть случайной. Для этого можно воспользоваться функцией randint следующим образом:
```Py
[Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), ...]
```
Начальные координаты x, y не расставленных кораблей равны None.
После этого, выполняется их расстановка на игровом поле со случайными координатами так, чтобы корабли не пересекались между собой.

get_ships() - возвращает коллекцию _ships;

move_ships() - перемещает каждый корабль из коллекции _ships на одну клетку (случайным образом вперед или назад) в направлении ориентации корабля; если перемещение в выбранную сторону невозможно (другой корабль или пределы игрового поля), то попытаться переместиться в противоположную сторону, иначе (если перемещения невозможны), оставаться на месте;

show() - отображение игрового поля в консоли (корабли должны отображаться значениями из коллекции _cells каждого корабля, вода - значением 0);

get_pole() - получение текущего игрового поля в виде двумерного (вложенного) кортежа размерами size x size элементов.

Пример отображения игрового поля:
```py
0 0 1 0 1 1 1 0 0 0
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 1
0 0 0 0 1 0 1 0 0 1
0 0 0 0 0 0 1 0 0 0
1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0
```
В программе требуется только объявить классы Ship и GamePole с соответствующим функционалом. На экран выводить ничего не нужно.

Завершите эту программу, добавив еще один класс SeaBattle для управления игровым процессом в целом. Игра должна осуществляться между человеком и компьютером. Выстрелы со стороны компьютера можно реализовать случайным образом в свободные клетки. Сыграйте в эту игру и выиграйте у компьютера.

## Листинг
```Py

from random import randint, choice

class Ship:
    def __init__(self, length, tp=1, x=None, y=None, size=10):
        # Инициализация объекта корабля
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * length
        self._size = size

    def set_start_coords(self, x, y):
        # Установка начальных координат корабля
        self._x = x
        self._y = y

    def get_start_coords(self):
        # Получение начальных координат корабля
        return self._x, self._y

    def move(self, go):
        # Перемещение корабля в направлении его ориентации
        if self._is_move:
            if self._tp == 1:
                self._x += go
            elif self._tp == 2:
                self._y += go

    def is_collide(self, other_ship):
        # Проверка на столкновение с другим кораблем
        if self._x is None or self._y is None or other_ship._x is None or other_ship._y is None:
            return False

        def is_in_proximity(x1, y1, x2, y2):
            # Проверка на соприкосновение координат
            return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

        for coord1 in self._get_ship_coords():
            for coord2 in other_ship._get_ship_coords():
                if is_in_proximity(*coord1, *coord2):
                    return True

        return False

    def is_out_pole(self, size) -> bool:
        # Проверка на выход корабля за пределы игрового поля
        x, y = self.get_start_coords()
        if self._tp == 1:
            if x is None or x < 0 or x + self._length > size:
                return True
        elif self._tp == 2:
            if y is None or y < 0 or y + self._length > size:
                return True
        return False

    def _get_ship_coords(self):
        # Получение координат корабля
        if self._tp == 1:
            return [(self._x + i, self._y) for i in range(self._length)]
        else:
            return [(self._x, self._y + i) for i in range(self._length)]

    def _is_coords_in_proximity(self, coords1, coords2):
        # Проверка соприкосновения координат
        for coord1 in coords1:
            for coord2 in coords2:
                if abs(coord1[0] - coord2[0]) <= 1 and abs(coord1[1] - coord2[1]) <= 1:
                    return True
        return False

    def __getitem__(self, index):
        # Получение значения из _cells по индексу
        return self._cells[index]

    def __setitem__(self, index, value):
        # Запись нового значения в _cells
        self._cells[index] = value


class GamePole:
    def __init__(self, size):
        # Инициализация объекта игрового поля
        self._size = size
        self._field = [[0] * size for _ in range(size)]  # Игровое поле, 0 - пустая ячейка
        self._ships = []  # Список кораблей, изначально пустой

    def init(self):
        # Начальная инициализация игрового поля
        ship_counts = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Количество кораблей каждой длины
        for length in ship_counts:
            tp = randint(1, 2)  # Случайная ориентация корабля
            ship = Ship(length, tp)
            self.place_ship_on_field(ship)

    def place_ship_on_field(self, ship):
        # Расстановка кораблей на игровом поле
        while True:
            ship.set_start_coords(randint(0, self._size - 1), randint(0, self._size - 1))
            if not self._is_ship_colliding(ship) and not ship.is_out_pole(self._size):
                self.place_ship(ship)
                break

    def _is_ship_colliding(self, ship):
        # Проверка на столкновение кораблей
        for other_ship in self._ships:
            if ship.is_collide(other_ship):
                return True
        return False

    def place_ship(self, ship):
        # Размещение корабля на игровом поле
        x, y = ship.get_start_coords()
        for i in range(ship._length):
            if ship._tp == 1:
                self._field[x + i][y] = 1  # 1 - ячейка с кораблем
            else:
                self._field[x][y + i] = 1
        self._ships.append(ship)

    def get_ships(self):
        # Получение списка кораблей
        return self._ships

    def move_ships(self):
        # Перемещение каждого корабля на одну клетку
        for ship in self._ships:
            go = randint(-1, 1)  # -1 - назад, 0 - остаться на месте, 1 - вперед
            ship.move(go)
            if not self._is_ship_colliding(ship) and not ship.is_out_pole(self._size):
                self._update_ship_position(ship, go * -1)  # Если корабль успешно переместился, вернуться обратно
            else:
                ship.move(go * -1)  # Вернуть корабль на место, если перемещение не удалось

    def _update_ship_position(self, ship, go):
        # Обновление позиции корабля после перемещения
        x, y = ship.get_start_coords()
        for i in range(ship._length):
            if ship._tp == 1:
                self._field[x + i - go][y] = 0  # Очистить предыдущее место корабля
                self._field[x + i][y] = 1  # 1 - ячейка с кораблем
            else:
                self._field[x][y + i - go] = 0
                self._field[x][y + i] = 1

    def show(self):
        # Отображение игрового поля в консоли
        for row in self._field:
            print(" ".join(map(str, row)))

    def get_pole(self):
        # Получение текущего игрового поля в виде двумерного (вложенного) кортежа
        return tuple(tuple(row) for row in self._field)


class SeaBattle:
    def __init__(self, size=10):
        # Создаем объекты игрового поля для игрока и компьютера
        self._player_pole = GamePole(size)
        self._computer_pole = GamePole(size)

    def play(self):
        # Инициализация полей компьютера и игрока
        self._computer_pole.init()
        self._player_pole.init()

        while True:
            # Вывод состояния полей на экран
            print("\nПоле игрока:")
            self._player_pole.show()
            print("\nПоле компьютера:")
            self._computer_pole.show()

            # Ход игрока
            player_shot = self._get_player_shot()
            self._process_shot(player_shot, self._computer_pole, "игрок")

            # Проверка на победу игрока
            if self._check_victory(self._computer_pole):
                print("\nПОБЕДА!")
                break

            # Ход компьютера
            computer_shot = self._get_computer_shot()
            self._process_shot(computer_shot, self._player_pole, "компьютер")

            # Проверка на победу компьютера
            if self._check_victory(self._player_pole):
                print("\nКомпьютер победил. Попробуйте еще раз!")
                break

    def _get_player_shot(self):
        while True:
            try:
                # Ввод координат выстрела от игрока
                x = int(input("\nВведите номер строки (от 1 до {}): ".format(self._player_pole._size))) - 1
                y = int(input("Введите номер столбца (от 1 до {}): ".format(self._player_pole._size))) - 1

                # Проверка введенных координат на корректность
                if 0 <= x < self._player_pole._size and 0 <= y < self._player_pole._size:
                    return x, y
                else:
                    print("Некорректные координаты. Попробуйте еще раз.")
            except ValueError:
                print("Введите целые числа.")

    def _get_computer_shot(self):
        # Случайный выстрел компьютера
        x, y = randint(0, self._computer_pole._size - 1), randint(0, self._computer_pole._size - 1)
        return x, y

    def _process_shot(self, shot, pole, shooter):
        x, y = shot
        if pole._field[x][y] == 1:
            # Обработка попадания
            print("\nПопадание {}!".format(shooter))
            pole._field[x][y] = "X"
        else:
            # Обработка промаха
            print("\nМимо {}.".format(shooter))
            pole._field[x][y] = "O"

    def _check_victory(self, pole):
        # Проверка на победу (все корабли потоплены)
        return all(cell != 1 for row in pole._field for cell in row)


# Игра
if __name__ == "__main__":
   # sea_battle = SeaBattle(10)
   # sea_battle.play()

    # Тесты
    ship = Ship(2)
    assert ship._length == 2 and ship._tp == 1 and ship._x is None and ship._y is None, "неверные значения атрибутов объекта класса Ship"
    assert ship._cells == [1, 1], "неверный список _cells"
    assert ship._is_move, "неверное значение атрибута _is_move"
    ship.set_start_coords(1, 2)
    assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
    assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"
    ship.move(1)

    s1 = Ship(4, 1, 0, 0)
    s2 = Ship(3, 2, 0, 0)
    s3 = Ship(3, 2, 0, 2)
    assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
    assert not s1.is_collide(s3), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"

    s2 = Ship(3, 2, 1, 1)
    assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"
    s2 = Ship(3, 1, 8, 1)
    assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"
    s2 = Ship(3, 2, 1, 5)
    assert not s2.is_out_pole(10), "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"
    s2[0] = 2
    assert s2[0] == 2, "неверно работает обращение ship[indx]"

    p = GamePole(10)
    p.init()
    for nn in range(5):
        for s in p._ships:
            assert not s.is_out_pole(10), "корабли выходят за пределы игрового поля"
            for ship in p.get_ships():
                if s != ship:
                    assert not s.is_collide(ship), "корабли на игровом поле соприкасаются"
        p.move_ships()

    gp = p.get_pole()
    assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
    assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"
    pole_size_8 = GamePole(8)
    pole_size_8.init()
    print("\nPassed")

```

## Скриншот

![alt text](https://github.com/Zhastik/Zhaslan_Dusaev_20321_HMI_CPD/blob/main/CPD/Task_2/res.png)
