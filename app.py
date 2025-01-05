import random
import json
from faker import Faker
from datetime import datetime, timedelta
import streamlit as st
import requests
import certifi
import pandas as pd
from io import BytesIO
import time
import openpyxl

fake = Faker()


# Función para generar datos de vendedores
def generar_vendedores(num_vendedores):
    vendedores = []
    for i in range(num_vendedores):
        response = requests.get("https://randomuser.me/api/", verify=certifi.where())
        if response.status_code == 200:
            data = response.json()
            # Extraer información relevante
            gender = data['results'][0]['gender']
            picture_url = data['results'][0]['picture']['large']
            nombre = fake.name()
            email = fake.email()
            telefono = fake.phone_number()

            # Crear el vendedor
            vendedor = {
                "vendedor": i + 1,
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "picture": {
                    "url": picture_url
                },
                "gender": gender
            }
            vendedores.append(vendedor)
            time.sleep(0.5)  # Retraso para evitar sobrecargar el servidor
        else:
            st.error(f"Error al obtener datos para el vendedor {i + 1}")
    
    return vendedores



# Función para generar datos de ventas simuladas
def generar_venta(clientes, vendedores, vehiculos, rango_fechas, cantidad_facturas):
    ventas = []
    for _ in range(cantidad_facturas):
        cliente = random.choice(clientes)
        vendedor = random.choice(vendedores)
        productos = random.sample(vehiculos, random.randint(1, 5))  # Seleccionar entre 1 y 3 vehículos
        total_venta = sum(producto["precio_venta"] for producto in productos)  # Total de todos los productos
        cantidad_total = sum(1 for _ in productos)  # Cantidad total de vehículos en la factura
        fecha_venta = fake.date_between(start_date=rango_fechas[0], end_date=rango_fechas[1])
        
        venta_detalles = []

        for producto in productos:
          if 'precio_venta' not in producto:
              print(f"Falta la clave 'precio_venta' en el producto: {producto}")
          else:
              venta_detalles.append({
                  "producto": producto["modelo"],
                  "cantidad": 1,
                  "total_producto": producto["precio_venta"],
                  "imagen": producto["imagen"]
        })


        # Calcular el total general para la factura
        total_gral = sum(detalle["total_producto"] for detalle in venta_detalles)

        # Obtener una ciudad al azar para la venta (de las definidas)
        ciudad_venta = random.choice(list(ciudades.keys()))

        # Crear una factura con todos los detalles
        venta = {
            "id_venta": fake.uuid4(),
            "vendedor": vendedor,
            "cliente": cliente,
            "productos": venta_detalles,
            "total_venta": total_venta,
            "cantidad_total": cantidad_total,  # Agregar la cantidad total
            "total_gral": total_gral,  # Agregar el total general de la factura
            "fecha_venta": str(fecha_venta),
            "ciudad_venta": ciudad_venta  # Agregar la ciudad de la venta
        }
        ventas.append(venta)
    
    return ventas

# Definición de ciudades
ciudades = {
    "Santo Domingo": {"codigo": "SDQ", "lat": 18.4861, "lon": -69.9312},
    "Santiago": {"codigo": "STI", "lat": 19.4500, "lon": -70.7000},
    "La Romana": {"codigo": "LRQ", "lat": 18.4333, "lon": -68.9667},
    "San Francisco de Macorís": {"codigo": "SFM", "lat": 19.3000, "lon": -70.2500},
    "Puerto Plata": {"codigo": "POP", "lat": 19.7953, "lon": -70.6944},
    "Moca": {"codigo": "MCQ", "lat": 19.3833, "lon": -70.5167},
    "Boca Chica": {"codigo": "BCQ", "lat": 18.4475, "lon": -69.6067},
    "Higüey": {"codigo": "HQG", "lat": 18.6153, "lon": -68.7072},
    "Nagua": {"codigo": "NGQ", "lat": 19.3833, "lon": -69.8500},
    "San Pedro de Macorís": {"codigo": "SPM", "lat": 18.4500, "lon": -69.3000},
    "Barahona": {"codigo": "BRH", "lat": 18.2194, "lon": -71.1194},
    "La Vega": {"codigo": "LVE", "lat": 19.2328, "lon": -70.5344},
    "San Cristóbal": {"codigo": "SCA", "lat": 18.3667, "lon": -70.0167},
    "Villa Altagracia": {"codigo": "VAL", "lat": 18.9603, "lon": -70.2433},
    "San Juan de la Maguana": {"codigo": "SJM", "lat": 18.8200, "lon": -71.1394},
    "Dajabón": {"codigo": "DAJ", "lat": 19.5553, "lon": -71.6844},
    "Azua": {"codigo": "AZU", "lat": 18.4344, "lon": -70.7356},
    "Constanza": {"codigo": "CON", "lat": 18.9214, "lon": -70.8956},
    "Sabaneta": {"codigo": "SAB", "lat": 18.5897, "lon": -71.2797},
    "Punta Cana": {"codigo": "PUC", "lat": 18.5810, "lon": -68.3749},
    "Pedernales": {"codigo": "PED", "lat": 18.1375, "lon": -71.7628},
    "Bani": {"codigo": "BAN", "lat": 18.2711, "lon": -70.3206},
    "Montecristi": {"codigo": "MTC", "lat": 19.8028, "lon": -71.6642},
    "Cotuí": {"codigo": "CTU", "lat": 19.0297, "lon": -70.2322},
    "San José de Ocoa": {"codigo": "SJO", "lat": 18.4731, "lon": -70.8839},
    "Jarabacoa": {"codigo": "JAR", "lat": 19.0853, "lon": -70.6792},
    "Hato Mayor": {"codigo": "HTM", "lat": 18.6439, "lon": -69.2767},
    "La Altagracia": {"codigo": "LAG", "lat": 18.5644, "lon": -68.3767},
    "Santiago Rodríguez": {"codigo": "SRO", "lat": 19.2217, "lon": -71.1647},
    "New York": {"codigo": "NYC", "lat": 40.7128, "lon": -74.0060},
    "Los Angeles": {"codigo": "LAX", "lat": 34.0522, "lon": -118.2437},
    "Chicago": {"codigo": "CHI", "lat": 41.8781, "lon": -87.6298},
    "Houston": {"codigo": "HOU", "lat": 29.7604, "lon": -95.3698},
    "Miami": {"codigo": "MIA", "lat": 25.7617, "lon": -80.1918},
    "Toronto": {"codigo": "TOR", "lat": 43.6510, "lon": -79.3470},
    "Vancouver": {"codigo": "VAN", "lat": 49.2827, "lon": -123.1207},
    "Montreal": {"codigo": "MTL", "lat": 45.5017, "lon": -73.5673},
    "Mexico City": {"codigo": "MEX", "lat": 19.4326, "lon": -99.1332},
    "Guadalajara": {"codigo": "GDL", "lat": 20.6597, "lon": -103.3496},
    "Lima": {"codigo": "LIM", "lat": -12.0464, "lon": -77.0428},
    "Bogotá": {"codigo": "BOG", "lat": 4.7110, "lon": -74.0721},
    "Buenos Aires": {"codigo": "BUE", "lat": -34.6037, "lon": -58.3816},
    "Santiago de Chile": {"codigo": "STG", "lat": -33.4489, "lon": -70.6693},
    "São Paulo": {"codigo": "SAO", "lat": -23.5505, "lon": -46.6333},
    "Rio de Janeiro": {"codigo": "RIO", "lat": -22.9068, "lon": -43.1729},
    "Madrid": {"codigo": "MAD", "lat": 40.4168, "lon": -3.7038},
    "Barcelona": {"codigo": "BCN", "lat": 41.3851, "lon": 2.1734},
    "Paris": {"codigo": "PAR", "lat": 48.8566, "lon": 2.3522},
    "Lyon": {"codigo": "LYN", "lat": 45.7640, "lon": 4.8357},
    "Berlin": {"codigo": "BER", "lat": 52.5200, "lon": 13.4050},
    "Munich": {"codigo": "MUC", "lat": 48.1351, "lon": 11.5820},
    "Rome": {"codigo": "ROM", "lat": 41.9028, "lon": 12.4964},
    "Milan": {"codigo": "MIL", "lat": 45.4642, "lon": 9.1900},
    "London": {"codigo": "LON", "lat": 51.5074, "lon": -0.1278},
    "Manchester": {"codigo": "MAN", "lat": 53.4808, "lon": -2.2426},
    "Tokyo": {"codigo": "TYO", "lat": 35.6895, "lon": 139.6917},
    "Osaka": {"codigo": "OSA", "lat": 34.6937, "lon": 135.5023},
    "Seoul": {"codigo": "SEO", "lat": 37.5665, "lon": 126.9780},
    "Beijing": {"codigo": "BEJ", "lat": 39.9042, "lon": 116.4074},
    "Shanghai": {"codigo": "SHA", "lat": 31.2304, "lon": 121.4737},
    "Sydney": {"codigo": "SYD", "lat": -33.8688, "lon": 151.2093},
    "Melbourne": {"codigo": "MEL", "lat": -37.8136, "lon": 144.9631},
    "Cape Town": {"codigo": "CPT", "lat": -33.9249, "lon": 18.4241},
    "Johannesburg": {"codigo": "JHB", "lat": -26.2041, "lon": 28.0473},
    "Dubai": {"codigo": "DXB", "lat": 25.276987, "lon": 55.296249},
    "Abu Dhabi": {"codigo": "AUH", "lat": 24.4539, "lon": 54.3773},
    "Istanbul": {"codigo": "IST", "lat": 41.0082, "lon": 28.9784},
    "Moscow": {"codigo": "MOS", "lat": 55.7558, "lon": 37.6173},
    "Saint Petersburg": {"codigo": "SPB", "lat": 59.9343, "lon": 30.3351},
    "New Delhi": {"codigo": "DEL", "lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"codigo": "BOM", "lat": 19.0760, "lon": 72.8777},
    "Bangkok": {"codigo": "BKK", "lat": 13.7563, "lon": 100.5018},
    "Kuala Lumpur": {"codigo": "KUL", "lat": 3.1390, "lon": 101.6869},
    "Singapore": {"codigo": "SIN", "lat": 1.3521, "lon": 103.8198},
    "Jakarta": {"codigo": "JKT", "lat": -6.2088, "lon": 106.8456},
    "Manila": {"codigo": "MNL", "lat": 14.5995, "lon": 120.9842},
    "Hanoi": {"codigo": "HAN", "lat": 21.0285, "lon": 105.8542}
}

# Datos de vehículos
# Datos de vehículos
vehiculos = [
    {
        "codigo": 1001,
        "tipo": "Sedán 🚗",
        "modelo": "Toyota Corolla",
        "caracteristicas": "5 asientos, motor de 2.0L",
        "imagen": "https://di-uploads-pod7.dealerinspire.com/toyotaofnorthmiami/uploads/2022/10/2023-GR-Corolla-1.png",
        "numeroPuertas": 4,
        "motor": "2.0L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 20000,
        "precio_venta": 23500
    },
    {
        "codigo": 1002,
        "tipo": "SUV 🚙",
        "modelo": "Honda CR-V",
        "caracteristicas": "7 asientos, tracción en las 4 ruedas",
        "imagen": "https://vehicle-images.dealerinspire.com/stock-images/chrome/7b86c6e9e60a2b8f14fd207fe964e40e.png",
        "numeroPuertas": 4,
        "motor": "2.4L",
        "combustible": "Gasolina",
        "categoria": "Intermedio",
        "precio_compra": 28000,
        "precio_venta": 32000
    },
    {
        "codigo": 1003,
        "tipo": "Deportivo 🏎️",
        "modelo": "Ford Mustang",
        "caracteristicas": "Potente motor V8, diseño aerodinámico",
        "imagen": "https://platform.cstatic-images.com/in/v2/stock_photos/6fc391c8-2e8b-4854-b84c-3c94c431fb19/ca5e1b68-4c6b-403b-b95a-a77a6f529da5.png",
        "numeroPuertas": 2,
        "motor": "V8",
        "combustible": "Gasolina",
        "categoria": "Deportivo Premium",
        "precio_compra": 40000,
        "precio_venta": 45000
    },
    {
        "codigo": 1004,
        "tipo": "Compacto 🚗",
        "modelo": "Volkswagen Golf",
        "caracteristicas": "4 asientos, económico y versátil",
        "imagen": "https://di-uploads-pod20.dealerinspire.com/hendrickvwfrisco/uploads/2023/02/mlp-img-top-2023-golf-r-temp.png",
        "numeroPuertas": 4,
        "motor": "1.8L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 22000,
        "precio_venta": 25000
    },
  {
    "codigo": 1005,
    "tipo": "Camioneta 🚚",
    "modelo": "Ford Explorer",
    "caracteristicas": "Capacidad para 7 pasajeros, tracción en las 4 ruedas",
    "imagen": "https://islarentacar.net/wp-content/uploads/2021/03/explorer-2012-.0.png",
    "numeroPuertas": 4,
    "motor": "3.5L",
    "combustible": "Gasolina",
    "categoria": "SUV Premium",
    "precio_compra": 40000,
    "precio_venta": 45000
  },
  {
    "codigo": 1006,
    "tipo": "Deportivo 🏎️",
    "modelo": "Chevrolet Camaro",
    "caracteristicas": "Potente motor V8, diseño deportivo",
    "imagen": "https://chevrolet.com.ph/wp-content/uploads/2022/06/camaro-Exterior-Crush-min.png",
    "numeroPuertas": 2,
    "motor": "V8",
    "combustible": "Gasolina",
    "categoria": "Deportivo Premium",
    "precio_compra": 38000,
    "precio_venta": 42000
  },
  {
    "codigo": 1007,
    "tipo": "Sedán 🚗",
    "modelo": "Honda Civic",
    "caracteristicas": "Espacioso y eficiente en combustible",
    "imagen": "https://vehicle-images.dealerinspire.com/stock-images/chrome/7b86c6e9e60a2b8f14fd207fe964e40e.png",
    "numeroPuertas": 4,
    "motor": "1.5L",
    "combustible": "Gasolina",
    "categoria": "Económico",
    "precio_compra": 22000,
    "precio_venta": 24000
  },
  {
    "codigo": 1008,
    "tipo": "SUV 🚙",
    "modelo": "Toyota RAV4",
    "caracteristicas": "Estilo deportivo, ideal para la aventura",
    "imagen": "https://deltacomercial.com.do/cdn/modelos/rav4/43670b4254bab43b747ec25fbfdf3713.png",
    "numeroPuertas": 4,
    "motor": "2.5L",
    "combustible": "Gasolina",
    "categoria": "Intermedio",
    "precio_compra": 30000,
    "precio_venta": 33000
  },
  {
    "codigo": 1009,
    "tipo": "Hatchback 🚗",
    "modelo": "Mazda 3",
    "caracteristicas": "Diseño elegante y deportivo, excelente manejo",
    "imagen": "https://di-uploads-pod2.dealerinspire.com/headquartermazdaspanishtoggle/uploads/2016/10/2017-Mazda3-Hatchback-On-White.png",
    "numeroPuertas": 4,
    "motor": "2.0L",
    "combustible": "Gasolina",
    "categoria": "Económico",
    "precio_compra": 23000,
    "precio_venta": 25500
  },
    {
    "codigo": 1010,
    "tipo": "Pickup 🚛",
    "modelo": "Ford F-150",
    "caracteristicas": "Resistente y duradero, capacidad de remolque",
    "imagen": "https://vehicle-images.dealerinspire.com/stock-images/ford/6e8545b98972a6fc71cb5386f12ed692.png",
    "numeroPuertas": 4,
    "motor": "5.0L",
    "combustible": "Gasolina",
    "categoria": "Trabajo Premium",
    "precio_compra": 48000,
    "precio_venta": 52000
  },
  {
    "codigo": 1011,
    "tipo": "Coupé 🏎️",
    "modelo": "BMW Serie 2",
    "caracteristicas": "Lujo y rendimiento en un diseño compacto",
    "imagen": "https://corporate.sixt.com/es-es/wp-content/uploads/sites/9/2022/10/sixt.com-alquiler-de-bmw-x4-sixt.com-bmw-2er-coupe-2d-blau.png",
    "numeroPuertas": 2,
    "motor": "3.0L",
    "combustible": "Gasolina",
    "categoria": "Lujo",
    "precio_compra": 45000,
    "precio_venta": 48000
  },
  {
    "codigo": 1012,
    "tipo": "Furgoneta 🚐",
    "modelo": "Mercedes-Benz Sprinter",
    "caracteristicas": "Gran capacidad de carga, ideal para negocios",
    "imagen": "https://www.motortrend.com/uploads/sites/10/2018/04/2018-mercedes-benz-sprinter-2500-170-wb-high-roof-passenger-van-angular-front.png",
    "numeroPuertas": 4,
    "motor": "2.1L",
    "combustible": "Diesel",
    "categoria": "Comercial Premium",
    "precio_compra": 42000,
    "precio_venta": 45000
  },
  {
    "codigo": 1013,
    "tipo": "Convertible 🚗",
    "modelo": "Chevrolet Corvette",
    "caracteristicas": "Estilo clásico y potencia deslumbrante",
    "imagen": "https://d3s2hob8w3xwk8.cloudfront.net/autos-landing/chevrolet/corvette-2023/colores/AMPLIFY-TINTCOAT.png",
    "numeroPuertas": 2,
    "motor": "6.2L",
    "combustible": "Gasolina",
    "categoria": "Superdeportivo",
    "precio_compra": 60000,
    "precio_venta": 65000
  },
  {
    "codigo": 1014,
    "tipo": "SUV 🚙",
    "modelo": "BMW X5",
    "caracteristicas": "5 asientos, potente motor y tecnología avanzada",
    "imagen": "https://images.carprices.com/pricebooks_data/usa/colorized/2023/BMW/View2/X5_M/X5_M/23XK_300.png",
    "numeroPuertas": 4,
    "motor": "3.0L",
    "combustible": "Gasolina",
    "categoria": "Lujo Premium",
    "precio_compra": 60000,
    "precio_venta": 65000
  },
  {
    "codigo": 1015,
    "tipo": "Sedán 🚗",
    "modelo": "Audi A4",
    "caracteristicas": "Diseño elegante, tecnología de punta",
    "imagen": "https://images.dealer.com/ddc/vehicles/2023/Audi/A4/Sedan/perspective/front-left/2023_76.png",
    "numeroPuertas": 4,
    "motor": "2.0L",
    "combustible": "Gasolina",
    "categoria": "Lujo",
    "precio_compra": 42000,
    "precio_venta": 45000
  },
  {
    "codigo": 1016,
    "tipo": "Sedán 🚗",
    "modelo": "Mercedes-Benz C-Class",
    "caracteristicas": "Lujo y rendimiento en cada detalle",
    "imagen": "https://images.dealer.com/ddc/vehicles/2023/Mercedes-Benz/C-Class/Coupe/perspective/front-left/2023_24.png",
    "numeroPuertas": 4,
    "motor": "2.0L",
    "combustible": "Gasolina",
    "categoria": "Lujo Premium",
    "precio_compra": 45000,
    "precio_venta": 48000
  },
    {
    "codigo": 1017,
    "tipo": "Eléctrico 🚗",
    "modelo": "Tesla Model S",
    "caracteristicas": "Rendimiento eléctrico, autonomía de largo alcance",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/52152/2024-Tesla-Model%20S-front_52152_032_1822x709_PPSB_cropped.png",
    "numeroPuertas": 4,
    "motor": "Eléctrico",
    "combustible": "Eléctrico",
    "categoria": "Lujo Premium Eléctrico",
    "precio_compra": 80000,
    "precio_venta": 85000
  },
  {
    "codigo": 1018,
    "tipo": "Sedán 🚗",
    "modelo": "Nissan Altima",
    "caracteristicas": "Tecnología avanzada, diseño aerodinámico",
    "imagen": "https://di-uploads-pod42.dealerinspire.com/southparknissan/uploads/2023/11/2024-nissan-altima-main.png",
    "numeroPuertas": 4,
    "motor": "2.5L",
    "combustible": "Gasolina",
    "categoria": "Intermedio",
    "precio_compra": 25000,
    "precio_venta": 27000
  },
  {
    "codigo": 1019,
    "tipo": "Híbrido 🚗",
    "modelo": "Toyota Prius",
    "caracteristicas": "Eficiencia híbrida, bajo consumo de combustible",
    "imagen": "https://www.toyota.com.sg/showroom/new-models/-/media/4ec94a5afd6d4faab5973c826ef1770b.png",
    "numeroPuertas": 4,
    "motor": "1.8L Híbrido",
    "combustible": "Híbrido",
    "categoria": "Económico Híbrido",
    "precio_compra": 28000,
    "precio_venta": 29500
  },
  {
    "codigo": 1020,
    "tipo": "SUV Eléctrico 🚙",
    "modelo": "Audi e-tron",
    "caracteristicas": "SUV totalmente eléctrico, lujo y sostenibilidad",
    "imagen": "https://www.motortrend.com/uploads/izmo/audi/e_tron_sportback/2021/e_tron_sportback.png",
    "numeroPuertas": 4,
    "motor": "Eléctrico Dual",
    "combustible": "Eléctrico",
    "categoria": "Lujo Premium Eléctrico",
    "precio_compra": 72000,
    "precio_venta": 75000
  },
  {
    "codigo": 1021,
    "tipo": "Pickup Lujo 🚛",
    "modelo": "RAM 1500 Limited",
    "caracteristicas": "Interior premium, capacidad todoterreno",
    "imagen": "https://di-uploads-pod11.dealerinspire.com/cdjconfidential/uploads/2019/10/limited-header.png",
    "numeroPuertas": 4,
    "motor": "5.7L HEMI",
    "combustible": "Gasolina",
    "categoria": "Pickup Premium",
    "precio_compra": 58000,
    "precio_venta": 62000
  },
  {
    "codigo": 1022,
    "tipo": "Superdeportivo 🏎️",
    "modelo": "Porsche 911",
    "caracteristicas": "Rendimiento legendario, diseño icónico",
    "imagen": "https://euroshop.com.pe/wp-content/uploads/2024/09/porsche-911.png",
    "numeroPuertas": 2,
    "motor": "3.0L Twin-Turbo",
    "combustible": "Gasolina",
    "categoria": "Superdeportivo Premium",
    "precio_compra": 110000,
    "precio_venta": 115000
  },
   {
    "codigo": 1023,
    "tipo": "SUV Compacto 🚙",
    "modelo": "Volvo XC40",
    "caracteristicas": "Seguridad avanzada, diseño escandinavo",
    "imagen": "https://images.dealer.com/ddc/vehicles/2021/Volvo/XC40/SUV/perspective/front-left/2021_76.png",
    "numeroPuertas": 4,
    "motor": "2.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "Lujo Compacto",
    "precio_compra": 35000,
    "precio_venta": 38500
  },
  {
    "codigo": 1024,
    "tipo": "Minivan 🚐",
    "modelo": "Honda Odyssey",
    "caracteristicas": "Espacio familiar, confort superior",
    "imagen": "https://www.swickardhonda.com/assets/stock/ColorMatched_01/Transparent/640/cc_2021HOV01_01_640/cc_2021HOV010072_01_640_BS.png",
    "numeroPuertas": 4,
    "motor": "3.5L V6",
    "combustible": "Gasolina",
    "categoria": "Familiar Premium",
    "precio_compra": 38000,
    "precio_venta": 42000
  },
  {
    "codigo": 1025,
    "tipo": "Crossover 🚙",
    "modelo": "Lexus NX",
    "caracteristicas": "Lujo compacto, tecnología híbrida",
    "imagen": "https://dealerimages.dealereprocess.com/image/upload/v1711401385/1/lexus/2025_NX/LEX-NXG-MY25-0001.07-E01-Base250FWD-Ext1-GrecianWater-W18inStdG4AD.png",
    "numeroPuertas": 4,
    "motor": "2.5L Híbrido",
    "combustible": "Híbrido",
    "categoria": "Lujo Híbrido",
    "precio_compra": 42000,
    "precio_venta": 45500
  },
  {
    "codigo": 1026,
    "tipo": "Superdeportivo 🏎️",
    "modelo": "Lamborghini Huracán",
    "caracteristicas": "Motor V10, diseño futurista, máximo rendimiento",
    "imagen": "https://images.dealer.com/ddc/vehicles/2024/Lamborghini/Huracan%20Tecnica/Coupe/trim_Base_3da5c4/perspective/side-left/2024_24.png",
    "numeroPuertas": 2,
    "motor": "5.2L V10",
    "combustible": "Gasolina",
    "categoria": "Superdeportivo Ultra Premium",
    "precio_compra": 245000,
    "precio_venta": 265000
  },
  {
    "codigo": 1027,
    "tipo": "Luxury Sedan 🚗",
    "modelo": "Rolls-Royce Ghost",
    "caracteristicas": "Lujo supremo, acabados artesanales, máximo confort",
    "imagen": "https://www.motortrend.com/uploads/2021/12/2022-Rolls-Royce-Ghost.png",
    "numeroPuertas": 4,
    "motor": "6.75L V12",
    "combustible": "Gasolina",
    "categoria": "Ultra Lujo Premium",
    "precio_compra": 295000,
    "precio_venta": 315000
  },
  {
    "codigo": 1028,
    "tipo": "Compacto 🚗",
    "modelo": "Chevrolet Spark",
    "caracteristicas": "Ultra compacto, excelente consumo de combustible",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/12451/2018-Chevrolet-Spark-front_12451_032_1887x956_GW7_cropped.png",
    "numeroPuertas": 4,
    "motor": "1.4L",
    "combustible": "Gasolina",
    "categoria": "Económico",
    "precio_compra": 14000,
    "precio_venta": 15500
  },
  {
    "codigo": 1029,
    "tipo": "Hatchback 🚗",
    "modelo": "Kia Rio",
    "caracteristicas": "Eficiente, práctico y bajo mantenimiento",
    "imagen": "https://kia.com.do/wp-content/uploads/2023/02/rio-color-5.webp",
    "numeroPuertas": 4,
    "motor": "1.6L",
    "combustible": "Gasolina",
    "categoria": "Económico",
    "precio_compra": 16000,
    "precio_venta": 17200
  },
  {
    "codigo": 1030,
    "tipo": "Sedán 🚗",
    "modelo": "Hyundai Accent",
    "caracteristicas": "Económico, espacioso, ideal para ciudad",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/13297/2021-Hyundai-Accent-front_13297_032_1844x803_R4R_cropped.png",
    "numeroPuertas": 4,
    "motor": "1.6L",
    "combustible": "Gasolina",
    "categoria": "Económico",
    "precio_compra": 15000,
    "precio_venta": 16800
  },
    {
    "codigo": 1031,
    "tipo": "Hypercar 🏎️",
    "modelo": "Bugatti Chiron",
    "caracteristicas": "Velocidad máxima 420 km/h, motor W16 quad-turbo, edición limitada",
    "imagen": "https://i.pinimg.com/originals/e9/34/ac/e934ac022c9ecf2dadf6954610176627.png",
    "numeroPuertas": 2,
    "motor": "8.0L W16 Quad-Turbo",
    "combustible": "Gasolina Premium",
    "categoria": "Hypercar Ultra Premium",
    "precio_compra": 2800000,
    "precio_venta": 3500000
  },
  {
    "codigo": 1032,
    "tipo": "Superdeportivo Eléctrico 🏎️",
    "modelo": "Rimac Nevera",
    "caracteristicas": "100% eléctrico, 1914 hp, 0-100 km/h en 1.85s",
    "imagen": "https://www.evspecifications.info/wp-content/uploads/2022/10/Rimac-Nevera.png",
    "numeroPuertas": 2,
    "motor": "Eléctrico Cuádruple",
    "combustible": "Eléctrico",
    "categoria": "Hypercar Eléctrico",
    "precio_compra": 2000000,
    "precio_venta": 2400000
  },
  {
    "codigo": 1033,
    "tipo": "Grand Tourer 🏎️",
    "modelo": "Aston Martin DBS",
    "caracteristicas": "Interior artesanal, V12 biturbo, máximo lujo deportivo",
    "imagen": "https://www.motortrend.com/uploads/sites/5/2020/06/2020-astonmartin-dbs.png",
    "numeroPuertas": 2,
    "motor": "5.2L V12 Twin-Turbo",
    "combustible": "Gasolina Premium",
    "categoria": "GT Ultra Premium",
    "precio_compra": 300000,
    "precio_venta": 375000
  },
  {
    "codigo": 1034,
    "tipo": "SUV Ultra Lujo 🚙",
    "modelo": "Bentley Bentayga",
    "caracteristicas": "SUV más lujoso del mundo, acabados personalizados",
    "imagen": "https://images.ctfassets.net/p77iaapls74f/5LOq3BscRS5f74C0eycbGq/f58fdab7d5c90b93efc789522f5a6d83/EWB.png",
    "numeroPuertas": 4,
    "motor": "6.0L W12 Twin-Turbo",
    "combustible": "Gasolina Premium",
    "categoria": "SUV Ultra Premium",
    "precio_compra": 350000,
    "precio_venta": 450000
  },
  {
    "codigo": 1035,
    "tipo": "Superdeportivo 🏎️",
    "modelo": "Ferrari SF90 Stradale",
    "caracteristicas": "Híbrido enchufable, 1000 hp, tecnología F1",
    "imagen": "https://cdn.wheel-size.com/automobile/body/ferrari-sf90-stradale-2019-2021-1606211392.6015837.webp",
    "numeroPuertas": 2,
    "motor": "4.0L V8 Híbrido",
    "combustible": "Híbrido Premium",
    "categoria": "Superdeportivo Híbrido Premium",
    "precio_compra": 500000,
    "precio_venta": 625000
  }
]


# Interfaz de usuario con elementos centrados
st.markdown(
    """
    <h1 style="text-align: center;">🚗 Generador de Datos de Ventas</h1>
    <h4 style="text-align: center; color: white;">📊 Si quieres aprender de Análisis y Visualización de Datos con Imágenes de Autos y Vendedores, este **dataset** es genial. 🧑‍💻</h4>
    <h5 style="text-align: center; color: orange;">✨Creado por Ing. Juancito Peña ✨</h5>
    """,
    unsafe_allow_html=True,
)

# Filtros en Streamlit
st.sidebar.title('Filtros de Generación de Datos')

num_clientes = st.sidebar.slider('Número de Clientes', 1, 5000, 100)
num_vendedores = st.sidebar.slider('Número de Vendedores', 1, 500, 50)
num_vehiculos = st.sidebar.slider('Número de Vehículos a Incluir', 1, len(vehiculos), len(vehiculos))
rango_fecha_inicio = st.sidebar.date_input('Fecha de Inicio', datetime(2020, 1, 1))
rango_fecha_fin = st.sidebar.date_input('Fecha de Fin', datetime(2024, 12, 12))
cantidad_facturas = st.sidebar.slider('Cantidad de Facturas', 1, 5000, 200)

# Función para convertir las fechas a string
def convertir_fechas_a_string(venta):
    venta['fecha_venta'] = venta['fecha_venta'].strftime('%Y-%m-%d')  # Convertir la fecha a string
    return venta

# Función para generar factura con cálculos adicionales
def generar_factura(clientes, vendedores, vehiculos, fecha_rango, id_factura, vendedores_usados):
    vendedores_disponibles = [v for v in vendedores if v['nombre'] not in vendedores_usados]

    if not vendedores_disponibles:
        vendedores_usados.clear()
        vendedores_disponibles = vendedores

    vendedor = random.choice(vendedores_disponibles)
    vendedores_usados.add(vendedor['nombre'])
    cliente = random.choice(clientes)
    fecha_venta = fake.date_between_dates(fecha_rango[0], fecha_rango[1])

    ciudad_venta = random.choice(list(ciudades.keys()))
    ciudad_data = ciudades[ciudad_venta]

    num_items = random.randint(1, 5)
    productos = []
    total_gral = 0
    costo_total = 0

    for _ in range(num_items):
        producto = random.choice(vehiculos)
        cantidad = random.randint(1, 10)

        costo = producto['precio_compra'] * cantidad
        total_producto = producto['precio_venta'] * cantidad
        margen = total_producto - costo
        porcentaje_margen = (margen / costo) * 100 if costo > 0 else 0

        total_gral += total_producto
        costo_total += costo

        productos.append({
            "producto": producto['modelo'],
            "cantidad": cantidad,
            "total_producto": total_producto,
            "costo": costo,
            "margen": margen,
            "porcentaje_margen": porcentaje_margen,
            "imagen": producto['imagen'],
        })

    random_number = random.random()
    if random_number < 0.90:
        estado_entrega = "Entregado"
        retorno_dinero = 0
    elif random_number < 0.98:
        estado_entrega = "En Proceso"
        retorno_dinero = 0
    else:
        estado_entrega = "Cancelado"
        retorno_dinero = total_gral

    return {
        "codigo_factura": f"FACT-{id_factura:04d}",
        "vendedor": vendedor,
        "cliente": cliente,
        "fecha_venta": fecha_venta,
        "ciudad_venta": ciudad_venta,
        "latitud_ciudad_venta": ciudad_data["lat"],
        "longitud_ciudad_venta": ciudad_data["lon"],
        "productos": productos,
        "cantidad_total": sum(item['cantidad'] for item in productos),
        "total_gral": total_gral,
        "costo_total": costo_total,
        "margen_total": total_gral - costo_total,
        "porcentaje_margen_total": ((total_gral - costo_total) / costo_total) * 100 if costo_total > 0 else 0,
        "estado_entrega": estado_entrega,
        "retorno_dinero": retorno_dinero,
    }

# Función para generar todas las ventas simuladas
def generar_venta(clientes, vendedores, vehiculos, fecha_rango, cantidad_facturas):
    ventas = []
    vendedores_usados = set()
    for i in range(1, cantidad_facturas + 1):
        factura = generar_factura(clientes, vendedores, vehiculos, fecha_rango, i, vendedores_usados)
        factura_convertida = convertir_fechas_a_string(factura)
        ventas.append(factura_convertida)
    return ventas

# Generación de datos cuando se presiona el botón
if st.sidebar.button('Generar'):
    st.info("Generando .... por favor espera...🔃")

    clientes = [fake.name() for _ in range(num_clientes)]
    vendedores = generar_vendedores(num_vendedores)

    ventas_simuladas = generar_venta(
        clientes,
        vendedores,
        vehiculos[:num_vehiculos],
        [rango_fecha_inicio, rango_fecha_fin],
        cantidad_facturas
    )

    st.title('Simulador de Ventas')
    st.write(f"Se generaron {len(ventas_simuladas)} facturas")

    for venta in ventas_simuladas:
        st.write(f"**Código de Factura:** {venta['codigo_factura']}")
        st.write(f"**Vendedor:** {venta['vendedor']['nombre']} - **Cliente:** {venta['cliente']}")
        st.image(venta['vendedor']['picture']['url'], width=100)
        st.write(f"**Fecha de Venta:** {venta['fecha_venta']}")
        st.write(f"**Ciudad de Venta:** {venta['ciudad_venta']}")
        st.write(f"**Latitud:** {venta['latitud_ciudad_venta']}, **Longitud:** {venta['longitud_ciudad_venta']}")
        st.write(f"**Estado de Entrega:** {venta['estado_entrega']}")
        st.write(f"**Retorno de Dinero:** ${venta['retorno_dinero']}")

        for detalle in venta["productos"]:
            st.write(f"  - **Producto:** {detalle['producto']} - **Cantidad:** {detalle['cantidad']} - **Total Producto:** ${detalle['total_producto']} - **Costo:** ${detalle['costo']} - **Margen:** ${detalle['margen']} - **% Margen:** {detalle['porcentaje_margen']:.2f}%")
            st.image(detalle['imagen'], width=300)

        st.write(f"**Total Venta:** ${venta['total_gral']}")
        st.write(f"**Costo Total:** ${venta['costo_total']}")
        st.write(f"**Margen Total:** ${venta['margen_total']}")
        st.write(f"**% Margen Total:** {venta['porcentaje_margen_total']:.2f}%")
        st.write("---")

    with open('ventas_simuladas.json', 'w') as outfile:
        json.dump(ventas_simuladas, outfile, indent=4)

    df_ventas = pd.DataFrame(ventas_simuladas)
    excel_buffer = BytesIO()
    df_ventas.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    st.sidebar.markdown("### Descargar Datos Generados")

    st.sidebar.download_button(
        label="Descargar ventas en formato JSON",
        data=json.dumps(ventas_simuladas, indent=4),
        file_name="ventas_simuladas.json",
        mime="application/json"
    )

    st.sidebar.download_button(
        label="Descargar ventas en formato Excel",
        data=excel_buffer,
        file_name="ventas_simuladas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
