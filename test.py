import tkinter as tk
import ctypes
from PIL import Image, ImageTk, ImageDraw

root = tk.Tk()
root.title("RoaringKnight Trail")
root.attributes("-topmost", True)

# Приховуємо системний курсор
root.config(cursor="none")

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

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg=TRANSPARENT_COLOR, highlightthickness=0, cursor="none")
canvas.pack()

# Ваша траєкторія з восьми чисел для горизонтального/верховного коливання
offsets = [0, 8, 12, 8, 0, -8, -12, -8]
index = 0

ghosts = []
counter = 0

def update_mouse_trail():
    global index, counter
    
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    
    counter += 1
    if counter % 4 == 0:
        index = (index + 1) % len(offsets)
        # Застосовуємо зсув тільки по горизонталі (або по вертикалі, якщо потрібно), 
        # щоб уникнути хаотичного руху по діагоналі
        offset_x = float(x + offsets[index])
        offset_y = float(y)
        ghosts.append([offset_x, offset_y, 0])

    canvas.delete("trail")
    canvas.images = []
    
    img_size = 25
    cursor_points = [0, 0, 0, 16, 4, 12, 10, 16, 12, 14, 6, 10, 11, 10]
    
    # 1. Головний чорний курсор у поточній точці
    main_img = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
    main_draw = ImageDraw.Draw(main_img)
    main_draw.polygon(cursor_points, fill=(0, 0, 0, 255), outline=(255, 255, 255, 255))
    
    tk_main_img = ImageTk.PhotoImage(main_img)
    canvas.images.append(tk_main_img)
    
    current_x = float(x + offsets[index])
    current_y = float(y)
    canvas.create_image(current_x, current_y, image=tk_main_img, anchor="nw", tags="trail")
    
    # 2. Шлейф із реальним згасанням (прозорістю)
    new_ghosts = []
    for g in ghosts:
        gx, gy, age = g
        
        # Рух праворуч
        gx += 15.0
        age += 1
        
        if age < 25:
            new_ghosts.append([gx, gy, age])
            
            # Справжня прозорості (alpha): від 255 (видимий) до 0 (повністю прозорий)
            alpha = int(max(0, 255 * (1 - (age / 25))))
            
            ghost_img = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
            ghost_draw = ImageDraw.Draw(ghost_img)
            # Малюємо чорний курсор із затухаючою прозорістю
            ghost_draw.polygon(cursor_points, fill=(0, 0, 0, alpha), outline=(255, 255, 255, int(alpha * 0.8)))
            
            tk_ghost_img = ImageTk.PhotoImage(ghost_img)
            canvas.images.append(tk_ghost_img)
            
            canvas.create_image(gx, gy, image=tk_ghost_img, anchor="nw", tags="trail")
            
    ghosts[:] = new_ghosts
    root.after(20, update_mouse_trail)

root.after(20, update_mouse_trail)
root.mainloop()
