from __future__ import annotations

import pygame

from juego.interfaz.practica import PantallaPractica


class PantallaPracticaEleccionMultiple(PantallaPractica):
    """Práctica reutilizable de tres opciones.

    Conserva el panel, el título, el cuadro de pregunta, el botón de
    responder, los estados normal/hover/clic, el rebote y el flujo de
    reintento de PantallaPractica.
    """

    BOTONES_OPCION = ("opcion_1", "opcion_2", "opcion_3")

    def __init__(self):
        # PantallaPractica carga exactamente los mismos PNG y estilos.
        super().__init__()

        self.opciones = ["Opción 1", "Opción 2", "Opción 3"]
        self.respuesta_correcta = 1
        self.seleccion = None

        # Se reutilizan los PNG de los botones de verdadero/falso.
        # No necesitas crear imágenes nuevas.
        estilos_base = ("falso", "verdadero", "falso")

        for nombre, estilo in zip(self.BOTONES_OPCION, estilos_base):
            self.img_botones[nombre] = dict(
                self.img_botones.get(estilo, {})
            )
            self.estados_rebote[nombre] = {
                "encima_anterior": False,
                "animando": False,
                "tiempo": 0.0,
                "offset_y": 0,
            }

        self.calcular_rects()

    def calcular_rects(self):
        """Mantiene el mismo formulario y agrega una tercera respuesta."""
        proporcion = self.diseno_ancho / self.diseno_alto

        area_x = round(1920 * self.area_practica_relativa[0])
        area_y = round(1080 * self.area_practica_relativa[1])
        area_ancho = round(1920 * self.area_practica_relativa[2])
        area_alto = round(1080 * self.area_practica_relativa[3])
        area_practica = pygame.Rect(
            area_x,
            area_y,
            area_ancho,
            area_alto,
        )

        panel_ancho = area_practica.width
        panel_alto = int(panel_ancho / proporcion)

        if panel_alto > area_practica.height:
            panel_alto = area_practica.height
            panel_ancho = int(panel_alto * proporcion)

        self.panel = pygame.Rect(0, 0, panel_ancho, panel_alto)
        self.panel.center = area_practica.center

        self.escala_x = self.panel.width / self.diseno_ancho
        self.escala_y = self.panel.height / self.diseno_alto
        self.actualizar_fuentes()

        self.rect_cerrar = self.rect_relativo(45, 38, 78, 72)
        self.rect_titulo = self.rect_relativo(140, 48, 245, 56)

        # El cuadro de pregunta se hace un poco más bajo únicamente
        # para dejar espacio al tercer botón.
        self.rect_pregunta = self.rect_relativo(57, 138, 1334, 260)

        self.rect_opcion_1 = self.rect_relativo(56, 420, 1338, 84)
        self.rect_opcion_2 = self.rect_relativo(56, 520, 1338, 84)
        self.rect_opcion_3 = self.rect_relativo(56, 620, 1338, 84)

        self.rect_resultado = self.rect_relativo(80, 715, 1288, 105)
        self.rect_responder = self.rect_relativo(430, 890, 590, 100)

    def iniciar(self, pregunta, configuracion):
        configuracion = dict(configuracion or {})
        opciones = list(configuracion.get("opciones", []) or [])

        if len(opciones) != 3:
            raise ValueError(
                "La elección múltiple necesita exactamente tres opciones."
            )

        self.visible = True
        self.pregunta = str(pregunta)
        self.opciones = [str(opcion) for opcion in opciones]

        correcta = configuracion.get("respuesta_correcta", 1)

        # Permite indicar la respuesta por posición (1, 2 o 3)
        # o escribiendo exactamente el texto de la opción.
        if isinstance(correcta, str) and correcta in self.opciones:
            correcta = self.opciones.index(correcta) + 1

        try:
            correcta = int(correcta)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "respuesta_correcta debe ser 1, 2, 3 o el texto "
                "exacto de una opción."
            ) from error

        if correcta not in (1, 2, 3):
            raise ValueError(
                "respuesta_correcta debe ser 1, 2 o 3."
            )

        self.respuesta_correcta = correcta
        self.seleccion = None
        self.respondido = False
        self.resultado = ""
        self.respuesta_final = None
        self.intento_incorrecto_pendiente = False
        self.boton_presionado = None
        self.reiniciar_rebotes()
        self.calcular_rects()

    def reintentar(self):
        self.seleccion = None
        self.respondido = False
        self.respuesta_final = None
        self.resultado = ""
        self.boton_presionado = None
        self.reiniciar_rebotes()

    def responder(self):
        if self.seleccion is None:
            self.resultado = "Selecciona una respuesta"
            return

        self.respondido = True
        self.respuesta_final = (
            self.seleccion == self.respuesta_correcta
        )

        if self.respuesta_final:
            self.resultado = "Correcto!"
        else:
            self.resultado = "Incorrecto!"
            self.intento_incorrecto_pendiente = True

    def obtener_rect_opcion(self, numero):
        return getattr(self, f"rect_opcion_{numero}")

    def obtener_boton_en_posicion(self, pos):
        if self.rect_cerrar.collidepoint(pos):
            return "cerrar"

        for numero, nombre in enumerate(self.BOTONES_OPCION, start=1):
            if self.obtener_rect_opcion(numero).collidepoint(pos):
                return nombre

        if self.rect_responder.collidepoint(pos):
            return "responder"

        return None

    def manejar_click_boton(self, boton):
        if boton == "cerrar":
            self.cerrar()
            return

        if boton in self.BOTONES_OPCION and not self.respondido:
            self.seleccion = self.BOTONES_OPCION.index(boton) + 1
            self.resultado = ""
            return

        if boton == "responder":
            if self.respondido and self.respuesta_final:
                self.cerrar()
            elif self.respondido:
                self.reintentar()
            else:
                self.responder()

    def manejar_evento(self, evento):
        if not self.visible:
            return False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.cerrar()
                return True

            if not self.respondido:
                teclas = {
                    pygame.K_1: 1,
                    pygame.K_KP1: 1,
                    pygame.K_2: 2,
                    pygame.K_KP2: 2,
                    pygame.K_3: 3,
                    pygame.K_KP3: 3,
                }

                if evento.key in teclas:
                    self.seleccion = teclas[evento.key]
                    self.resultado = ""
                    return True

            if evento.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE,
            ):
                if self.respondido and self.respuesta_final:
                    self.cerrar()
                elif self.respondido:
                    self.reintentar()
                else:
                    self.responder()
                return True

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.boton_presionado = self.obtener_boton_en_posicion(
                evento.pos
            )
            return True

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            boton = self.obtener_boton_en_posicion(evento.pos)

            if boton is not None and boton == self.boton_presionado:
                self.manejar_click_boton(boton)

            self.boton_presionado = None
            return True

        return True

    def obtener_estado_boton(self, nombre, rect):
        mouse_pos = pygame.mouse.get_pos()
        encima = rect.collidepoint(mouse_pos)

        if self.boton_presionado == nombre and encima:
            return "clic"

        if nombre in self.BOTONES_OPCION:
            numero = self.BOTONES_OPCION.index(nombre) + 1
            if self.seleccion == numero:
                return "clic"

        if encima:
            return "hover"

        return "normal"

    def actualizar(self, dt):
        if not self.visible:
            return

        mouse_pos = pygame.mouse.get_pos()
        rects = {
            "cerrar": self.rect_cerrar,
            "opcion_1": self.rect_opcion_1,
            "opcion_2": self.rect_opcion_2,
            "opcion_3": self.rect_opcion_3,
            "responder": self.rect_responder,
        }

        desplazamiento = max(
            8,
            round(self.desplazamiento_rebote * self.escala_y),
        )

        for nombre, rect in rects.items():
            estado = self.estados_rebote[nombre]
            encima = rect.collidepoint(mouse_pos)

            if encima and not estado["encima_anterior"]:
                estado["animando"] = True
                estado["tiempo"] = 0.0

            estado["encima_anterior"] = encima

            if not estado["animando"]:
                estado["offset_y"] = 0
                continue

            estado["tiempo"] += max(0.0, dt)
            tiempo = estado["tiempo"]

            if tiempo <= self.duracion_subida_rebote:
                progreso = min(
                    tiempo / self.duracion_subida_rebote,
                    1.0,
                )
                suavizado = 1.0 - (1.0 - progreso) ** 2
                estado["offset_y"] = -round(
                    desplazamiento * suavizado
                )
                continue

            tiempo_bajada = tiempo - self.duracion_subida_rebote

            if tiempo_bajada <= self.duracion_bajada_rebote:
                progreso = min(
                    tiempo_bajada / self.duracion_bajada_rebote,
                    1.0,
                )
                rebote = self._ease_out_bounce(progreso)
                estado["offset_y"] = -round(
                    desplazamiento * (1.0 - rebote)
                )
                continue

            estado["animando"] = False
            estado["tiempo"] = 0.0
            estado["offset_y"] = 0

    def dibujar(self, pantalla):
        if not self.visible:
            return

        pantalla.blit(self._sombra_fondo, (0, 0))

        if not self.dibujar_imagen_ajustada(
            pantalla,
            self.img_formulario,
            self.panel,
            mantener_aspecto=False,
        ):
            self.dibujar_panel_respaldo(pantalla)

        if not self.dibujar_imagen_ajustada(
            pantalla,
            self.img_titulo,
            self.rect_titulo,
            mantener_aspecto=True,
        ):
            self.dibujar_titulo_respaldo(pantalla)

        self.dibujar_boton(
            pantalla,
            "cerrar",
            self.rect_cerrar,
            "X",
            (255, 70, 70),
        )

        if not self.dibujar_imagen_ajustada(
            pantalla,
            self.img_pregunta,
            self.rect_pregunta,
            mantener_aspecto=False,
        ):
            self.dibujar_caja_pixel(
                pantalla,
                self.rect_pregunta,
                (207, 244, 250),
                (8, 35, 70),
                sombra=True,
            )

        self.dibujar_texto_centrado(
            pantalla,
            self.pregunta,
            self.fuente_pregunta,
            self.rect_pregunta,
            (16, 35, 65),
        )

        colores_respaldo = (
            (0, 125, 235),
            (0, 190, 175),
            (95, 85, 210),
        )

        for numero, nombre in enumerate(self.BOTONES_OPCION, start=1):
            self.dibujar_boton(
                pantalla,
                nombre,
                self.obtener_rect_opcion(numero),
                self.opciones[numero - 1],
                colores_respaldo[numero - 1],
            )

        self.dibujar_resultado(pantalla)

        if self.respondido and self.respuesta_final:
            texto_boton = "CONTINUAR"
        elif self.respondido:
            texto_boton = "REINTENTAR"
        else:
            texto_boton = "RESPONDER"

        self.dibujar_boton(
            pantalla,
            "responder",
            self.rect_responder,
            texto_boton,
            (255, 105, 0),
        )


__all__ = ["PantallaPracticaEleccionMultiple"]
