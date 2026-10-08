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

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg=TRANSPARENT_COLOR, highlightthickness=0)
canvas.pack()

# Канонічна послідовність зсувів
offsets = [-6, -4, 0, 4, 6, 4, 0, -4]
index = 0

ghosts = []
counter = 0

def update_mouse_trail():
    global index, counter
    
    # Точні координати миші відносно вікна
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    
    counter += 1
    # Повільніша поява (кожні 8 кадрів)
    if counter % 8 == 0:
        offset_x = float(x + offsets[index])
        offset_y = float(y + offsets[index])
        ghosts.append([offset_x, offset_y, 0])
        index = (index + 1) % len(offsets)
    
    canvas.delete("trail")
    
    new_ghosts = []
    for g in ghosts:
        gx, gy, age = g
        
        # Рух праворуч і збільшення віку
        gx += 5.0
        age += 1
        
        # Максимальний час життя копії
        if age < 25:
            new_ghosts.append([gx, gy, age])
            
            # ПРАВИЛЬНЕ ЗГАСАННЯ: починає яскравим (255) і з кожним кадром стає темнішим (менш видимим), 
            # поки повністю не зіллється з чорним тлом (0)
            fade = max(0, 255 - (age * 10))
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
