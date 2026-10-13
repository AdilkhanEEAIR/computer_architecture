# Computer Architecture and Operating System

Homework on graphical libraries.

**Student:** Adilkhan Dzhanteliev, group EEAIR24
**University:** Ala-Too International University

## Assignment

1. Use the graphical libraries that come pre-installed with programming languages to build a window with text, buttons and input fields.
2. Draw complex figures with libraries like Qt, OpenGL or Vulkan.

From the board:

| Language | Built-in GUI library |
|----------|----------------------|
| Python   | Tk (tkinter)         |
| Java     | Swing                |
| Frontend | HTML tags            |

## Files

| File | Task | What it does |
|------|------|--------------|
| `task1_python_tk.py` | 1 | Student form in Tkinter: labels, two input fields, radio buttons, Submit and Clear |
| `Task1Swing.java` | 1 | The same form in Java Swing, with a drop-down list instead of radio buttons |
| `task1_frontend.html` | 1 | The same form built from HTML tags, runs in any browser |
| `task2_qt_figures.py` | 2 | Four rotating 2D figures drawn with Qt (QPainter) |
| `task2_opengl.py` | 2 | Three lit 3D objects rendered with OpenGL |

All three forms in task 1 do the same thing, so it is easy to compare how each library handles the same UI.

### Task 2 figures

**Qt (`task2_qt_figures.py`)**

- Seven-point star with a radial gradient fill
- Flower made of cubic Bezier curves
- Spirograph (hypotrochoid), a parametric curve
- Koch snowflake, a fractal built by recursion (depth 4)

**OpenGL (`task2_opengl.py`)**

- Torus, built from quad strips with normals computed by hand
- Icosahedron with flat shading
- Trefoil knot: a tube swept along a 3D curve

The scene uses one light source, a depth buffer and smooth shading.

| Key   | Action |
|-------|--------|
| W     | Switch between wireframe and solid |
| Space | Pause rotation |
| Esc   | Quit |

## Requirements

- Python 3.10 or newer (tkinter is included)
- JDK 17 or newer
- Any modern browser
- For task 2: PySide6, PyOpenGL, pygame-ce

```powershell
pip install PySide6 PyOpenGL pygame-ce
```

## How to run

```powershell
# Task 1
python task1_python_tk.py
javac Task1Swing.java
java Task1Swing
start task1_frontend.html

# Task 2
python task2_qt_figures.py
python task2_opengl.py
```

## Troubleshooting

**pygame fails to install.** The original `pygame` package has no ready build for new Python versions, so pip tries to compile it and fails. Use `pygame-ce` instead. It is a maintained fork and is imported the same way (`import pygame`).

**`DLL load failed while importing QtCore` on Anaconda / Miniforge.** The conda environment has older system DLLs than the ones PySide6 from pip expects. Install PySide6 from conda-forge instead:

```powershell
pip uninstall -y PySide6 PySide6_Essentials PySide6_Addons shiboken6
conda install -c conda-forge pyside6 -y
```

## Why there is no Vulkan example

Vulkan is a low-level API. Even a single triangle needs around a thousand lines: instance, device, swapchain, render pass, pipeline and shaders compiled to SPIR-V. The assignment says "like Qt, OpenGL, Vulkan", so Qt and OpenGL cover it. The main difference is that in Vulkan the programmer manages GPU memory and synchronization directly, while OpenGL does it inside the driver.
