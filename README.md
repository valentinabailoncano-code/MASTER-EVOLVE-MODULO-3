[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://master-evolve-modulo-3.streamlit.app/)

# 🧾 Sistema CRM en Streamlit

Aplicación web desarrollada en Python con Streamlit para gestionar usuarios y facturas, simulando un sistema CRM (Customer Relationship Management) básico.

> 📌 Proyecto individual desarrollado por **Valentina Bailón Cano** como parte del Máster en Data Science & Inteligencia Artificial en **Evolve**.

---

## 🚀 ¿Qué puedes hacer?

```text
- Registrar nuevos usuarios con validaciones
- Emitir facturas para cada usuario
- Consultar facturas por usuario
- Buscar usuarios por nombre o email
- Visualizar un resumen financiero (total, pagado y pendiente)
- Persistencia automática en archivos `.json`

---

## 🛠️ Cómo usar

#### ▶️ Ejecutar localmente


1. Clona este repositorio:

   git clone https://github.com/valentinabailoncano-code/MASTER-EVOLVE-MODULO-3.git
   cd MASTER-EVOLVE-MODULO-3

2. Instala las dependencias:

   pip install -r requirements.txt

3. Ejecuta la app:

   streamlit run proyecto/app.py

4. Se abrirá automáticamente en tu navegador.

---

### 🌐 Despliegue en Streamlit Cloud

1. Sube estos archivos a un repositorio de GitHub:
   - proyecto/app.py
   - data/usuarios.json
   - data/facturas.json
   - requirements.txt

2. Ve a https://streamlit.io/cloud y conecta tu cuenta de GitHub.

3. Elige tu repositorio y presiona "Deploy".


---

### 📁 Estructura del Proyecto

MASTER-EVOLVE-MODULO-3/
│
├── proyecto/
│   └── app.py                    # App principal en Streamlit
│
├── data/
│   ├── usuarios.json             # Base de datos de usuarios
│   └── facturas.json             # Base de datos de facturas
│
├── docs/
│   └── CRM_Valentina_Analisis_Tecnico_FINAL.docx
│
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo

---

### 💻 Comandos necesarios para que funcione el proyecto

💡 En Git Bash o terminal general

# Clonar el repositorio
git clone https://github.com/valentinabailoncano-code/MASTER-EVOLVE-MODULO-3.git
cd MASTER-EVOLVE-MODULO-3

# Crear y activar entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/Scripts/activate  # O .\venv\Scripts\activate en CMD/Powershell

# Instalar dependencias
pip install -r requirements.txt

# Lanzar la app
streamlit run proyecto/app.py

💡 En Visual Studio Code
1. Abrir la carpeta del proyecto (MASTER-EVOLVE-MODULO-3/)
2. Abrir una terminal integrada (View → Terminal)
3. Activar entorno virtual si lo creaste:
   .\venv\Scripts\activate
4. Ejecutar la app:
   streamlit run proyecto/app.py

---

### 👩‍💻 Autora

Valentina Bailón Cano  
Máster en Data Science & Inteligencia Artificial – EVOLVE  
LinkedIn: https://www.linkedin.com/in/valentina-bailon-2653b22b7
