import datetime
import re
import json

# ===========================================================
# SISTEMA CRM POR CONSOLA CON PERSISTENCIA EN ARCHIVOS JSON
# ===========================================================
# Este sistema permite registrar usuarios y asociarles facturas.
# Se pueden realizar búsquedas, consultar resúmenes financieros
# y los datos se guardan automáticamente en disco para no perderse.

# -----------------------------------------------------------
# ARCHIVOS DE PERSISTENCIA
# -----------------------------------------------------------
# Guardamos los usuarios y facturas en archivos separados (.json)
# Esto nos permite mantener la información aunque el programa se cierre.
USUARIOS_FILE = "usuarios.json"
FACTURAS_FILE = "facturas.json"

# -----------------------------------------------------------
# FUNCIONES DE CARGA Y GUARDADO DE DATOS
# -----------------------------------------------------------
def cargar_datos():
    """Carga los datos desde archivos JSON si existen."""
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = {}
    try:
        with open(FACTURAS_FILE, "r", encoding="utf-8") as f:
            facturas = json.load(f)
    except FileNotFoundError:
        facturas = []
    return usuarios, facturas

def guardar_datos():
    """Guarda los datos en archivos JSON para mantener persistencia."""
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    with open(FACTURAS_FILE, "w", encoding="utf-8") as f:
        json.dump(facturas, f, indent=4, ensure_ascii=False)

# -----------------------------------------------------------
# VARIABLES GLOBALES INICIALES
# -----------------------------------------------------------
# Al iniciar el sistema, cargamos los datos existentes (si los hay)
usuarios, facturas = cargar_datos()

# Los contadores se basan en el número de entradas actuales
contador_usuarios = len(usuarios) + 1
contador_facturas = len(facturas) + 1

# -----------------------------------------------------------
# FUNCIONES DE UTILIDAD
# -----------------------------------------------------------
def generar_id_usuario():
    """Genera un ID único para cada usuario nuevo."""
    global contador_usuarios
    nuevo_id = f"USR{contador_usuarios:03d}"  # USR001, USR002...
    contador_usuarios += 1
    return nuevo_id

def generar_id_factura():
    """Genera un ID único para cada factura nueva."""
    global contador_facturas
    nuevo_id = f"FAC{contador_facturas:03d}"  # FAC001, FAC002...
    contador_facturas += 1
    return nuevo_id

def email_valido(email):
    """Valida que el email tenga un formato correcto."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# -----------------------------------------------------------
# REGISTRO DE USUARIOS
# -----------------------------------------------------------
def registrar_usuario():
    """Registra un nuevo usuario con validaciones obligatorias."""
    print("=== REGISTRO DE NUEVO USUARIO ===")
    nombre = input("Ingrese nombre: ").strip()
    apellidos = input("Ingrese apellidos: ").strip()
    email = input("Ingrese email: ").strip()

    # Validaciones obligatorias
    if not nombre or not apellidos or not email:
        print("Error: campos obligatorios vacíos.")
        return
    if not email_valido(email):
        print("Error: formato de email inválido.")
        return
    if email in usuarios:
        print("Error: ya existe un usuario con ese email.")
        return

    # Campos opcionales
    telefono = input("Ingrese teléfono (opcional): ").strip()
    direccion = input("Ingrese dirección (opcional): ").strip()
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    nuevo_id = generar_id_usuario()

    # Guardamos los datos en el diccionario de usuarios
    usuarios[email] = {
        "id": nuevo_id,
        "nombre": f"{nombre} {apellidos}",
        "email": email,
        "telefono": telefono if telefono else "No especificado",
        "direccion": direccion if direccion else "No especificado",
        "fecha_registro": fecha
    }

    # Persistencia automática
    guardar_datos()
    print(f"Usuario registrado con éxito. ID asignado: {nuevo_id}")

# -----------------------------------------------------------
# BÚSQUEDA DE USUARIOS
# -----------------------------------------------------------
def buscar_usuario():
    """Permite buscar un usuario por email o por nombre."""
    print("=== BUSCAR USUARIO ===")
    metodo = input("1. Buscar por email\n2. Buscar por nombre\nSeleccione opción: ")
    if metodo == "1":
        email = input("Ingrese email: ").strip()
        usuario = usuarios.get(email)
        if usuario:
            imprimir_usuario(usuario)
        else:
            print("Usuario no encontrado.")
    elif metodo == "2":
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
    """Imprime la información detallada de un usuario."""
    print(f"""\nID: {usuario['id']}
Nombre: {usuario['nombre']}
Email: {usuario['email']}
Teléfono: {usuario['telefono']}
Dirección: {usuario['direccion']}
Fecha de registro: {usuario['fecha_registro']}\n""")

# -----------------------------------------------------------
# CREACIÓN DE FACTURAS
# -----------------------------------------------------------
def crear_factura():
    """Permite crear una factura asociada a un usuario existente."""
    print("=== CREAR FACTURA ===")
    email = input("Ingrese email del cliente: ").strip()
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

    estado = input("Estado (1. Pendiente, 2. Pagada, 3. Cancelada): ").strip()
    estado_final = {"1": "Pendiente", "2": "Pagada", "3": "Cancelada"}.get(estado)
    if not estado_final:
        print("Estado inválido.")
        return

    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    numero = generar_id_factura()

    # Creamos la factura con la información proporcionada
    factura = {
        "numero": numero,
        "fecha": fecha,
        "descripcion": descripcion,
        "monto": monto,
        "estado": estado_final,
        "cliente": usuario['nombre'],
        "email": email
    }

    # La agregamos al registro y guardamos
    facturas.append(factura)
    guardar_datos()
    print(f"Factura {numero} registrada correctamente.")

# -----------------------------------------------------------
# LISTADO DE TODOS LOS USUARIOS
# -----------------------------------------------------------
def listar_usuarios():
    """Lista todos los usuarios registrados en el sistema."""
    print("=== TODOS LOS USUARIOS ===")
    for i, u in enumerate(usuarios.values(), 1):
        print(f"""Usuario #{i}
ID: {u['id']}
Nombre: {u['nombre']}
Email: {u['email']}
Teléfono: {u['telefono']}
Registro: {u['fecha_registro']}\n""")

# -----------------------------------------------------------
# CONSULTA DE FACTURAS POR USUARIO
# -----------------------------------------------------------
def mostrar_facturas_usuario():
    """Muestra las facturas de un usuario específico."""
    email = input("Email del usuario: ").strip()
    usuario = usuarios.get(email)
    if not usuario:
        print("Usuario no encontrado.")
        return
    user_facts = [f for f in facturas if f['email'] == email]
    total = sum(f['monto'] for f in user_facts)
    pendientes = sum(f['monto'] for f in user_facts if f['estado'] == "Pendiente")
    print(f"Facturas de {usuario['nombre']}:")
    for f in user_facts:
        print(f"""\nFactura: {f['numero']}
Fecha: {f['fecha']}
Descripción: {f['descripcion']}
Monto: €{f['monto']}
Estado: {f['estado']}\n""")

    print(f"Total: €{total} / Pendiente: €{pendientes}")

# -----------------------------------------------------------
# RESUMEN FINANCIERO POR USUARIO
# -----------------------------------------------------------
def resumen_financiero():
    """Muestra resumen de facturación total, pagada y pendiente por usuario y global."""
    print("=== RESUMEN FINANCIERO ===")
    total_fact = 0
    total_ing = 0
    total_recibido = 0
    total_pendiente = 0
    for email, u in usuarios.items():
        user_facts = [f for f in facturas if f['email'] == email]
        total = sum(f['monto'] for f in user_facts)
        pagadas = sum(f['monto'] for f in user_facts if f['estado'] == "Pagada")
        pendientes = sum(f['monto'] for f in user_facts if f['estado'] == "Pendiente")
        print(f"""\nUsuario: {u['nombre']} ({email})
- Facturas: {len(user_facts)}
- Total facturado: €{total}
- Pagado: €{pagadas}
- Pendiente: €{pendientes}""")
        total_fact += len(user_facts)
        total_ing += total
        total_recibido += pagadas
        total_pendiente += pendientes

    print(f"""\n--- RESUMEN GENERAL ---
Usuarios: {len(usuarios)}
Facturas emitidas: {total_fact}
Ingresos totales: €{total_ing}
Recibido: €{total_recibido}
Pendiente: €{total_pendiente}""")

# -----------------------------------------------------------
# MENÚ PRINCIPAL DEL SISTEMA
# -----------------------------------------------------------
def menu():
    """Muestra el menú principal con opciones disponibles."""
    while True:
        print("""\n=== SISTEMA CRM ===
1. Registrar nuevo usuario
2. Buscar usuario
3. Crear factura para usuario
4. Mostrar todos los usuarios
5. Mostrar facturas de un usuario
6. Resumen financiero por usuario
7. Salir""")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            buscar_usuario()
        elif opcion == "3":
            crear_factura()
        elif opcion == "4":
            listar_usuarios()
        elif opcion == "5":
            mostrar_facturas_usuario()
        elif opcion == "6":
            resumen_financiero()
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
