import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Entrenador, Gym
from django.db.models import Q
from django.http import Http404
from math import ceil
from concurrent.futures import ThreadPoolExecutor
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.db import IntegrityError, transaction
from .forms import FormsEntrenador, FormsGym




def inicio(request):
    return render(request, 'pokedex/inicio.html')









# ==========================================
# CONSULTAR UN POKÉMON
# ==========================================

def obtener_pokemon(url):

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()

        datos = respuesta.json()

        return {
            'id': datos['id'],
            'nombre': datos['name'],
            'imagen': datos['sprites']['other']['official-artwork']['front_default'],
            'tipo1': datos['types'][0]['type']['name'],
            'tipo2': datos['types'][1]['type']['name']
                     if len(datos['types']) > 1 else None,
        }

    except (requests.RequestException, KeyError, IndexError):
        return None


# ==========================================
# LISTADO DE POKÉMON
# ==========================================

@cache_page(60 * 15)
def pokemon(request):

    url = "https://pokeapi.co/api/v2/pokemon/"

    buscar = request.GET.get('buscar', '').strip()
    pagina = request.GET.get('pagina', '1')

    pokemones = []
    total_pokemones = 0
    total_paginas = 0

    try:

        # ==================================
        # BUSCADOR
        # ==================================

        if buscar:

            pokemon_encontrado = obtener_pokemon(
                f"{url}{buscar.lower()}/"
            )

            if pokemon_encontrado:
                pokemones.append(pokemon_encontrado)

        # ==================================
        # LISTADO CON PAGINACIÓN
        # ==================================

        else:

            try:
                pagina = max(1, int(pagina))
            except ValueError:
                pagina = 1

            limite = 20
            offset = (pagina - 1) * limite

            respuesta = requests.get(
                f"{url}?limit={limite}&offset={offset}",
                timeout=10
            )

            respuesta.raise_for_status()

            datos = respuesta.json()

            total_pokemones = datos['count']
            total_paginas = ceil(total_pokemones / limite)

            # Consultar los 20 Pokémon simultáneamente
            with ThreadPoolExecutor(max_workers=10) as executor:

                resultados = executor.map(
                    obtener_pokemon,
                    [resultado['url'] for resultado in datos['results']]
                )

                pokemones = [
                    resultado
                    for resultado in resultados
                    if resultado is not None
                ]

    except requests.RequestException:

        pokemones = []

    # ==================================
    # CONTEXTO
    # ==================================

    pagina_actual = pagina if not buscar else 1

    contexto = {
        'pokemones': pokemones,
        'total_pokemones': total_pokemones,
        'total_paginas': total_paginas,
        'pagina_actual': pagina_actual,
        'pagina_anterior': max(1, pagina_actual - 1),
        'pagina_siguiente': pagina_actual + 1,
        'buscar': buscar,
    }

    return render(
        request,
        'pokedex/pokemon.html',
        contexto
    )






def entrenadores(request):

    lista_entrenadores = Entrenador.objects.all().order_by('nombre')

    buscar = request.GET.get('buscar', '').strip()

    if buscar:
        lista_entrenadores = lista_entrenadores.filter(
            Q(nombre__icontains=buscar) |
            Q(apellido__icontains=buscar) |
            Q(documento__icontains=buscar) |
            Q(pueblo__icontains=buscar)
        )

    contexto = {
        'entrenadores': lista_entrenadores,
        'total_entrenadores': lista_entrenadores.count(),
        'buscar': buscar
    }

    return render(request, 'pokedex/entrenadores.html', contexto)







def pokemon_detalle(request, pokemon_id):

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"

    try:
        respuesta = requests.get(url, timeout=15)
        respuesta.raise_for_status()

        datos = respuesta.json()

        # Obtener imagen oficial
        imagen = datos['sprites']['other']['official-artwork']['front_default']

        # Imagen alternativa si no existe la oficial
        if not imagen:
            imagen = datos['sprites']['front_default']

        # Preparar datos para el HTML
        datos['imagen'] = imagen
        datos['height_m'] = datos['height'] / 10
        datos['weight_kg'] = datos['weight'] / 10

    except requests.RequestException:
        raise Http404("No se pudo encontrar el Pokémon solicitado.")

    contexto = {
        'pokemon': datos
    }

    return render(request, 'pokedex/pokemon_detalle.html', contexto)







def registrar_entrenador(request):

    if request.method == 'POST':

        form = FormsEntrenador(request.POST)

        if form.is_valid():

            # Obtener los identificadores seleccionados desde el HTML
            pokemon_ids = list(set(request.POST.getlist('pokemon')))

            if not pokemon_ids:
                form.add_error(
                    None,
                    'Debes seleccionar al menos un Pokémon.'
                )

            else:
                try:
                    pokemones_seleccionados = []

                    # Consultar cada Pokémon en PokéAPI
                    for pokemon_id in pokemon_ids:

                        if not pokemon_id.isdigit():
                            raise ValueError(
                                'Uno de los Pokémon seleccionados no es válido.'
                            )

                        respuesta = requests.get(
                            f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/',
                            timeout=10
                        )

                        respuesta.raise_for_status()

                        datos = respuesta.json()

                        # Obtener los tipos
                        tipos = datos.get('types', [])

                        if not tipos:
                            raise ValueError(
                                'No se encontraron los tipos del Pokémon.'
                            )

                        tipo1 = tipos[0]['type']['name']

                        tipo2 = (
                            tipos[1]['type']['name']
                            if len(tipos) > 1 else None
                        )

                        # Obtener la habilidad
                        habilidades = datos.get('abilities', [])

                        habilidad = (
                            habilidades[0]['ability']['name']
                            if habilidades else 'Desconocida'
                        )

                        # Obtener la imagen
                        sprites = datos.get('sprites', {})

                        imagen = (
                            sprites.get('other', {})
                            .get('official-artwork', {})
                            .get('front_default')
                            or sprites.get('front_default')
                        )

                        if not imagen:
                            raise ValueError(
                                f'No se encontró una imagen para {datos["name"]}.'
                            )

                        # Obtener estadísticas
                        estadisticas = {
                            estadistica['stat']['name']:
                            estadistica['base_stat']
                            for estadistica in datos.get('stats', [])
                        }

                        # Guardar o recuperar el Pokémon de PostgreSQL
                        pokemon, creado = Pokemon.objects.get_or_create(
                            nombre=datos['name'],
                            defaults={
                                'imagen': imagen,
                                'estadisticas': estadisticas,
                                'tipo1': tipo1,
                                'tipo2': tipo2,
                                'habilidad': habilidad,
                                'evolucion': '',
                                'legendario': False,
                            }
                        )

                        pokemones_seleccionados.append(pokemon)

                    # Guardar entrenador y relacionar sus Pokémon
                    with transaction.atomic():

                        entrenador = form.save()

                        entrenador.pokemon.set(
                            pokemones_seleccionados
                        )

                    messages.success(
                        request,
                        '¡Entrenador registrado correctamente!'
                    )

                    return redirect('entrenadores')

                except ValueError as error:

                    form.add_error(None, str(error))

                except requests.RequestException:

                    form.add_error(
                        None,
                        'No fue posible consultar PokéAPI. Intenta nuevamente.'
                    )

                except (KeyError, TypeError, IndexError):

                    form.add_error(
                        None,
                        'Ocurrió un problema al procesar los datos del Pokémon.'
                    )

    else:
        form = FormsEntrenador()

    contexto = {
        'form': form
    }

    return render(
        request,
        'create/entrenador.html',
        contexto
    )


def obtener_o_registrar_pokemon(api_id):

    respuesta = requests.get(
        f'https://pokeapi.co/api/v2/pokemon/{api_id}/',
        timeout=10
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    nombre = datos['name']

    imagen = (
        datos['sprites']['other']['official-artwork']['front_default']
        or datos['sprites']['front_default']
    )

    tipos = datos['types']

    tipo1 = tipos[0]['type']['name']
    tipo2 = tipos[1]['type']['name'] if len(tipos) > 1 else None

    estadisticas = {
        estadistica['stat']['name']: estadistica['base_stat']
        for estadistica in datos['stats']
    }

    habilidad = datos['abilities'][0]['ability']['name'] if datos['abilities'] else ''

    pokemon, creado = Pokemon.objects.get_or_create(
        nombre=nombre,
        defaults={
            'imagen': imagen,
            'estadisticas': estadisticas,
            'tipo1': tipo1,
            'tipo2': tipo2,
            'habilidad': habilidad,
            'evolucion': '',
            'legendario': False
        }
    )

    return pokemon


def editar_entrenador(request, entrenador_id):

    entrenador = get_object_or_404(Entrenador, id=entrenador_id)

    if request.method == 'POST':

        form = FormsEntrenador(
            request.POST,
            request.FILES,
            instance=entrenador
        )

        if form.is_valid():

            # Pokémon que ya existen en la base de datos
            pokemon_ids = request.POST.getlist('pokemon')

            # Pokémon nuevos seleccionados desde PokéAPI
            pokemon_api_ids = request.POST.getlist('pokemon_api')

            if not pokemon_ids and not pokemon_api_ids:

                form.add_error(
                    None,
                    'Debes seleccionar al menos un Pokémon.'
                )

            else:

                try:
                    with transaction.atomic():

                        # Guardar los datos del entrenador
                        entrenador = form.save()

                        pokemon_seleccionados = list(
                            Pokemon.objects.filter(id__in=pokemon_ids)
                        )

                        # Consultar y registrar los nuevos Pokémon
                        for api_id in pokemon_api_ids:

                            pokemon = obtener_o_registrar_pokemon(api_id)

                            if pokemon not in pokemon_seleccionados:
                                pokemon_seleccionados.append(pokemon)

                        # Actualizar los Pokémon relacionados
                        entrenador.pokemon.set(pokemon_seleccionados)

                    messages.success(
                        request,
                        'Entrenador actualizado correctamente.'
                    )

                    return redirect('entrenadores')

                except (requests.RequestException, ValueError, KeyError, TypeError) as error:

                    messages.error(
                        request,
                        f'No fue posible registrar los Pokémon: {error}'
                    )

    else:

        form = FormsEntrenador(instance=entrenador)

    contexto = {
        'form': form,
        'entrenador': entrenador,
        'pokemon_seleccionados': entrenador.pokemon.all()
    }

    return render(request,'edit/entrenador.html',contexto)


def eliminar_entrenador(request, entrenador_id):

    entrenador = get_object_or_404(Entrenador, id=entrenador_id)

    if request.method == 'POST':

        nombre = entrenador.nombre
        apellido = entrenador.apellido

        entrenador.delete()

        messages.success(
            request,
            f'El entrenador {nombre} {apellido} fue eliminado correctamente.'
        )

        return redirect('entrenadores')

    contexto = {
        'entrenador': entrenador
    }

    return render(request, 'eliminate/entrenador.html', contexto)



def entrenador_detalle(request, entrenador_id):

    entrenador = get_object_or_404(
        Entrenador,
        id=entrenador_id
    )

    equipo_pokemon = entrenador.pokemon.all()

    contexto = {
        'entrenador': entrenador,
        'equipo_pokemon': equipo_pokemon,
        'total_pokemon': equipo_pokemon.count()
    }

    return render(
        request,
        'pokedex/entrenador_detalle.html',
        contexto
    )



def gimnasios(request):

    lista_gimnasios = Gym.objects.all().order_by('lider_gimnasio')

    # Obtener el texto de búsqueda
    buscar = request.GET.get('buscar', '').strip()

    # Filtrar los gimnasios
    if buscar:
        lista_gimnasios = lista_gimnasios.filter(
            Q(lider_gimnasio__icontains=buscar) |
            Q(tipo_elemento__icontains=buscar) |
            Q(medalla__icontains=buscar) |
            Q(ciudad__icontains=buscar) |
            Q(telefono__icontains=buscar) |
            Q(region__icontains=buscar)
        )

    # Preparar los datos para el HTML
    contexto = {
        'gimnasios': lista_gimnasios,
        'total_gimnasios': lista_gimnasios.count(),
        'buscar': buscar
    }

    return render(request, 'pokedex/gimnasios.html', contexto)



def agregar_gimnasio(request):

    if request.method == 'POST':

        form = FormsGym(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Gimnasio registrado correctamente.'
            )

            return redirect('gimnasios')

    else:
        form = FormsGym()

    contexto = {
        'form': form
    }

    return render(request, 'create/gimnasio.html', contexto)


def detalle_gimnasio(request, gimnasio_id):

    gimnasio = get_object_or_404(Gym, id=gimnasio_id)

    contexto = {
        'gimnasio': gimnasio
    }

    return render(
        request,
        'detail/gimnasio.html',
        contexto
    )

def editar_gimnasio(request, gimnasio_id):

    gimnasio = get_object_or_404(Gym, id=gimnasio_id)

    if request.method == 'POST':

        form = FormsGym(request.POST, instance=gimnasio)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Gimnasio actualizado correctamente.'
            )

            return redirect('gimnasios')

    else:
        form = FormsGym(instance=gimnasio)

    contexto = {
        'form': form,
        'gimnasio': gimnasio
    }

    return render(
        request,
        'edit/gimnasio.html',
        contexto
    )

def eliminar_gimnasio(request, gimnasio_id):
    gimnasio = get_object_or_404(Gym, id=gimnasio_id)

    if request.method == 'POST':
        nombre = gimnasio.lider_gimnasio
        gimnasio.delete()

        messages.success(
            request,
            f'El gimnasio de {nombre} fue eliminado correctamente.'
        )

        return redirect('gimnasios')

    contexto = {'gimnasio': gimnasio}

    return render(request, 'eliminate/gimnasio.html', contexto)



def probar_api(request):

    try:
        respuesta = requests.get(
            'https://pokeapi.co/api/v2/pokemon/pikachu/',
            timeout=15
        )

        print("ESTADO:", respuesta.status_code)

        respuesta.raise_for_status()

        datos = respuesta.json()

        print("NOMBRE:", datos['name'])
        print("ID:", datos['id'])

        return render(request, 'pokedex/inicio.html')

    except requests.RequestException as error:

        print("ERROR DE API:", error)

        raise