import tkinter as tk
import ctypes
from PIL import Image, ImageTk, ImageDraw

root = tk.Tk()
root.title("RoaringKnight Trail")
root.attributes("-topmost", True)

# Приховуємо стандартний системний курсор у вікні
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

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg=TRANSPARENT_COLOR, highlightthickness=0)
canvas.pack()

# Ваша амплітуда та послідовність зсувів
offsets = [0, 8, 12, 8, 0, -8, -12, -8]
index = 0

ghosts = []
counter = 0

def update_mouse_trail():
    global index, counter
    
    # Координати миші відносно вікна
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    
    counter += 1
    if counter % 4 == 0:
        offset_x = float(x + offsets[index])
        offset_y = float(y + offsets[index])
        ghosts.append([offset_x, offset_y, 0])
        index = (index + 1) % len(offsets)
    
    canvas.delete("trail")
    
    new_ghosts = []
    canvas.images = []
    
    # 1. Малюємо головний чорний курсор у поточній точці траєкторії
    current_offset_x = float(x + offsets[index - 1 if index > 0 else len(offsets) - 1])
    current_offset_y = float(y + offsets[index - 1 if index > 0 else len(offsets) - 1])
    
    img_size = 20
    main_img = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
    main_draw = ImageDraw.Draw(main_img)
    cursor_points = [0, 0, 0, 16, 4, 12, 10, 16, 12, 14, 6, 10, 11, 10]
    
    # Головний курсор — повністю чорний і непрозорий (alpha = 255)
    main_draw.polygon(cursor_points, fill=(0, 0, 0, 255), outline=(255, 255, 255, 255))
    tk_main_img = ImageTk.PhotoImage(main_img)
    canvas.images.append(tk_main_img)
    canvas.create_image(current_offset_x, current_offset_y, image=tk_main_img, anchor="nw", tags="trail")
    
    # 2. Малюємо сліди (гости), що згасають
    for g in ghosts:
        gx, gy, age = g
        
        gx += 15.0
        age += 1
        
        if age < 25:
            new_ghosts.append([gx, gy, age])
            
            # Прозорість сліду (від білого до прозорого)
            alpha = int(max(0, 255 - (age * (255 / 25))))
            
            img = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon(cursor_points, fill=(255, 255, 255, alpha))
            
            tk_img = ImageTk.PhotoImage(img)
            canvas.images.append(tk_img)
            
            canvas.create_image(gx, gy, image=tk_img, anchor="nw", tags="trail")
            
    ghosts[:] = new_ghosts
    root.after(20, update_mouse_trail)

root.after(20, update_mouse_trail)
root.mainloop()
