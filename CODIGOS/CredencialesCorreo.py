

# ============================================================
# CUENTA QUE ENVIA LOS DIPLOMAS
# ============================================================

# Escribe el correo completo que enviara los certificados.
CORREO_REMITENTE = "educoregt@gmail.com"

# Para Gmail usa una contrasena de aplicacion, no la contrasena normal de la
# cuenta. Copiala exactamente como fue generada.
CONTRASENA_APLICACION = "tqfjltrpqvutlbjs"


# ============================================================
# SERVIDOR SMTP
# ============================================================

# Estos valores ya estan preparados para Gmail.
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PUERTO = 587
SMTP_USAR_TLS = True
SMTP_USAR_SSL = False
SMTP_REQUIERE_AUTENTICACION = True
SMTP_TIMEOUT_SEGUNDOS = 30


def credenciales_configuradas():
    """Indica si ya se escribieron el correo y la contrasena."""
    return bool(
        str(CORREO_REMITENTE).strip()
        and str(CONTRASENA_APLICACION).strip()
    )


if __name__ == "__main__":
    if credenciales_configuradas():
        print("Las credenciales del correo estan configuradas.")
        print(f"Cuenta remitente: {CORREO_REMITENTE}")
    else:
        print("Todavia faltan las credenciales del correo.")
        print("Abre este archivo y completa:")
        print("- CORREO_REMITENTE")
        print("- CONTRASENA_APLICACION")
