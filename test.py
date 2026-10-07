import tkinter as tk

class RoaringKnightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roaring Knight Mouse Trail")
        self.root.geometry("600x600")
        
        # Холст для малювання у стилі темного підземелля
        self.canvas = tk.Canvas(root, bg="#101015", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Масив зсувів [0, -4, -6, -4, 0, 4, 6, 4] (оригінал поділений на 5)
        self.offsets = [0, -4, -6, -4, 0, 4, 6, 4]
        self.index = 0
        
        self.radius = 18
        self.knight_shape = self.canvas.create_oval(
            0, 0, 0, 0, 
            fill="#e74c3c", outline="#ffffff", width=2
        )
        
        # Запуск анімаційного циклу
        self.update_loop()

    def update_loop(self):
        # Безпечне опитування координат миші (без помилок TclError)
        try:
            root_x = self.root.winfo_pointerx()
            root_y = self.root.winfo_pointery()
            win_x = self.root.winfo_rootx()
            win_y = self.root.winfo_rooty()
            cursor_x = root_x - win_x
            cursor_y = root_y - win_y
        except Exception:
            cursor_x, cursor_y = 300, 300

        # Розрахунок позиції з урахуванням масиву зсувів
        current_offset = self.offsets[self.index]
        target_x = cursor_x + current_offset
        target_y = cursor_y + current_offset
        
        # Оновлення координат спрайта
        self.canvas.coords(
            self.knight_shape, 
            target_x - self.radius, target_y - self.radius, 
            target_x + self.radius, target_y + self.radius
        )
        
        # Циклічний перехід по масиву
        self.index = (self.index + 1) % len(self.offsets)
        
        # Наступний кадр через 40 мс
        self.root.after(40, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = RoaringKnightApp(root)
    root.mainloop()
