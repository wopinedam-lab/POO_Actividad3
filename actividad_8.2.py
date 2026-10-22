 
import tkinter as tk
from tkinter import ttk, messagebox
import unicodedata
class Registro:

 
    def __init__(self, nombres, apellidos, telefono, direccion):
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.direccion = direccion
    def descripcion(self):
        return f"{self.nombres} {self.apellidos}"
      
class DirectorioApp(tk.Tk):
    def __init__(self):
        super().__init__()
      
        self.title("registro de personas")
        self.geometry("1100x550")
        self.resizable(False, False)
        self.directorio = []
        self.indice_seleccionado = None
        self.campos = {}
        self.crear_ventana()
      
    def crear_ventana(self):
        # Panel principal

        contenido = tk.Frame(self)
        contenido.pack(fill="both", expand=True, padx=18, pady=15)
        # Formulario de contacto

        formulario = tk.LabelFrame(
            contenido,
            text="Información del contacto",
            padx=12,
            pady=12
        )

        formulario.pack(side="left", fill="y", padx=(0, 15))
        etiquetas = [
            ("Nombres:", "nombres"),
            ("Apellidos:", "apellidos"),
            ("Teléfono:", "telefono"),
            ("Dirección:", "direccion")

        ]
        for fila, (texto, clave) in enumerate(etiquetas):
            tk.Label(
                formulario,
                text=texto
            ).grid(row=fila, column=0, sticky="w", pady=10)
          
            entrada = ttk.Entry(formulario, width=27)
            entrada.grid(row=fila, column=1, padx=6, pady=10)
            self.campos[clave] = entrada

        self.estado = tk.Label(
            formulario,
            text="Completa los datos para registrar.",
            wraplength=280,
            justify="left",
            fg="gray"

        )

        self.estado.grid(
            row=4, column=0, columnspan=2,
            sticky="w", pady=15

        )
        # Panel blanco grande con toda la información

        panel_lista = tk.LabelFrame(
            contenido,
            text="Directorio de personas registradas",
            padx=10,
            pady=10

        )

        panel_lista.pack(side="left", fill="both", expand=True)

        columnas = (
            "nombres",
            "apellidos",
            "telefono",
            "direccion"

        )

 

        self.lista = ttk.Treeview(
            panel_lista,
            columns=columnas,
            show="headings",
            height=18,
            selectmode="browse"

        )

 

        self.lista.heading("nombres", text="Nombres")
        self.lista.heading("apellidos", text="Apellidos")
        self.lista.heading("telefono", text="Teléfono")
        self.lista.heading("direccion", text="Dirección")
        self.lista.column("nombres", width=140, anchor="w")
        self.lista.column("apellidos", width=140, anchor="w")
        self.lista.column("telefono", width=125, anchor="w")
        self.lista.column("direccion", width=230, anchor="w")

 

        # Barras de desplazamiento

        barra_vertical = ttk.Scrollbar(
            panel_lista,
            orient="vertical",
            command=self.lista.yview

        )

 

        barra_horizontal = ttk.Scrollbar(
            panel_lista,
            orient="horizontal",
            command=self.lista.xview

        )

 

        self.lista.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set

        )

 

        self.lista.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")
        panel_lista.rowconfigure(0, weight=1)
        panel_lista.columnconfigure(0, weight=1)
        self.lista.bind(

            "<<TreeviewSelect>>",

            self.cargar_seleccion

        )

 

        # Botones

        acciones = tk.Frame(self)
        acciones.pack(fill="x", padx=18, pady=(0, 15))
        ttk.Button(
            acciones,
            text="Nuevo registro",
            command=self.registrar
        ).pack(side="left", padx=5)


        ttk.Button(
            acciones,
            text="Guardar edición",
            command=self.guardar
        ).pack(side="left", padx=5)
        ttk.Button(
            acciones,
            text="Eliminar persona",
            command=self.eliminar
        ).pack(side="left", padx=5)
        ttk.Button(
            acciones,
            text="Limpiar todo",
            command=self.limpiar
        ).pack(side="left", padx=5)

 
        ttk.Button(
            acciones,
            text="Limpiar formulario",
            command=self.limpiar_formulario
        ).pack(side="left", padx=5)

 

    # Normalizar texto para comparar nombres

    def clave_texto(self, texto):
        texto = " ".join(texto.strip().split())
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            letra for letra in texto
            if unicodedata.category(letra) != "Mn"

        )
        return texto.casefold()

 

    # Leer los datos del formulario

    def leer_datos(self):
        datos = {
            nombre: campo.get().strip()
            for nombre, campo in self.campos.items()

        }

        if not datos["nombres"] or not datos["apellidos"]:
            messagebox.showwarning(
                "Faltan datos",
                "Los nombres y apellidos son obligatorios."

            )

            return None

        return datos

 

    # Comprobar si ya existe esa persona

    def duplicado(self, nombres, apellidos, excluir=None):
        for posicion, registro in enumerate(self.directorio):
            if posicion == excluir:
                continue

 

            coincide_nombre = (
                self.clave_texto(registro.nombres)
                == self.clave_texto(nombres)

            )

 

            coincide_apellido = (
                self.clave_texto(registro.apellidos)
                == self.clave_texto(apellidos)

            )

 

            if coincide_nombre and coincide_apellido:
                return True

        return False

 

    # Registrar una persona nueva

    def registrar(self):
        datos = self.leer_datos()
        if datos is None:
            return

        if self.duplicado(datos["nombres"], datos["apellidos"]):
            messagebox.showwarning(
                "Contacto existente",
                "Ya existe una persona con esos nombres y apellidos."

            )

            return

        nuevo = Registro(**datos)
        self.directorio.append(nuevo)
        self.refrescar()
        self.limpiar_formulario()
        self.estado.config(
            text="Persona registrada correctamente.",
            fg="green"

        )

    # Mostrar todos los datos en la tabla

    def refrescar(self):
        for elemento in self.lista.get_children():
            self.lista.delete(elemento)
        for posicion, persona in enumerate(self.directorio):
            self.lista.insert(
                "",
                "end",
                iid=str(posicion),
                values=(
                    persona.nombres,
                    persona.apellidos,
                    persona.telefono,
                    persona.direccion

                )

            )

    # Cargar los datos al seleccionar una persona

    def cargar_seleccion(self, evento=None):
        seleccion = self.lista.selection()
        if not seleccion:
            return


        self.indice_seleccionado = int(seleccion[0])
        persona = self.directorio[self.indice_seleccionado]


        for clave in self.campos:
            self.campos[clave].delete(0, tk.END)
            self.campos[clave].insert(
                0,

                getattr(persona, clave)

            )
 

        self.estado.config(
            text="Edita los datos y pulsa Guardar edición.",
            fg="blue"

        )
 

    # Guardar los cambios de una persona

    def guardar(self):
        if self.indice_seleccionado is None:
            messagebox.showinfo(
                "Seleccion requerida",

                "Selecciona una persona de la tabla para editarla."

            )

            return

        datos = self.leer_datos()
        if datos is None:

            return

        if self.duplicado(
            datos["nombres"],
            datos["apellidos"],
            excluir=self.indice_seleccionado

        ):

            messagebox.showwarning(
                "Datos repetidos",
                "Otra persona ya tiene esos nombres y apellidos."

            )

            return
 

        persona = self.directorio[self.indice_seleccionado]
        for clave, valor in datos.items():
            setattr(persona, clave, valor)

 

        posicion = self.indice_seleccionado
        self.refrescar()
        self.lista.selection_set(str(posicion))
        self.lista.focus(str(posicion))
        self.limpiar_formulario()
        self.estado.config(
            text="Cambios guardados correctamente.",

            fg="green"

        )
 
    # Eliminar una persona seleccionada

    def eliminar(self):
        seleccion = self.lista.selection()
        if not seleccion:
            messagebox.showinfo(
                "Sin selección",
                "Primero selecciona una persona de la tabla."

            )

            return
        posicion = int(seleccion[0])
        persona = self.directorio[posicion]

 

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",

            f"¿Eliminar a {persona.descripcion()}?"

        )

        if respuesta:
            self.directorio.pop(posicion)
            self.refrescar()
            self.limpiar_formulario()
            self.estado.config(
                text="Persona eliminada correctamente.",

                fg="green"

            )
 
    # Limpiar los campos y quitar la selección

    def limpiar_formulario(self):
        for campo in self.campos.values():
            campo.delete(0, tk.END)
        for elemento in self.lista.selection():
            self.lista.selection_remove(elemento)
        self.indice_seleccionado = None

    # Eliminar todos los registros

    def limpiar(self):
        if not self.directorio:
            self.limpiar_formulario()
            self.estado.config(
                text="No hay contactos para eliminar.",

                fg="gray"

            )

            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar todos los contactos?"

        )

        if respuesta:
            self.directorio.clear()
            self.refrescar()
            self.limpiar_formulario()
            self.estado.config(

                text="Todos los contactos han sido eliminados.",

                fg="green"

            )


if __name__ == "__main__":
    app = DirectorioApp()
    app.mainloop()
