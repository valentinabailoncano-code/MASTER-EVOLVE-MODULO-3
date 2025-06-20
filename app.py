import streamlit as st
import json
import datetime
import re
import os

# ---------- Cargar o inicializar datos ----------
USUARIOS_FILE = "usuarios.json"
FACTURAS_FILE = "facturas.json"

def cargar_datos():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    else:
        usuarios = {}

    if os.path.exists(FACTURAS_FILE):
        with open(FACTURAS_FILE, "r", encoding="utf-8") as f:
            facturas = json.load(f)
    else:
        facturas = []

    return usuarios, facturas

def guardar_datos(usuarios, facturas):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    with open(FACTURAS_FILE, "w", encoding="utf-8") as f:
        json.dump(facturas, f, indent=4, ensure_ascii=False)

usuarios, facturas = cargar_datos()

def generar_id(base, cantidad):
    return f"{base}{cantidad+1:03d}"

# ---------- Funciones de utilidad ----------
def email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def resumen_financiero(usuarios, facturas):
    resumen = []
    for email, u in usuarios.items():
        user_facts = [f for f in facturas if f['email'] == email]
        total = sum(f['monto'] for f in user_facts)
        pagadas = sum(f['monto'] for f in user_facts if f['estado'] == "Pagada")
        pendientes = sum(f['monto'] for f in user_facts if f['estado'] == "Pendiente")
        resumen.append({
            "Usuario": u['nombre'],
            "Email": email,
            "Facturas": len(user_facts),
            "Total (€)": total,
            "Pagado (€)": pagadas,
            "Pendiente (€)": pendientes
        })
    return resumen

# ---------- Interfaz Streamlit ----------
st.set_page_config(page_title="Sistema CRM", layout="wide")
st.title("Sistema CRM - Gestión de Clientes y Facturación")

menu = st.sidebar.radio("Menú", [
    "Registrar Usuario",
    "Crear Factura",
    "Ver Usuarios",
    "Buscar Usuario",
    "Facturas por Usuario",
    "Eliminar Usuario",
    "Resumen Financiero"
])

# ---------- Registrar Usuario ----------
if menu == "Registrar Usuario":
    st.subheader("Registrar Nuevo Usuario")
    nombre = st.text_input("Nombre")
    apellidos = st.text_input("Apellidos")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono (opcional)")
    direccion = st.text_input("Dirección (opcional)")

    if st.button("Registrar"):
        if not nombre or not apellidos or not email:
            st.warning("Nombre, apellidos y email son obligatorios.")
        elif not email_valido(email):
            st.warning("Formato de email no válido.")
        elif email in usuarios:
            st.error("Este email ya está registrado.")
        else:
            id_usuario = generar_id("USR", len(usuarios))
            usuarios[email] = {
                "id": id_usuario,
                "nombre": f"{nombre} {apellidos}",
                "email": email,
                "telefono": telefono if telefono else "No especificado",
                "direccion": direccion if direccion else "No especificado",
                "fecha_registro": datetime.date.today().strftime("%d/%m/%Y")
            }
            guardar_datos(usuarios, facturas)
            st.success(f"Usuario registrado con ID {id_usuario}")

# ---------- Crear Factura ----------
elif menu == "Crear Factura":
    st.subheader("Crear Factura")
    if usuarios:
        selected_email = st.selectbox("Seleccionar Usuario", list(usuarios.keys()))
        descripcion = st.text_input("Descripción del servicio/producto")
        monto = st.number_input("Monto total (€)", min_value=0.01)
        estado = st.selectbox("Estado", ["Pendiente", "Pagada", "Cancelada"])

        if st.button("Emitir Factura"):
            factura = {
                "numero": generar_id("FAC", len(facturas)),
                "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "descripcion": descripcion,
                "monto": monto,
                "estado": estado,
                "cliente": usuarios[selected_email]['nombre'],
                "email": selected_email
            }
            facturas.append(factura)
            guardar_datos(usuarios, facturas)
            st.success(f"Factura registrada correctamente.")
    else:
        st.info("No hay usuarios registrados.")

# ---------- Ver todos los usuarios ----------
elif menu == "Ver Usuarios":
    st.subheader("Lista de Usuarios Registrados")
    if usuarios:
        df = []
        for u in usuarios.values():
            df.append({
                "ID": u["id"],
                "Nombre": u["nombre"],
                "Email": u["email"],
                "Teléfono": u["telefono"],
                "Fecha de registro": u["fecha_registro"]
            })
        st.dataframe(df)
    else:
        st.info("Aún no hay usuarios registrados.")

# ---------- Buscar Usuario ----------
elif menu == "Buscar Usuario":
    st.subheader("Buscar Usuario")
    criterio = st.radio("Buscar por:", ["Email", "Nombre"])
    consulta = st.text_input("Introduce tu búsqueda")

    if st.button("Buscar"):
        resultados = []
        if criterio == "Email":
            usuario = usuarios.get(consulta)
            if usuario:
                resultados.append(usuario)
        else:
            resultados = [u for u in usuarios.values() if consulta.lower() in u['nombre'].lower()]

        if resultados:
            for u in resultados:
                st.write(f"**{u['nombre']}** ({u['email']})")
                st.write(f"- Teléfono: {u['telefono']}")
                st.write(f"- Dirección: {u['direccion']}")
                st.write(f"- Fecha de registro: {u['fecha_registro']}")
        else:
            st.warning("No se encontraron coincidencias.")

# ---------- Facturas por Usuario ----------
elif menu == "Facturas por Usuario":
    st.subheader("Facturas por Usuario")
    if usuarios:
        selected_email = st.selectbox("Seleccionar Usuario", list(usuarios.keys()))
        user_facts = [f for f in facturas if f["email"] == selected_email]
        if user_facts:
            st.write(f"Facturas de {usuarios[selected_email]['nombre']}:")
            st.table(user_facts)
        else:
            st.info("Este usuario no tiene facturas registradas.")
    else:
        st.info("No hay usuarios en el sistema.")

# ---------- Eliminar Usuario ----------
elif menu == "Eliminar Usuario":
    st.subheader("Eliminar Usuario Registrado")
    if usuarios:
        selected_email = st.selectbox("Selecciona un usuario para eliminar", list(usuarios.keys()))
        usuario = usuarios[selected_email]
        st.write(f"**Nombre:** {usuario['nombre']}")
        st.write(f"**Email:** {usuario['email']}")
        confirm = st.checkbox("Confirmar eliminación")

        if confirm and st.button("Eliminar"):
            del usuarios[selected_email]
            facturas = [f for f in facturas if f["email"] != selected_email]
            guardar_datos(usuarios, facturas)
            st.success("Usuario y facturas eliminados correctamente.")
    else:
        st.info("No hay usuarios para eliminar.")

# ---------- Resumen Financiero ----------
elif menu == "Resumen Financiero":
    st.subheader("Resumen Financiero por Usuario")
    resumen = resumen_financiero(usuarios, facturas)
    if resumen:
        st.dataframe(resumen)
    else:
        st.info("No hay datos suficientes para mostrar el resumen.")