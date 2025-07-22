import json
import datetime
import re
import os
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# ============================================
# -------- CARGA Y GUARDADO DE DATOS --------
# ============================================

USUARIOS_FILE = "data/usuarios.json"
FACTURAS_FILE = "data/facturas.json"

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

def generar_id(base, cantidad):
    return f"{base}{cantidad+1:03d}"

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

# ============================================
# -------- CLASES Y FUNCIONES PDF --------
# ============================================

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, self.title, ln=True, align="C")
        self.ln(10)

    def table(self, header, data, col_widths):
        self.set_font("Arial", "B", 10)
        for i, col in enumerate(header):
            self.cell(col_widths[i], 8, col, border=1)
        self.ln()
        self.set_font("Arial", "", 9)
        for row in data:
            for i, col in enumerate(row):
                self.cell(col_widths[i], 8, str(col), border=1)
            self.ln()

def generar_pdf_usuarios(usuarios):
    pdf = PDF()
    pdf.title = "Listado de Usuarios"
    pdf.add_page()
    header = ["Nombre", "Email", "Teléfono", "Registro"]
    rows = [[u["nombre"], u["email"], u["telefono"], u["fecha_registro"]] for u in usuarios.values()]
    pdf.table(header, rows, [40, 50, 40, 40])
    return pdf.output(dest='S').encode('latin1')

def generar_pdf_facturas(facturas):
    pdf = PDF()
    pdf.title = "Listado de Facturas"
    pdf.add_page()
    header = ["Cliente", "Email", "Fecha", "Monto"]
    rows = [[f["cliente"], f["email"], f["fecha"], f["monto"]] for f in facturas]
    pdf.table(header, rows, [40, 50, 40, 30])
    return pdf.output(dest='S').encode('latin1')

def boton_descarga_pdf(bytes_data, filename):
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 Descargar {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)

# ============================================
# -------- CARGA INICIAL --------
# ============================================

usuarios, facturas = cargar_datos()

# ============================================
# -------- CONFIGURACIÓN STREAMLIT --------
# ============================================

st.set_page_config(page_title="Sistema CRM", layout="wide")
st.title("📋 Sistema CRM - Gestión de Clientes y Facturación")

# ============================================
# -------- MENÚ LATERAL --------
# ============================================

menu = st.sidebar.radio("📁 Menú Principal", [
    "Registrar Usuario",
    "Crear Factura",
    "Ver Usuarios",
    "Buscar Usuario",
    "Facturas por Usuario",
    "Eliminar Usuario",
    "Resumen Financiero",
    "Ver Estadísticas",
    "Exportar Datos"
])

# ============================================
# -------- OPCIONES DEL MENÚ --------
# ============================================

if menu == "Registrar Usuario":
    st.subheader("➕ Registrar Nuevo Usuario")
    nombre = st.text_input("Nombre")
    apellidos = st.text_input("Apellidos")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono (opcional)")
    direccion = st.text_input("Dirección (opcional)")

    if st.button("Registrar"):
        email = email.strip().lower()
        if not nombre or not apellidos or not email:
            st.warning("❗ Nombre, apellidos y email son obligatorios.")
        elif not email_valido(email):
            st.warning("❗ Formato de email no válido.")
        elif email in usuarios:
            st.error("⚠️ Este email ya está registrado.")
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
            st.success(f"✅ Usuario registrado con ID {id_usuario}")

elif menu == "Crear Factura":
    st.subheader("🧾 Crear Factura")
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
            st.success("✅ Factura registrada correctamente.")
    else:
        st.info("ℹ️ No hay usuarios registrados.")

elif menu == "Ver Usuarios":
    st.subheader("📄 Lista de Usuarios Registrados")
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
        st.info("ℹ️ Aún no hay usuarios registrados.")

elif menu == "Buscar Usuario":
    st.subheader("🔍 Buscar Usuario")
    criterio = st.radio("Buscar por:", ["Email", "Nombre"])
    consulta = st.text_input("Introduce tu búsqueda")

    if st.button("Buscar"):
        resultados = []
        if criterio == "Email":
            usuario = usuarios.get(consulta.strip().lower())
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
            st.warning("⚠️ No se encontraron coincidencias.")

elif menu == "Facturas por Usuario":
    st.subheader("📑 Facturas por Usuario")
    if usuarios:
        selected_email = st.selectbox("Seleccionar Usuario", list(usuarios.keys()))
        user_facts = [f for f in facturas if f["email"] == selected_email]
        if user_facts:
            st.write(f"📄 Facturas de {usuarios[selected_email]['nombre']}:")
            st.table(user_facts)
        else:
            st.info("ℹ️ Este usuario no tiene facturas registradas.")
    else:
        st.info("ℹ️ No hay usuarios en el sistema.")

elif menu == "Eliminar Usuario":
    st.subheader("🗑️ Eliminar Usuario Registrado")
    if usuarios:
        selected_email = st.selectbox("Selecciona un usuario para eliminar", list(usuarios.keys()))
        usuario = usuarios[selected_email]
        st.write(f"**Nombre:** {usuario['nombre']}")
        st.write(f"**Email:** {usuario['email']}")
        confirm = st.checkbox("✅ Confirmar eliminación")

        if confirm and st.button("Eliminar"):
            del usuarios[selected_email]
            facturas = [f for f in facturas if f["email"] != selected_email]
            guardar_datos(usuarios, facturas)
            st.success("✅ Usuario y facturas eliminados correctamente.")
    else:
        st.info("ℹ️ No hay usuarios para eliminar.")

elif menu == "Resumen Financiero":
    st.subheader("📊 Resumen Financiero por Usuario")
    resumen = resumen_financiero(usuarios, facturas)
    if resumen:
        st.dataframe(resumen)
    else:
        st.info("ℹ️ No hay datos suficientes para mostrar el resumen.")

elif menu == "Ver Estadísticas":
    st.header("📈 Estadísticas del Sistema")
    if facturas:
        df_f = pd.DataFrame(facturas)
        df_f["fecha"] = pd.to_datetime(df_f["fecha"], format="%d/%m/%Y %H:%M")
        facturas_mes = df_f.groupby(df_f["fecha"].dt.to_period("M")).size()
        st.bar_chart(facturas_mes)
        st.metric("Facturas totales", len(facturas))
        st.metric("Importe medio (€)", round(df_f["monto"].mean(), 2))
    else:
        st.info("No hay datos de facturación disponibles.")

elif menu == "Exportar Datos":
    st.header("⬇️ Exportar datos como CSV o PDF")

    # CSV
    st.markdown("### 📥 Exportar como CSV")
    df_u = pd.DataFrame(usuarios).T
    df_f = pd.DataFrame(facturas)

    st.download_button("📥 Descargar CSV de Usuarios", data=df_u.to_csv(index=False), file_name="usuarios.csv", mime="text/csv")
    st.download_button("📥 Descargar CSV de Facturas", data=df_f.to_csv(index=False), file_name="facturas.csv", mime="text/csv")

    # PDF
    st.markdown("### 🧾 Exportar como PDF")
    if st.button("📤 Exportar Usuarios en PDF"):
        pdf_usuarios = generar_pdf_usuarios(usuarios)
        boton_descarga_pdf(pdf_usuarios, "usuarios.pdf")

    if st.button("📤 Exportar Facturas en PDF"):
        pdf_facturas = generar_pdf_facturas(facturas)
        boton_descarga_pdf(pdf_facturas, "facturas.pdf")
