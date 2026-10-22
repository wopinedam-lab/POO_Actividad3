import tkinter as tk
from tkinter import ttk, messagebox
import math
from abc import ABC, abstractmethod

# ==========================================

# MODELO MATEMATICO DE LAS FIGURAS

# ==========================================
class SolidoGeometrico(ABC):
    @abstractmethod
    def volumen(self):
        pass

    @abstractmethod
    def area_total(self):
        pass

class CilindroRecto(SolidoGeometrico):
    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura
    def volumen(self):
        return math.pi * self.radio**2 * self.altura
    def area_total(self):
        return 2 * math.pi * self.radio * (
            self.radio + self.altura

        )

 

 

class Esfera(SolidoGeometrico):
    def __init__(self, radio):
        self.radio = radio
    def volumen(self):
        return (4 / 3) * math.pi * self.radio**3
    def area_total(self):
        return 4 * math.pi * self.radio**2


class PiramideCuadrada(SolidoGeometrico):
    def __init__(self, lado, altura, apotema):
        self.lado = lado
        self.altura = altura
        self.apotema = apotema
    def volumen(self):
        return (self.lado**2 * self.altura) / 3
    def area_total(self):
        return self.lado**2 + 2 * self.lado * self.apotema

 
# ==========================================

# INTERFAZ GRAFICA

# ==========================================

class CalculadoraSolidos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Calculadora de volumen y superficie")
        self.ventana.geometry("460x440")
        self.ventana.resizable(False, False)
        titulo = tk.Label(
            ventana,
            text="CALCULADORA GEOMETRICA",
            font=("Arial", 15, "bold")

        )
        titulo.pack(pady=15)

        tk.Label(
            ventana,
            text="Selecciona una figura:",
            font=("Arial", 11)
        ).pack()

 
        self.seleccion = tk.StringVar(value="Cilindro")
        self.menu = ttk.Combobox(
            ventana,
            textvariable=self.seleccion,
            values=("Cilindro", "Esfera", "Piramide"),
            state="readonly",
            width=25
        )
        self.menu.pack(pady=8)
        self.menu.bind("<<ComboboxSelected>>", self.mostrar_entradas)
        self.panel = tk.Frame(ventana)
        self.panel.pack(pady=8)
        self.entradas = {}
        self.salida = tk.Label(
            ventana,
            text="Introduce las medidas de la figura.",
            font=("Arial", 10),
            justify="left"

        )

        self.salida.pack(pady=12)
        tk.Button(
            ventana,
            text="CALCULAR",
            command=self.procesar,
            width=18,
            bg="#1976D2",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=8)
        self.mostrar_entradas()

 

    def mostrar_entradas(self, evento=None):
        # Limpiar las entradas de la figura anterior
        for elemento in self.panel.winfo_children():
            elemento.destroy()
        self.entradas.clear()
        figura = self.seleccion.get()
        if figura == "Cilindro":
            datos = [
                ("Radio en cm:", "radio"),
                ("Altura en cm:", "altura")
            ]
        elif figura == "Esfera":
            datos = [
                ("Radio en cm:", "radio")

            ]
        else:
            datos = [
                ("Lado de la base en cm:", "lado"),
                ("Altura en cm:", "altura"),
                ("Apotema en cm:", "apotema")

            ]

        for fila, (etiqueta, clave) in enumerate(datos):
            tk.Label(
                self.panel,
                text=etiqueta,
                width=24,
                anchor="w"
            ).grid(row=fila, column=0, padx=5, pady=5)
            entrada = ttk.Entry(self.panel, width=18)
            entrada.grid(row=fila, column=1, padx=5, pady=5)
            self.entradas[clave] = entrada
        self.salida.config(
            text="Introduce las medidas de la figura."

        )

    def procesar(self):
        try:
            medidas = {}


            # Leer y comprobar los datos introducidos
            for clave, entrada in self.entradas.items():
                texto = entrada.get().strip().replace(",", ".")

                if not texto:
                    raise ValueError("Debes completar todas las medidas.")
                numero = float(texto)
                if not math.isfinite(numero) or numero <= 0:
                    raise ValueError(
                        "Todas las medidas deben ser positivas."

                    )

                medidas[clave] = numero
            tipo = self.seleccion.get()
            # Construir la figura elegida

            if tipo == "Cilindro":
                figura = CilindroRecto(
                    medidas["radio"],
                    medidas["altura"]

                )

            elif tipo == "Esfera":
                figura = Esfera(medidas["radio"])


            else:
                lado = medidas["lado"]
                altura = medidas["altura"]
                apotema = medidas["apotema"]

                # Verificar la compatibilidad geometrica

                apotema_necesaria = math.sqrt(
                    altura**2 + (lado / 2)**2

                )

                if apotema < apotema_necesaria - 1e-9:
                    raise ValueError(
                        "La apotema no es compatible con la altura "
                        "y el lado de la base."

                    )
                figura = PiramideCuadrada(
                    lado, altura, apotema

                )
            # Obtener y presentar los resultados
            volumen = figura.volumen()
            superficie = figura.area_total()
            self.salida.config(
                text=(
                    f"FIGURA: {tipo}\n\n"
                    f"Volumen: {volumen:.2f} cm³\n"
                    f"Superficie total: {superficie:.2f} cm²"
                ),
                fg="darkgreen"
            )
        except ValueError as error:
            messagebox.showerror("Error", str(error))

# ==========================================

# INICIO DEL PROGRAMA

# ==========================================
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    programa = CalculadoraSolidos(ventana_principal)
    ventana_principal.mainloop()
