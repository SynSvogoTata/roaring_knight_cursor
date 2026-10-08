import tkinter as tk

root = tk.Tk()
root.attributes("-alpha", 0.9)
root.overrideredirect(True)
root.attributes("-topmost", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

TRANSPARENT_COLOR = "black"
root.config(bg=TRANSPARENT_COLOR)
root.attributes("-transparentcolor", TRANSPARENT_COLOR)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg=TRANSPARENT_COLOR, highlightthickness=0)
canvas.pack()

# Ваш циклический масив зсувів
offsets = [0, -4, -6, -4, 0, 4, 6, 4]
index = 0

# Список для збереження копій курсорів [x, y, "вік" (для згасання)]
ghosts = []

def update_mouse_trail():
    global index
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    
    # Додаємо нову копію курсора з урахуванням зсуву
    offset_x = float(x + offsets[index])
    offset_y = float(y + offsets[index])
    ghosts.append([offset_x, offset_y, 0])
    
    index = (index + 1) % len(offsets)
    
    # Очищуємо попередній кадр малювання
    canvas.delete("trail")
    
    new_ghosts = []
    for g in ghosts:
        gx, gy, age = g
        
        # Зміщуємо копію курсора праворуч і збільшуємо "вік"
        gx += 2.5
        age += 1
        
        # Поки курсор "живе" (менше 18 кадрів)
        if age < 18:
            new_ghosts.append([gx, gy, age])
            
            # Імітуємо згасання: змінюємо колір від білого до темнішого сірого
            color_val = int(255 - (age * 12))
            if color_val < 30: 
                color_val = 30
            color_hex = f"#{color_val:02x}{color_val:02x}{color_val:02x}"
            
            # Малюємо класичну форму стрілочки курсора
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
    
    # Повторюємо кожні 20 мс
    root.after(20, update_mouse_trail)

root.after(20, update_mouse_trail)
root.mainloop()
