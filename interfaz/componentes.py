
import ttkbootstrap as ttk


def crear_tarjeta(parent, titulo, valor, descripcion):
    tarjeta = ttk.Frame(
        parent,
        bootstyle="secondary",
        padding=20
    )

    ttk.Label(
        tarjeta,
        text=titulo,
        font=("Segoe UI", 11),
        bootstyle="inverse-secondary"
    ).pack(anchor="w")

    etiqueta_valor = ttk.Label(
        tarjeta,
        text=valor,
        font=("Segoe UI", 26, "bold"),
        bootstyle="inverse-secondary"
    )
    etiqueta_valor.pack(anchor="w", pady=8)

    ttk.Label(
        tarjeta,
        text=descripcion,
        font=("Segoe UI", 9),
        bootstyle="inverse-secondary"
    ).pack(anchor="w")

    return tarjeta, etiqueta_valor
