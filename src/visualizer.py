import numpy as np
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from gradient_descent import cost, grad


class GDVisualizer:      # Vẽ đường cong f(x) và animation các bước gradient descent.

    def __init__(self, interval=700):
        self.fig = Figure(figsize=(4.5, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.interval = interval      # độ trễ giữa 2 frame
        self.anim = None
        self.x = []
        self._setup_axes()

    # ---------- Khung hình tĩnh ----------
    def _setup_axes(self, title=''):
        ax = self.ax
        ax.clear()
        xs = np.linspace(-4.5, 5.5, 400)
        ax.plot(xs, cost(xs), 'b')
        ax.set_xlim(-6, 6)
        ax.set_ylim(-8, 30)
        ax.set_title(title)
        ax.set_xlabel('iter 00/00: cost = 00.00, grad = 0.0000')
        self.seg, = ax.plot([], [], 'k-')                                   # đoạn nối
        self.prev_pt, = ax.plot([], [], 'ko', markersize=8, zorder=3)       # chấm đen
        self.cur_pt, = ax.plot([], [], 'ro', markersize=8, zorder=4)        # chấm đỏ
        self.fig.tight_layout()
        ax.set_xlabel('')

    # ---------- Animation ----------
    def _update(self, i):
        x = self.x
        prev = x[i - 1] if i > 0 else x[0]
        cur = x[i]
        self.seg.set_data([prev, cur], [cost(prev), cost(cur)])
        self.prev_pt.set_data([prev], [cost(prev)])
        self.cur_pt.set_data([cur], [cost(cur)])
        self.ax.set_xlabel('iter %d/%d: cost = %.2f, grad = %.4f'
                           % (i, len(x) - 1, cost(cur), grad(cur)))
        return self.seg, self.prev_pt, self.cur_pt

    def play(self, x, eta, x0):      # Bắt đầu animation cho dãy điểm x (kết quả của myGD1).
        
        self.stop()
        self.x = list(x)
        title = r'$f(x) = x^2 + 5\sin(x)$; $x_0 = %g$; $\eta = %.2f$' % (x0, eta)
        self._setup_axes(title)
        self.anim = FuncAnimation(self.fig, self._update, frames=len(self.x),
                                  interval=self.interval, repeat=False, blit=False)
        self.fig.canvas.draw_idle()

    def stop(self):
        if self.anim is not None:
            if self.anim.event_source is not None:
                self.anim.event_source.stop()
            self.anim = None

    def reset(self):
        self.stop()
        self.x = []
        self._setup_axes()
        self.fig.canvas.draw_idle()

    def save_gif(self, path):    #Lưu animation hiện tại ra GIF (cần: pip install pillow).

        if not self.x:
            raise ValueError('Chưa có dữ liệu, hãy bấm Start trước.')
        self.stop()
        anim = FuncAnimation(self.fig, self._update, frames=len(self.x),
                             interval=self.interval, repeat=False)
        anim.save(path, writer='pillow', fps=max(1, int(1000 / self.interval)))
