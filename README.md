[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://master-evolve-modulo-3.streamlit.app/)


# 🧾 Sistema CRM en Streamlit

Aplicación web desarrollada en Python con Streamlit para gestionar usuarios y facturas, simulando un sistema CRM (Customer Relationship Management) básico.

---

## 🚀 ¿Qué puedes hacer?

- Registrar nuevos usuarios con validaciones
- Emitir facturas para cada usuario
- Consultar facturas por usuario
- Buscar usuarios por nombre o email
- Visualizar un resumen financiero (total, pagado y pendiente)
- Persistencia automática en archivos `.json`

---

## 🛠️ Cómo usar

### ▶️ Ejecutar localmente

1. Clona este repositorio:
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

2. Instala las dependencias:
```bash
pip install streamlit
```

3. Ejecuta la app:
```bash
streamlit run app.py
```

4. Se abrirá automáticamente en tu navegador.

---

## 🌐 Despliegue en Streamlit Cloud

1. Sube los archivos a un repositorio de GitHub:
   - `app.py`
   - `usuarios.json`
   - `facturas.json`
   - `requirements.txt` (contiene al menos `streamlit`)

2. Ve a [https://streamlit.io/cloud](https://streamlit.io/cloud) y conecta tu cuenta de GitHub.

3. Elige el repositorio y despliega la app.

---

## 📁 Archivos clave

- `app.py` → código principal de la app en Streamlit.
- `usuarios.json` → almacena los datos de los usuarios.
- `facturas.json` → almacena las facturas.
- `requirements.txt` → lista de dependencias.

---

## 👩‍💻 Autora

Valentina Bailón Cano — Proyecto académico del Máster en Data Science & IA en Evolve.
