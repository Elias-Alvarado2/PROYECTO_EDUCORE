import sys
import os
from PyQt6 import QtWidgets, uic


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        
        # 1. ENCONTRAR LAS RUTAS ABSOLUTAS DEL PROYECTO
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta hacia el archivo .ui
        ruta_ui = os.path.join(BASE_DIR, "expo-diseños", "DESIGNER", "Login.ui")
        
        # Nombre exacto de tu imagen
        nombre_imagen = "LoginNuevo.png" 
        ruta_imagen = os.path.join(BASE_DIR, "assets", "diseños", nombre_imagen)
        
        try:
            # 2. CARGAR EL DISEÑO
            uic.loadUi(ruta_ui, self)
            
            # 3. FORZAR EL TAMAÑO DE LA VENTANA
            self.resize(1020, 720)
            
            # 4. APLICAR EL FONDO
            ruta_css = ruta_imagen.replace(os.sep, '/')
            
            self.setStyleSheet(f"""
                QDialog {{
                    border-image: url('{ruta_css}') 0 0 0 0 stretch stretch;
                }}
            """)

            # --- MOSTRAR / OCULTAR CONTRASEÑA ---

            # La contraseña empieza oculta
            self.txtcontrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

            # Hace que el botón funcione como interruptor
            self.btnMostrarContrasena.setCheckable(True)

            # El botón del ojo muestra/oculta la contraseña
            self.btnMostrarContrasena.clicked.connect(self.mostrar_ocultar_contrasena)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error de Sistema", 
                f"No se pudo cargar la interfaz o el fondo.\n\nDetalles: {str(e)}"
            )
            sys.exit(1)
            
        # --- 5. LÓGICA DE TUS BOTONES ---
        # self.btn_ingresar.clicked.connect(self.funcion_login)

    def mostrar_ocultar_contrasena(self, checked):
        if checked:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.txtContrasena.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def funcion_login(self):
        print("¡El botón está vivo y respondiendo en Python!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec())