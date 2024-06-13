import os
from tkinter.filedialog import *

from solar_objects import *

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

orbit_perform = False
"""Флаг цикличности выполнения обновления изображения орбит """

physical_time = 0, 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = 0.0
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = 0
"""Шаг по времени при моделировании.
Тип: float"""

r = 0

time_speed = 0

space_objects = []
"""Список космических объектов."""


def create_orbit():
    global orbit_perform
    orbit_perform = True
    screen.trigger_button(4, "Delete Orbit", delete_orbit)
    screen.create_orbit_image(space_objects)
    screen.tag_lower('circle')


def delete_orbit():
    screen.create_orbit_image([])
    global orbit_perform
    orbit_perform = False
    screen.trigger_button(4, "Create Orbit", create_orbit)


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через 1-100 миллисекунд.
    """
    global physical_time
    global displayed_time

    try:
        p.move(space_objects, time_step.get())
        sp.move(space_objects, time_step.get(), r)
        screen.update_object_position(space_objects, orbit_perform)
        physical_time += time_step.get()
        displayed_time.set("%.1f" % physical_time + " seconds gone")

        if perform_execution:
            screen.after(time_speed.get(), execution)
    except NameError:
        physical_time += time_step.get()
        displayed_time.set("%.1f" % physical_time + " seconds gone")

        if perform_execution:
            screen.after(time_speed.get(), execution)
        pass
    except TclError:
        pass


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    screen.trigger_button(1, "Pause", stop_execution)
    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    screen.trigger_button(1, "Start", start_execution)
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global st
    global sp
    global p
    global r
    stop_execution()
    for obj in space_objects:
        screen.delete(obj[6])
    delete_orbit()
    space_objects = []
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    filename = os.path.splitext(os.path.basename(in_filename))[0]

    screen.update_system_name(filename)
    st = Star(in_filename)
    p = Planet(in_filename)
    sp = Sputnik(in_filename)
    try:
        p.read_parameters()
        st.read_parameters()
        sp.read_parameters()
        sp.append(space_objects)
        p.append(space_objects)
        st.append(space_objects)
        r = sp.radius(space_objects)
        screen.change_distance(space_objects)
        p.move(space_objects, 0)
        sp.move(space_objects, 0, r)
        for obj in space_objects:
            screen.create_image(obj)
    except (FileNotFoundError, UnicodeDecodeError, IndexError, ValueError):
        pass


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    try:
        p.write_data_to_file(out_filename, 'w')
        st.write_data_to_file(out_filename, 'a')
        sp.write_data_to_file(out_filename, 'a')
    except NameError:
        pass


def static_save_dialog():
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    try:
        st.write_static_to_file(out_filename, 'w')
        p.write_static_to_file(out_filename, 'a')
        sp.write_static_to_file(out_filename, 'a')
    except NameError:
        pass


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global Buttons
    global screen

    print('Modelling started!')
    physical_time = 0

    screen = University("Arial-16", None)

    Buttons = screen.button(5, ["Start", "Open file", "Save to file", "Create Orbit", "Static Save "],
                            [start_execution, open_file_dialog, save_file_dialog, create_orbit, static_save_dialog])

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    entries = screen.entry(1, [time_step])

    time_speed = tkinter.DoubleVar()
    scales = screen.scale(1, [time_speed], ["horizontal"])

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")
    labels = screen.label(1, [displayed_time], [30])

    screen.location(Buttons, ["left", "", " ", "", ""], entries, ['left'], scales, ["left"], labels, ["right"])
    screen.location(Buttons, ["left", "left", "left", "left", "left"], entries, [''], scales, [""], labels, [""])

    screen.scale_objects()

    try:
        screen.loop()
    except KeyboardInterrupt:
        pass
    print('Modelling finished!')


if __name__ == "__main__":
    main()
