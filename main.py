import sys
import os
from PyQt5 import QtWidgets, uic

# Obtenemos la ruta absoluta de la carpeta raíz (PROYECTO_EDUCORE)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class LoginVentana(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginVentana, self).__init__()
        
        # Ruta exacta hacia EXPO-DISEÑOS/DESIGNER/Login.ui
        ruta_ui = os.path.join(BASE_DIR, 'EXPO-DISEÑOS', 'DESIGNER', 'Login.ui')
        uic.loadUi(ruta_ui, self)
        
        # Conexión de botones usando los objectName de tu interfaz
        self.btnIniciar_Sesion.clicked.connect(self.abrir_menu)
        self.btn_Registrarse.clicked.connect(self.abrir_registro)

    def abrir_menu(self):
        self.menu_ventana = MenuAdminVentana()
        self.menu_ventana.show()
        self.close()  # Cierra la ventana de Login actual

    def abrir_registro(self):
        self.registro_ventana = RegistroVentana()
        self.registro_ventana.show()
        self.close()  # Cierra la ventana de Login actual


class MenuAdminVentana(QtWidgets.QMainWindow):
    def __init__(self):
        super(MenuAdminVentana, self).__init__()
        ruta_ui = os.path.join(BASE_DIR, 'EXPO-DISEÑOS', 'DESIGNER', 'Menu-Administrador.ui')
        uic.loadUi(ruta_ui, self)


class RegistroVentana(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegistroVentana, self).__init__()
        ruta_ui = os.path.join(BASE_DIR, 'EXPO-DISEÑOS', 'DESIGNER', 'Registro.ui')
        uic.loadUi(ruta_ui, self)


# --- INICIO DE LA APLICACIÓN ---
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # Forzamos a Python a situarse en PROYECTO_EDUCORE para que encuentre 'assets'
    os.chdir(BASE_DIR) 
    
    ventana = LoginVentana()
    ventana.show()
    sys.exit(app.exec_())