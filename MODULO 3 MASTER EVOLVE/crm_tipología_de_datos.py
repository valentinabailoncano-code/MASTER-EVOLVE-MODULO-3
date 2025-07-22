# ===========================================================
# SISTEMA CRM POR CONSOLA CON PERSISTENCIA EN ARCHIVOS JSON
# ===========================================================
# Este sistema permite registrar usuarios y asociarles facturas.
# Se pueden realizar búsquedas, consultar resúmenes financieros
# y los datos se guardan automáticamente en disco para no perderse.

import datetime
import re
import json
import os

# -----------------------------------------------------------
# ARCHIVOS DE PERSISTENCIA
# -----------------------------------------------------------
# Guardamos los usuarios y facturas en archivos separados (.json)
# Esto nos permite mantener la información aunque el programa se cierre.
USUARIOS_FILE = "usuarios.json"
FACTURAS_FILE = "facturas.json"

# -----------------------------------------------------------
# FUNCIONES DE CARGA Y GUARDADO
# -----------------------------------------------------------
def cargar_datos():
    """Carga los datos desde archivos JSON si existen."""
    usuarios = {}
    facturas = []
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    if os.path.exists(FACTURAS_FILE):
        with open(FACTURAS_FILE, "r", encoding="utf-8") as f:
            facturas = json.load(f)
    return usuarios, facturas

def guardar_datos(usuarios, facturas):
    """Guarda los datos en archivos JSON para persistencia."""
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    with open(FACTURAS_FILE, "w", encoding="utf-8") as f:
        json.dump(facturas, f, indent=4, ensure_ascii=False)

# -----------------------------------------------------------
# VALIDACIONES Y GENERACIÓN DE IDS
# -----------------------------------------------------------
def email_valido(email):
    """Valida formato básico de email."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def generar_id_usuario(usuarios):
    """Genera un ID único para usuario, e.g. USR001"""
    contador = len(usuarios) + 1
    return f"USR{contador:03d}"

def generar_id_factura(facturas):
    """Genera un ID único para factura, e.g. FAC001"""
    contador = len(facturas) + 1
    return f"FAC{contador:03d}"

# -----------------------------------------------------------
# FUNCIONES DE NEGOCIO
# -----------------------------------------------------------
def registrar_usuario(usuarios, facturas):
    print("=== REGISTRO DE NUEVO USUARIO ===")
    nombre = input("Ingrese nombre: ").strip()
    apellidos = input("Ingrese apellidos: ").strip()
    email = input("Ingrese email: ").strip().lower()

    if not nombre or not apellidos or not email:
        print("Error: campos obligatorios vacíos.")
        return
    if not email_valido(email):
        print("Error: formato de email inválido.")
        return
    if email in usuarios:
        print("Error: ya existe un usuario con ese email.")
        return

    telefono = input("Ingrese teléfono (opcional): ").strip()
    direccion = input("Ingrese dirección (opcional): ").strip()
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    nuevo_id = generar_id_usuario(usuarios)

    usuarios[email] = {
        "id": nuevo_id,
        "nombre": f"{nombre} {apellidos}",
        "email": email,
        "telefono": telefono if telefono else "No especificado",
        "direccion": direccion if direccion else "No especificado",
        "fecha_registro": fecha
    }

    guardar_datos(usuarios, facturas)
    print(f"Usuario registrado con éxito. ID asignado: {nuevo_id}")

def buscar_usuario(usuarios):
    print("=== BUSCAR USUARIO ===")
    opcion = input("1. Buscar por email\n2. Buscar por nombre\nSeleccione opción: ")
    if opcion == "1":
        email = input("Ingrese email: ").strip().lower()
        usuario = usuarios.get(email)
        if usuario:
            imprimir_usuario(usuario)
        else:
            print("Usuario no encontrado.")
    elif opcion == "2":
        nombre = input("Ingrese nombre: ").strip().lower()
        encontrados = [u for u in usuarios.values() if nombre in u['nombre'].lower()]
        if encontrados:
            for u in encontrados:
                imprimir_usuario(u)
        else:
            print("No se encontraron coincidencias.")
    else:
        print("Opción inválida.")

def imprimir_usuario(usuario):
    print(f"""
ID: {usuario['id']}
Nombre: {usuario['nombre']}
Email: {usuario['email']}
Teléfono: {usuario['telefono']}
Dirección: {usuario['direccion']}
Fecha de registro: {usuario['fecha_registro']}
""")

def crear_factura(usuarios, facturas):
    print("=== CREAR FACTURA ===")
    email = input("Ingrese email del cliente: ").strip().lower()
    usuario = usuarios.get(email)
    if not usuario:
        print("Error: usuario no registrado.")
        return

    descripcion = input("Descripción del servicio/producto: ").strip()
    try:
        monto = float(input("Monto total (€): "))
        if monto <= 0:
            raise ValueError
    except ValueError:
        print("Error: monto no válido.")
        return

    estado_opc = {"1": "Pendiente", "2": "Pagada", "3": "Cancelada"}
    estado = input("Estado (1. Pendiente, 2. Pagada, 3. Cancelada): ").strip()
    estado_final = estado_opc.get(estado)
    if not estado_final:
        print("Estado inválido.")
        return

    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    numero = generar_id_factura(facturas)

    factura = {
        "numero": numero,
        "fecha": fecha,
        "descripcion": descripcion,
        "monto": monto,
        "estado": estado_final,
        "cliente": usuario['nombre'],
        "email": email
    }

    facturas.append(factura)
    guardar_datos(usuarios, facturas)
    print(f"Factura {numero} registrada correctamente.")

def listar_usuarios(usuarios):
    print("=== TODOS LOS USUARIOS ===")
    for i, u in enumerate(usuarios.values(), 1):
        print(f"""Usuario #{i}
ID: {u['id']}
Nombre: {u['nombre']}
Email: {u['email']}
Teléfono: {u['telefono']}
Registro: {u['fecha_registro']}
""")

def mostrar_facturas_usuario(usuarios, facturas):
    email = input("Email del usuario: ").strip().lower()
    usuario = usuarios.get(email)
    if not usuario:
        print("Usuario no encontrado.")
        return

    user_facts = [f for f in facturas if f['email'] == email]
    total = sum(f['monto'] for f in user_facts)
    pendientes = sum(f['monto'] for f in user_facts if f['estado'] == "Pendiente")

    print(f"Facturas de {usuario['nombre']}:")
    for f in user_facts:
        print(f"""
Factura: {f['numero']}
Fecha: {f['fecha']}
Descripción: {f['descripcion']}
Monto: €{f['monto']}
Estado: {f['estado']}
""")
    print(f"Total: €{total} / Pendiente: €{pendientes}")

def resumen_financiero(usuarios, facturas):
    print("=== RESUMEN FINANCIERO ===")
    total_facturas = 0
    total_ingresos = 0
    total_recibido = 0
    total_pendiente = 0

    for email, u in usuarios.items():
        user_facts = [f for f in facturas if f['email'] == email]
        total = sum(f['monto'] for f in user_facts)
        pagadas = sum(f['monto'] for f in user_facts if f['estado'] == "Pagada")
        pendientes = sum(f['monto'] for f in user_facts if f['estado'] == "Pendiente")

        print(f"""
Usuario: {u['nombre']} ({email})
- Facturas: {len(user_facts)}
- Total facturado: €{total}
- Pagado: €{pagadas}
- Pendiente: €{pendientes}
""")
        total_facturas += len(user_facts)
        total_ingresos += total
        total_recibido += pagadas
        total_pendiente += pendientes

    print(f"""
--- RESUMEN GENERAL ---
Usuarios: {len(usuarios)}
Facturas emitidas: {total_facturas}
Ingresos totales: €{total_ingresos}
Recibido: €{total_recibido}
Pendiente: €{total_pendiente}
""")

# -----------------------------------------------------------
# MENÚ PRINCIPAL
# -----------------------------------------------------------
def menu():
    usuarios, facturas = cargar_datos()
    while True:
        print("""
=== SISTEMA CRM ===
1. Registrar nuevo usuario
2. Buscar usuario
3. Crear factura para usuario
4. Mostrar todos los usuarios
5. Mostrar facturas de un usuario
6. Resumen financiero por usuario
7. Salir
""")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_usuario(usuarios, facturas)
        elif opcion == "2":
            buscar_usuario(usuarios)
        elif opcion == "3":
            crear_factura(usuarios, facturas)
        elif opcion == "4":
            listar_usuarios(usuarios)
        elif opcion == "5":
            mostrar_facturas_usuario(usuarios, facturas)
        elif opcion == "6":
            resumen_financiero(usuarios, facturas)
        elif opcion == "7":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

# -----------------------------------------------------------
# PUNTO DE ENTRADA
# -----------------------------------------------------------
if __name__ == "__main__":
    menu()
