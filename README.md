## **Primary Math Helper "Mathints"**

This application focuses on GCD & LCM computation and common fractions, chosen because mastering  
these fundamentals opens the door to the vast world of exact sciences, and not only...

The app does not cover every aspect of these topics. Instead, it serves as a concise, beginner-level hints  
for pupils and their parent, providing essential rules and computation algorithms.

### **Features**
- Application interactivity is built mainly with Tkinter, while all logic is implemented using standard Python tools.
- Step-by-step guidance for GCD & LCM calculations and common fraction operations.
- For usability of quick demonstrations, a three-mode number randomizer is included: natural, even, and prime.
- Resizable interface with consistent content rendering.
- Lightweight selection menu to navigate between math units while preserving current data.

### **Structure**
- `conductor.py` – launching the app and handling unit selection.
- `mu0.py` – the GCD/LCM math unit.
- `mu1.py` – the Common Fractions math unit.
- `common_ui.py` – building and managing active unit windows.
- `values.py` – constants for texts, settings, and key bindings.

Additional modules handle decomposition, optimization, and internal logic support.

### **Development Helper**
The `_helpDev/` directory contains a small developer-only tool. It is not required at runtime.

### **Running Tests**
>pip install pytest  
>pytest _testing/unit
