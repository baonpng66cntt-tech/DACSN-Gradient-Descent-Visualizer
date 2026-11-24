import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gradient_descent import myGD1, cost
from visualizer import GDVisualizer


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gradient Descent demo: f(x) = x² + 5 sin(x)')

        # ----- khung điều khiển bên trái -----
        ctrl = ttk.Frame(self, padding=10)
        ctrl.grid(row=0, column=0, sticky='ns')

        self.eta_var = tk.StringVar(value='0.1')
        self.x0_var = tk.StringVar(value='-5')
        self.speed_var = tk.StringVar(value='700')

        for r, (text, var) in enumerate([('Learning rate η', self.eta_var),
                                         ('Điểm bắt đầu x₀', self.x0_var),
                                         ('Tốc độ (ms/bước)', self.speed_var)]):
            ttk.Label(ctrl, text=text).grid(row=2 * r, column=0, sticky='w')
            ttk.Entry(ctrl, textvariable=var, width=12).grid(row=2 * r + 1, column=0, pady=(0, 8))

        ttk.Button(ctrl, text='Start', command=self.on_start).grid(row=6, column=0, sticky='ew', pady=2)
        ttk.Button(ctrl, text='Reset', command=self.on_reset).grid(row=7, column=0, sticky='ew', pady=2)
        ttk.Button(ctrl, text='Lưu GIF', command=self.on_save).grid(row=8, column=0, sticky='ew', pady=2)

        self.result_var = tk.StringVar(value='')
        ttk.Label(ctrl, textvariable=self.result_var, wraplength=160, justify='left').grid(
            row=9, column=0, pady=(12, 0), sticky='w')

        # ----- khung hình bên phải -----
        self.viz = GDVisualizer()
        self.canvas = FigureCanvasTkAgg(self.viz.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1)
        self.canvas.draw()

        self.protocol('WM_DELETE_WINDOW', self.on_close)

    def _read_inputs(self):
        try:
            eta = float(self.eta_var.get())
            x0 = float(self.x0_var.get())
            interval = int(float(self.speed_var.get()))
        except ValueError:
            raise ValueError('η, x₀ và tốc độ phải là số.')
        if eta <= 0:
            raise ValueError('η phải > 0.')
        if interval < 50:
            raise ValueError('Tốc độ tối thiểu 50 ms.')
        return eta, x0, interval

    def on_start(self):
        try:
            eta, x0, interval = self._read_inputs()
        except ValueError as e:
            messagebox.showerror('Lỗi nhập liệu', str(e))
            return
        x, it = myGD1(eta, x0)
        self.viz.interval = interval
        self.viz.play(x, eta, x0)
        self.canvas.draw()   # kích hoạt frame đầu tiên
        self.result_var.set('x* = %.6f\ncost = %.6f\n%d vòng lặp' % (x[-1], cost(x[-1]), it))

    def on_reset(self):
        self.viz.reset()
        self.canvas.draw()
        self.result_var.set('')

    def on_save(self):
        path = filedialog.asksaveasfilename(defaultextension='.gif', filetypes=[('GIF', '*.gif')])
        if not path:
            return
        try:
            self.viz.save_gif(path)
            messagebox.showinfo('Xong', 'Đã lưu: ' + path)
        except Exception as e:
            messagebox.showerror('Không lưu được', str(e))

    def on_close(self):
        self.viz.stop()
        self.destroy()


if __name__ == '__main__':
    App().mainloop()
