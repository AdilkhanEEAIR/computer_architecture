import math
import sys

import pygame
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective

W, H = 1000, 600


def build_torus(R=1.0, r=0.35, n_major=48, n_minor=24):
    strips = []
    for i in range(n_major):
        strip = []
        for k in (i, i + 1):
            u = 2 * math.pi * k / n_major
            for j in range(n_minor + 1):
                v = 2 * math.pi * j / n_minor
                nx, ny, nz = math.cos(u) * math.cos(v), math.sin(u) * math.cos(v), math.sin(v)
                x = (R + r * math.cos(v)) * math.cos(u)
                y = (R + r * math.cos(v)) * math.sin(u)
                z = r * math.sin(v)
                strip.append(((nx, ny, nz), (x, y, z)))
        half = n_minor + 1
        strips.append([p for pair in zip(strip[:half], strip[half:]) for p in pair])
    return strips


def build_icosahedron():
    t = (1 + 5 ** 0.5) / 2
    v = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
         (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
         (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
         (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
         (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
         (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    tris = []
    for a, b, c in f:
        pa, pb, pc = v[a], v[b], v[c]
        cx, cy, cz = [(pa[i] + pb[i] + pc[i]) / 3 for i in range(3)]
        ln = math.sqrt(cx * cx + cy * cy + cz * cz)
        tris.append(((cx / ln, cy / ln, cz / ln), (pa, pb, pc)))
    return tris


def trefoil(t):
    return (math.sin(t) + 2 * math.sin(2 * t),
            math.cos(t) - 2 * math.cos(2 * t),
            -math.sin(3 * t))


def build_knot(segments=200, sides=16, radius=0.35):
    rings = []
    for i in range(segments + 1):
        t = 2 * math.pi * i / segments
        p = trefoil(t)
        p2 = trefoil(t + 0.001)
        T = [p2[k] - p[k] for k in range(3)]
        lt = math.sqrt(sum(x * x for x in T))
        T = [x / lt for x in T]
        up = (0, 0, 1)
        N = [T[1] * up[2] - T[2] * up[1], T[2] * up[0] - T[0] * up[2], T[0] * up[1] - T[1] * up[0]]
        ln = math.sqrt(sum(x * x for x in N)) or 1
        N = [x / ln for x in N]
        B = [T[1] * N[2] - T[2] * N[1], T[2] * N[0] - T[0] * N[2], T[0] * N[1] - T[1] * N[0]]
        ring = []
        for j in range(sides + 1):
            a = 2 * math.pi * j / sides
            n = [math.cos(a) * N[k] + math.sin(a) * B[k] for k in range(3)]
            ring.append((tuple(n), tuple(p[k] + radius * n[k] for k in range(3))))
        rings.append(ring)
    return rings


def set_material(r, g, b):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (r, g, b, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.8, 0.8, 0.8, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)


def draw_torus(strips):
    for strip in strips:
        glBegin(GL_QUAD_STRIP)
        for n, v in strip:
            glNormal3fv(n)
            glVertex3fv(v)
        glEnd()


def draw_icosahedron(tris):
    glBegin(GL_TRIANGLES)
    for n, verts in tris:
        glNormal3fv(n)
        for v in verts:
            glVertex3fv(v)
    glEnd()


def draw_knot(rings):
    for a, b in zip(rings, rings[1:]):
        glBegin(GL_QUAD_STRIP)
        for (na, va), (nb, vb) in zip(a, b):
            glNormal3fv(na); glVertex3fv(va)
            glNormal3fv(nb); glVertex3fv(vb)
        glEnd()


def init_gl():
    glClearColor(0.08, 0.09, 0.12, 1)
    glEnable(GL_DEPTH_TEST)  
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)  
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_POSITION, (4, 5, 6, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.15, 0.15, 0.2, 1))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, W / H, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)


def main():
    pygame.init()
    pygame.display.set_mode((W, H), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("OpenGL 3D figures — Dzhanteliev EEAIR24  [W wireframe, Space pause]")
    init_gl()

    torus = build_torus()
    ico = build_icosahedron()
    knot = build_knot()

    clock = pygame.time.Clock()
    angle, paused, wire = 0.0, False, False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                paused = not paused
            if e.type == pygame.KEYDOWN and e.key == pygame.K_w:
                wire = not wire
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wire else GL_FILL)

        if not paused:
            angle += 1.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -9)

        glPushMatrix()
        glTranslatef(-3.2, 0, 0)
        glRotatef(angle, 1, 1, 0)
        set_material(0.95, 0.55, 0.15)
        draw_torus(torus)
        glPopMatrix()

        glPushMatrix()
        glRotatef(angle * 0.7, 0, 1, 0.3)
        set_material(0.3, 0.75, 0.45)
        draw_icosahedron(ico)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(3.2, 0, 0)
        glRotatef(angle * 0.8, 0.3, 1, 0)
        glScalef(0.4, 0.4, 0.4)
        set_material(0.35, 0.5, 0.95)
        draw_knot(knot)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
