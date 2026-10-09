import tkinter as tk
import ctypes

root = tk.Tk()
root.title("RoaringKnight Trail")
root.attributes("-topmost", True)

# Повністю приховуємо системний курсор
root.config(cursor="none")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Колір, який стає повністю прозорим (невидимим)
TRANSPARENT_COLOR = "#010101" 
root.config(bg=TRANSPARENT_COLOR)
root.attributes("-transparentcolor", TRANSPARENT_COLOR)

def set_taskbar_behavior(e=None):
    try:
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
        style = style & ~0x00080000  # WS_CAPTION
        style = style & ~0x00040000  # WS_SIZEBOX
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
    except Exception:
        pass

root.after(100, set_taskbar_behavior)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg=TRANSPARENT_COLOR, highlightthickness=0, cursor="none")
canvas.pack()

# Ваша траєкторія з восьми чисел
offsets = [0, 8, 12, 8, 0, -8, -12, -8]
index = 0

ghosts = []
counter = 0

def update_mouse_trail():
    global index, counter
    
    # Реальні координати миші
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    
    counter += 1
    if counter % 4 == 0:
        index = (index + 1) % len(offsets)
        offset_x = float(x + offsets[index])
        offset_y = float(y + offsets[index])
        ghosts.append([offset_x, offset_y, 0])

    canvas.delete("trail")
    
    # 1. Головний чорний курсор за поточною точкою траєкторії
    current_x = float(x + offsets[index])
    current_y = float(y + offsets[index])
    
    main_cursor_points = [
        current_x, current_y,
        current_x, current_y + 16,
        current_x + 4, current_y + 12,
        current_x + 10, current_y + 16,
        current_x + 12, current_y + 14,
        current_x + 6, current_y + 10,
        current_x + 11, current_y + 10
    ]
    canvas.create_polygon(main_cursor_points, fill="black", outline="white", width=1, tags="trail")
    
    # 2. Шлейф: тепер копії народжуються яскравими і згасають до прозорості
    new_ghosts = []
    for g in ghosts:
        gx, gy, age = g
        
        gx += 15.0
        age += 1
        
        if age < 25:
            new_ghosts.append([gx, gy, age])
            
            # ІНВЕРСІЯ: При age = 0 колір найяскравіший (видикремлюється), 
            # а з ростом age значення прямує до 0 (зливається з прозорим фоном)
            gray_val = int(max(0, 255 * (1 - (age / 25))))
            color_hex = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"
            
            trail_points = [
                gx, gy,
                gx, gy + 16,
                gx + 4, gy + 12,
                gx + 10, gy + 16,
                gx + 12, gy + 14,
                gx + 6, gy + 10,
                gx + 11, gy + 10
            ]
            canvas.create_polygon(trail_points, fill=color_hex, outline="", tags="trail")
            
    ghosts[:] = new_ghosts
    root.after(20, update_mouse_trail)

root.after(20, update_mouse_trail)
root.mainloop()
