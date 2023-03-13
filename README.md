# APICompresion

API para comprimir archivos PDF. Esta API está construida con Flask y utiliza PyPDF2 para la compresión de archivos PDF.

## Instalación

Para utilizar esta API, es necesario tener instalado Python 3 y pip.

1. Clonar el repositorio: **```git clone https://github.com/Fran3000vv/APICompresion```**
2. Instalar las dependencias: **```pip install -r requirements.txt```**
3. Configurar la base de datos
4. Iniciar la aplicación: python application.py

## Uso
### Comprimir un Archivo PDF
Para comprimir un archivo PDF, envía una petición POST a la URL **/compress_pdf** con el archivo en el campo **file_post**.  

Ejemplo:  
```python
import requests

url = 'http://localhost:5000/compress_pdf'
files = {'file_post': open('example.pdf', 'rb')}
response = requests.post(url, files=files)

print(response.json())
```

La respuesta será un objeto JSON con un token que identifica el archivo comprimido:

```json
{
  "token": "XOy8blB6OAHjKNOJF6KLlA"
}

```

## Cambiar un archivo PDF comprimido

Para cambiar un archivo PDF comprimido, envía una petición PUT a la URL **/change_pdf/<token>** con el nuevo archivo en el campo **file_put** y el token del archivo a cambiar en la URL.  

Ejemplo:  
```python
import requests

url = 'http://localhost:5000/change_pdf/XOy8blB6OAHjKNOJF6KLlA'
files = {'file_put': open('example.pdf', 'rb')}
response = requests.put(url, files=files)

print(response.json())
```

La respuesta será un objeto JSON con un token que identifica el archivo comprimido:

```json
{
  "token": "XOy8blB6OAHjKNOJF6KLlA"
}
```

## Eliminar un archivo PDF comprimido
Para eliminar un archivo PDF comprimido, envía una petición DELETE a la URL **/delete_pdf/<token>** con el token del archivo a eliminar en la URL.

Ejemplo:  
```python
import requests

url = 'http://localhost:5000/delete_pdf/XOy8blB6OAHjKNOJF6KLlA'
response = requests.delete(url)

print(response.json())
```

La respuesta será un objeto JSON confirmando la eliminación:

```json
{
  "result": "Your Operation has been realized successfully"
}
```

## Obtener un archivo PDF comprimido
Para obtener un archivo PDF comprimido, envía una petición GET a la URL **/get_compressed_pdf/<token>** con el token del archivo a obtener en la URL.

Ejemplo:
```python
import requests

url = 'http://localhost:5000/get_compressed_pdf/XOy8blB6OAHjKNOJF6KLlA'
response = requests.get(url)

with open('compressed_file.pdf', 'wb') as f:
    f.write(response.content)
```
Esto descargará el archivo comprimido con el nombre **compressed_file.pdf**.
