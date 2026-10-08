import tkinter as tk
import ctypes

root = tk.Tk()
root.title("RoaringKnight Trail")
root.attributes("-topmost", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

TRANSPARENT_COLOR = "black"
root.config(bg=TRANSPARENT_COLOR)
root.attributes("-transparentcolor", TRANSPARENT_COLOR)

# Функція для налаштування системного стилю Windows через ctypes
def set_taskbar_behavior(e=None):
    try:
        # Отримуємо дескриптор вікна Tkinter
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        # Стилі Windows: залишаємо вікно на панелі завдань, але прибираємо зайву рамку заголовка
        # GWL_STYLE = -16, WS_POPUP = 0x80000000, WS_VISIBLE = 0x10000000, WS_EX_APPWINDOW = 0x00040000
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
        # Прибираємо звичайний заголовок рамки, але залишаємо системні функції для панелі завдань
        style = style & ~0x00080000  # WS_CAPTION
        style = style & ~0x00040000  # WS_SIZEBOX (щоб не можна було змінювати розмір мишею)
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
    except Exception:
        pass

# Викликаємо після побудови вікна
root.after(100, set_taskbar_behavior)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg=TRANSPARENT_COLOR, highlightthickness=0)
canvas.pack()

# Канонічна послідовність зсувів
offsets = [-6, -4, 0, 4, 6, 4, 0, -4]
index = 0

ghosts = []
counter = 0

def update_mouse_trail():
    global index, counter
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    
    counter += 1
    if counter % 2 == 0:
        offset_x = float(x + offsets[index])
        offset_y = float(y + offsets[index])
        ghosts.append([offset_x, offset_y, 0])
        index = (index + 1) % len(offsets)
    
    canvas.delete("trail")
    
    new_ghosts = []
    for g in ghosts:
        gx, gy, age = g
        
        # Швидкість пересування праворуч
        gx += 5.0
        age += 1
        
        if age < 25:
            new_ghosts.append([gx, gy, age])
            
            # Плавне згасання
            fade = int(255 - (age * 10))
            if fade < 0:
                fade = 0
            color_hex = f"#{fade:02x}{fade:02x}{fade:02x}"
            
            # Форма курсора-стрілочки
            points = [
                gx, gy,
                gx, gy + 16,
                gx + 4, gy + 12,
                gx + 10, gy + 16,
                gx + 12, gy + 14,
                gx + 6, gy + 10,
                gx + 11, gy + 10
            ]
            canvas.create_polygon(points, fill=color_hex, outline="", tags="trail")
            
    ghosts[:] = new_ghosts
    root.after(20, update_mouse_trail)

root.after(20, update_mouse_trail)
root.mainloop()
