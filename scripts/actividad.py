import argparse
import base64
import json
import os
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ORGANIZACION = 'Colorado-Roleplay-Company'
REPOSITORIO = ORGANIZACION + '/.github'
DESARROLLADOR = 'em4nu3i69dll'
INICIO = '<!-- ACTIVIDAD:INICIO -->'
FIN = '<!-- ACTIVIDAD:FIN -->'
ZONA = timezone(timedelta(hours=-3))


def api(ruta, datos=None, metodo=None):
    if not ruta.startswith('/') or ruta.startswith('//'):
        raise ValueError('Ruta de API inválida')
    cabeceras = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Colorado-Actividad'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        cabeceras['Authorization'] = 'Bearer ' + token
    cuerpo = None
    if datos is not None:
        cuerpo = json.dumps(datos).encode('utf-8')
        cabeceras['Content-Type'] = 'application/json'
    solicitud = urllib.request.Request('https://api.github.com' + ruta, headers=cabeceras, data=cuerpo, method=metodo)
    with urllib.request.urlopen(solicitud, timeout=30) as respuesta:
        return json.load(respuesta)


def paginas(ruta, consultar=api):
    separador = '&' if '?' in ruta else '?'
    for numero in range(1, 21):
        lote = consultar(ruta + separador + urllib.parse.urlencode({'per_page': 100, 'page': numero}))
        if not isinstance(lote, list):
            raise ValueError('Respuesta de GitHub inesperada')
        yield from lote
        if len(lote) < 100:
            return
    raise RuntimeError('La consulta supera el límite de páginas y no se publica un resumen parcial')


def recoger(ahora, consultar=api):
    hoy = ahora.astimezone(ZONA).date()
    primer_dia = hoy - timedelta(days=13)
    desde = datetime.combine(primer_dia, datetime.min.time(), ZONA).isoformat()
    proyectos = []
    for repo in paginas('/orgs/' + ORGANIZACION + '/repos?type=public', consultar):
        if repo.get('private') is not False or repo.get('visibility', 'public') != 'public':
            continue
        nombre = repo.get('name', '')
        if nombre == '.github' or repo.get('archived'):
            continue
        if repo.get('owner', {}).get('login', '').casefold() != ORGANIZACION.casefold():
            continue
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', nombre):
            continue
        ruta = '/repos/' + ORGANIZACION + '/' + nombre + '/commits?'
        ruta += urllib.parse.urlencode({'sha': repo['default_branch'], 'since': desde})
        cambios = {}
        for commit in paginas(ruta, consultar):
            autor = commit.get('author') or {}
            if autor.get('type') == 'Bot' or autor.get('login', '').casefold() != DESARROLLADOR:
                continue
            sha = commit.get('sha', '')
            if not re.fullmatch(r'[0-9a-f]{40}', sha):
                continue
            fecha = datetime.fromisoformat(commit['commit']['committer']['date'].replace('Z', '+00:00'))
            if fecha.tzinfo is None or fecha > ahora:
                continue
            dia = fecha.astimezone(ZONA).date()
            if primer_dia <= dia <= hoy:
                cambios[sha] = {'dia': dia, 'fecha': fecha, 'sha': sha}
        if cambios:
            proyectos.append({'nombre': nombre, 'cambios': list(cambios.values())})
    return proyectos


def resumen(proyectos, ahora):
    hoy = ahora.astimezone(ZONA).date()
    por_dia = defaultdict(set)
    for proyecto in proyectos:
        for cambio in proyecto['cambios']:
            por_dia[cambio['dia']].add(cambio['sha'])
    total = len(set().union(*por_dia.values())) if por_dia else 0
    cantidad_dias = len(por_dia)
    proyectos_texto = 'proyecto con cambios' if len(proyectos) == 1 else 'proyectos con cambios'
    dias_texto = 'día con actividad' if cantidad_dias == 1 else 'días con actividad'
    commits_texto = 'commit público' if total == 1 else 'commits públicos'
    lineas = [
        '**Últimos 14 días**', '',
        f"**{total} {commits_texto} · {len(proyectos)} {proyectos_texto} · {cantidad_dias} {dias_texto}**", '',
        '| Proyecto | Commits | Último cambio |', '| --- | --- | --- |'
    ]
    for proyecto in sorted(proyectos, key=lambda p: max(c['fecha'] for c in p['cambios']), reverse=True):
        ultimo = max(proyecto['cambios'], key=lambda c: c['fecha'])
        nombre = proyecto['nombre']
        enlace = 'https://github.com/' + ORGANIZACION + '/' + nombre
        fecha = ultimo['dia'].strftime('%d/%m')
        lineas.append(f"| [{nombre}]({enlace}) | {len(proyecto['cambios'])} | [{fecha}]({enlace}/commit/{ultimo['sha']}) |")
    if not proyectos:
        lineas.append('| Sin commits públicos en este período | 0 | — |')
    lineas.extend(['', '<details>', '<summary>Actividad por día</summary>', '', '| Día | Commits públicos |', '| --- | --- |'])
    maximo = max((len(x) for x in por_dia.values()), default=0)
    for atraso in range(13, -1, -1):
        dia = hoy - timedelta(days=atraso)
        cantidad = len(por_dia.get(dia, set()))
        barra = '▰' * max(1, round(cantidad * 10 / maximo)) if cantidad else '—'
        lineas.append(f"| {dia.strftime('%d/%m')} | {barra} {cantidad} |")
    lineas.extend(['', '</details>', '', 'Actualizado el ' + ahora.astimezone(ZONA).strftime('%d/%m/%Y a las %H.%M') + ' UTC−3.'])
    return '\n'.join(lineas)


def reemplazar(texto, bloque):
    if texto.count(INICIO) != 1 or texto.count(FIN) != 1:
        raise ValueError('El perfil debe tener un único bloque de actividad')
    antes, resto = texto.split(INICIO, 1)
    _, despues = resto.split(FIN, 1)
    return antes + INICIO + '\n' + bloque + '\n' + FIN + despues


def main():
    argumentos = argparse.ArgumentParser()
    argumentos.add_argument('--publicar', action='store_true')
    opciones = argumentos.parse_args()
    ahora = datetime.now(timezone.utc)
    bloque = resumen(recoger(ahora), ahora)
    if opciones.publicar:
        if not os.environ.get('GITHUB_TOKEN'):
            raise RuntimeError('Falta el token del workflow')
        ruta = '/repos/' + REPOSITORIO + '/contents/profile/README.md'
        documento = api(ruta + '?ref=main')
        anterior = base64.b64decode(documento['content']).decode('utf-8')
        nuevo = reemplazar(anterior, bloque)
        if nuevo != anterior:
            api(ruta, {'message': 'Actualizar actividad pública', 'branch': 'main', 'sha': documento['sha'],
                       'content': base64.b64encode(nuevo.encode('utf-8')).decode('ascii')}, 'PUT')
        print('Actividad pública actualizada')
    else:
        archivo = Path(__file__).resolve().parents[1] / 'profile/README.md'
        archivo.write_text(reemplazar(archivo.read_text(encoding='utf-8'), bloque), encoding='utf-8')
        print('Resumen generado con los commits públicos de GitHub')


if __name__ == '__main__':
    main()
