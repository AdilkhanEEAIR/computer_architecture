import math
import sys

from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import (QBrush, QColor, QFont, QPainter, QPainterPath, QPen,
                           QPolygonF, QRadialGradient)
from PySide6.QtWidgets import QApplication, QWidget


def star_polygon(points: int, r_outer: float, r_inner: float) -> QPolygonF:
    poly = QPolygonF()
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        poly.append(QPointF(r * math.cos(a), r * math.sin(a)))
    return poly


def flower_path(petals: int, radius: float) -> QPainterPath:
    path = QPainterPath()
    for i in range(petals):
        a = 2 * math.pi * i / petals
        tip = QPointF(radius * math.cos(a), radius * math.sin(a))
        spread = math.pi / petals
        c1 = QPointF(radius * 0.9 * math.cos(a - spread), radius * 0.9 * math.sin(a - spread))
        c2 = QPointF(radius * 0.9 * math.cos(a + spread), radius * 0.9 * math.sin(a + spread))
        path.moveTo(0, 0)
        path.cubicTo(c1, tip, tip)
        path.cubicTo(tip, c2, QPointF(0, 0))
    return path


def spirograph_path(R: float, r: float, d: float, scale: float) -> QPainterPath:
    path = QPainterPath()
    turns = int(r / math.gcd(int(R), int(r)))
    steps = 2000
    for i in range(steps + 1):
        t = 2 * math.pi * turns * i / steps
        x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        p = QPointF(x * scale, y * scale)
        if i == 0:
            path.moveTo(p)
        else:
            path.lineTo(p)
    return path


def koch_segment(p1: QPointF, p2: QPointF, depth: int, out: list):
    if depth == 0:
        out.append(p1)
        return
    dx, dy = (p2.x() - p1.x()) / 3, (p2.y() - p1.y()) / 3
    a = QPointF(p1.x() + dx, p1.y() + dy)
    b = QPointF(p1.x() + 2 * dx, p1.y() + 2 * dy)
    ang = -math.pi / 3
    peak = QPointF(a.x() + dx * math.cos(ang) - dy * math.sin(ang),
                   a.y() + dx * math.sin(ang) + dy * math.cos(ang))
    for s, e in ((p1, a), (a, peak), (peak, b), (b, p2)):
        koch_segment(s, e, depth - 1, out)


def koch_snowflake(radius: float, depth: int) -> QPolygonF:
    verts = [QPointF(radius * math.cos(a), radius * math.sin(a))
             for a in (-math.pi / 2, -math.pi / 2 + 2 * math.pi / 3, -math.pi / 2 + 4 * math.pi / 3)]
    pts = []
    for i in range(3):
        koch_segment(verts[i], verts[(i + 1) % 3], depth, pts)
    return QPolygonF(pts)


class FiguresWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt complex figures — Dzhanteliev EEAIR24")
        self.resize(800, 800)
        self.angle = 0.0
        self.star = star_polygon(7, 1.0, 0.45)
        self.flower = flower_path(8, 1.0)
        self.spiro = spirograph_path(8, 5, 5, 1 / 8)
        self.koch = koch_snowflake(1.0, 4)

        timer = QTimer(self)
        timer.timeout.connect(self.tick)
        timer.start(16)  

    def tick(self):
        self.angle = (self.angle + 0.5) % 360
        self.update()

    def draw_cell(self, p: QPainter, col: int, row: int, title: str, draw):
        w, h = self.width() / 2, self.height() / 2
        cx, cy = w * col + w / 2, h * row + h / 2
        size = min(w, h) * 0.38

        p.save()
        p.setPen(QColor("#555"))
        p.setFont(QFont("Arial", 11))
        p.drawText(int(w * col), int(h * row + 8), int(w), 24, Qt.AlignHCenter, title)
        p.translate(cx, cy + 10)
        p.rotate(self.angle if col == row else -self.angle)
        p.scale(size, size)
        draw(p)
        p.restore()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor("#fbfbf8"))

        def pen(color, width=2):
            pn = QPen(QColor(color), width)
            pn.setCosmetic(True)
            return pn

        def draw_star(p):
            g = QRadialGradient(0, 0, 1)
            g.setColorAt(0, QColor("#ffe066"))
            g.setColorAt(1, QColor("#e8590c"))
            p.setBrush(QBrush(g))
            p.setPen(pen("#862e0a"))
            p.drawPolygon(self.star)

        def draw_flower(p):
            p.setBrush(QColor(214, 51, 108, 150))
            p.setPen(pen("#a61e4d"))
            p.drawPath(self.flower)
            p.setBrush(QColor("#fcc419"))
            p.drawEllipse(QPointF(0, 0), 0.15, 0.15)

        def draw_spiro(p):
            p.setBrush(Qt.NoBrush)
            p.setPen(pen("#1971c2", 1.5))
            p.drawPath(self.spiro)

        def draw_koch(p):
            p.setBrush(QColor("#d0ebff"))
            p.setPen(pen("#1864ab", 1.2))
            p.drawPolygon(self.koch)

        self.draw_cell(p, 0, 0, "Star + radial gradient", draw_star)
        self.draw_cell(p, 1, 0, "Bezier-curve flower", draw_flower)
        self.draw_cell(p, 0, 1, "Spirograph (hypotrochoid)", draw_spiro)
        self.draw_cell(p, 1, 1, "Koch snowflake (fractal)", draw_koch)

        p.setPen(QPen(QColor("#ddd"), 1))
        p.drawLine(self.width() // 2, 0, self.width() // 2, self.height())
        p.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
        p.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FiguresWidget()
    w.show()
    sys.exit(app.exec())
