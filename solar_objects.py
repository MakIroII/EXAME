import math
import tkinter

from _tkinter import TclError


class SpaceObjects:

    def __init__(self, filename):

        self.filename = filename
        self.parameter = []
        self.type = ""
        self.Datas = []

    def read_parameters(self):
        with open(self.filename) as input_file:
            for line in input_file:

                if len(line.strip()) == 0 or line[0] == '#':
                    continue  # пустые строки пропускаем
                object_type = line.split()[0]
                if self.type == object_type:
                    data = line.split()
                    try:
                        self.parameter = [data[0], float(data[1]), data[2], float(data[3]),
                                          float(data[4]), float(data[5]), float(data[6]), float(data[7]), int(data[8]),
                                          int(data[9])]
                    except IndexError:
                        self.parameter = [data[0], float(data[1]), data[2], float(data[3]),
                                          float(data[4]), float(data[5]), float(data[6]), float(data[7]), int(data[8])]
                    self.Datas.append(self.parameter)
        return (self.Datas)

    def append(self, objects):
        objects.extend(self.Datas)
        return (objects)

    def write_data_to_file(self, output_filename, t):
        with open(output_filename, t) as out_file:
            for obj in self.Datas:
                if obj[0] == self.type:
                    s = ' '.join(map(str, obj))
                    out_file.write(s + "\n")

    def write_static_to_file(self, output_filename, t,dt):
        parameters = []
        with open(self.filename) as input_file:

            for line in input_file:

                if len(line.strip()) == 0 or line[0] == '#':
                    continue  # пустые строки пропускаем
                object_type = line.split()[0]
                if self.type == object_type:
                    data = line.split()
                    try:
                        self.parameter = [data[0], float(data[1]), data[2], float(data[3]),
                                          float(data[4]), float(data[5]), float(data[6]), float(data[7]), int(data[8]),
                                          int(data[9])]
                    except IndexError:
                        self.parameter = [data[0], float(data[1]), data[2], float(data[3]),
                                          float(data[4]), float(data[5]), float(data[6]), float(data[7]), int(data[8])]
                    parameters.append(self.parameter)
        with open(output_filename, t) as out_file:
            out_file.write("За время : " + str(dt) + "\n")
            for i in range(len(self.Datas)):
                s = ""
                for j in range(len(self.Datas[i])):
                    try:
                        if j == 0 or j == 1 or j == 2 or j == 3:
                            s += " " + str(parameters[i][j])
                        if j == 4:
                            s += " Изменение координаты x: " + str(float(self.Datas[i][j]) - float(parameters[i][j]))
                        if j == 5:
                            s += " Изменение координаты y: " + str(float(self.Datas[i][j]) - float(parameters[i][j]))
                        if j == 7:
                            s += " Изменение угла: " + str(float(self.Datas[i][j]) - float(parameters[i][j])) + \
                                 " Окружностей: " + str(abs(float((self.Datas[i][j]) - float(parameters[i][j]))) / 360)
                    except IndexError:
                        pass
                out_file.write(s + "\n")


class Star(SpaceObjects):
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.type = 'Star'


class Planet(SpaceObjects):
    """Тип данных, описывающий планету.
        Содержит массу, координаты, скорость планеты,
        а также визуальный радиус планеты в пикселах и её цвет
        """

    def __init__(self, filename):
        super().__init__(filename)
        self.type = 'Planet'

    def orbit(self):
        p = Star(self.filename).read_parameters()
        orbits = []
        for i in range(len(p)):
            for j in range(len(self.Datas)):
                if p[i - 1][8] == self.Datas[j - 1][8]:
                    r = ((p[i - 1][4] - self.Datas[j - 1][4]) ** 2 + (p[i - 1][5] - self.Datas[j - 1][5]) ** 2) ** 0.5
                    orbit_cords = [float(p[i - 1][4] - r), float(p[i - 1][5] - r), float(p[i - 1][4] + r),
                                   float(p[i - 1][5] + r)]
                    orbits.append(orbit_cords)
        return (orbits)

    def move(self, objects, dt):
        for obj in objects:
            if obj[0] == 'Star':
                x = obj[4]
                y = obj[5]
                ids = obj[8]
                for body in self.Datas:
                    if body[8] == ids:
                        r = ((body[4] - x) ** 2 + (body[5] - y) ** 2) ** 0.5
                        body[7] += body[3] * dt
                        body[4] = x + r * math.cos(math.radians(body[7]))
                        body[5] = y + r * math.sin(math.radians(body[7]))


class Sputnik(SpaceObjects):
    def __init__(self, filename):
        super().__init__(filename)
        self.type = 'Sputnik'

    def radius(self, objects):
        rad = []
        r = 0
        for obj in objects:
            if obj[0] == 'Planet':
                x = obj[4]
                y = obj[5]
                ids = obj[9]
                for body in self.Datas:
                    if body[8] == ids:
                        r = ((body[4] - x) ** 2 + (body[5] - y) ** 2) ** 0.5
                    rad.insert(ids, r)
        return (rad)

    def move(self, objects, dt, r):
        for obj in objects:
            if obj[0] == 'Planet':
                x = obj[4]
                y = obj[5]
                ids = obj[9]
                for body in self.Datas:
                    if body[8] == ids:
                        body[7] += body[3] * dt
                        body[4] = x + r[ids] * math.cos(math.radians(body[7]))
                        body[5] = y + r[ids] * math.sin(math.radians(body[7]))

    def orbit(self):
        p = Planet(self.filename).read_parameters()
        orbits = []
        for i in range(len(p)):
            for j in range(len(self.Datas)):
                if p[i - 1][9] == self.Datas[j - 1][8]:
                    r = ((p[i - 1][4] - self.Datas[j - 1][4]) ** 2 + (
                            p[i - 1][5] - self.Datas[j - 1][5]) ** 2) ** 0.5
                    orbit_cords = [float(p[i - 1][4] - r), float(p[i - 1][5] - r), float(p[i - 1][4] + r),
                                   float(p[i - 1][5] + r)]
                    orbits.append(orbit_cords)

        return (orbits)


class University:

    def __init__(self, font, scale):
        self.root = tkinter.Tk()
        self.header_font = font
        self.scale_factor = scale
        self.buttons = []
        self.max_distance = 0
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = self.root.winfo_screenheight()
        self.space = tkinter.Canvas(self.root, width=self.window_width, height=self.window_height - 119, bg="black")
        self.frame = tkinter.Frame(self.root)
        self.scale_factor = 0
        self.t = self.space.create_text(0, 0, font=self.header_font, anchor='nw', text='', fill="white")
        self.dx = self.dy = 0
        self.indent = 0

    def change_distance(self, space_objects):
        max_list = []
        min_list = []
        for objs in space_objects:
            for objp in space_objects:
                for objsp in space_objects:
                    if objs[0] == "Star" and objp[0] == "Planet" and objs[8] == objp[8]:
                        radius_max = (((objs[4] - objp[4]) ** 2 + (objs[5] - objp[5]) ** 2) ** 0.5 + objs[5]) + \
                                     objp[1]
                        radius_min = -(((objs[4] - objp[4]) ** 2 + (objs[5] - objp[5]) ** 2) ** 0.5) + objs[5] - objp[1]
                        if objsp[0] == "Sputnik" and objp[9] == objsp[8]:
                            radius_max += ((objsp[4] - objp[4]) ** 2 + (objsp[5] - objp[5]) ** 2) ** 0.5 - objp[1] + \
                                          objsp[1]
                            radius_min += -(((objsp[4] - objp[4]) ** 2 + (objsp[5] - objp[5]) ** 2) ** 0.5) + \
                                          objp[1] - objsp[1]
                        max_list.append(radius_max)
                        min_list.append(radius_min)
        print(max(max_list), min(min_list))
        self.max_distance = max(max_list) - (min(min_list))
        self.indent = -(min(min_list))
        self.scale_factor = min(self.window_height - 119, self.window_width) / (self.max_distance)
        print(self.window_height, self.window_width, self.scale_factor)
        self.dx = self.dy = self.scale_cord(self.indent)

    def location(self, buttons, place_b, entries, place_e, scales, place_s, labels, place_l):
        self.space.pack(side=tkinter.TOP)
        self.frame.pack(side=tkinter.BOTTOM)
        i = 0
        for button in buttons:
            try:
                button.pack(side=place_b[i])
            except TclError:
                pass
            i += 1
        i = 0
        for entry in entries:
            try:
                entry.pack(side=place_e[i])
            except TclError:
                pass
            i += 1
        i = 0
        for scale in scales:
            try:
                scale.pack(side=place_s[i])
            except TclError:
                pass
            i += 1
        i = 0
        for label in labels:
            try:
                label.pack(side=place_l[i])
            except TclError:
                pass
            i += 1

    def button(self, n, text, commands):
        buttons = []
        for i in range(n):
            button1 = tkinter.Button(self.frame, text=text[i], command=commands[i])
            buttons.append(button1)
        self.buttons = buttons
        return (buttons)

    def entry(self, n, text):
        entries = []
        for i in range(n):
            entry = tkinter.Entry(self.frame, textvariable=text[i])
            entries.append(entry)
        return (entries)

    def scale(self, n, text, orient):
        scales = []
        for i in range(n):
            scale = tkinter.Scale(self.frame, variable=text[i], orient=orient[i])
            scales.append(scale)
        return (scales)

    def label(self, n, text, width):
        labels = []
        for i in range(n):
            one_label = tkinter.Label(self.frame, textvariable=text[i], width=width[i])
            labels.append(one_label)
        return (labels)

    def trigger_button(self, i, text, command):
        self.buttons[i - 1]["text"] = text
        self.buttons[i - 1]["command"] = command

    def create_image(self, object):
        """Создаёт отображаемый объект спутника.

        Параметры:

        **space** — холст для рисования.
        **star** — объект звезды.
        """

        x = object[4]
        y = object[5]
        r = object[1]
        object[6] = self.space.create_oval(self.scale_cord(x - r) + self.dx, self.scale_cord(y - r) + self.dy,
                                           self.scale_cord(x + r) + self.dx,
                                           self.scale_cord(y + r) + self.dy, fill=object[2])

    def create_orbit_image(self, objects):
        orbits = []
        for obj in objects:
            for body in objects:
                if obj[0] == 'Star' and body[0] == 'Planet' and obj[8] == body[8]:
                    r = ((obj[4] - body[4]) ** 2 + (obj[5] - body[5]) ** 2) ** 0.5
                    orbit_cords = [float(obj[4] - r), float(obj[5] - r), float(obj[4] + r),
                                   float(obj[5] + r)]
                    orbits.append(orbit_cords)
                if obj[0] == 'Planet' and body[0] == 'Sputnik' and obj[9] == body[8]:
                    r = ((obj[4] - body[4]) ** 2 + (obj[5] - body[5]) ** 2) ** 0.5
                    orbit_cords = [float(obj[4] - r), float(obj[5] - r), float(obj[4] + r),
                                   float(obj[5] + r)]
                    orbits.append(orbit_cords)
        for orbit in orbits:
            self.space.create_oval(self.scale_cord(orbit[0]) + self.dx, self.scale_cord(orbit[1]) + self.dy,
                                   self.scale_cord(orbit[2]) + self.dx,
                                   self.scale_cord(orbit[3]) + self.dy,
                                   outline="white", tags='circle')

    def update_system_name(self, system_name):
        """Создаёт на холсте текст с названием системы небесных тел.
        Если текст уже был, обновляет его содержание.

        Параметры:

        **space** — холст для рисования.
        **system_name** — название системы тел.
        """
        self.space.delete(self.t)
        self.t = self.space.create_text(0, 0, font=self.header_font, anchor='nw', text=system_name, fill="white")

    def update_object_position(self, objects, orbit_perform):
        """Перемещает отображаемый объект на холсте.

        Параметры:

        **space** — холст для рисования.
        **body** — тело, которое нужно переместить.
        """
        circles = self.space.find_withtag('circle')
        if orbit_perform:
            for circle in circles:
                self.space.delete(circle)
            self.create_orbit_image(objects)
            self.space.tag_lower('circle')
        if not orbit_perform and circles:
            for circle in circles:
                self.space.delete(circle)

        for body in objects:
            x = body[4]
            y = body[5]
            r = body[1]
            if x + r < 0 or x - r > self.window_width or y + r < 0 or y - r > self.window_height:
                self.space.coords(body[6], self.window_width + r, self.window_height + r,
                                  self.window_width + 2 * r, self.window_height + 2 * r)  # положить за пределы окна
            self.space.coords(body[6], self.scale_cord(x - r) + self.dx, self.scale_cord(y - r) + self.dy,
                              self.scale_cord(x + r) + self.dx,
                              self.scale_cord(y + r) + self.dy)

    def loop(self):
        self.root.mainloop()

    def after(self, time_speed, command):
        self.space.after(101 - int(time_speed), command)

    def delete(self, obj):
        self.space.delete(obj)

    def tag_lower(self, obj):
        self.space.tag_lower(obj)

    def scale_cord(self, cord):
        """Возвращает экранную **y** координату по **y** координате модели.
        Принимает вещественное число, возвращает целое число.
        В случае выхода **y** координаты за пределы экрана возвращает
        координату, лежащую за пределами холста.
        Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

        Параметры:

        **y** — y-координата модели.
        """

        return int(cord * self.scale_factor)

    def scale_objects(self, n=1.2):
        def more(event):
            event.x = self.scale_cord(event.x)
            event.y = self.scale_cord(event.y)
            self.scale_factor *= n
            self.dx -= self.scale_cord(event.x) - self.scale_cord(self.dx)
            self.dy -= self.scale_cord(event.y) - self.scale_cord(self.dy)

        def small(event):
            self.scale_factor /= n
            self.dx = self.dy = self.scale_cord(self.indent)

        self.space.bind("<Button-1>", more)
        self.space.bind("<Button-3>", small)
