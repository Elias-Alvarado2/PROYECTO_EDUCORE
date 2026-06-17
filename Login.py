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
        
        # ⚠️ REEMPLAZA ESTO: Pon el nombre exacto de tu imagen (ejemplo: "fondo.png")
        nombre_imagen = "LoginNuevo.png" 
        ruta_imagen = os.path.join(BASE_DIR, "assets", "diseños", nombre_imagen)
        
        try:
            # 2. CARGAR EL DISEÑO (BOTONES, TEXTOS, ETC.)
            uic.loadUi(ruta_ui, self)
            
            # 3. FORZAR EL TAMAÑO DE LA VENTANA A 1920x1080
            self.resize(1920, 1080)
            
            # [TRUCO PARA LA EXPO]: Si quitas el '#' de la línea de abajo, 
            # la ventana se abrirá en pantalla completa real ocultando la barra de Windows.
            # self.showFullScreen()
            
            # 4. APLICAR EL FONDO ESTILIZADO (AJUSTE PERFECTO)
            # Cambiamos las diagonales de Windows (\) por las de entorno web (/) para evitar fallos de CSS
            ruta_css = ruta_imagen.replace(os.sep, '/')
            
            # Usamos 'border-image' que clava las esquinas de la imagen a los bordes del Dialog
            self.setStyleSheet(f"""
                QDialog {{
                    border-image: url('{ruta_css}') 0 0 0 0 stretch stretch;
                }}
            """)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Error de Sistema", 
                f"No se pudo cargar la interfaz o el fondo.\n\nDetalles: {str(e)}"
            )
            sys.exit(1)
            
        # --- 5. LÓGICA DE TUS BOTONES ---
        # Si en Qt Designer tu botón de inicio se llama 'btn_ingresar', descomenta la línea de abajo:
        # self.btn_ingresar.clicked.connect(self.funcion_login)

    def funcion_login(self):
        print("¡El botón está vivo y respondiendo en Python!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.show()
    sys.exit(app.exec())