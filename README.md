# Pokédex

Aplicación web desarrollada con **Python y Django** que permite explorar el mundo Pokémon, consultar información de diferentes especies, gestionar entrenadores y organizar sus equipos Pokémon.

---

## 📌 DESCRIPCIÓN DEL PROYECTO

**Pokédex** es una aplicación web inspirada en el universo Pokémon, desarrollada utilizando Python y el framework Django.

Su objetivo es ofrecer una plataforma interactiva en la que los usuarios puedan consultar información de Pokémon mediante la API pública **PokéAPI**, evitando tener que registrar manualmente toda la información de cada especie.

Además, el sistema permite administrar entrenadores Pokémon, gestionar sus equipos, consultar gimnasios y organizar la información relacionada con el mundo Pokémon.

La aplicación cuenta con una interfaz personalizada inspirada en el diseño de una Pokédex, con diferentes apartados para facilitar la navegación y la gestión de la información.

## FUNCIONALIDADES PRINCIPALES

- **Exploración de Pokémon:** consulta de diferentes Pokémon utilizando la API PokéAPI.
- **Búsqueda de Pokémon:** permite buscar especies por su nombre.
- **Paginación:** navegación entre las diferentes páginas del catálogo.
- **Información detallada:** visualización de imágenes, estadísticas, tipos, habilidades y otros datos de cada Pokémon.
- **Gestión de entrenadores:** registro, consulta, edición y eliminación de entrenadores.
- **Equipos Pokémon:** asociación de Pokémon a los entrenadores registrados.
- **Gestión de gimnasios:** apartado para consultar y administrar gimnasios Pokémon.
- **Diseño personalizado:** interfaz inspirada en los colores y elementos visuales de una Pokédex.
- **Integración con API:** obtención de información mediante PokéAPI.

## 🛠️ TECNOLOGÍAS UTILIZADAS

### Backend
- Python 3.13
- Django 6.1
- Requests (consumo de API REST)

### Frontend
- HTML5
- CSS3
- JavaScript

### Base de datos
- PostgreSQL
- Django ORM

### API externa
- [PokéAPI](https://pokeapi.co/)

### Herramientas
- Git
- GitHub
- Visual Studio Code
- Entorno virtual de Python (venv)

## REQUISITOS PREVIOS

Antes de ejecutar el proyecto necesitas tener instalado:

- Python 3.13 o compatible.
- Git.
- pip.
- PostgreSQL (si utilizas la configuración de base de datos PostgreSQL).

## ⚙️ INSTALACIÓN

### 1. Clonar el repositorio

```bash
git clone https://github.com/LegnaF/Pokedex.git
```

### 2. Entrar a la carpeta del proyecto

```bash
cd Pokedex
```

### 3. Crear un entorno virtual

```bash
python -m venv env
```

### 4. Activar el entorno virtual

**Windows PowerShell:**

```powershell
.\env\Scripts\Activate.ps1
```

**Windows CMD:**

```cmd
env\Scripts\activate
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Ejecutar las migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

### 8. Abrir el proyecto

Abre tu navegador e ingresa a:

http://127.0.0.1:8000/

## ESTRUCTURA DEL PROYECTO

```text
Pokedex/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pokedex/
│   ├── migrations/
│   ├── templates/
│   │   ├── pokedex/
│   │   ├── create/
│   │   └── edit/
│   │
│   ├── static/
│   │   ├── pokedex/
│   │   ├── create/
│   │   └── edit/
│   │
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
└── env/
```

*La estructura es una representación general y puede variar según la organización actual de los archivos del proyecto.*

## 🌐 API UTILIZADA

Este proyecto utiliza **PokéAPI**, una API REST pública que proporciona información del universo Pokémon.

Permite obtener datos como:

- Nombre e identificador del Pokémon.
- Imágenes oficiales.
- Tipos.
- Estadísticas.
- Habilidades.
- Información de evolución.

Documentación oficial:

https://pokeapi.co/docs/v2

## AUTOR

**LegnaF**

GitHub: https://github.com/LegnaF

## REPOSITORIO

Puedes encontrar el código fuente del proyecto en:

https://github.com/LegnaF/Pokedex

## LICENCIA

Proyecto desarrollado con fines educativos y de aprendizaje, como parte de la práctica y fortalecimiento de conocimientos en desarrollo de software utilizando Python y Django.
