from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.popup import Popup
import shutil
import os

DOCUMENTOS_DIR = 'documentos'
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

class DocumentManager(MDBoxLayout):
    documentos = ListProperty([])
    mensaje = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cargar_documentos()

    def cargar_documentos(self):
        if not os.path.exists(DOCUMENTOS_DIR):
            os.makedirs(DOCUMENTOS_DIR)
        self.documentos = os.listdir(DOCUMENTOS_DIR)
        self.ids.doc_list.clear_widgets()
        for doc in self.documentos:
            self.agregar_fila_documento(doc)

    def agregar_fila_documento(self, nombre):
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel

        fila = MDBoxLayout(size_hint_y=None, height=50, padding=10, spacing=10)
        etiqueta = MDLabel(text=nombre, halign='left')

        btn_ver = MDIconButton(icon="eye", icon_color=(0, 0.7, 0, 1), on_press=lambda x: self.ver_documento(nombre))
        btn_act = MDIconButton(icon="file-replace", icon_color=(0, 0, 1, 1), on_press=lambda x: self.actualizar_documento(nombre))

        fila.add_widget(etiqueta)
        fila.add_widget(btn_ver)
        fila.add_widget(btn_act)

        self.ids.doc_list.add_widget(fila)

    def ver_documento(self, nombre):
        ruta = os.path.join(DOCUMENTOS_DIR, nombre)
        if os.path.exists(ruta):
            os.startfile(ruta)
        else:
            self.mostrar_mensaje("No se encontró el archivo.")

    def actualizar_documento(self, nombre):
        content = FileChooserPopup(nombre_objetivo=nombre, actualizar_callback=self.actualizar_archivo)
        content.open()

    def actualizar_archivo(self, archivo, nombre_objetivo):
        if archivo and self.validar_archivo(archivo):
            destino = os.path.join(DOCUMENTOS_DIR, nombre_objetivo)
            shutil.copy(archivo, destino)
            self.mostrar_mensaje(f"Documento '{nombre_objetivo}' actualizado.")
            self.cargar_documentos()
        else:
            self.mostrar_mensaje("Archivo no válido o no seleccionado.")

    def validar_archivo(self, archivo):
        return os.path.splitext(archivo)[1].lower() in ALLOWED_EXTENSIONS

    def mostrar_mensaje(self, mensaje):
        dialog = MDDialog(
            title="Notificación",
            text=mensaje,
            buttons=[MDFlatButton(text="Aceptar", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

class FileChooserPopup(Popup):
    actualizar_callback = ObjectProperty(None)
    nombre_objetivo = StringProperty("")

    def seleccionar(self, path, filename):
        if filename:
            self.dismiss()
            self.actualizar_callback(filename[0], self.nombre_objetivo)

class GestorApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        return DocumentManager()

if __name__ == '__main__':
    GestorApp().run()