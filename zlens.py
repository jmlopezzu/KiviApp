from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage
from kivy.uix.filechooser import FileChooserIconView
from pyzbar.pyzbar import decode
from PIL import Image as PILImage
import io
import os


class BarcodeScannerApp(App):
    def build(self):
        # Layout principal
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Cámara
        self.camera = Camera(play=True, resolution=(640, 480))
        self.camera.allow_stretch = True
        self.layout.add_widget(self.camera)

        # Botón para capturar
        self.capture_button = Button(text="Capturar y Decodificar", size_hint=(1, 0.1))
        self.capture_button.bind(on_press=self.capture_image)
        self.layout.add_widget(self.capture_button)

        # Botón para seleccionar una imagen
        self.upload_button = Button(text="Subir Imagen", size_hint=(1, 0.1))
        self.upload_button.bind(on_press=self.open_filechooser)
        self.layout.add_widget(self.upload_button)

        # Área de resultados
        self.result_label = Label(text="Resultado del Código de Barras aparecerá aquí.", size_hint=(1, 0.2))
        self.layout.add_widget(self.result_label)

        # FileChooser para seleccionar una imagen
        self.filechooser = FileChooserIconView(size_hint=(1, 0.6))
        self.filechooser.bind(on_selection=self.load_image)
        self.layout.add_widget(self.filechooser)
        self.filechooser.opacity = 0  # Ocultamos inicialmente el FileChooser

        return self.layout

    def capture_image(self, instance):
        # Captura de textura de la cámara
        texture = self.camera.texture
        if texture is None:
            self.result_label.text = "Error: No se pudo capturar la imagen."
            return

        # Convertir textura a PIL Image
        data = io.BytesIO(texture.pixels)
        pil_image = PILImage.frombytes("RGBA", (texture.size[0], texture.size[1]), texture.pixels)
        
        # Decodificar código de barras
        decoded_objects = decode(pil_image)
        if decoded_objects:
            for obj in decoded_objects:
                barcode_data = obj.data.decode("utf-8")
                barcode_type = obj.type

                if barcode_type == "CODE39":
                    self.result_label.text = f"¡Código Code39 detectado!: {barcode_data}"
                else:
                    self.result_label.text = f"Código detectado pero no es Code39: {barcode_data} ({barcode_type})"
        else:
            self.result_label.text = "No se detectó ningún código de barras en la imagen."

    def open_filechooser(self, instance):
        # Mostrar el filechooser para seleccionar una imagen
        self.filechooser.opacity = 1

    def load_image(self, filechooser, selection):
        if selection:
            image_path = selection[0]
            try:
                # Filtrar archivos del sistema (por ejemplo, pagefile.sys, hiberfil.sys)
                if os.path.basename(image_path).startswith(('.', 'hiberfil', 'pagefile', 'swapfile', 'DumpStack')):
                    self.result_label.text = "El archivo seleccionado no es accesible."
                    return

                # Abrir la imagen seleccionada
                pil_image = PILImage.open(image_path)
                # Decodificar el código de barras
                decoded_objects = decode(pil_image)
                if decoded_objects:
                    for obj in decoded_objects:
                        barcode_data = obj.data.decode("utf-8")
                        barcode_type = obj.type
                        if barcode_type == "CODE39":
                            self.result_label.text = f"¡Código Code39 detectado!: {barcode_data}"
                        else:
                            self.result_label.text = f"Código detectado pero no es Code39: {barcode_data} ({barcode_type})"
                else:
                    self.result_label.text = "No se detectó ningún código de barras en la imagen."
            except Exception as e:
                self.result_label.text = f"Error al cargar la imagen: {str(e)}"
            # Ocultar el filechooser después de cargar la imagen
            self.filechooser.opacity = 0


if __name__ == "__main__":
    BarcodeScannerApp().run()
