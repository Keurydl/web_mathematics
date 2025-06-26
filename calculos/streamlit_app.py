import streamlit as st
import re
import numpy as np

# Verificar e importar bibliotecas con manejo de errores
MATPLOTLIB_AVAILABLE = False
SCIPY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    pass

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    pass

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="centered", page_title="Calculadora Científica", page_icon="🧮")

# --- DICCIONARIO DE SECCIONES ---
sections = {
    'Aritmética': '➕',
    'Química': '🧪',
    'Física': '🔬',
    'Geometría': '📐',
    'Estadística': '📊',
    'Matemática Avanzada': '🔢',
}

# --- BARRA LATERAL DE NAVEGACIÓN ---
with st.sidebar:
    st.title("Menú de Calculadoras")
    # Elige la sección por defecto como 'Química'
    if 'selected_section' not in st.session_state:
        st.session_state.selected_section = 'Química'

    selected_section = st.radio(
        "Elige una sección:",
        list(sections.keys()),
        format_func=lambda x: f"{sections[x]} {x}",
        key='selected_section'
    )
    st.markdown("---")
    st.info("Esta es una aplicación de calculadoras interactiva. Para ver la web principal con toda la teoría, [haz clic aquí](http://127.0.0.1:8000/) ")

# --- CONTENIDO PRINCIPAL ---

# --- SECCIÓN DE ARITMÉTICA (CALCULADORA BÁSICA) ---
if selected_section == "Aritmética":
    st.title(f"{sections[selected_section]} {selected_section}")

    # --- Estado de la Calculadora ---
    if 'expression' not in st.session_state:
        st.session_state.expression = ""
    if 'history' not in st.session_state:
        st.session_state.history = []

    # --- Lógica de la Calculadora (Callbacks) ---
    def append_to_expression(value):
        st.session_state.expression += str(value)

    def calculate_expression():
        # Sanitizar la expresión justo antes de evaluarla para seguridad
        expr_to_eval = st.session_state.get("expression", "")
        allowed_chars = "0123456789.+-*/()"
        sanitized_expr = "".join(c for c in expr_to_eval if c in allowed_chars)
        
        if not sanitized_expr:
            return

        try:
            result = eval(sanitized_expr, {"__builtins__": {}})
            st.session_state.history.insert(0, f"{sanitized_expr} = {result}")
            st.session_state.expression = str(result)
        except Exception:
            st.session_state.expression = "Error"

    def clear_expression():
        st.session_state.expression = ""

    def backspace_expression():
        current_expr = st.session_state.get("expression", "")
        st.session_state.expression = current_expr[:-1]

    # --- Interfaz de la Calculadora ---
    st.text_input("Expression", key="expression", label_visibility="collapsed")

    col1, col2, col3, col4 = st.columns(4)
    ops = {'÷': '/', '×': '*', '−': '-', '+': '+'}

    # Usar on_click para modificar el estado antes de que la app se redibuje
    with col1:
        st.button("7", use_container_width=True, on_click=append_to_expression, args=("7",))
        st.button("4", use_container_width=True, on_click=append_to_expression, args=("4",))
        st.button("1", use_container_width=True, on_click=append_to_expression, args=("1",))
        st.button("0", use_container_width=True, on_click=append_to_expression, args=("0",))

    with col2:
        st.button("8", use_container_width=True, on_click=append_to_expression, args=("8",))
        st.button("5", use_container_width=True, on_click=append_to_expression, args=("5",))
        st.button("2", use_container_width=True, on_click=append_to_expression, args=("2",))
        st.button(".", use_container_width=True, on_click=append_to_expression, args=(".",))

    with col3:
        st.button("9", use_container_width=True, on_click=append_to_expression, args=("9",))
        st.button("6", use_container_width=True, on_click=append_to_expression, args=("6",))
        st.button("3", use_container_width=True, on_click=append_to_expression, args=("3",))
        st.button("=", use_container_width=True, type="primary", on_click=calculate_expression)

    with col4:
        st.button("÷", use_container_width=True, on_click=append_to_expression, args=(ops['÷'],))
        st.button("×", use_container_width=True, on_click=append_to_expression, args=(ops['×'],))
        st.button("−", use_container_width=True, on_click=append_to_expression, args=(ops['−'],))
        st.button("(+)", use_container_width=True, on_click=append_to_expression, args=(ops['+'],))

    control_col1, control_col2 = st.columns(2)
    with control_col1:
        st.button("C (Limpiar)", use_container_width=True, on_click=clear_expression)
    with control_col2:
        st.button("← (Borrar)", use_container_width=True, on_click=backspace_expression)

    st.markdown("### Historial")
    if st.session_state.history:
        st.text_area("History", "\n".join(st.session_state.history), height=200, key="history_display", disabled=True, label_visibility="collapsed")

# --- SECCIÓN DE NÚMEROS COMPLEJOS ---
elif selected_section == "Matemática Avanzada":
    st.title(f"{sections[selected_section]} {selected_section}")
    st.write("Herramientas para operaciones con números complejos, incluyendo el Teorema de De Moivre.")

    # --- Calculadora de Números Complejos ---
    st.header("Calculadora de Números Complejos")
    st.write("Introduce los números complejos en formato 'a+bj' (ej: 3+4j, 2-1j, 5j, -2.5+1.7j)")

    # Selección de operación
    operation = st.selectbox(
        "Selecciona una operación:",
        ["Suma", "Resta", "Multiplicación", "División", "Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"],
        key="complex_operation"
    )

    col1, col2 = st.columns(2)
    
    with col1:
        z1_str = st.text_input("Número Complejo z1:", value="1+2j", key="z1_input")
    
    with col2:
        if operation not in ["Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"]:
            z2_str = st.text_input("Número Complejo z2:", value="3-4j", key="z2_input")
        elif operation == "Potencia (De Moivre)":
            n_power = st.number_input("Exponente (n):", value=2, step=1, key="power_input")
        else:  # Raíz n-ésima
            n_root = st.number_input("Índice de la raíz (n):", value=2, min_value=1, step=1, key="root_input")

    # Función para validar y convertir números complejos
    def parse_complex(c_str):
        try:
            # Evaluar la cadena como una expresión compleja de Python
            c = complex(c_str)
            return c
        except (ValueError, SyntaxError):
            st.error(f"Formato inválido para el número complejo: {c_str}. Usa el formato 'a+bj' o 'a-bj'")
            return None

    # Función para mostrar un número complejo en formato legible
    def format_complex(z):
        if z.imag == 0:
            return f"{z.real:.2f}"
        elif z.real == 0:
            return f"{z.imag:.2f}j"
        else:
            return f"{z.real:.2f} {'+' if z.imag >= 0 else '-'} {abs(z.imag):.2f}j"

    # Función para convertir a forma polar
    def to_polar(z):
        r = abs(z)
        theta = np.angle(z, deg=True)
        return r, theta

    # Procesar la operación seleccionada
    if st.button("Calcular"):
        z1 = parse_complex(z1_str)
        if z1 is None:
            st.stop()
            
        if operation not in ["Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"]:
            z2 = parse_complex(z2_str)
            if z2 is None:
                st.stop()
        
        # Realizar la operación seleccionada
        if operation == "Suma":
            result = z1 + z2
            st.success(f"**Resultado:** {format_complex(z1)} + {format_complex(z2)} = {format_complex(result)}")
            
        elif operation == "Resta":
            result = z1 - z2
            st.success(f"**Resultado:** {format_complex(z1)} - {format_complex(z2)} = {format_complex(result)}")
            
        elif operation == "Multiplicación":
            result = z1 * z2
            st.success(f"**Resultado:** {format_complex(z1)} × {format_complex(z2)} = {format_complex(result)}")
            
        elif operation == "División":
            if z2 == 0:
                st.error("Error: No se puede dividir por cero")
            else:
                result = z1 / z2
                st.success(f"**Resultado:** {format_complex(z1)} / {format_complex(z2)} = {format_complex(result)}")
                
        elif operation == "Potencia (De Moivre)":
            r, theta = to_polar(z1)
            result = (r ** n_power) * (np.cos(np.radians(theta * n_power)) + 1j * np.sin(np.radians(theta * n_power)))
            st.success(f"**Teorema de De Moivre:** (r∠θ)ⁿ = rⁿ(cos(nθ) + j·sin(nθ))")
            st.success(f"**Resultado:** ({r:.2f}∠{theta:.2f}°)^{n_power} = {format_complex(result)}")
            
        elif operation == "Raíz n-ésima (De Moivre)":
            if n_root < 1:
                st.error("El índice de la raíz debe ser un entero positivo")
            else:
                r, theta = to_polar(z1)
                roots = []
                for k in range(n_root):
                    root_r = r ** (1/n_root)
                    root_theta = (theta + 360 * k) / n_root
                    root = root_r * (np.cos(np.radians(root_theta)) + 1j * np.sin(np.radians(root_theta)))
                    roots.append(root)
                
                st.success(f"**Teorema de De Moivre para raíces:** ⁰√(r∠θ) = ⁰√r ∠ (θ + 360°k)/n para k = 0, 1, ..., n-1")
                st.success(f"**Raíces {n_root}-ésimas de {format_complex(z1)}:**")
                for i, root in enumerate(roots):
                    st.write(f"- Raíz {i+1}: {format_complex(root)}")
        
        # Mostrar información adicional en formato polar
        with st.expander("Ver en formato polar"):
            if operation in ["Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"]:
                r, theta = to_polar(z1)
                st.write(f"**z₁ en forma polar:** {r:.4f} ∠ {theta:.2f}°")
                if operation == "Potencia (De Moivre)":
                    st.write(f"**z₁^{n_power} en forma polar:** {r**n_power:.4f} ∠ {theta*n_power:.2f}°")
            else:
                r1, theta1 = to_polar(z1)
                r2, theta2 = to_polar(z2)
                st.write(f"**z₁ en forma polar:** {r1:.4f} ∠ {theta1:.2f}°")
                st.write(f"**z₂ en forma polar:** {r2:.4f} ∠ {theta2:.2f}°")
                
                if operation in ["Multiplicación", "División"]:
                    if operation == "Multiplicación":
                        r_res = r1 * r2
                        theta_res = theta1 + theta2
                    else:  # División
                        r_res = r1 / r2
                        theta_res = theta1 - theta2
                    
                    # Normalizar el ángulo entre -180° y 180°
                    while theta_res > 180:
                        theta_res -= 360
                    while theta_res <= -180:
                        theta_res += 360
                        
                    st.write(f"**Resultado en forma polar:** {r_res:.4f} ∠ {theta_res:.2f}°")

    # --- Teoría sobre Números Complejos ---
    with st.expander("📚 Teoría: Números Complejos"):
        st.markdown("""
        ### Números Complejos
        Los números complejos son una extensión de los números reales que incluyen una parte imaginaria (con la unidad imaginaria j, donde j² = -1).
        
        **Forma rectangular:** z = a + bj
        - a: Parte real
        - b: Parte imaginaria
        - j: Unidad imaginaria (j² = -1)
        
        **Forma polar:** z = r(cosθ + j·sinθ) = r∠θ
        - r: Módulo (distancia al origen)
        - θ: Argumento (ángulo con el eje real positivo, en grados)
        
        ### Operaciones Básicas
        - **Suma/Resta:** Se suman/restan las partes reales e imaginarias por separado
        - **Multiplicación/División:** Más fáciles en forma polar (se multiplican/dividen los módulos y se suman/restan los argumentos)
        
        ### Teorema de De Moivre
        Para cualquier número complejo z = r(cosθ + j·sinθ) y número entero n:
        
        **Potencia:** zⁿ = rⁿ(cos(nθ) + j·sin(nθ))
        
        **Raíz n-ésima:** Para k = 0, 1, ..., n-1:
        z^(1/n) = r^(1/n) [cos((θ + 360°k)/n) + j·sin((θ + 360°k)/n)]
        
        Las raíces n-ésimas de un número complejo forman un polígono regular de n lados en el plano complejo.
        """)

# --- SECCIÓN DE QUÍMICA ---
elif selected_section == "Química":
    st.title(f"{sections[selected_section]} {selected_section}")
    st.info("Herramientas para cálculos de estequiometría, soluciones y termoquímica.")

    # --- Función Auxiliar para convertir texto a float ---
    def get_float_from_text(text_value, label):
        if not text_value:
            return None
        try:
            # Reemplazar coma por punto para la conversión
            return float(text_value.replace(',', '.'))
        except ValueError:
            st.warning(f"Por favor, introduce un número válido para '{label}'.")
            return None

    # --- Calculadora de Masa Molar ---
    st.subheader("Calculadora de Masa Molar")
    atomic_masses = {
        'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180, 'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'K': 39.098, 'Ar': 39.948, 'Ca': 40.078, 'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Ni': 58.693, 'Co': 58.933, 'Cu': 63.546, 'Zn': 65.38, 'Ga': 69.723, 'Ge': 72.630, 'As': 74.922, 'Se': 78.971, 'Br': 79.904, 'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224, 'Nb': 92.906, 'Mo': 95.96, 'Tc': 98.0, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41, 'In': 114.82, 'Sn': 118.71, 'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91, 'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24, 'Pm': 145.0, 'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93, 'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93, 'Yb': 173.05, 'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95, 'W': 183.84, 'Re': 186.21, 'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59, 'Tl': 204.38, 'Pb': 207.2, 'Bi': 208.98, 'Po': 209.0, 'At': 210.0, 'Rn': 222.0, 'Fr': 223.0, 'Ra': 226.0, 'Ac': 227.0, 'Th': 232.04, 'Pa': 231.04, 'U': 238.03, 'Np': 237.0, 'Pu': 244.0, 'Am': 243.0, 'Cm': 247.0, 'Bk': 247.0, 'Cf': 251.0, 'Es': 252.0, 'Fm': 257.0, 'Md': 258.0, 'No': 259.0, 'Lr': 262.0, 'Rf': 267.0, 'Db': 268.0, 'Sg': 271.0, 'Bh': 270.0, 'Hs': 277.0, 'Mt': 276.0, 'Ds': 281.0, 'Rg': 280.0, 'Cn': 285.0, 'Nh': 284.0, 'Fl': 289.0, 'Mc': 288.0, 'Lv': 293.0, 'Ts': 294.0, 'Og': 294.0
    }
    formula = st.text_input("Introduce la fórmula química (ej. H2O, C6H12O6):", "H2O", key="formula_input")
    if formula:
        try:
            tokens = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
            if not tokens:
                st.warning("Por favor, introduce una fórmula válida.")
            else:
                total_mass = 0
                calculation_str = []
                valid_formula = True
                for element, count in tokens:
                    if element in atomic_masses:
                        atom_count = int(count) if count else 1
                        mass = atomic_masses[element]
                        total_mass += mass * atom_count
                        calculation_str.append(f"{element}: {atom_count} × {mass} g/mol")
                    else:
                        st.error(f"Elemento '{element}' no encontrado.")
                        valid_formula = False
                        break
                if valid_formula:
                    st.success(f"**Masa Molar de {formula}:** `{total_mass:.4f} g/mol`")
                    with st.expander("Ver desglose del cálculo"):
                        for item in calculation_str:
                            st.write(item)
        except Exception as e:
            st.error(f"Error al procesar la fórmula: {e}")

    # --- Calculadora de Densidad ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Calculadora de Densidad")
    col1, col2 = st.columns(2)
    with col1:
        mass_density_str = st.text_input("Masa (g)", key="mass_density_str", value="0")
    with col2:
        volume_density_str = st.text_input("Volumen (mL)", key="volume_density_str", value="1")
    
    if st.button("Calcular Densidad", key="density_button"):
        mass_density = get_float_from_text(mass_density_str, "Masa")
        volume_density = get_float_from_text(volume_density_str, "Volumen")
        
        if mass_density is not None and volume_density is not None:
            if volume_density == 0:
                st.error("El volumen no puede ser cero.")
            else:
                density = mass_density / volume_density
                st.success(f"**Densidad:** `{density:.4f} g/mL`")

    # --- Calculadora de Calor Específico (q = mcΔT) ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Calculadora de Calor Específico (q = mcΔT)")
    col1, col2, col3 = st.columns(3)
    with col1:
        mass_q_str = st.text_input("Masa (g)", key="mass_q_str", value="0")
    with col2:
        c_str = st.text_input("Calor Específico (J/g°C)", key="c_str", value="4.184", help="Agua: 4.184 J/g°C")
    with col3:
        delta_t_str = st.text_input("ΔT (°C)", key="delta_t_str", value="0")

    if st.button("Calcular Calor (q)", key="heat_button"):
        mass_q = get_float_from_text(mass_q_str, "Masa")
        c = get_float_from_text(c_str, "Calor Específico")
        delta_t = get_float_from_text(delta_t_str, "ΔT")

        if all(v is not None for v in [mass_q, c, delta_t]):
            q = mass_q * c * delta_t
            st.success(f"**Calor (q):** `{q:.4f} Joules`")

    # --- Calculadora de Molaridad ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Calculadora de Molaridad")
    col1, col2 = st.columns(2)
    with col1:
        moles_molarity_str = st.text_input("Moles de soluto (mol)", key="moles_molarity_str", value="0")
    with col2:
        liters_molarity_str = st.text_input("Litros de solución (L)", key="liters_molarity_str", value="1")

    if st.button("Calcular Molaridad", key="molarity_button"):
        moles_molarity = get_float_from_text(moles_molarity_str, "Moles de soluto")
        liters_molarity = get_float_from_text(liters_molarity_str, "Litros de solución")

        if moles_molarity is not None and liters_molarity is not None:
            if liters_molarity == 0:
                st.error("El volumen de la solución no puede ser cero.")
            else:
                molarity = moles_molarity / liters_molarity
                st.success(f"**Molaridad:** `{molarity:.4f} M`")

# --- SECCIÓN DE FÍSICA ---
elif selected_section == "Física":
    st.title(f"{sections[selected_section]} {selected_section}")
    st.info("Herramientas para cálculos de mecánica clásica, incluyendo MRU, MRUA, leyes de Newton y energía.")
    
    # Pestañas para organizar las diferentes calculadoras de Física
    tab_mru, tab_mrua, tab_newton, tab_energia = st.tabs(["MRU", "MRUA", "Leyes de Newton", "Energía"])
    
    with tab_mru:
        st.header("Movimiento Rectilíneo Uniforme (MRU)")
        st.markdown("""
        El **Movimiento Rectilíneo Uniforme (MRU)** es un movimiento en línea recta con velocidad constante.
        
        **Fórmula principal:** \( d = v \cdot t \)
        - \( d \): distancia recorrida (m)
        - \( v \): velocidad (m/s)
        - \( t \): tiempo (s)
        """)
        
        # Selector de incógnita
        incognita = st.radio("¿Qué quieres calcular?", ["Distancia (d)", "Velocidad (v)", "Tiempo (t)"], horizontal=True)
        
        col1, col2 = st.columns(2)
        
        if incognita == "Distancia (d)":
            with col1:
                v = st.number_input("Velocidad (m/s)", min_value=0.0, value=10.0, step=0.1, format="%.2f")
                t = st.number_input("Tiempo (s)", min_value=0.0, value=5.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Distancia"):
                d = v * t
                st.success(f"La distancia recorrida es: **{d:.2f} metros**")
                
                # Mostrar fórmula aplicada
                st.latex(fr"d = v \cdot t = {v:.2f} \, \text{{m/s}} \cdot {t:.2f} \, \text{{s}} = {d:.2f} \, \text{{m}}")
        
        elif incognita == "Velocidad (v)":
            with col1:
                d = st.number_input("Distancia (m)", min_value=0.0, value=50.0, step=0.1, format="%.2f")
                t = st.number_input("Tiempo (s)", min_value=0.0, value=5.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Velocidad"):
                if t > 0:
                    v = d / t
                    st.success(f"La velocidad es: **{v:.2f} m/s**")
                    st.latex(fr"v = \frac{{d}}{{t}} = \frac{{{d:.2f} \, \text{{m}}}}{{{t:.2f} \, \text{{s}}}} = {v:.2f} \, \text{{m/s}}")
                else:
                    st.error("El tiempo debe ser mayor que cero.")
        
        elif incognita == "Tiempo (t)":
            with col1:
                d = st.number_input("Distancia (m)", min_value=0.0, value=50.0, step=0.1, format="%.2f")
                v = st.number_input("Velocidad (m/s)", min_value=0.0, value=10.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Tiempo"):
                if v > 0:
                    t = d / v
                    st.success(f"El tiempo transcurrido es: **{t:.2f} segundos**")
                    st.latex(fr"t = \frac{{d}}{{v}} = \frac{{{d:.2f} \, \text{{m}}}}{{{v:.2f} \, \text{{m/s}}}} = {t:.2f} \, \text{{s}}")
                else:
                    st.error("La velocidad debe ser mayor que cero.")
        
        # Sección de gráfica
        if 'v' in locals() and 't' in locals() and v > 0 and t > 0:
            st.subheader("Gráfica de Posición vs Tiempo")
            
            if not MATPLOTLIB_AVAILABLE:
                st.warning(
                    "La generación de gráficos requiere la biblioteca matplotlib. "
                    "Por favor, instálala ejecutando: `pip install matplotlib`"
                )
            else:
                try:
                    # Crear datos para la gráfica
                    tiempo = np.linspace(0, t * 1.5, 100)
                    posicion = v * tiempo
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(tiempo, posicion, 'b-', linewidth=2, label=f'v = {v} m/s')
                    ax.set_xlabel('Tiempo (s)')
                    ax.set_ylabel('Posición (m)')
                    ax.set_title('Gráfica de Posición vs Tiempo (MRU)')
                    ax.grid(True, linestyle='--', alpha=0.7)
                    ax.legend()
                    
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error al generar la gráfica: {str(e)}")
    
    # Sección de MRUA
    with tab_mrua:
        st.header("Movimiento Rectilíneo Uniformemente Acelerado (MRUA)")
        st.markdown("""
        El **Movimiento Rectilíneo Uniformemente Acelerado (MRUA)** es un movimiento en línea recta con aceleración constante.

        **Fórmulas principales:**
        - Velocidad final: \\( v = v_0 + a \\cdot t \\)
        - Posición: \\( x = x_0 + v_0 t + \\frac{1}{2} a t^2 \\)
        - Sin tiempo: \\( v^2 = v_0^2 + 2a\\Delta x \\)
        """)

        # Selector de escenario
        escenario = st.radio("Seleccione un escenario:", 
                           ["General", "Caída libre", "Tiro vertical"], 
                           horizontal=True)

        # Selector de incógnita
        incognita = st.radio("¿Qué quieres calcular?", 
                           ["Velocidad final (v)", "Posición final (x)", "Tiempo (t)", "Aceleración (a)"], 
                           horizontal=True)

        col1, col2 = st.columns(2)
        
        # Valores iniciales según el escenario
        if escenario == "Caída libre":
            a = -9.81  # m/s² (hacia abajo)
            st.info("Considerando aceleración de gravedad: -9.81 m/s² (hacia abajo)")
        elif escenario == "Tiro vertical":
            a = 9.81  # m/s² (hacia arriba)
            st.info("Considerando aceleración de gravedad: 9.81 m/s² (hacia arriba)")
        
        # Inicializar variables
        v0 = x0 = t = v = x = 0.0
        
        # Campos de entrada según la incógnita
        with col1:
            if incognita != "Velocidad final (v)":
                v0 = st.number_input("Velocidad inicial (m/s)", value=0.0, step=0.1, format="%.2f")
            
            if incognita != "Posición final (x)":
                x0 = st.number_input("Posición inicial (m)", value=0.0, step=0.1, format="%.2f")
            
            if incognita != "Tiempo (t)":
                t = st.number_input("Tiempo (s)", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            if incognita != "Aceleración (a)" and escenario == "General":
                a = st.number_input("Aceleración (m/s²)", value=0.0, step=0.1, format="%.2f")
            
            if incognita == "Velocidad final (v)":
                v = st.number_input("Velocidad final (m/s)", value=0.0, step=0.1, format="%.2f")
            
            if incognita == "Posición final (x)":
                x = st.number_input("Posición final (m)", value=0.0, step=0.1, format="%.2f")

        # Cálculos
        if st.button("Calcular"):
            try:
                if incognita == "Velocidad final (v)":
                    # v = v0 + a*t
                    v = v0 + a * t
                    st.success(f"La velocidad final es: **{v:.2f} m/s**")
                    st.latex(fr"v = v_0 + a \\cdot t = {v0:.2f} + ({a:.2f}) \\cdot {t:.2f} = {v:.2f} \\, \\text{{m/s}}")
                
                elif incognita == "Posición final (x)":
                    # x = x0 + v0*t + 0.5*a*t^2
                    x = x0 + v0 * t + 0.5 * a * t**2
                    st.success(f"La posición final es: **{x:.2f} metros**")
                    st.latex(fr"x = x_0 + v_0 t + \\frac{{1}}{{2}} a t^2 = {x0:.2f} + {v0:.2f} \\cdot {t:.2f} + 0.5 \\cdot {a:.2f} \\cdot {t:.2f}^2 = {x:.2f} \\, \\text{{m}}")
                
                elif incognita == "Tiempo (t)":
                    # Resuelve t de v = v0 + a*t
                    if a != 0:
                        t = (v - v0) / a
                        if t >= 0:
                            st.success(f"El tiempo transcurrido es: **{t:.2f} segundos**")
                            st.latex(fr"t = \\frac{{v - v_0}}{{a}} = \\frac{{{v:.2f} - {v0:.2f}}}{{{a:.2f}}} = {t:.2f} \\, \\text{{s}}")
                        else:
                            st.error("El tiempo no puede ser negativo. Verifica los valores de velocidad y aceleración.")
                    else:
                        st.error("La aceleración no puede ser cero para calcular el tiempo.")
                
                elif incognita == "Aceleración (a)":
                    # Resuelve a de v = v0 + a*t
                    if t > 0:
                        a = (v - v0) / t
                        st.success(f"La aceleración es: **{a:.2f} m/s²**")
                        st.latex(fr"a = \\frac{{v - v_0}}{{t}} = \\frac{{{v:.2f} - {v0:.2f}}}{{{t:.2f}}} = {a:.2f} \\, \\text{{m/s}}^2")
                    else:
                        st.error("El tiempo debe ser mayor que cero.")

                # Gráficas si matplotlib está disponible
                if MATPLOTLIB_AVAILABLE and 't' in locals() and t > 0:
                    st.subheader("Gráficas de Movimiento")
                    
                    # Crear datos para las gráficas
                    tiempo_graf = np.linspace(0, t * 1.5, 100)
                    
                    # Gráfica de posición vs tiempo
                    fig_pos, ax_pos = plt.subplots(figsize=(10, 4))
                    posicion = x0 + v0 * tiempo_graf + 0.5 * a * tiempo_graf**2
                    ax_pos.plot(tiempo_graf, posicion, 'b-', linewidth=2)
                    ax_pos.set_xlabel('Tiempo (s)')
                    ax_pos.set_ylabel('Posición (m)')
                    ax_pos.set_title('Posición vs Tiempo')
                    ax_pos.grid(True, linestyle='--', alpha=0.7)
                    st.pyplot(fig_pos)
                    
                    # Gráfica de velocidad vs tiempo
                    fig_vel, ax_vel = plt.subplots(figsize=(10, 4))
                    velocidad = v0 + a * tiempo_graf
                    ax_vel.plot(tiempo_graf, velocidad, 'r-', linewidth=2)
                    ax_vel.set_xlabel('Tiempo (s)')
                    ax_vel.set_ylabel('Velocidad (m/s)')
                    ax_vel.set_title('Velocidad vs Tiempo')
                    ax_vel.grid(True, linestyle='--', alpha=0.7)
                    st.pyplot(fig_vel)
                    
                    # Gráfica de aceleración vs tiempo
                    fig_acc, ax_acc = plt.subplots(figsize=(10, 4))
                    aceleracion = np.full_like(tiempo_graf, a)
                    ax_acc.plot(tiempo_graf, aceleracion, 'g-', linewidth=2)
                    ax_acc.set_xlabel('Tiempo (s)')
                    ax_acc.set_ylabel('Aceleración (m/s²)')
                    ax_acc.set_title('Aceleración vs Tiempo')
                    ax_acc.grid(True, linestyle='--', alpha=0.7)
                    st.pyplot(fig_acc)
                    
            except Exception as e:
                st.error(f"Error en el cálculo: {str(e)}")
        else:
            if not MATPLOTLIB_AVAILABLE:
                st.warning(
                    "La generación de gráficos requiere la biblioteca matplotlib. "
                    "Por favor, instálala ejecutando: `pip install matplotlib`"
                )
    
    # Sección de Leyes de Newton
    with tab_newton:
        st.header("Leyes de Newton")
        
        # Pestañas para cada ley
        tab1, tab2, tab3 = st.tabs(["Primera Ley", "Segunda Ley", "Tercera Ley"])
        
        with tab1:
            st.subheader("Primera Ley de Newton (Ley de Inercia)")
            st.markdown("""
            > *"Todo cuerpo permanece en su estado de reposo o de movimiento rectilíneo uniforme 
            > a menos que otros cuerpos actúen sobre él."*
            
            **Concepto clave:** La inercia es la resistencia que opone un cuerpo a cambiar su estado de movimiento.
            
            ### Ejemplos prácticos:
            - Los pasajeros de un autobús se inclinan hacia adelante cuando frena bruscamente.
            - Un mantel puede sacarse de una mesa sin tirar los objetos que hay sobre él.
            - Los cinturones de seguridad evitan que los ocupantes sigan en movimiento en caso de frenada brusca.
            """)
            
            # Construir la ruta absoluta a la imagen
            import os
            
            # Obtener el directorio actual del script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construir la ruta a la imagen
            primera_ley_img = os.path.join(script_dir, 'static', 'images', 'primera_ley_newton.jpg')
            
            # Verificar si el archivo existe
            if os.path.exists(primera_ley_img):
                st.image(primera_ley_img, 
                        caption="Primera Ley de Newton - Ejemplo de inercia", 
                        width=400,
                        use_container_width=True)
            else:
                st.warning(f"No se encontró la imagen de la Primera Ley de Newton en: {primera_ley_img}")
        
        with tab2:
            st.subheader("Segunda Ley de Newton (Ley Fundamental de la Dinámica)")
            st.markdown("""
            > *"La aceleración de un objeto es directamente proporcional a la fuerza neta que actúa sobre él 
            > e inversamente proporcional a su masa."*
            
            **Fórmula:** \\( \\vec{F} = m \\cdot \\vec{a} \\)
            
            Donde:
            - \\( \\vec{F} \\): Fuerza neta (N)
            - \\( m \\): Masa del objeto (kg)
            - \\( \\vec{a} \\): Aceleración (m/s²)
            """)
            
            # Calculadora de la Segunda Ley
            st.markdown("### Calculadora de Fuerza, Masa y Aceleración")
            
            # Selector de lo que se quiere calcular
            calculo = st.radio("Calcular:", ["Fuerza (F)", "Masa (m)", "Aceleración (a)"], 
                             horizontal=True, key="newton_calculo")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if calculo == "Fuerza (F)":
                    m = st.number_input("Masa (kg)", min_value=0.01, value=1.0, step=0.1, format="%.2f")
                    a = st.number_input("Aceleración (m/s²)", value=9.81, step=0.1, format="%.2f")
                elif calculo == "Masa (m)":
                    F = st.number_input("Fuerza (N)", min_value=0.01, value=9.81, step=0.1, format="%.2f")
                    a = st.number_input("Aceleración (m/s²)", min_value=0.01, value=9.81, step=0.1, format="%.2f")
                else:  # Aceleración
                    F = st.number_input("Fuerza (N)", min_value=0.01, value=9.81, step=0.1, format="%.2f")
                    m = st.number_input("Masa (kg)", min_value=0.01, value=1.0, step=0.1, format="%.2f")
            
            # Cálculo y resultado
            if st.button("Calcular", key="calc_newton"):
                try:
                    if calculo == "Fuerza (F)":
                        F = m * a
                        st.success(f"La fuerza es: **{F:.2f} N**")
                        st.latex(fr"F = m \\cdot a = {m:.2f} \\, \\text{{kg}} \\cdot {a:.2f} \\, \\text{{m/s}}^2 = {F:.2f} \\, \\text{{N}}")
                    elif calculo == "Masa (m)":
                        if a != 0:
                            m = F / a
                            st.success(f"La masa es: **{m:.2f} kg**")
                            st.latex(fr"m = \\frac{{F}}{{a}} = \\frac{{{F:.2f} \\, \\text{{N}}}}{{{a:.2f} \\, \\text{{m/s}}^2}} = {m:.2f} \\, \\text{{kg}}")
                        else:
                            st.error("La aceleración no puede ser cero.")
                    else:  # Aceleración
                        if m > 0:
                            a = F / m
                            st.success(f"La aceleración es: **{a:.2f} m/s²**")
                            st.latex(fr"a = \\frac{{F}}{{m}} = \\frac{{{F:.2f} \\, \\text{{N}}}}{{{m:.2f} \\, \\text{{kg}}}} = {a:.2f} \\, \\text{{m/s}}^2")
                        else:
                            st.error("La masa debe ser mayor que cero.")
                except Exception as e:
                    st.error(f"Error en el cálculo: {str(e)}")
            
            # Ejemplos comunes
            with st.expander("📚 Ejemplos de aplicación"):
                st.markdown("""
                ### Ejemplos de la Segunda Ley de Newton:
                
                1. **Empujar un carrito de supermercado**
                   - Masa: 20 kg
                   - Fuerza aplicada: 50 N
                   - Aceleración: \( a = \\frac{50\\, \\text{N}}{20\\, \\text{kg}} = 2.5\\, \\text{m/s}^2 \)
                
                2. **Frenado de un automóvil**
                   - Masa: 1000 kg
                   - Fuerza de frenado: -5000 N (negativa porque frena)
                   - Aceleración: \( a = \\frac{-5000\\, \\text{N}}{1000\\, \\text{kg}} = -5\\, \\text{m/s}^2 \)
                
                3. **Cohete despegando**
                   - Masa: 5000 kg
                   - Empuje: 100000 N
                   - Peso: \( 5000 \\, \\text{kg} \\cdot 9.81\\, \\text{m/s}^2 = 49050\\, \\text{N} \)
                   - Fuerza neta: \( 100000\\, \\text{N} - 49050\\, \\text{N} = 50950\\, \\text{N} \)
                   - Aceleración: \( a = \\frac{50950\\, \\text{N}}{5000\\, \\text{kg}} \\approx 10.19\\, \\text{m/s}^2 \)
                """)
        
        with tab3:
            st.subheader("Tercera Ley de Newton (Principio de Acción y Reacción)")
            st.markdown("""
            > *"Con toda acción ocurre siempre una reacción igual y contraria; 
            > las acciones mutuas de dos cuerpos siempre son iguales y dirigidas en sentidos opuestos."*
            
            **Concepto clave:** Las fuerzas siempre ocurren en pares (acción-reacción) que actúan sobre cuerpos diferentes.
            
            ### Ejemplos prácticos:
            - Al caminar, empujas el suelo hacia atrás (acción) y el suelo te empuja hacia adelante (reacción).
            - Un cohete expulsa gases hacia abajo (acción) y los gases empujan al cohete hacia arriba (reacción).
            - Al disparar un arma, la bala sale hacia adelante (acción) y el arma retrocede (reacción).
            """)
            
            # Construir la ruta absoluta a la imagen
            tercera_ley_img = os.path.join(script_dir, 'static', 'images', 'tercera_ley_newton.jpg')
            
            # Verificar si el archivo existe
            if os.path.exists(tercera_ley_img):
                st.image(tercera_ley_img,
                        caption="Tercera Ley de Newton - Acción y reacción",
                        width=400,
                        use_container_width=True)
            else:
                st.warning(f"No se encontró la imagen de la Tercera Ley de Newton en: {tercera_ley_img}")
        
        # Sección de Fuerza de Rozamiento y Plano Inclinado
        st.markdown("---")
        st.subheader("Fuerza de Rozamiento y Plano Inclinado")
        
        # Selector de tipo de cálculo
        tipo_calculo = st.radio("Tipo de cálculo:", 
                              ["Fuerza de Rozamiento", "Plano Inclinado"], 
                              horizontal=True)
        
        if tipo_calculo == "Fuerza de Rozamiento":
            st.markdown("""
            **Fuerza de Rozamiento Cinético:** \( f_k = \\mu_k \\cdot N \)
            
            **Fuerza de Rozamiento Estático Máximo:** \( f_{s,\\text{max}} = \\mu_s \\cdot N \)
            
            Donde:
            - \( \\mu_k \): Coeficiente de rozamiento cinético
            - \( \\mu_s \): Coeficiente de rozamiento estático
            - \( N \): Fuerza normal (N)
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                mu_k = st.number_input("Coeficiente de rozamiento cinético (μₖ)", 
                                     min_value=0.0, value=0.3, step=0.05, format="%.2f")
                mu_s = st.number_input("Coeficiente de rozamiento estático (μₛ)", 
                                     min_value=0.0, value=0.4, step=0.05, format="%.2f")
                N = st.number_input("Fuerza normal (N)", min_value=0.1, value=50.0, step=1.0, format="%.1f")
            
            with col2:
                f_k = mu_k * N
                f_s_max = mu_s * N
                
                st.metric("Fuerza de rozamiento cinético", f"{f_k:.2f} N")
                st.metric("Fuerza de rozamiento estático máximo", f"{f_s_max:.2f} N")
                
                st.latex(fr"f_k = \\mu_k \\cdot N = {mu_k:.2f} \\cdot {N:.1f} \\, \\text{{N}} = {f_k:.2f} \\, \\text{{N}}")
                st.latex(fr"f_{{s,\\text{{max}}}} = \\mu_s \\cdot N = {mu_s:.2f} \\cdot {N:.1f} \\, \\text{{N}} = {f_s_max:.2f} \\, \\text{{N}}")
        
        else:  # Plano Inclinado
            st.markdown("""
            **Fuerzas en un plano inclinado:**
            - Componente paralela al plano: \( F_{\\parallel} = m \\cdot g \\cdot \\sin(\\theta) \)
            - Componente normal al plano: \( F_{\\perp} = m \\cdot g \\cdot \\cos(\\theta) \)
            - Aceleración: \( a = g \\cdot (\\sin \\theta - \\mu_k \\cos \\theta) \)
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                masa = st.number_input("Masa (kg)", min_value=0.1, value=1.0, step=0.1, format="%.1f")
                angulo = st.slider("Ángulo de inclinación (grados)", 0, 90, 30)
                mu_k = st.number_input("Coeficiente de rozamiento cinético (μₖ)", 
                                     min_value=0.0, value=0.1, step=0.01, format="%.2f")
            
            with col2:
                # Convertir ángulo a radianes
                theta = np.radians(angulo)
                g = 9.81  # m/s²
                
                # Calcular componentes
                F_paralela = masa * g * np.sin(theta)
                F_normal = masa * g * np.cos(theta)
                
                # Calcular aceleración
                a = g * (np.sin(theta) - mu_k * np.cos(theta))
                
                st.metric("Componente paralela", f"{F_paralela:.2f} N")
                st.metric("Componente normal", f"{F_normal:.2f} N")
                st.metric("Aceleración", f"{a:.2f} m/s²")
                
                st.latex(fr"F_{{\\parallel}} = {masa:.1f} \\cdot 9.81 \\cdot \\sin({angulo}°) = {F_paralela:.2f} \\, \\text{{N}}")
                st.latex(fr"F_{{\\perp}} = {masa:.1f} \\cdot 9.81 \\cdot \\cos({angulo}°) = {F_normal:.2f} \\, \\text{{N}}")
                st.latex(fr"a = 9.81 \\cdot (\\sin {angulo}° - {mu_k:.2f} \\cdot \\cos {angulo}°) = {a:.2f} \\, \\text{{m/s}}^2")
    
    # Sección de Energía Mecánica
    with tab_energia:
        st.header("Energía Mecánica")
        
        # Pestañas para diferentes cálculos de energía
        tab_teoria, tab_calc, tab_ejemplos = st.tabs(["📚 Teoría", "🧮 Calculadora", "📝 Ejemplos"])
        
        with tab_teoria:
            st.markdown("""
            ## Conceptos Básicos de Energía Mecánica
            
            La **energía mecánica** es la suma de la energía cinética y potencial de un objeto. 
            Se conserva en sistemas aislados donde solo actúan fuerzas conservativas.
            
            ### Fórmulas Principales
            
            - **Energía Cinética (Ec):**
              \\[ E_c = \\frac{1}{2} m v^2 \\]
              
            - **Energía Potencial Gravitatoria (Ep):**
              \\[ E_p = m g h \\]
              
            - **Energía Mecánica Total (Em):**
              \\[ E_m = E_c + E_p \\]
              
            Donde:
            - \( m \) = masa (kg)
            - \( v \) = velocidad (m/s)
            - \( g \) = aceleración de la gravedad (9.81 m/s²)
            - \( h \) = altura (m)
            
            
            """)
        
        with tab_calc:
            st.subheader("Calculadora de Energía")
            
            # Selector de tipo de cálculo
            tipo_calculo = st.radio("Selecciona el tipo de cálculo:", 
                                 ["Energía Cinética (Ec)", 
                                  "Energía Potencial (Ep)",
                                  "Energía Mecánica Total (Em)",
                                  "Conservación de la Energía"],
                                 horizontal=True)
            
            # Constantes
            g = 9.81  # m/s²
            
            if tipo_calculo == "Energía Cinética (Ec)":
                st.markdown("""
                ### Energía Cinética
                \\[ E_c = \\frac{1}{2} m v^2 \\]
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    masa = st.number_input("Masa (kg)", min_value=0.01, value=1.0, step=0.1, format="%.2f", key="ec_masa")
                    velocidad = st.number_input("Velocidad (m/s)", value=10.0, step=0.1, format="%.2f", key="ec_velocidad")
                
                # Cálculo
                if st.button("Calcular Energía Cinética"):
                    energia_cinetica = 0.5 * masa * (velocidad ** 2)
                    st.success(f"Energía Cinética: **{energia_cinetica:.2f} J**")
                    st.latex(fr"E_c = \\frac{{1}}{{2}} \\cdot {masa:.2f} \\, \\text{{kg}} \\cdot ({velocidad:.2f} \\, \\text{{m/s}})^2 = {energia_cinetica:.2f} \\, \\text{{J}}")
            
            elif tipo_calculo == "Energía Potencial (Ep)":
                st.markdown("""
                ### Energía Potencial Gravitatoria
                \\[ E_p = m g h \\]
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    masa = st.number_input("Masa (kg)", min_value=0.01, value=1.0, step=0.1, format="%.2f", key="ep_masa")
                    altura = st.number_input("Altura (m)", min_value=0.0, value=10.0, step=0.1, format="%.2f", key="ep_altura")
                
                # Cálculo
                if st.button("Calcular Energía Potencial"):
                    energia_potencial = masa * g * altura
                    st.success(f"Energía Potencial: **{energia_potencial:.2f} J**")
                    st.latex(fr"E_p = {masa:.2f} \\, \\text{{kg}} \\cdot 9.81 \\, \\text{{m/s}}^2 \\cdot {altura:.2f} \\, \\text{{m}} = {energia_potencial:.2f} \\, \\text{{J}}")
            
            elif tipo_calculo == "Energía Mecánica Total (Em)":
                st.markdown("""
                ### Energía Mecánica Total
                \\[ E_m = E_c + E_p = \\frac{1}{2} m v^2 + m g h \\]
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    masa = st.number_input("Masa (kg)", min_value=0.01, value=1.0, step=0.1, format="%.2f", key="em_masa")
                    velocidad = st.number_input("Velocidad (m/s)", value=5.0, step=0.1, format="%.2f", key="em_velocidad")
                    altura = st.number_input("Altura (m)", min_value=0.0, value=10.0, step=0.1, format="%.2f", key="em_altura")
                
                # Cálculo
                if st.button("Calcular Energía Mecánica"):
                    energia_cinetica = 0.5 * masa * (velocidad ** 2)
                    energia_potencial = masa * g * altura
                    energia_mecanica = energia_cinetica + energia_potencial
                    
                    st.success(f"Energía Mecánica Total: **{energia_mecanica:.2f} J**")
                    st.latex(fr"E_m = E_c + E_p = \\frac{{1}}{{2}} \\cdot {masa:.2f} \\, \\text{{kg}} \\cdot ({velocidad:.2f} \\, \\text{{m/s}})^2 + {masa:.2f} \\, \\text{{kg}} \\cdot 9.81 \\, \\text{{m/s}}^2 \\cdot {altura:.2f} \\, \\text{{m}} = {energia_mecanica:.2f} \\, \\text{{J}}")
                    
                    # Mostrar desglose
                    st.markdown("#### Desglose:")
                    st.latex(fr"E_c = {energia_cinetica:.2f} \\, \\text{{J}}")
                    st.latex(fr"E_p = {energia_potencial:.2f} \\, \\text{{J}}")
            
            else:  # Conservación de la Energía
                st.markdown("""
                ### Conservación de la Energía Mecánica
                \\[ E_{m_1} = E_{m_2} \\]
                \\[ E_{c_1} + E_{p_1} = E_{c_2} + E_{p_2} \\]
                """)
                
                st.subheader("Estado Inicial")
                col1, col2 = st.columns(2)
                with col1:
                    masa = st.number_input("Masa (kg)", min_value=0.01, value=1.0, step=0.1, format="%.2f", key="cons_masa")
                    velocidad1 = st.number_input("Velocidad inicial (m/s)", value=0.0, step=0.1, format="%.2f", key="cons_velocidad1")
                    altura1 = st.number_input("Altura inicial (m)", min_value=0.0, value=20.0, step=0.1, format="%.2f", key="cons_altura1")
                
                st.subheader("Estado Final")
                col1, col2 = st.columns(2)
                with col1:
                    velocidad2 = st.number_input("Velocidad final (m/s)", value=0.0, step=0.1, format="%.2f", key="cons_velocidad2")
                    altura2 = st.number_input("Altura final (m)", min_value=0.0, value=0.0, step=0.1, format="%.2f", key="cons_altura2")
                
                # Cálculo
                if st.button("Verificar Conservación de la Energía"):
                    # Energía en el estado 1
                    ec1 = 0.5 * masa * (velocidad1 ** 2)
                    ep1 = masa * g * altura1
                    em1 = ec1 + ep1
                    
                    # Energía en el estado 2
                    ec2 = 0.5 * masa * (velocidad2 ** 2)
                    ep2 = masa * g * altura2
                    em2 = ec2 + ep2
                    
                    # Resultados
                    st.markdown("#### Estado Inicial (1):")
                    st.latex(fr"E_{{c_1}} = {ec1:.2f} \\, \\text{{J}}")
                    st.latex(fr"E_{{p_1}} = {ep1:.2f} \\, \\text{{J}}")
                    st.latex(fr"E_{{m_1}} = {em1:.2f} \\, \\text{{J}}")
                    
                    st.markdown("#### Estado Final (2):")
                    st.latex(fr"E_{{c_2}} = {ec2:.2f} \\, \\text{{J}}")
                    st.latex(fr"E_{{p_2}} = {ep2:.2f} \\, \\text{{J}}")
                    st.latex(fr"E_{{m_2}} = {em2:.2f} \\, \\text{{J}}")
                    
                    # Verificar conservación
                    diferencia = abs(em1 - em2)
                    if diferencia < 0.01:  # Tolerancia para errores de redondeo
                        st.success("✅ La energía mecánica se conserva (E₁ ≈ E₂)")
                    else:
                        st.warning(f"⚠️ La energía mecánica no se conserva. Diferencia: {diferencia:.2f} J")
                        st.info("Esto puede deberse a la presencia de fuerzas no conservativas como la fricción.")
        
        with tab_ejemplos:
            st.markdown("""
            ## Ejemplos Prácticos de Energía Mecánica
            
            ### 1. Montaña Rusa
            - **Situación:** Un vagón de 500 kg está en la cima de una montaña rusa a 30 m de altura y en reposo.
            - **Energía en la cima:** \( E_p = mgh = 500 \\, \\text{kg} \\times 9.81 \\, \\text{m/s}² \\times 30 \\, \\text{m} = 147,150 \\, \\text{J} \)
            - **En la base (h=0):** \( E_c = 147,150 \\, \\text{J} \)
              \\[ v = \\sqrt{\\frac{2E_c}{m}} = \\sqrt{\\frac{2 \\times 147150}{500}} \\approx 24.26 \\, \\text{m/s} \]
            
            ### 2. Salto de Bungee
            - **Situación:** Una persona de 70 kg salta desde un puente de 50 m de altura.
            - **Energía en el salto:** \( E_p = 70 \\times 9.81 \\times 50 = 34,335 \\, \\text{J} \)
            - **A 20 m del suelo:** \( E_p = 70 \\times 9.81 \\times 20 = 13,734 \\, \\text{J} \)
            - **Energía cinética restante:** \( E_c = 34,335 - 13,734 = 20,601 \\, \\text{J} \)
            - **Velocidad:** \( v = \\sqrt{\\frac{2 \\times 20601}{70}} \\approx 24.3 \\, \\text{m/s} \)
            
            ### 3. Péndulo Simple
            - **En el punto más alto:** Toda la energía es potencial.
            - **En el punto más bajo:** Toda la energía es cinética.
            - La energía total se conserva (si despreciamos la fricción del aire).
            """)

# --- SECCIÓN DE ESTADÍSTICA ---
elif selected_section == "Estadística":
    st.title(f"{sections[selected_section]} {selected_section}")
    st.info("Herramientas para cálculos estadísticos básicos, incluyendo medidas de tendencia central, dispersión y visualización de datos.")
    
    # Pestañas para organizar las diferentes herramientas estadísticas
    tab_desc, tab_inf, tab_vis = st.tabs(["📊 Descriptiva", "📈 Inferencial", "📉 Visualización"])
    
    with tab_desc:
        st.header("Estadística Descriptiva")
        
        # Entrada de datos
        st.subheader("Ingreso de Datos")
        data_input = st.text_area("Ingresa tus datos (separados por comas o espacios):", "5, 7, 8, 9, 10, 12, 15")
        
        # Procesar datos de entrada
        try:
            # Limpiar y convertir los datos
            data = []
            for x in re.split(r'[,\s]+', data_input.strip()):
                try:
                    data.append(float(x))
                except ValueError:
                    continue
            
            if not data:
                st.warning("Por favor ingresa datos válidos.")
            else:
                # Calcular medidas de tendencia central
                st.subheader("Medidas de Tendencia Central")
                
                import numpy as np
                
                mean = np.mean(data)
                median = np.median(data)
                
                # Calcular la moda con o sin scipy
                if SCIPY_AVAILABLE:
                    try:
                        mode_result = stats.mode(data)
                        if hasattr(mode_result, 'mode') and len(mode_result.mode) > 0:
                            mode = mode_result.mode[0]
                        else:
                            mode = "No hay moda"
                    except Exception:
                        mode = "No hay moda"
                else:
                    # Implementación básica de moda sin scipy
                    counts = {}
                    for num in data:
                        counts[num] = counts.get(num, 0) + 1
                    max_count = max(counts.values()) if counts else 0
                    modes = [num for num, count in counts.items() if count == max_count]
                    
                    if len(modes) == 0:
                        mode = "No hay moda"
                    elif len(modes) == 1:
                        mode = modes[0]
                    else:
                        mode = f"Múltiples modas: {', '.join(map(str, modes))}"
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Media (Promedio)", f"{mean:.2f}")
                with col2:
                    st.metric("Mediana", f"{median:.2f}")
                with col3:
                    st.metric("Moda", f"{mode}" if isinstance(mode, str) else f"{mode:.2f}")
                
                # Calcular medidas de dispersión
                st.subheader("Medidas de Dispersión")
                
                data_range = max(data) - min(data)
                variance = np.var(data, ddof=1)  # Varianza muestral (n-1)
                std_dev = np.std(data, ddof=1)   # Desviación estándar muestral
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rango", f"{data_range:.2f}")
                with col2:
                    st.metric("Varianza Muestral", f"{variance:.2f}")
                with col3:
                    st.metric("Desviación Estándar", f"{std_dev:.2f}")
                
                # Mostrar resumen de datos
                st.subheader("Resumen de Datos")
                
                import pandas as pd
                df = pd.DataFrame({"Valores": data})
                st.dataframe(df.describe(), use_container_width=True)
                
        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")
    
    with tab_vis:
        st.header("Visualización de Datos")
        
        if 'data' in locals() and len(data) > 0:
            plot_type = st.selectbox(
                "Selecciona el tipo de gráfico:",
                ["Histograma", "Gráfico de Caja", "Gráfico de Dispersión"]
            )
            
            if MATPLOTLIB_AVAILABLE:
                fig, ax = plt.subplots(figsize=(10, 5))
                
                if plot_type == "Histograma":
                    ax.hist(data, bins='auto', color='skyblue', edgecolor='black')
                    ax.set_title("Distribución de los Datos")
                    ax.set_xlabel("Valores")
                    ax.set_ylabel("Frecuencia")
                    
                elif plot_type == "Gráfico de Caja":
                    ax.boxplot(data, vert=False)
                    ax.set_title("Gráfico de Caja")
                    ax.set_xlabel("Valores")
                    
                elif plot_type == "Gráfico de Dispersión":
                    ax.scatter(range(len(data)), data, color='blue', alpha=0.6)
                    ax.set_title("Gráfico de Dispersión")
                    ax.set_xlabel("Índice")
                    ax.set_ylabel("Valor")
                
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.warning("La visualización de gráficos no está disponible. Por favor instala matplotlib.")
        else:
            st.info("Ingresa datos en la pestaña 'Descriptiva' para visualizarlos aquí.")
    
    with tab_inf:
        st.header("Estadística Inferencial")
        
        # Pestañas para diferentes tipos de análisis inferencial
        tab_ci, tab_ttest, tab_chisq, tab_corr = st.tabs([
            "📏 Intervalos de Confianza", 
            "🔍 Pruebas t", 
            "📊 Chi-cuadrado",
            "🔗 Correlación"
        ])
        
        with tab_ci:
            st.subheader("Intervalos de Confianza para la Media")
            
            # Usar los datos de la pestaña descriptiva si están disponibles
            if 'data' in locals() and len(data) > 0:
                sample_data = data
                st.info(f"Usando los datos ingresados (n={len(sample_data)}). Puedes modificarlos en la pestaña 'Descriptiva'.")
            else:
                sample_data = [5, 7, 8, 9, 10, 12, 15]  # Datos de ejemplo
                st.warning("No hay datos ingresados. Usando datos de ejemplo.")
            
            # Configuración del intervalo de confianza
            confidence_level = st.slider("Nivel de confianza (%)", 80, 99, 95, 1) / 100
            
            # Calcular intervalo de confianza
            if len(sample_data) >= 2:
                import math
                from scipy import stats
                
                n = len(sample_data)
                mean = np.mean(sample_data)
                std_err = np.std(sample_data, ddof=1) / math.sqrt(n)
                
                # Usar t-distribución para n < 30, normal para n >= 30
                if n < 30:
                    critical_value = stats.t.ppf((1 + confidence_level) / 2, df=n-1)
                    dist_name = "t-Student"
                else:
                    critical_value = stats.norm.ppf((1 + confidence_level) / 2)
                    dist_name = "Normal"
                
                margin_of_error = critical_value * std_err
                ci_lower = mean - margin_of_error
                ci_upper = mean + margin_of_error
                
                # Mostrar resultados
                st.metric(f"Media muestral (n={n})", f"{mean:.4f}")
                st.metric("Error estándar", f"{std_err:.4f}")
                st.metric("Margen de error", f"±{margin_of_error:.4f} ({dist_name}, {confidence_level*100:.0f}%)")
                
                # Mostrar intervalo de confianza
                st.subheader(f"Intervalo de Confianza al {confidence_level*100:.0f}%")
                st.latex(f"{ci_lower:.4f} \\leq \\mu \\leq {ci_upper:.4f}")
                
                # Gráfico del intervalo de confianza
                if MATPLOTLIB_AVAILABLE:
                    fig, ax = plt.subplots(figsize=(10, 2))
                    ax.errorbar(mean, 0, xerr=[[mean - ci_lower], [ci_upper - mean]], 
                               fmt='o', color='black', capsize=5, markersize=8)
                    ax.set_yticks([])
                    ax.set_xlabel('Valor')
                    ax.set_title(f'Intervalo de Confianza al {confidence_level*100:.0f}% para la Media')
                    st.pyplot(fig)
                    plt.close(fig)
            else:
                st.warning("Se necesitan al menos 2 puntos de datos para calcular un intervalo de confianza.")
        
        with tab_ttest:
            st.subheader("Pruebas t")
            
            test_type = st.radio(
                "Tipo de prueba t:",
                ["Una muestra", "Dos muestras independientes", "Muestras pareadas"]
            )
            
            if test_type == "Una muestra":
                st.write("Compara la media de una muestra con un valor teórico.")
                
                if 'data' in locals() and len(data) > 0:
                    sample_data = data
                    st.info(f"Usando los datos ingresados (n={len(sample_data)}).")
                else:
                    sample_data = [48, 52, 55, 49, 50, 53, 51, 52, 50, 51]
                    st.warning("Usando datos de ejemplo.")
                
                pop_mean = st.number_input("Valor teórico (μ₀)", value=50.0, step=0.1)
                
                if st.button("Realizar prueba t de una muestra"):
                    t_stat, p_value = stats.ttest_1samp(sample_data, pop_mean)
                    
                    st.subheader("Resultados")
                    st.metric("Estadístico t", f"{t_stat:.4f}")
                    st.metric("Valor p", f"{p_value:.4f}")
                    
                    # Interpretación
                    alpha = 0.05
                    if p_value < alpha:
                        st.success(f"Se rechaza H₀ (p < {alpha}). Hay evidencia de una diferencia significativa con μ₀ = {pop_mean}.")
                    else:
                        st.info(f"No se rechaza H₀ (p ≥ {alpha}). No hay evidencia suficiente para afirmar una diferencia con μ₀ = {pop_mean}.")
            
            elif test_type == "Dos muestras independientes":
                st.write("Compara las medias de dos grupos independientes.")
                
                # Datos de ejemplo o entrada manual
                data_option = st.radio("Opciones de datos:", ["Usar ejemplos", "Ingresar manualmente"])
                
                if data_option == "Usar ejemplos":
                    group1 = [68, 72, 75, 69, 70, 73, 71, 72, 70, 71]
                    group2 = [62, 65, 68, 64, 63, 66, 65, 64, 66, 65]
                else:
                    group1 = [float(x) for x in st.text_area("Grupo 1 (separado por comas)", "68, 72, 75, 69, 70, 73, 71, 72, 70, 71").split(",") if x.strip()]
                    group2 = [float(x) for x in st.text_area("Grupo 2 (separado por comas)", "62, 65, 68, 64, 63, 66, 65, 64, 66, 65").split(",") if x.strip()]
                
                if st.button("Realizar prueba t para muestras independientes"):
                    t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=True)
                    
                    st.subheader("Resultados")
                    st.metric("Media Grupo 1", f"{np.mean(group1):.2f} (n={len(group1)})")
                    st.metric("Media Grupo 2", f"{np.mean(group2):.2f} (n={len(group2)})")
                    st.metric("Estadístico t", f"{t_stat:.4f}")
                    st.metric("Valor p (dos colas)", f"{p_value:.4f}")
                    
                    # Interpretación
                    alpha = 0.05
                    if p_value < alpha:
                        st.success(f"Se rechaza H₀ (p < {alpha}). Hay evidencia de una diferencia significativa entre los grupos.")
                    else:
                        st.info(f"No se rechaza H₀ (p ≥ {alpha}). No hay evidencia suficiente para afirmar una diferencia entre los grupos.")
                    
                    # Gráfico de cajas comparativo
                    if MATPLOTLIB_AVAILABLE:
                        fig, ax = plt.subplots(figsize=(8, 6))
                        ax.boxplot([group1, group2], labels=["Grupo 1", "Grupo 2"])
                        ax.set_title("Comparación de Grupos")
                        ax.set_ylabel("Valores")
                        st.pyplot(fig)
                        plt.close(fig)
            
            else:  # Muestras pareadas
                st.write("Compara las medias de mediciones pareadas (antes/después).")
                
                # Datos de ejemplo o entrada manual
                data_option = st.radio("Opciones de datos:", ["Usar ejemplo", "Ingresar manualmente"], key="paired_radio")
                
                if data_option == "Usar ejemplo":
                    before = [72, 80, 85, 71, 69, 65, 82, 76, 70, 75]
                    after = [68, 72, 82, 70, 65, 60, 71, 77, 65, 68]
                else:
                    before = [float(x) for x in st.text_area("Antes (separado por comas)", "72, 80, 85, 71, 69, 65, 82, 76, 70, 75").split(",") if x.strip()]
                    after = [float(x) for x in st.text_area("Después (separado por comas)", "68, 72, 82, 70, 65, 60, 71, 77, 65, 68").split(",") if x.strip()]
                
                if st.button("Realizar prueba t para muestras pareadas"):
                    if len(before) != len(after):
                        st.error("Error: Las muestras deben tener el mismo tamaño.")
                    else:
                        t_stat, p_value = stats.ttest_rel(before, after)
                        differences = [a - b for a, b in zip(before, after)]
                        
                        st.subheader("Resultados")
                        st.metric("Media Antes", f"{np.mean(before):.2f}")
                        st.metric("Media Después", f"{np.mean(after):.2f}")
                        st.metric("Diferencia Media", f"{np.mean(differences):.2f}")
                        st.metric("Estadístico t", f"{t_stat:.4f}")
                        st.metric("Valor p (dos colas)", f"{p_value:.4f}")
                        
                        # Interpretación
                        alpha = 0.05
                        if p_value < alpha:
                            st.success(f"Se rechaza H₀ (p < {alpha}). Hay evidencia de una diferencia significativa entre las mediciones pareadas.")
                        else:
                            st.info(f"No se rechaza H₀ (p ≥ {alpha}). No hay evidencia suficiente para afirmar una diferencia entre las mediciones pareadas.")
                        
                        # Gráfico de diferencias
                        if MATPLOTLIB_AVAILABLE:
                            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                            
                            # Gráfico de líneas conectadas
                            for i in range(len(before)):
                                ax1.plot([1, 2], [before[i], after[i]], 'o-', color='gray', alpha=0.5)
                            ax1.set_xticks([1, 2])
                            ax1.set_xticklabels(['Antes', 'Después'])
                            ax1.set_ylabel('Valor')
                            ax1.set_title('Mediciones Pareadas')
                            
                            # Gráfico de diferencias
                            ax2.hist(differences, bins='auto', color='skyblue', edgecolor='black')
                            ax2.axvline(0, color='red', linestyle='--')
                            ax2.set_xlabel('Diferencia (Después - Antes)')
                            ax2.set_ylabel('Frecuencia')
                            ax2.set_title('Distribución de Diferencias')
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
        
        with tab_chisq:
            st.subheader("Prueba Chi-cuadrado de Independencia")
            st.write("Evalúa si existe una asociación entre dos variables categóricas.")
            
            # Tabla de contingencia de ejemplo
            st.write("Ingresa los conteos en una tabla de contingencia 2x2:")
            
            col1, col2 = st.columns(2)
            with col1:
                a = st.number_input("Categoría A, Grupo 1", min_value=0, value=30)
                b = st.number_input("Categoría A, Grupo 2", min_value=0, value=20)
            with col2:
                c = st.number_input("Categoría B, Grupo 1", min_value=0, value=10)
                d = st.number_input("Categoría B, Grupo 2", min_value=0, value=40)
            
            if st.button("Realizar prueba Chi-cuadrado"):
                try:
                    from scipy.stats import chi2_contingency
                    
                    # Crear tabla de contingencia
                    observed = [[a, b], [c, d]]
                    chi2, p_value, dof, expected = chi2_contingency(observed)
                    
                    # Mostrar resultados
                    st.subheader("Resultados")
                    
                    # Mostrar tabla observada
                    st.write("**Tabla Observada:**")
                    obs_df = pd.DataFrame(observed, 
                                        index=["Categoría A", "Categoría B"],
                                        columns=["Grupo 1", "Grupo 2"])
                    st.dataframe(obs_df, use_container_width=True)
                    
                    # Mostrar tabla esperada bajo H0
                    st.write("**Frecuencias Esperadas bajo H₀ (independencia):**")
                    exp_df = pd.DataFrame(expected.round(2), 
                                         index=["Categoría A", "Categoría B"],
                                         columns=["Grupo 1", "Grupo 2"])
                    st.dataframe(exp_df, use_container_width=True)
                    
                    # Mostrar estadísticos
                    st.metric("Estadístico Chi-cuadrado", f"{chi2:.4f}")
                    st.metric("Grados de libertad", dof)
                    st.metric("Valor p", f"{p_value:.4f}")
                    
                    # Interpretación
                    alpha = 0.05
                    if p_value < alpha:
                        st.success(f"Se rechaza H₀ (p < {alpha}). Hay evidencia de una asociación significativa entre las variables.")
                    else:
                        st.info(f"No se rechaza H₀ (p ≥ {alpha}). No hay evidencia suficiente para afirmar una asociación entre las variables.")
                    
                except Exception as e:
                    st.error(f"Error al realizar la prueba: {str(e)}")
        
        with tab_corr:
            st.subheader("Análisis de Correlación")
            
            # Opciones de datos
            data_option = st.radio("Opciones de datos:", ["Usar ejemplo", "Cargar archivo CSV", "Ingresar manualmente"], key="corr_radio")
            
            if data_option == "Usar ejemplo":
                # Datos de ejemplo: Altura vs Peso
                np.random.seed(42)
                altura = np.random.normal(170, 10, 50)
                peso = 50 + 0.7 * altura + np.random.normal(0, 5, 50)
                df = pd.DataFrame({'Altura (cm)': altura, 'Peso (kg)': peso})
                
                st.write("**Datos de ejemplo:** Altura vs Peso")
                st.dataframe(df.head(), use_container_width=True)
                
            elif data_option == "Cargar archivo CSV":
                uploaded_file = st.file_uploader("Sube un archivo CSV con dos columnas numéricas", type=["csv"])
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                        if len(df.columns) < 2:
                            st.error("El archivo debe contener al menos dos columnas numéricas.")
                        else:
                            st.success(f"Archivo cargado: {uploaded_file.name}")
                            st.dataframe(df.head(), use_container_width=True)
                    except Exception as e:
                        st.error(f"Error al cargar el archivo: {str(e)}")
                        df = None
                else:
                    df = None
            
            else:  # Ingresar manualmente
                col1, col2 = st.columns(2)
                with col1:
                    x_data = st.text_area("Variable X (una por línea)", "165\n170\n175\n180\n185")
                    x_values = [float(x.strip()) for x in x_data.split("\n") if x.strip()]
                with col2:
                    y_data = st.text_area("Variable Y (una por línea)", "60\n65\n70\n75\n80")
                    y_values = [float(y.strip()) for y in y_data.split("\n") if y.strip()]
                
                if len(x_values) == len(y_values) and len(x_values) >= 2:
                    df = pd.DataFrame({'X': x_values, 'Y': y_values})
                    st.dataframe(df, use_container_width=True)
                else:
                    st.error("Ambas variables deben tener el mismo número de valores (mínimo 2).")
                    df = None
            
            if 'df' in locals() and df is not None and len(df.columns) >= 2:
                # Seleccionar columnas para correlación
                if data_option == "Cargar archivo CSV":
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("Selecciona la variable X", df.columns)
                    with col2:
                        y_col = st.selectbox("Selecciona la variable Y", df.columns)
                else:
                    x_col, y_col = df.columns[0], df.columns[1]
                
                # Calcular correlación
                if st.button("Calcular Correlación"):
                    try:
                        # Calcular coeficientes
                        pearson_r, pearson_p = stats.pearsonr(df[x_col], df[y_col])
                        spearman_r, spearman_p = stats.spearmanr(df[x_col], df[y_col])
                        
                        # Mostrar resultados
                        st.subheader("Resultados de Correlación")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Correlación de Pearson (r)", f"{pearson_r:.4f}")
                            st.metric("Valor p (Pearson)", f"{pearson_p:.4f}")
                        with col2:
                            st.metric("Correlación de Spearman (ρ)", f"{spearman_r:.4f}")
                            st.metric("Valor p (Spearman)", f"{spearman_p:.4f}")
                        
                        # Interpretación
                        st.subheader("Interpretación")
                        st.write("**Correlación de Pearson:** Mide la relación lineal entre variables continuas.")
                        st.write("**Correlación de Spearman:** Mide la relación monótona (no necesariamente lineal) entre variables.")
                        
                        # Gráfico de dispersión con línea de regresión
                        if MATPLOTLIB_AVAILABLE:
                            fig, ax = plt.subplots(figsize=(10, 6))
                            
                            # Gráfico de dispersión
                            scatter = ax.scatter(df[x_col], df[y_col], alpha=0.7)
                            
                            # Línea de regresión
                            if len(df) >= 2:
                                z = np.polyfit(df[x_col], df[y_col], 1)
                                p = np.poly1d(z)
                                ax.plot(df[x_col], p(df[x_col]), "r--")
                            
                            ax.set_xlabel(x_col)
                            ax.set_ylabel(y_col)
                            ax.set_title(f"Diagrama de Dispersión")
                            ax.grid(True, linestyle='--', alpha=0.7)
                            
                            st.pyplot(fig)
                            plt.close(fig)
                        
                    except Exception as e:
                        st.error(f"Error al calcular la correlación: {str(e)}")

# --- SECCIÓN DE GEOMETRÍA ---
elif selected_section == "Geometría":
    st.title(f"{sections[selected_section]} {selected_section}")
    st.info("Calculadora de áreas y volúmenes de figuras geométricas.")
    
    # Pestañas para organizar los diferentes tipos de cálculos
    tab_areas, tab_volumenes = st.tabs(["📏 Áreas", "📦 Volúmenes"])
    
    with tab_areas:
        st.header("Cálculo de Áreas")
        figura_plana = st.selectbox(
            "Selecciona una figura plana:",
            ["Triángulo", "Rectángulo", "Círculo", "Trapecio", "Polígono Regular"]
        )
        
        if figura_plana == "Triángulo":
            col1, col2 = st.columns(2)
            with col1:
                base = st.number_input("Base (b):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            with col2:
                altura = st.number_input("Altura (h):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Área"):
                area = 0.5 * base * altura
                st.latex(f"A = \\frac{{1}}{{2}} \\times b \\times h = \\frac{{1}}{{2}} \\times {base} \\times {altura} = {area:.2f}")
                st.success(f"El área del triángulo es: {area:.2f} unidades cuadradas")
        
        elif figura_plana == "Rectángulo":
            col1, col2 = st.columns(2)
            with col1:
                base = st.number_input("Base (b):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            with col2:
                altura = st.number_input("Altura (h):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Área"):
                area = base * altura
                st.latex(f"A = b \\times h = {base} \\times {altura} = {area:.2f}")
                st.success(f"El área del rectángulo es: {area:.2f} unidades cuadradas")
        
        elif figura_plana == "Círculo":
            radio = st.number_input("Radio (r):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Área"):
                area = 3.1416 * (radio ** 2)
                st.latex(f"A = \\pi r^2 = \\pi \\times {radio}^2 = {area:.2f}")
                st.success(f"El área del círculo es: {area:.2f} unidades cuadradas")
        
        elif figura_plana == "Trapecio":
            col1, col2 = st.columns(2)
            with col1:
                base_mayor = st.number_input("Base mayor (B):", min_value=0.0, value=5.0, step=0.1, format="%.2f", key="trapecio_base_mayor")
                base_menor = st.number_input("Base menor (b):", min_value=0.0, value=3.0, step=0.1, format="%.2f", key="trapecio_base_menor")
            with col2:
                altura = st.number_input("Altura (h):", min_value=0.0, value=4.0, step=0.1, format="%.2f", key="trapecio_altura")
            
            if st.button("Calcular Área"):
                area = 0.5 * (base_mayor + base_menor) * altura
                st.latex(f"A = \\frac{{B + b}}{{2}} \\times h = \\frac{{{base_mayor} + {base_menor}}}{{2}} \\times {altura} = {area:.2f}")
                st.success(f"El área del trapecio es: {area:.2f} unidades cuadradas")
        
        elif figura_plana == "Polígono Regular":
            col1, col2 = st.columns(2)
            with col1:
                num_lados = st.number_input("Número de lados (n):", min_value=3, value=5, step=1, key="poligono_lados")
                longitud_lado = st.number_input("Longitud del lado (l):", min_value=0.0, value=1.0, step=0.1, format="%.2f", key="poligono_lado")
            with col2:
                apotema = st.number_input("Apotema (a):", min_value=0.0, value=0.69, step=0.01, format="%.2f", 
                                      help="Distancia del centro al punto medio de un lado", key="poligono_apotema")
            
            if st.button("Calcular Área"):
                perimetro = num_lados * longitud_lado
                area = 0.5 * perimetro * apotema
                st.latex(f"A = \\frac{{P \\times a}}{{2}} = \\frac{{{perimetro} \\times {apotema}}}{{2}} = {area:.2f}")
                st.success(f"El área del polígono regular es: {area:.2f} unidades cuadradas")
    
    with tab_volumenes:
        st.header("Cálculo de Volúmenes")
        solido = st.selectbox(
            "Selecciona un sólido:",
            ["Cubo", "Esfera", "Cilindro", "Cono", "Pirámide"]
        )
        
        if solido == "Cubo":
            lado = st.number_input("Longitud de la arista (a):", min_value=0.0, value=1.0, step=0.1, format="%.2f", key="cubo_lado")
            
            if st.button("Calcular Volumen"):
                volumen = lado ** 3
                st.latex(f"V = a^3 = {lado}^3 = {volumen:.2f}")
                st.success(f"El volumen del cubo es: {volumen:.2f} unidades cúbicas")
        
        elif solido == "Esfera":
            radio = st.number_input("Radio (r):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Volumen"):
                volumen = (4/3) * 3.1416 * (radio ** 3)
                st.latex(f"V = \\frac{{4}}{{3}}\\pi r^3 = \\frac{{4}}{{3}} \\times \\pi \\times {radio}^3 = {volumen:.2f}")
                st.success(f"El volumen de la esfera es: {volumen:.2f} unidades cúbicas")
        
        elif solido == "Cilindro":
            col1, col2 = st.columns(2)
            with col1:
                radio = st.number_input("Radio de la base (r):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            with col2:
                altura = st.number_input("Altura (h):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Volumen"):
                volumen = 3.1416 * (radio ** 2) * altura
                st.latex(f"V = \\pi r^2 h = \\pi \\times {radio}^2 \\times {altura} = {volumen:.2f}")
                st.success(f"El volumen del cilindro es: {volumen:.2f} unidades cúbicas")
        
        elif solido == "Cono":
            col1, col2 = st.columns(2)
            with col1:
                radio = st.number_input("Radio de la base (r):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            with col2:
                altura = st.number_input("Altura (h):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
            
            if st.button("Calcular Volumen"):
                volumen = (1/3) * 3.1416 * (radio ** 2) * altura
                st.latex(f"V = \\frac{{1}}{{3}} \\pi r^2 h = \\frac{{1}}{{3}} \\times \\pi \\times {radio}^2 \\times {altura} = {volumen:.2f}")
                st.success(f"El volumen del cono es: {volumen:.2f} unidades cúbicas")
        
        elif solido == "Pirámide":
            col1, col2 = st.columns(2)
            with col1:
                area_base = st.number_input("Área de la base (B):", min_value=0.0, value=1.0, step=0.1, format="%.2f", key="piramide_area")
            with col2:
                altura = st.number_input("Altura (h):", min_value=0.0, value=1.0, step=0.1, format="%.2f", key="piramide_altura")
            
            if st.button("Calcular Volumen"):
                volumen = (1/3) * area_base * altura
                st.latex(f"V = \\frac{{1}}{{3}} B h = \\frac{{1}}{{3}} \\times {area_base} \\times {altura} = {volumen:.2f}")
                st.success(f"El volumen de la pirámide es: {volumen:.2f} unidades cúbicas")

# --- SECCIÓN DE MATEMÁTICA AVANZADA ---
elif selected_section == "Matemática Avanzada":
    st.title(f"{sections[selected_section]} {selected_section}")
    
    # Pestañas para organizar las diferentes calculadoras
    tab1, tab2 = st.tabs(["Números Complejos", "Operaciones con Matrices"])
    
    with tab1:
        st.header("Calculadora de Números Complejos")
        st.write("Herramientas para operaciones con números complejos, incluyendo el Teorema de De Moivre.")
        
        # Código existente de números complejos...
        # (Este código se mantiene igual, solo cambia la indentación)
        operation = st.selectbox(
            "Selecciona una operación:",
            ["Suma", "Resta", "Multiplicación", "División", "Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"],
            key="complex_operation"
        )

        col1, col2 = st.columns(2)
        
        with col1:
            z1_str = st.text_input("Número Complejo z1:", value="1+2j", key="z1_input")
        
        with col2:
            if operation not in ["Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"]:
                z2_str = st.text_input("Número Complejo z2:", value="3-4j", key="z2_input")
            elif operation == "Potencia (De Moivre)":
                n_power = st.number_input("Exponente (n):", value=2, step=1, key="power_input")
            else:  # Raíz n-ésima
                n_root = st.number_input("Índice de la raíz (n):", value=2, min_value=1, step=1, key="root_input")

        # Código de números complejos (se mantiene igual)
        z1 = parse_complex(z1_str)
        
        if operation not in ["Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"]:
            z2 = parse_complex(z2_str)
        else:
            z2 = None
            
        if z1 is not None and (z2 is not None or operation in ["Potencia (De Moivre)", "Raíz n-ésima (De Moivre)"]):
            if operation == "Suma":
                result = z1 + z2
                st.success(f"**Resultado:** {format_complex(z1)} + {format_complex(z2)} = {format_complex(result)}")
                
            elif operation == "Resta":
                result = z1 - z2
                st.success(f"**Resultado:** {format_complex(z1)} - {format_complex(z2)} = {format_complex(result)}")
                
            elif operation == "Multiplicación":
                result = z1 * z2
                st.success(f"**Resultado:** {format_complex(z1)} × {format_complex(z2)} = {format_complex(result)}")
                
            elif operation == "División":
                if z2 == 0:
                    st.error("Error: No se puede dividir por cero")
                else:
                    result = z1 / z2
                    st.success(f"**Resultado:** {format_complex(z1)} / {format_complex(z2)} = {format_complex(result)}")
                    
            elif operation == "Potencia (De Moivre)":
                r, theta = to_polar(z1)
                result_r = r ** n_power
                result_theta = theta * n_power
                result = result_r * (math.cos(result_theta) + 1j * math.sin(result_theta))
                st.success(f"**Resultado (forma polar):** ({r:.4f}∠{math.degrees(theta):.2f}°)^{n_power} = {result_r:.4f}∠{math.degrees(result_theta):.2f}°")
                st.success(f"**Resultado (forma rectangular):** {format_complex(result, 4)}")
                
            elif operation == "Raíz n-ésima (De Moivre)":
                if n_root < 1:
                    st.error("El índice de la raíz debe ser mayor o igual a 1")
                else:
                    r, theta = to_polar(z1)
                    roots = []
                    for k in range(n_root):
                        root_r = r ** (1/n_root)
                        root_theta = (theta + 2 * k * math.pi) / n_root
                        root = root_r * (math.cos(root_theta) + 1j * math.sin(root_theta))
                        roots.append(root)
                    
                    st.success(f"**Raíces {n_root}-ésimas de {format_complex(z1)}:")
                    for i, root in enumerate(roots, 1):
                        st.write(f"- Raíz {i}: {format_complex(root, 4)}")
    
    with tab2:
        st.header("Calculadora de Matrices")
        st.info("Realiza operaciones con matrices: suma, resta y multiplicación.")
        
        # Código de la calculadora de matrices
        st.subheader("Operaciones con Matrices")
        
        # Función para parsear matrices
        def parse_matrix(matrix_string, matrix_name):
            try:
                rows = matrix_string.strip().splitlines()
                if not rows:
                    st.warning(f"La Matriz {matrix_name} está vacía.")
                    return None
                
                parsed_rows = [list(map(float, row.replace(',', ' ').split())) for row in rows]
                
                it = iter(parsed_rows)
                the_len = len(next(it))
                if not all(len(l) == the_len for l in it):
                    st.warning(f"La Matriz {matrix_name} tiene filas de diferentes longitudes. Por favor, corrígela.")
                    return None
                
                return np.array(parsed_rows)
            except (ValueError, StopIteration):
                st.error(f"Error al procesar la Matriz {matrix_name}. Asegúrate de que los números son válidos y están separados por espacios o comas.")
                return None
            except Exception as e:
                st.error(f"Ocurrió un error inesperado con la Matriz {matrix_name}: {e}")
                return None

        # Interfaz para introducir las matrices
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Matriz A")
            matrix_a_str = st.text_area(
                "Introduce la Matriz A (filas con saltos de línea, números con espacios/comas):",
                "1 2\n3 4",
                key="matrix_a",
                height=150
            )

        with col2:
            st.markdown("##### Matriz B")
            matrix_b_str = st.text_area(
                "Introduce la Matriz B (filas con saltos de línea, números con espacios/comas):",
                "5 6\n7 8",
                key="matrix_b",
                height=150
            )

        # Botones de operación
        op_col1, op_col2, op_col3 = st.columns(3)
        
        result_matrix = None
        operation_char = ""
        matrix_a, matrix_b = None, None

        if op_col1.button("Sumar (A + B)", use_container_width=True):
            matrix_a = parse_matrix(matrix_a_str, "A")
            matrix_b = parse_matrix(matrix_b_str, "B")
            
            if matrix_a is not None and matrix_b is not None:
                if matrix_a.shape == matrix_b.shape:
                    result_matrix = matrix_a + matrix_b
                    operation_char = "+"
                else:
                    st.error("Las matrices deben tener las mismas dimensiones para poder sumarse.")

        if op_col2.button("Restar (A - B)", use_container_width=True):
            matrix_a = parse_matrix(matrix_a_str, "A")
            matrix_b = parse_matrix(matrix_b_str, "B")

            if matrix_a is not None and matrix_b is not None:
                if matrix_a.shape == matrix_b.shape:
                    result_matrix = matrix_a - matrix_b
                    operation_char = "-"
                else:
                    st.error("Las matrices deben tener las mismas dimensiones para poder restarse.")

        if op_col3.button("Multiplicar (A × B)", use_container_width=True):
            matrix_a = parse_matrix(matrix_a_str, "A")
            matrix_b = parse_matrix(matrix_b_str, "B")

            if matrix_a is not None and matrix_b is not None:
                if matrix_a.shape[1] == matrix_b.shape[0]:
                    result_matrix = np.dot(matrix_a, matrix_b)
                    operation_char = "×"
                else:
                    st.error(f"Para multiplicar, el número de columnas de A ({matrix_a.shape[1]}) debe ser igual al número de filas de B ({matrix_b.shape[0]}).")

        # Mostrar resultado
        if result_matrix is not None:
            st.markdown("---")
            st.subheader("Resultado")
            
            def format_matrix_for_display(matrix):
                return '\n'.join([' '.join(map(str, row)) for row in matrix])

            matrix_a_nice = format_matrix_for_display(matrix_a)
            matrix_b_nice = format_matrix_for_display(matrix_b)
            result_matrix_nice = format_matrix_for_display(result_matrix)

            res_col1, res_col2, res_col3, res_col4, res_col5 = st.columns([2,1,2,1,2])
            with res_col1:
                st.text_area("Matriz A", value=matrix_a_nice, disabled=True, height=150, key="res_a")
            with res_col2:
                st.markdown(f"<div style='text-align: center; font-size: 2em; padding-top: 40px;'>{operation_char}</div>", unsafe_allow_html=True)
            with res_col3:
                st.text_area("Matriz B", value=matrix_b_nice, disabled=True, height=150, key="res_b")
            with res_col4:
                st.markdown(f"<div style='text-align: center; font-size: 2em; padding-top: 40px;'> = </div>", unsafe_allow_html=True)
            with res_col5:
                st.text_area("Resultado", value=result_matrix_nice, disabled=True, height=150, key="res_c")

    # --- Función para parsear la matriz desde un string ---
    def parse_matrix(matrix_string, matrix_name):
        try:
            rows = matrix_string.strip().splitlines()
            if not rows:
                st.warning(f"La Matriz {matrix_name} está vacía.")
                return None
            
            parsed_rows = [list(map(float, row.replace(',', ' ').split())) for row in rows]
            
            it = iter(parsed_rows)
            the_len = len(next(it))
            if not all(len(l) == the_len for l in it):
                st.warning(f"La Matriz {matrix_name} tiene filas de diferentes longitudes. Por favor, corrígela.")
                return None
            
            return np.array(parsed_rows)
        except (ValueError, StopIteration):
            st.error(f"Error al procesar la Matriz {matrix_name}. Asegúrate de que los números son válidos y están separados por espacios o comas.")
            return None
        except Exception as e:
            st.error(f"Ocurrió un error inesperado con la Matriz {matrix_name}: {e}")
            return None

    # --- Interfaz para introducir las matrices ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Matriz A")
        matrix_a_str = st.text_area(
            "Introduce la Matriz A (filas con saltos de línea, números con espacios/comas):",
            "1 2\n3 4",
            key="matrix_a",
            height=150
        )

    with col2:
        st.markdown("##### Matriz B")
        matrix_b_str = st.text_area(
            "Introduce la Matriz B (filas con saltos de línea, números con espacios/comas):",
            "5 6\n7 8",
            key="matrix_b",
            height=150
        )

    # --- Botones de operación ---
    op_col1, op_col2, op_col3 = st.columns(3)
    
    result_matrix = None
    operation_char = ""
    matrix_a, matrix_b = None, None

    if op_col1.button("Sumar (A + B)", use_container_width=True):
        matrix_a = parse_matrix(matrix_a_str, "A")
        matrix_b = parse_matrix(matrix_b_str, "B")
        
        if matrix_a is not None and matrix_b is not None:
            if matrix_a.shape == matrix_b.shape:
                result_matrix = matrix_a + matrix_b
                operation_char = "+"
            else:
                st.error("Las matrices deben tener las mismas dimensiones para poder sumarse.")

    if op_col2.button("Restar (A - B)", use_container_width=True):
        matrix_a = parse_matrix(matrix_a_str, "A")
        matrix_b = parse_matrix(matrix_b_str, "B")

        if matrix_a is not None and matrix_b is not None:
            if matrix_a.shape == matrix_b.shape:
                result_matrix = matrix_a - matrix_b
                operation_char = "-"
            else:
                st.error("Las matrices deben tener las mismas dimensiones para poder restarse.")

    if op_col3.button("Multiplicar (A × B)", use_container_width=True):
        matrix_a = parse_matrix(matrix_a_str, "A")
        matrix_b = parse_matrix(matrix_b_str, "B")

        if matrix_a is not None and matrix_b is not None:
            if matrix_a.shape[1] == matrix_b.shape[0]:
                result_matrix = np.dot(matrix_a, matrix_b)
                operation_char = "×"
            else:
                st.error(f"Para multiplicar, el número de columnas de A ({matrix_a.shape[1]}) debe ser igual al número de filas de B ({matrix_b.shape[0]}).")

    # --- Mostrar resultado ---
    if result_matrix is not None:
        st.markdown("---")
        st.subheader("Resultado")
        
        def format_matrix_for_display(matrix):
            return '\n'.join([' '.join(map(str, row)) for row in matrix])

        matrix_a_nice = format_matrix_for_display(matrix_a)
        matrix_b_nice = format_matrix_for_display(matrix_b)
        result_matrix_nice = format_matrix_for_display(result_matrix)

        res_col1, res_col2, res_col3, res_col4, res_col5 = st.columns([2,1,2,1,2])
        with res_col1:
            st.text_area("Matriz A", value=matrix_a_nice, disabled=True, height=150, key="res_a")
        with res_col2:
            st.markdown(f"<div style='text-align: center; font-size: 2em; padding-top: 40px;'>{operation_char}</div>", unsafe_allow_html=True)
        with res_col3:
            st.text_area("Matriz B", value=matrix_b_nice, disabled=True, height=150, key="res_b")
        with res_col4:
            st.markdown(f"<div style='text-align: center; font-size: 2em; padding-top: 40px;'>=</div>", unsafe_allow_html=True)
        with res_col5:
            st.text_area("Resultado", value=result_matrix_nice, disabled=True, height=150, key="res_c")

# --- OTRAS SECCIONES (PLACEHOLDERS) ---
elif selected_section in ["Física", "Geometría", "Estadística"]:
    st.title(f"{sections[selected_section]} {selected_section}")
    st.write(f"Aquí irán las herramientas y calculadoras para {selected_section}.")