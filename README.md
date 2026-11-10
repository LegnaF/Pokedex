
# POKEDEX

Aplicación web desarrollada con Python y Django para explorar y consultar información de Pokémon.

---

## DESCRIPCIÓN DEL PROYECTO

Pokedex es una aplicación web desarrollada utilizando Python y Django. Su objetivo es ofrecer una plataforma para consultar y visualizar información relacionada con el mundo Pokémon.

---

## TECNOLOGÍAS UTILIZADAS

- Python
- Django
- HTML5
- CSS3
- JavaScript
- PostgreSQL

---

## REQUISITOS PREVIOS

Antes de ejecutar el proyecto necesitas tener instalado:

- Python
- Git
- pip

---

## INSTALACIÓN

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
python -m venv venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

En Windows CMD:

```bash
venv\Scripts\activate
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Ejecutar las migraciones

```bash
python manage.py migrate
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

### 8. Abrir el proyecto

Abre tu navegador e ingresa a:

http://127.0.0.1:8000/

---

## ESTRUCTURA DEL PROYECTO

```text
Pokedex/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── nombre_de_tu_app/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
└── static/
```

---

## AUTOR

**LegnaF**

GitHub: https://github.com/LegnaF

---

## REPOSITORIO

Puedes encontrar el código fuente aquí:

https://github.com/LegnaF/Pokedex

---

## LICENCIA

Proyecto desarrollado con fines educativos y de aprendizaje.
