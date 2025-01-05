
![Generador de Datos de Ventas](generador.webp)


# 🚗 Generador de Datos de Ventas

Este proyecto es una herramienta diseñada para estudiantes, desarrolladores y profesionales interesados en la generación, visualización y análisis de datos estructurados. A través de este sistema, podrás crear datos simulados sobre ventas de vehículos en República Dominicana, facilitando el aprendizaje y la implementación de técnicas de análisis de datos en aplicaciones prácticas como proyectos web, aplicaciones móviles y sistemas de consumo de datos.

---

## 📋 Características
- **Generación de Datos:** Permite simular información detallada sobre clientes, vendedores, vehículos y transacciones de ventas.
- **Visualización Interactiva:** Interfaz gráfica creada con [Streamlit](https://streamlit.io/) que facilita la interacción con los datos.
- **Consumo de APIs Externas:** Integración con [RandomUser.me](https://randomuser.me/) para obtener imágenes y datos de usuarios ficticios.
- **Exportación de Datos:** Posibilidad de guardar los datos generados en formatos JSON, CSV o Excel para su posterior análisis o integración en otros sistemas.
- **Contexto Educativo:** Ideal para aprender sobre consumo de APIs, visualización de datos, y análisis en herramientas como Power BI o Tableau.

---

## 🌟 Aportes del Proyecto
Este proyecto se adapta a diferentes contextos y necesidades, brindando soluciones prácticas como:

1. **Creación de Datos:** Genera datos realistas para pruebas y desarrollo de aplicaciones web, móviles y sistemas backend.
2. **Consumo de Datos:** Sirve como base para practicar con protocolos como REST API y realizar solicitudes GET, POST, PUT y DELETE.
3. **Visualización:** Permite explorar gráficos y métricas clave, lo que es útil para proyectos en ciencia de datos y análisis de negocios.
4. **Análisis de Impacto:** Facilita la simulación de escenarios para entender tendencias de ventas, comportamiento del cliente y rendimiento de los vendedores.

---

## 🔧 Tecnologías Utilizadas

### Lenguajes y Herramientas
- **Python:** El lenguaje principal utilizado para construir la lógica del proyecto.
- **Streamlit:** Framework para crear interfaces gráficas interactivas de manera rápida y eficiente.
- **Faker:** Librería especializada en la generación de datos ficticios como nombres, correos y direcciones.
- **Pandas:** Herramienta poderosa para el manejo y análisis de datos.
- **Requests:** Utilizada para realizar solicitudes HTTP y consumir la API de RandomUser.

### Instalación de Herramientas

1. **Python**: Descárgalo desde [python.org](https://www.python.org/).
2. **Streamlit**:
   ```bash
   pip install streamlit
   ```
3. **Faker**:
   ```bash
   pip install faker
   ```
4. **Pandas**:
   ```bash
   pip install pandas
   ```
5. **Requests**:
   ```bash
   pip install requests
   ```

---

## 🚀 Instalación del Proyecto

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone  https://github.com/JUANCITOPENA/GENERAR_VENTAS_AUTOS_FOTOS_VENDEDOR_FOTOS.git
   cd tu_repositorio
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

---

## 🎮 Cómo Usar

1. **Configura los Filtros:** Desde la barra lateral, ajusta parámetros como el número de clientes, vendedores, vehículos, fechas y cantidad de facturas a generar.
2. **Genera Datos:** Haz clic en el botón **Generar** para producir los datos simulados.
3. **Visualiza los Resultados:** Explora las tablas y gráficos generados en la interfaz principal.
4. **Exporta los Datos:** Descarga los datos en el formato deseado para integrarlos en otros proyectos.

---

## 📊 Estructura de los Datos

### Clientes
- Nombres, correos y teléfonos generados de manera aleatoria.

### Vendedores
- Información de contacto y fotos obtenidas desde la API de RandomUser.

### Vehículos
- Modelos predefinidos con características como marca, precio y tipo de combustible.

### Ventas
- Facturas detalladas con productos, cantidades, totales y ciudades de venta.

### Ejemplo de Salida
```json
{
  "id_venta": "123e4567-e89b-12d3-a456-426614174000",
  "vendedor": {
    "nombre": "Juan Pérez",
    "email": "juan.perez@example.com",
    "telefono": "809-555-1234",
    "gender": "male",
    "picture": {
      "url": "https://randomuser.me/api/portraits/men/1.jpg"
    }
  },
  "cliente": "María Gómez",
  "productos": [
    {
      "producto": "Toyota Corolla",
      "cantidad": 1,
      "total_producto": 23500,
      "imagen": "https://di-uploads-pod7.dealerinspire.com/toyotaofnorthmiami/uploads/2022/10/2023-GR-Corolla-1.png"
    }
  ],
  "total_venta": 23500,
  "fecha_venta": "2023-12-01",
  "ciudad_venta": "Santo Domingo"
}
```

---

## 🌍 Ciudades Soportadas
- Santo Domingo, Santiago, La Romana, Puerto Plata, y más.

---

## ✨ Autor
- **Ing. Juancito Peña**
  - 🚀 Contacto: [LinkedIn](https://www.linkedin.com/in/juancitopeña) | [GitHub](https://github.com/JUANCITOPENA)

---

## 📜 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🛠️ Futuras Ampliaciones
- **Soporte Multilenguaje:** Implementar configuraciones para diferentes idiomas.
- **Datos Geolocalizados:** Adicionar coordenadas geográficas para análisis espacial.
- **Dashboards Avanzados:** Crear paneles interactivos para análisis en tiempo real.
- **Automatización de APIs:** Integrar datos con servicios externos como Google Maps o Twilio.
