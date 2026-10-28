import unittest
from datetime import datetime, timezone
from scripts.actividad import INICIO, FIN, paginas, recoger, reemplazar, resumen


class ActividadPublica(unittest.TestCase):
    def setUp(self):
        self.ahora = datetime(2026, 10, 28, 15, tzinfo=timezone.utc)

    def repo(self, nombre, privado=False, **otros):
        return {'name': nombre, 'private': privado, 'visibility': 'private' if privado else 'public',
                'owner': {'login': 'Colorado-Roleplay-Company'}, 'default_branch': 'main', **otros}

    def commit(self, letra='a', fecha='2026-10-28T01:00:00Z', **autor):
        return {'sha': letra * 40, 'author': autor or {'login': 'em4nu3i69dll', 'type': 'User'},
                'commit': {'committer': {'date': fecha}}}

    def test_solo_consulta_proyectos_publicos_de_la_organizacion(self):
        rutas = []
        def consultar(ruta):
            rutas.append(ruta)
            if ruta.startswith('/orgs/'):
                return [self.repo('ejemplo'), self.repo('privado', True), self.repo('.github'),
                        self.repo('fork', fork=True), self.repo('archivo', archived=True),
                        self.repo('ajeno', owner={'login': 'otra-organizacion'})]
            return [self.commit(), self.commit('b', login='dependabot[bot]', type='Bot'), self.commit('c', login='otra-persona', type='User')]
        resultado = recoger(self.ahora, consultar)
        self.assertEqual([x['nombre'] for x in resultado], ['ejemplo', 'fork'])
        self.assertEqual(len(resultado[0]['cambios']), 1)
        self.assertEqual(len(rutas), 3)
        self.assertIn('/ejemplo/commits?', rutas[1])

    def test_fechas_locales_futuras_y_repetidas(self):
        def consultar(ruta):
            if ruta.startswith('/orgs/'):
                return [self.repo('ejemplo')]
            return [self.commit(), self.commit(), self.commit('b', '2026-10-28T16:00:00Z'),
                    self.commit('c', '2026-10-15T02:00:00Z')]
        resultado = recoger(self.ahora, consultar)
        self.assertEqual(len(resultado[0]['cambios']), 1)
        self.assertEqual(str(resultado[0]['cambios'][0]['dia']), '2026-10-27')

    def test_no_multiplica_un_commit_compartido_entre_repositorios(self):
        def consultar(ruta):
            return [self.repo('uno'), self.repo('dos')] if ruta.startswith('/orgs/') else [self.commit()]
        texto = resumen(recoger(self.ahora, consultar), self.ahora)
        self.assertIn('1 commit público · 2 proyectos con cambios · 1 día con actividad', texto)
        self.assertEqual(texto.count('| 15/10 |'), 1)
        self.assertEqual(texto.count('| 28/10 |'), 1)

    def test_paginacion_no_trunca_las_consultas(self):
        peticiones = []
        def consultar(ruta):
            peticiones.append(ruta)
            return list(range(100)) if ruta.endswith('page=1') else [100]
        self.assertEqual(len(list(paginas('/ejemplo?sha=main', consultar))), 101)
        self.assertEqual(len(peticiones), 2)
        with self.assertRaises(RuntimeError):
            list(paginas('/ejemplo', lambda ruta: list(range(100))))

    def test_no_publica_errores_como_cero_actividad(self):
        with self.assertRaises(OSError):
            recoger(self.ahora, lambda ruta: (_ for _ in ()).throw(OSError('API no disponible')))

    def test_actualiza_solo_el_bloque_del_perfil(self):
        original = 'antes\n' + INICIO + '\nanterior\n' + FIN + '\ndespués'
        nuevo = reemplazar(original, 'datos nuevos')
        self.assertEqual(nuevo, 'antes\n' + INICIO + '\ndatos nuevos\n' + FIN + '\ndespués')
        for invalido in ['sin marcadores', original + FIN, FIN + INICIO]:
            with self.assertRaises(ValueError):
                reemplazar(invalido, 'nuevo')

    def test_sin_actividad_no_inventa_resultados(self):
        texto = resumen([], self.ahora)
        self.assertIn('0 commits públicos · 0 proyectos con cambios · 0 días con actividad', texto)
        self.assertIn('Sin commits públicos en este período', texto)


if __name__ == '__main__':
    unittest.main()
