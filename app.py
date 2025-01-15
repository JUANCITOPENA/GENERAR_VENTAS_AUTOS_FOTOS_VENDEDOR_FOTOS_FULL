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
            gender = data['results'][0]['gender']  # 'male' o 'female'
            picture_url = data['results'][0]['picture']['large']
            email = fake.email()
            telefono = fake.phone_number()

            # Generar nombre acorde al género
            if gender == "male":
                nombre = fake.first_name_male() + " " + fake.last_name_male()
            elif gender == "female":
                nombre = fake.first_name_female() + " " + fake.last_name_female()
            else:
                nombre = fake.name()  # En caso de algún error, genera un nombre genérico

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
    
    # Definición de tipos de pago y sus probabilidades
    tipos_pago = ["Efectivo", "Tarjeta de Crédito", "Crédito", "Transferencias"]
    probabilidades_pago = [0.40, 0.28, 0.20, 0.12]
    
    for _ in range(cantidad_facturas):
        cliente = random.choice(clientes)
        vendedor = random.choice(vendedores)
        productos = random.sample(vehiculos, random.randint(1, 5))  # Seleccionar entre 1 y 5 vehículos
        total_venta = sum(producto["precio_venta"] for producto in productos)  # Total de todos los productos
        cantidad_total = sum(1 for _ in productos)  # Cantidad total de vehículos en la factura
        fecha_venta = fake.date_between(start_date=rango_fechas[0], end_date=rango_fechas[1])
        
        venta_detalles = []

        for producto in productos:
            if 'precio_venta' not in producto or 'logo' not in producto:
                print(f"Falta la clave 'precio_venta' o 'logo' en el producto: {producto}")
            else:
                venta_detalles.append({
                    "producto": producto["modelo"],
                    "cantidad": 1,
                    "total_producto": producto["precio_venta"],
                    "imagen": producto["imagen"],  # Imagen principal
                    "logo": producto["logo"]  # Logo del producto
                })

        # Calcular el total general para la factura
        total_gral = sum(detalle["total_producto"] for detalle in venta_detalles)

        # Obtener una ciudad al azar para la venta (de las definidas)
        ciudad_venta = random.choice(list(ciudades.keys()))

        # Asignar tipo de pago basado en probabilidades
        tipo_pago = random.choices(tipos_pago, probabilidades_pago)[0]

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
            "ciudad_venta": ciudad_venta,  # Agregar la ciudad de la venta
            "tipo_pago": tipo_pago  # Agregar el tipo de pago
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
        "marca": "Toyota",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Toyota_logo_%28Red%29.svg/2560px-Toyota_logo_%28Red%29.svg.png",
        "tipo": "Sedán 🚗",
        "modelo": "Toyota Corolla",
        "caracteristicas": "5 asientos, motor de 2.0L",
        "imagen": "https://di-uploads-pod7.dealerinspire.com/toyotaofnorthmiami/uploads/2022/10/2023-GR-Corolla-1.png",
        "numeroPuertas": 4,
        "motor": "2.0L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 20000,
        "precio_venta": 23500,
        "existencia": 2000
    },
    {
        "codigo": 1002,
        "marca": "Honda",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Logo_Honda_F1.png",
        "tipo": "SUV 🚙",
        "modelo": "Honda CR-V",
        "caracteristicas": "7 asientos, tracción en las 4 ruedas",
        "imagen": "https://vehicle-images.dealerinspire.com/stock-images/chrome/7b86c6e9e60a2b8f14fd207fe964e40e.png",
        "numeroPuertas": 4,
        "motor": "2.4L",
        "combustible": "Gasolina",
        "categoria": "Intermedio",
        "precio_compra": 28000,
        "precio_venta": 32000,
        "existencia": 2000
    },
    {
        "codigo": 1003,
        "marca": "Ford",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ford_logo_flat.svg/1200px-Ford_logo_flat.svg.png",
        "tipo": "Deportivo 🏎️",
        "modelo": "Ford Mustang",
        "caracteristicas": "Potente motor V8, diseño aerodinámico",
        "imagen": "https://platform.cstatic-images.com/in/v2/stock_photos/6fc391c8-2e8b-4854-b84c-3c94c431fb19/ca5e1b68-4c6b-403b-b95a-a77a6f529da5.png",
        "numeroPuertas": 2,
        "motor": "V8",
        "combustible": "Gasolina",
        "categoria": "Deportivo Premium",
        "precio_compra": 40000,
        "precio_venta": 45000,
        "existencia": 2000
    },
    {
        "codigo": 1004,
        "marca": "Volkswagen",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Volkswagen_logo_2019.svg/2048px-Volkswagen_logo_2019.svg.png",
        "tipo": "Compacto 🚗",
        "modelo": "Volkswagen Golf",
        "caracteristicas": "4 asientos, económico y versátil",
        "imagen": "https://di-uploads-pod20.dealerinspire.com/hendrickvwfrisco/uploads/2023/02/mlp-img-top-2023-golf-r-temp.png",
        "numeroPuertas": 4,
        "motor": "1.8L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 22000,
        "precio_venta": 25000,
        "existencia": 2000
    },
    {
        "codigo": 1005,
        "marca": "Ford",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ford_logo_flat.svg/1200px-Ford_logo_flat.svg.png",
        "tipo": "Camioneta 🚚",
        "modelo": "Ford Explorer",
        "caracteristicas": "Capacidad para 7 pasajeros, tracción en las 4 ruedas",
        "imagen": "https://islarentacar.net/wp-content/uploads/2021/03/explorer-2012-.0.png",
        "numeroPuertas": 4,
        "motor": "3.5L",
        "combustible": "Gasolina",
        "categoria": "SUV Premium",
        "precio_compra": 40000,
        "precio_venta": 45000,
        "existencia": 2000
    },
    {
        "codigo": 1006,
        "marca": "Chevrolet",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/Chevrolet-logo.png",
        "tipo": "Deportivo 🏎️",
        "modelo": "Chevrolet Camaro",
        "caracteristicas": "Potente motor V8, diseño deportivo",
        "imagen": "https://chevrolet.com.ph/wp-content/uploads/2022/06/camaro-Exterior-Crush-min.png",
        "numeroPuertas": 2,
        "motor": "V8",
        "combustible": "Gasolina",
        "categoria": "Deportivo Premium",
        "precio_compra": 38000,
        "precio_venta": 42000,
        "existencia": 2000
    },
    {
        "codigo": 1007,
        "marca": "Honda",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Logo_Honda_F1.png",
        "tipo": "Sedán 🚗",
        "modelo": "Honda Civic",
        "caracteristicas": "Espacioso y eficiente en combustible",
        "imagen": "https://vehicle-images.dealerinspire.com/stock-images/chrome/7b86c6e9e60a2b8f14fd207fe964e40e.png",
        "numeroPuertas": 4,
        "motor": "1.5L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 22000,
        "precio_venta": 24000,
        "existencia": 2000
    },
    {
        "codigo": 1008,
        "marca": "Toyota",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Toyota_logo_%28Red%29.svg/2560px-Toyota_logo_%28Red%29.svg.png",
        "tipo": "SUV 🚙",
        "modelo": "Toyota RAV4",
        "caracteristicas": "Estilo deportivo, ideal para la aventura",
        "imagen": "https://deltacomercial.com.do/cdn/modelos/rav4/43670b4254bab43b747ec25fbfdf3713.png",
        "numeroPuertas": 4,
        "motor": "2.5L",
        "combustible": "Gasolina",
        "categoria": "Intermedio",
        "precio_compra": 30000,
        "precio_venta": 33000,
        "existencia": 2000
    },
    {
        "codigo": 1009,
        "marca": "Mazda",
        "logo": "https://pngimg.com/d/mazda_PNG86.png",
        "tipo": "Hatchback 🚗",
        "modelo": "Mazda 3",
        "caracteristicas": "Diseño elegante y deportivo, excelente manejo",
        "imagen": "https://di-uploads-pod2.dealerinspire.com/headquartermazdaspanishtoggle/uploads/2016/10/2017-Mazda3-Hatchback-On-White.png",
        "numeroPuertas": 4,
        "motor": "2.0L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 23000,
        "precio_venta": 25500,
        "existencia": 2000
    },
    {
        "codigo": 1010,
        "marca": "Ford",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ford_logo_flat.svg/1200px-Ford_logo_flat.svg.png",
        "tipo": "Pickup 🚛",
        "modelo": "Ford F-150",
        "caracteristicas": "Resistente y duradero, capacidad de remolque",
        "imagen": "https://vehicle-images.dealerinspire.com/stock-images/ford/6e8545b98972a6fc71cb5386f12ed692.png",
        "numeroPuertas": 4,
        "motor": "5.0L",
        "combustible": "Gasolina",
        "categoria": "Trabajo Premium",
        "precio_compra": 48000,
        "precio_venta": 52000,
        "existencia": 2000
    },
    {
        "codigo": 1011,
        "marca": "BMW",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/1024px-BMW.svg.png",
        "tipo": "Coupé 🏎️",
        "modelo": "BMW Serie 2",
        "caracteristicas": "Lujo y rendimiento en un diseño compacto",
        "imagen": "https://corporate.sixt.com/es-es/wp-content/uploads/sites/9/2022/10/sixt.com-alquiler-de-bmw-x4-sixt.com-bmw-2er-coupe-2d-blau.png",
        "numeroPuertas": 2,
        "motor": "3.0L",
        "combustible": "Gasolina",
        "categoria": "Lujo",
        "precio_compra": 45000,
        "precio_venta": 48000,
        "existencia": 2000
    },
    {
        "codigo": 1012,
        "marca": "Mercedes-Benz",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Mercedes-Benz_Star_2022.svg/800px-Mercedes-Benz_Star_2022.svg.png",
        "tipo": "Furgoneta 🚐",
        "modelo": "Mercedes-Benz Sprinter",
        "caracteristicas": "Gran capacidad de carga, ideal para negocios",
        "imagen": "https://www.motortrend.com/uploads/sites/10/2018/04/2018-mercedes-benz-sprinter-2500-170-wb-high-roof-passenger-van-angular-front.png",
        "numeroPuertas": 4,
        "motor": "2.1L",
        "combustible": "Diesel",
        "categoria": "Comercial Premium",
        "precio_compra": 42000,
        "precio_venta": 45000,
        "existencia": 2000
    },
    {
        "codigo": 1013,
        "marca": "Chevrolet",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/Chevrolet-logo.png",
        "tipo": "Convertible 🚗",
        "modelo": "Chevrolet Corvette",
        "caracteristicas": "Estilo clásico y potencia deslumbrante",
        "imagen": "https://d3s2hob8w3xwk8.cloudfront.net/autos-landing/chevrolet/corvette-2023/colores/AMPLIFY-TINTCOAT.png",
        "numeroPuertas": 2,
        "motor": "6.2L",
        "combustible": "Gasolina",
        "categoria": "Superdeportivo",
        "precio_compra": 60000,
        "precio_venta": 65000,
        "existencia": 2000
    },
    {
        "codigo": 1014,
        "marca": "BMW",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/1024px-BMW.svg.png",
        "tipo": "SUV 🚙",
        "modelo": "BMW X5",
        "caracteristicas": "5 asientos, potente motor y tecnología avanzada",
        "imagen": "https://images.carprices.com/pricebooks_data/usa/colorized/2023/BMW/View2/X5_M/X5_M/23XK_300.png",
        "numeroPuertas": 4,
        "motor": "3.0L",
        "combustible": "Gasolina",
        "categoria": "Lujo Premium",
        "precio_compra": 60000,
        "precio_venta": 65000,
        "existencia": 2000
    },
    {
        "codigo": 1015,
        "marca": "Audi",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Audi_logo_detail.svg/1024px-Audi_logo_detail.svg.png",
        "tipo": "Sedán 🚗",
        "modelo": "Audi A4",
        "caracteristicas": "Diseño elegante, tecnología de punta",
        "imagen": "https://images.dealer.com/ddc/vehicles/2023/Audi/A4/Sedan/perspective/front-left/2023_76.png",
        "numeroPuertas": 4,
        "motor": "2.0L",
        "combustible": "Gasolina",
        "categoria": "Lujo",
        "precio_compra": 42000,
        "precio_venta": 45000,
        "existencia": 2000
    },
    {
        "codigo": 1016,
        "marca": "Mercedes-Benz",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Mercedes-Benz_Star_2022.svg/800px-Mercedes-Benz_Star_2022.svg.png",
        "tipo": "Sedán 🚗",
        "modelo": "Mercedes-Benz C-Class",
        "caracteristicas": "Lujo y rendimiento en cada detalle",
        "imagen": "https://images.dealer.com/ddc/vehicles/2023/Mercedes-Benz/C-Class/Coupe/perspective/front-left/2023_24.png",
        "numeroPuertas": 4,
        "motor": "2.0L",
        "combustible": "Gasolina",
        "categoria": "Lujo Premium",
        "precio_compra": 45000,
        "precio_venta": 48000,
        "existencia": 2000
    },
    {
        "codigo": 1017,
        "marca": "Tesla",
        "logo": "https://seeklogo.com/images/T/tesla-inc-logo-B7ACFAE927-seeklogo.com.png",
        "tipo": "Eléctrico 🚗",
        "modelo": "Tesla Model S",
        "caracteristicas": "Rendimiento eléctrico, autonomía de largo alcance",
        "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/52152/2024-Tesla-Model%20S-front_52152_032_1822x709_PPSB_cropped.png",
        "numeroPuertas": 4,
        "motor": "Eléctrico",
        "combustible": "Eléctrico",
        "categoria": "Lujo Premium Eléctrico",
        "precio_compra": 80000,
        "precio_venta": 85000,
        "existencia": 2000
    },
    {
        "codigo": 1018,
        "marca": "Nissan",
        "logo": "https://belloautomotriz.com/wp-content/uploads/2017/08/4-Nissan-logo.svg_.png",
        "tipo": "Sedán 🚗",
        "modelo": "Nissan Altima",
        "caracteristicas": "Tecnología avanzada, diseño aerodinámico",
        "imagen": "https://di-uploads-pod42.dealerinspire.com/southparknissan/uploads/2023/11/2024-nissan-altima-main.png",
        "numeroPuertas": 4,
        "motor": "2.5L",
        "combustible": "Gasolina",
        "categoria": "Intermedio",
        "precio_compra": 25000,
        "precio_venta": 27000,
        "existencia": 2000
    },
    {
        "codigo": 1019,
        "marca": "Toyota",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Toyota_logo_%28Red%29.svg/2560px-Toyota_logo_%28Red%29.svg.png",
        "tipo": "Híbrido 🚗",
        "modelo": "Toyota Prius",
        "caracteristicas": "Eficiencia híbrida, bajo consumo de combustible",
        "imagen": "https://www.toyota.com.sg/showroom/new-models/-/media/4ec94a5afd6d4faab5973c826ef1770b.png",
        "numeroPuertas": 4,
        "motor": "1.8L Híbrido",
        "combustible": "Híbrido",
        "categoria": "Económico Híbrido",
        "precio_compra": 28000,
        "precio_venta": 29500,
        "existencia": 2000
    },
    {
        "codigo": 1020,
        "marca": "Audi",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Audi_logo_detail.svg/1024px-Audi_logo_detail.svg.png",
        "tipo": "SUV Eléctrico 🚙",
        "modelo": "Audi e-tron",
        "caracteristicas": "SUV totalmente eléctrico, lujo y sostenibilidad",
        "imagen": "https://www.motortrend.com/uploads/izmo/audi/e_tron_sportback/2021/e_tron_sportback.png",
        "numeroPuertas": 4,
        "motor": "Eléctrico Dual",
        "combustible": "Eléctrico",
        "categoria": "Lujo Premium Eléctrico",
        "precio_compra": 72000,
        "precio_venta": 75000,
        "existencia": 2000
    },
    {
        "codigo": 1021,
        "marca": "RAM",
        "logo": "https://1000marcas.net/wp-content/uploads/2023/04/Ram-Logo-1993.png",
        "tipo": "Pickup Lujo 🚛",
        "modelo": "RAM 1500 Limited",
        "caracteristicas": "Interior premium, capacidad todoterreno",
        "imagen": "https://di-uploads-pod11.dealerinspire.com/cdjconfidential/uploads/2019/10/limited-header.png",
        "numeroPuertas": 4,
        "motor": "5.7L HEMI",
        "combustible": "Gasolina",
        "categoria": "Pickup Premium",
        "precio_compra": 58000,
        "precio_venta": 62000,
        "existencia": 2000
    },
    {
        "codigo": 1022,
        "marca": "Porsche",
        "logo": "https://1000marcas.net/wp-content/uploads/2019/12/Porsche-Logo-1994.png",
        "tipo": "Superdeportivo 🏎️",
        "modelo": "Porsche 911",
        "caracteristicas": "Rendimiento legendario, diseño icónico",
        "imagen": "https://euroshop.com.pe/wp-content/uploads/2024/09/porsche-911.png",
        "numeroPuertas": 2,
        "motor": "3.0L Twin-Turbo",
        "combustible": "Gasolina",
        "categoria": "Superdeportivo Premium",
        "precio_compra": 110000,
        "precio_venta": 115000,
        "existencia": 2000
    },
    {
        "codigo": 1023,
        "marca": "Volvo",
        "logo": "https://images.seeklogo.com/logo-png/15/2/volvo-logo-png_seeklogo-150599.png?v=1958568231624957072",
        "tipo": "SUV Compacto 🚙",
        "modelo": "Volvo XC40",
        "caracteristicas": "Seguridad avanzada, diseño escandinavo",
        "imagen": "https://images.dealer.com/ddc/vehicles/2021/Volvo/XC40/SUV/perspective/front-left/2021_76.png",
        "numeroPuertas": 4,
        "motor": "2.0L Turbo",
        "combustible": "Gasolina",
        "categoria": "Lujo Compacto",
        "precio_compra": 35000,
        "precio_venta": 38500,
        "existencia": 2000
    },
    {
        "codigo": 1024,
        "marca": "Honda",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Logo_Honda_F1.png",
        "tipo": "Minivan 🚐",
        "modelo": "Honda Odyssey",
        "caracteristicas": "Espacio familiar, confort superior",
        "imagen": "https://www.swickardhonda.com/assets/stock/ColorMatched_01/Transparent/640/cc_2021HOV01_01_640/cc_2021HOV010072_01_640_BS.png",
        "numeroPuertas": 4,
        "motor": "3.5L V6",
        "combustible": "Gasolina",
        "categoria": "Familiar Premium",
        "precio_compra": 38000,
        "precio_venta": 42000,
        "existencia": 2000
    },
    {
        "codigo": 1025,
        "marca": "Lexus",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/Lexus-logotipo.png",
        "tipo": "Crossover 🚙",
        "modelo": "Lexus NX",
        "caracteristicas": "Lujo compacto, tecnología híbrida",
        "imagen": "https://dealerimages.dealereprocess.com/image/upload/v1711401385/1/lexus/2025_NX/LEX-NXG-MY25-0001.07-E01-Base250FWD-Ext1-GrecianWater-W18inStdG4AD.png",
        "numeroPuertas": 4,
        "motor": "2.5L Híbrido",
        "combustible": "Híbrido",
        "categoria": "Lujo Híbrido",
        "precio_compra": 42000,
        "precio_venta": 45500,
        "existencia": 2000
    },
    {
        "codigo": 1026,
        "marca": "Lamborghini",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/Lamborghini-Logo-1998.png",
        "tipo": "Superdeportivo 🏎️",
        "modelo": "Lamborghini Huracán",
        "caracteristicas": "Motor V10, diseño futurista, máximo rendimiento",
        "imagen": "https://images.dealer.com/ddc/vehicles/2024/Lamborghini/Huracan%20Tecnica/Coupe/trim_Base_3da5c4/perspective/side-left/2024_24.png",
        "numeroPuertas": 2,
        "motor": "5.2L V10",
        "combustible": "Gasolina",
        "categoria": "Superdeportivo Ultra Premium",
        "precio_compra": 245000,
        "precio_venta": 265000,
        "existencia": 2000
    },
    {
        "codigo": 1027,
        "marca": "Rolls-Royce",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/Rolls-Royce-Logo-1.png",
        "tipo": "Luxury Sedan 🚗",
        "modelo": "Rolls-Royce Ghost",
        "caracteristicas": "Lujo supremo, acabados artesanales, máximo confort",
        "imagen": "https://www.motortrend.com/uploads/2021/12/2022-Rolls-Royce-Ghost.png",
        "numeroPuertas": 4,
        "motor": "6.75L V12",
        "combustible": "Gasolina",
        "categoria": "Ultra Lujo Premium",
        "precio_compra": 295000,
        "precio_venta": 315000,
        "existencia": 2000
    },
    {
        "codigo": 1028,
         "marca": "Chevrolet",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/Chevrolet-logo.png",
        "tipo": "Compacto 🚗",
        "modelo": "Chevrolet Spark",
        "caracteristicas": "Ultra compacto, excelente consumo de combustible",
        "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/12451/2018-Chevrolet-Spark-front_12451_032_1887x956_GW7_cropped.png",
        "numeroPuertas": 4,
        "motor": "1.4L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 14000,
        "precio_venta": 15500,
        "existencia": 2000
    },
    {
        "codigo": 1029,
        "marca": "Kia",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/KIA-Logo-1.png",
        "tipo": "Hatchback 🚗",
        "modelo": "Kia Rio",
        "caracteristicas": "Eficiente, práctico y bajo mantenimiento",
        "imagen": "https://kia.com.do/wp-content/uploads/2023/02/rio-color-5.webp",
        "numeroPuertas": 4,
        "motor": "1.6L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 16000,
        "precio_venta": 17200,
        "existencia": 2000
    },
    {
        "codigo": 1030,
        "marca": "Hyundai",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/logo-Hyundai.png",
        "tipo": "Sedán 🚗",
        "modelo": "Hyundai Accent",
        "caracteristicas": "Económico, espacioso, ideal para ciudad",
        "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/13297/2021-Hyundai-Accent-front_13297_032_1844x803_R4R_cropped.png",
        "numeroPuertas": 4,
        "motor": "1.6L",
        "combustible": "Gasolina",
        "categoria": "Económico",
        "precio_compra": 15000,
        "precio_venta": 16800,
        "existencia": 2000
    },
    {
        "codigo": 1031,
        "marca": "Bugatti",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Bugatti_logo.svg/2560px-Bugatti_logo.svg.png",
        "tipo": "Hypercar 🏎️",
        "modelo": "Bugatti Chiron",
        "caracteristicas": "Velocidad máxima 420 km/h, motor W16 quad-turbo, edición limitada",
        "imagen": "https://i.pinimg.com/originals/e9/34/ac/e934ac022c9ecf2dadf6954610176627.png",
        "numeroPuertas": 2,
        "motor": "8.0L W16 Quad-Turbo",
        "combustible": "Gasolina Premium",
        "categoria": "Hypercar Ultra Premium",
        "precio_compra": 2800000,
        "precio_venta": 3500000,
        "existencia": 2000
    },
    {
        "codigo": 1032,
        "marca": "Rimac",
        "logo": "https://1000marcas.net/wp-content/uploads/2021/02/Rimac-Logo.png",
        "tipo": "Superdeportivo Eléctrico 🏎️",
        "modelo": "Rimac Nevera",
        "caracteristicas": "100% eléctrico, 1914 hp, 0-100 km/h en 1.85s",
        "imagen": "https://www.evspecifications.info/wp-content/uploads/2022/10/Rimac-Nevera.png",
        "numeroPuertas": 2,
        "motor": "Eléctrico Cuádruple",
        "combustible": "Eléctrico",
        "categoria": "Hypercar Eléctrico",
        "precio_compra": 2000000,
        "precio_venta": 2400000,
        "existencia": 2000
    },
    {
        "codigo": 1033,
        "marca": "Aston Martin",
        "logo": "https://i.pinimg.com/originals/47/e4/90/47e4904c2b17a540b60a473e4a9ba3a8.png",
        "tipo": "Grand Tourer 🏎️",
        "modelo": "Aston Martin DBS",
        "caracteristicas": "Interior artesanal, V12 biturbo, máximo lujo deportivo",
        "imagen": "https://www.motortrend.com/uploads/sites/5/2020/06/2020-astonmartin-dbs.png",
        "numeroPuertas": 2,
        "motor": "5.2L V12 Twin-Turbo",
        "combustible": "Gasolina Premium",
        "categoria": "GT Ultra Premium",
        "precio_compra": 300000,
        "precio_venta": 375000,
        "existencia": 2000
    },
    {
        "codigo": 1034,
        "marca": "Bentley",
        "logo": "https://1000marcas.net/wp-content/uploads/2020/01/Bentley-logo.png",
        "tipo": "SUV Ultra Lujo 🚙",
        "modelo": "Bentley Bentayga",
        "caracteristicas": "SUV más lujoso del mundo, acabados personalizados",
        "imagen": "https://images.ctfassets.net/p77iaapls74f/5LOq3BscRS5f74C0eycbGq/f58fdab7d5c90b93efc789522f5a6d83/EWB.png",
        "numeroPuertas": 4,
        "motor": "6.0L W12 Twin-Turbo",
        "combustible": "Gasolina Premium",
        "categoria": "SUV Ultra Premium",
        "precio_compra": 350000,
        "precio_venta": 450000,
        "existencia": 2000
    },
    {
        "codigo": 1035,
        "marca": "Ferrari",
        "logo": "https://1000marcas.net/wp-content/uploads/2019/12/Ferrari-Emblema-1984.png",
        "tipo": "Superdeportivo 🏎️",
        "modelo": "Ferrari SF90 Stradale",
        "caracteristicas": "Híbrido enchufable, 1000 hp, tecnología F1",
        "imagen": "https://cdn.wheel-size.com/automobile/body/ferrari-sf90-stradale-2019-2021-1606211392.6015837.webp",
        "numeroPuertas": 2,
        "motor": "4.0L V8 Híbrido",
        "combustible": "Híbrido Premium",
        "categoria": "Superdeportivo Híbrido Premium",
        "precio_compra": 500000,
        "precio_venta": 625000,
        "existencia": 2000
    },
    {
        "codigo": 1036,
        "marca": "Porsche",
        "logo": "https://logos-world.net/wp-content/uploads/2021/04/Porsche-Symbol.png",
        "tipo": "Superdeportivo 🏎️",
        "modelo": "Porsche 911 Turbo S",
        "caracteristicas": "Motor 6 cilindros, 650 hp, tracción total",
        "imagen": "https://gld-creative.s3.us-west-2.amazonaws.com/2024-porsche-911-carrera-gts-558470726aa4-600x300.png",
        "numeroPuertas": 2,
        "motor": "3.8L 6 cilindros Twin-Turbo",
        "combustible": "Gasolina Premium",
        "categoria": "Superdeportivo Gasolina",
        "precio_compra": 200000,
        "precio_venta": 250000,
        "existencia": 1500
    },
    {
        "codigo": 1037,
        "marca": "Porsche",
        "logo": "https://logos-world.net/wp-content/uploads/2021/04/Porsche-Symbol.png",
        "tipo": "SUV Deportivo 🚙",
        "modelo": "Porsche Cayenne Turbo",
        "caracteristicas": "Motor V8, 550 hp, tecnología avanzada",
        "imagen": "https://motork.com/media/2021/03/motork_porsche_cayenne_turbo_main-1.png",
        "numeroPuertas": 5,
        "motor": "4.0L V8 Turbo",
        "combustible": "Gasolina Premium",
        "categoria": "SUV Deportivo Gasolina",
        "precio_compra": 120000,
        "precio_venta": 150000,
        "existencia": 1000
    },
    {
        "codigo": 1038,
        "marca": "Porsche",
        "logo": "https://logos-world.net/wp-content/uploads/2021/04/Porsche-Symbol.png",       
        "tipo": "Coupé Deportivo 🚗",
        "modelo": "Porsche 718 Cayman GTS",
        "caracteristicas": "Motor 4 cilindros, 365 hp, tracción trasera",
        "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/54662/2025-Porsche-718%20Cayman-front_54662_032_1816x736_D7_cropped.png",
        "numeroPuertas": 2,
        "motor": "2.5L 4 cilindros Turbo",
        "combustible": "Gasolina Premium",
        "categoria": "Coupé Deportivo Gasolina",
        "precio_compra": 70000,
        "precio_venta": 85000,
        "existencia": 800
    },
    {
        "codigo": 1039,
        "marca": "Mercedes-Benz",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Mercedes-Benz_Star_2022.svg/800px-Mercedes-Benz_Star_2022.svg.png",        
        "tipo": "SUV de lujo 🚙",
        "modelo": "Mercedes-Benz G-Class",
        "caracteristicas": "Motor V8, 577 hp, tracción total, lujo y rendimiento",
        "imagen": "https://www.motortrend.com/uploads/sites/10/2019/04/2019-mercedes-benz-g-class-550-suv-angular-front.png",
        "numeroPuertas": 5,
        "motor": "4.0L V8 Biturbo",
        "combustible": "Gasolina Premium",
        "categoria": "SUV de lujo Gasolina",
        "precio_compra": 130000,
        "precio_venta": 160000,
        "existencia": 1000
    },
    {
        "codigo": 1040,
        "marca": "Mercedes-Benz",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Mercedes-Benz_Star_2022.svg/800px-Mercedes-Benz_Star_2022.svg.png",
        "tipo": "Sedán de lujo 🚗",
        "modelo": "Mercedes-Benz S-Class",
        "caracteristicas": "Motor V8, 496 hp, tecnología avanzada, interior de lujo",
        "imagen": "https://www.motortrend.com/uploads/sites/10/2019/12/2020-mercedes-benz-s-class-s450-sedan-angular-front.png",
        "numeroPuertas": 4,
        "motor": "4.0L V8 Biturbo",
        "combustible": "Gasolina Premium",
        "categoria": "Sedán de lujo Gasolina",
        "precio_compra": 120000,
        "precio_venta": 150000,
        "existencia": 800
    },
    {
        "codigo": 1041,
        "marca": "Mercedes-Benz",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Mercedes-Benz_Star_2022.svg/800px-Mercedes-Benz_Star_2022.svg.png",       
        "tipo": "Coupé deportivo 🚗",
        "modelo": "Mercedes-Benz AMG GT",
        "caracteristicas": "Motor V8, 523 hp, tracción trasera, diseño agresivo y deportivo",
        "imagen": "https://65e81151f52e248c552b-fe74cd567ea2f1228f846834bd67571e.ssl.cf1.rackcdn.com/ldm-images/2021-Mercedes-Benz-AMG-GT-color-Designo-Selenite-Grey-Magno.png",
        "numeroPuertas": 2,
        "motor": "4.0L V8 Biturbo",
        "combustible": "Gasolina Premium",
        "categoria": "Coupé deportivo Gasolina",
        "precio_compra": 150000,
        "precio_venta": 185000,
        "existencia": 500
      },
      {
        "codigo": 1042,
        "marca": "Mercedes-Benz",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Mercedes-Benz_Star_2022.svg/800px-Mercedes-Benz_Star_2022.svg.png",
        "tipo": "Sedán de lujo 🚗",
        "modelo": "Mercedes-Benz E-Class",
        "caracteristicas": "Motor V6, 362 hp, interior de lujo, suspensión avanzada",
        "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/54500/2024-Mercedes-Benz-E-Class-front_54500_032_1844x736_149_cropped.png",
        "numeroPuertas": 4,
        "motor": "3.0L V6 Turbo",
        "combustible": "Gasolina Premium",
        "categoria": "Sedán de lujo Gasolina",
        "precio_compra": 65000,
        "precio_venta": 80000,
        "existencia": 1000
      },
      {
        "codigo": 1043,
        "marca": "Nissan",
        "logo": "https://belloautomotriz.com/wp-content/uploads/2017/08/4-Nissan-logo.svg_.png",       
        "tipo": "SUV",
        "modelo": "Nissan X-Trail",
        "caracteristicas": "SUV, tracción integral, 2.5L 4 cilindros",
        "imagen": "https://static.foxdealer.com/635/2023/10/XTRAIL.png",
        "numeroPuertas": 5,
        "motor": "2.5L 4 Cilindros",
        "combustible": "Gasolina",
        "categoria": "SUV",
        "precio_compra": 25000,
        "precio_venta": 30000,
        "existencia": 1500
      }, 
      {
        "codigo": 1044,
        "marca": "Nissan",
        "logo": "https://belloautomotriz.com/wp-content/uploads/2017/08/4-Nissan-logo.svg_.png",      
        "tipo": "Camioneta",
        "modelo": "Nissan Frontier",
        "caracteristicas": "Camioneta, 4x4, motor V6, capacidad de carga 1000kg",
        "imagen": "https://floresrentacar.com/wp-content/uploads/2022/04/fronier-2020-negro.png",
        "numeroPuertas": 4,
        "motor": "3.8L V6",
        "combustible": "Gasolina",
        "categoria": "Camioneta",
        "precio_compra": 35000,
        "precio_venta": 42000,
        "existencia": 1300
      },
      {
        "codigo": 1045,
        "marca": "Nissan",
        "logo": "https://belloautomotriz.com/wp-content/uploads/2017/08/4-Nissan-logo.svg_.png",      
        "tipo": "Crossover",
        "modelo": "Nissan Juke",
        "caracteristicas": "Crossover compacto, 1.6L, diseño deportivo",
        "imagen": "https://cdn.bipicar.com/specificvehicleplans/652f881bd9d1a20b5437fa1f/vehicle-images/6691080726f37aaa48607f21_2024_07_12_11_40_07.png",
        "numeroPuertas": 5,
        "motor": "1.6L 4 Cilindros",
        "combustible": "Gasolina",
        "categoria": "Crossover",
        "precio_compra": 18000,
        "precio_venta": 22000,
        "existencia": 1600
      },
      {
        "codigo": 1046,
        "marca": "Ford",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ford_logo_flat.svg/1200px-Ford_logo_flat.svg.png",
        "tipo": "SUV",
        "modelo": "Ford Edge",
        "caracteristicas": "SUV, tecnología avanzada, asientos de cuero, tracción delantera",
        "imagen": "https://platform.cstatic-images.com/in/v2/stock_photos/7d621c6a-e3a8-40ac-80b7-241155f8fbfd/647aa9fe-c454-4eda-a55c-b6b88f820819.png",
        "numeroPuertas": 5,
        "motor": "2.0L 4 Cilindros Turbo",
        "combustible": "Gasolina",
        "categoria": "SUV",
        "precio_compra": 38000,
        "precio_venta": 45000,
        "existencia": 600
      },
      {
        "codigo": 1047,
        "marca": "Ford",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ford_logo_flat.svg/1200px-Ford_logo_flat.svg.png",       
        "tipo": "Sedán",
        "modelo": "Ford Taurus",
        "caracteristicas": "Sedán, espacioso, eficiente en combustible, tecnología avanzada",
        "imagen": "https://platform.cstatic-images.com/in/v2/stock_photos/59b340bb-ac9f-46a1-8a66-7134f8e33cf0/7ebd7420-0d06-4dcb-9f88-27419d7fd8e3.png",
        "numeroPuertas": 4,
        "motor": "3.5L V6",
        "combustible": "Gasolina",
        "categoria": "Sedán",
        "precio_compra": 35000,
        "precio_venta": 42000,
        "existencia": 800
      },
      {
        "codigo": 1048,
        "marca": "Toyota",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Toyota_logo_%28Red%29.svg/2560px-Toyota_logo_%28Red%29.svg.png",       
        "tipo": "Clásico",
        "modelo": "Toyota Corolla 1969",
        "caracteristicas": "Clásico, diseño atemporal, motor eficiente",
        "imagen": "https://www.toyota-global.com/company/history_of_toyota/75years/vehicle_lineage/car/id60003154/images/m1.png",
        "numeroPuertas": 4,
        "motor": "1.6L 4 Cilindros",
        "combustible": "Gasolina",
        "categoria": "Clásico",
        "precio_compra": 8000,
        "precio_venta": 12000,
        "existencia": 500
      },
      {
        "codigo": 1049,
        "marca": "Toyota",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Toyota_logo_%28Red%29.svg/2560px-Toyota_logo_%28Red%29.svg.png",       
        "tipo": "Clásico",
        "modelo": "Toyota Land Cruiser 1984",
        "caracteristicas": "SUV clásico, robusto, ideal para off-road",
        "imagen": "https://www.toyota-global.com/company/history_of_toyota/75years/vehicle_lineage/car/id60012612/images/m1.png",
        "numeroPuertas": 5,
        "motor": "4.2L 6 Cilindros",
        "combustible": "Gasolina",
        "categoria": "Clásico",
        "precio_compra": 10000,
        "precio_venta": 15000,
        "existencia": 400
      },
      {
        "codigo": 1050,
        "marca": "Toyota",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Toyota_logo_%28Red%29.svg/2560px-Toyota_logo_%28Red%29.svg.png",       
        "tipo": "Deportivo 🏎️",
        "modelo": "Toyota Supra 2020",
        "caracteristicas": "Deportivo, 335 hp, diseño agresivo",
        "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/14086/2020-Toyota-GR%20Supra-front_14086_032_1836x741_D06_cropped.png",
        "numeroPuertas": 2,
        "motor": "3.0L I6 Turbo",
        "combustible": "Gasolina",
        "categoria": "Deportivo",
        "precio_compra": 45000,
        "precio_venta": 60000,
        "existencia": 300
      },
      {
        "codigo": 1051,
        "marca": "Toyota",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Toyota_logo_%28Red%29.svg/2560px-Toyota_logo_%28Red%29.svg.png",        
        "tipo": "Deportivo 🏎️",
        "modelo": "Toyota 86",
        "caracteristicas": "Deportivo, tracción trasera, manejo ágil",
        "imagen": "https://images.dealer.com/ddc/vehicles/2019/Toyota/86/Coupe/perspective/front-left/0019_24.png",
        "numeroPuertas": 2,
        "motor": "2.0L 4 Cilindros",
        "combustible": "Gasolina",
        "categoria": "Deportivo",
        "precio_compra": 25000,
        "precio_venta": 30000,
        "existencia": 200
      },

  {
    "codigo": 1052,
    "marca": "Acura",
    "logo": "https://1000marcas.net/wp-content/uploads/2020/03/Acura-Color.jpg",
    "tipo": "Sedán 🚗",
    "modelo": "Acura TLX",
    "caracteristicas": "Sedán de lujo, diseño elegante, tecnología avanzada",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/12106/2020-Acura-TLX-front_12106_032_1836x760_RE_cropped.png",
    "numeroPuertas": 4,
    "motor": "2.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "Sedán",
    "precio_compra": 38000,
    "precio_venta": 42000,
    "existencia": 200
  },
  {
    "codigo": 1053,
    "marca": "Acura",
    "logo": "https://1000marcas.net/wp-content/uploads/2020/03/Acura-Color.jpg",
    "tipo": "Deportivo 🏎️",
    "modelo": "Acura NSX",
    "caracteristicas": "Deportivo híbrido, alta velocidad, diseño exclusivo",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/11810/2019-Acura-NSX-front_11810_032_1827x688_RH_cropped.png",
    "numeroPuertas": 2,
    "motor": "3.5L V6 Híbrido",
    "combustible": "Híbrido",
    "categoria": "Deportivo",
    "precio_compra": 157000,
    "precio_venta": 170000,
    "existencia": 20
  },
  {
    "codigo": 1054,
    "marca": "Acura",
    "logo": "https://1000marcas.net/wp-content/uploads/2020/03/Acura-Color.jpg",
    "tipo": "Crossover 🚙",
    "modelo": "Acura RDX",
    "caracteristicas": "Crossover compacto, interior lujoso, conducción ágil",
    "imagen": "https://images.dealer.com/ddc/vehicles/2019/Acura/RDX/SUV/perspective/front-left/2019_56.png",
    "numeroPuertas": 4,
    "motor": "2.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "Crossover",
    "precio_compra": 42000,
    "precio_venta": 47000,
    "existencia": 180
  },
  {
    "codigo": 1055,
    "marca": "Audi",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Audi_logo_detail.svg/1024px-Audi_logo_detail.svg.png",
    "tipo": "Sedán 🚗",
    "modelo": "Audi A4",
    "caracteristicas": "Sedán de lujo, interior premium, diseño moderno",
    "imagen": "https://images.dealer.com/ddc/vehicles/2024/Audi/A4/Sedan/perspective/front-left/2024_24.png",
    "numeroPuertas": 4,
    "motor": "2.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "Sedán",
    "precio_compra": 39000,
    "precio_venta": 45000,
    "existencia": 180
  },
  {
    "codigo": 1056,
    "marca": "Audi",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Audi_logo_detail.svg/1024px-Audi_logo_detail.svg.png",
    "tipo": "SUV 🚙",
    "modelo": "Audi Q5",
    "caracteristicas": "SUV compacto, tracción integral, tecnología avanzada",
    "imagen": "https://cdn.prod.website-files.com/66aa9b074bb515bf9ab24bc3/67193237c6e71893e63f3047_WEBFLOW%20PNG%20(4).png",
    "numeroPuertas": 4,
    "motor": "2.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 43000,
    "precio_venta": 48000,
    "existencia": 140
  },
  {
    "codigo": 1057,
    "marca": "Audi",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Audi_logo_detail.svg/1024px-Audi_logo_detail.svg.png",
    "tipo": "Deportivo 🏎️",
    "modelo": "Audi R8",
    "caracteristicas": "Deportivo, motor V10, velocidad máxima impresionante",
    "imagen": "https://platform.cstatic-images.com/in/v2/stock_photos/be047596-1e3a-46c5-b1b0-f0354d3a1d9c/ea399b6e-73de-4484-8cee-824f8415dcdf.png",
    "numeroPuertas": 2,
    "motor": "5.2L V10",
    "combustible": "Gasolina",
    "categoria": "Deportivo",
    "precio_compra": 150000,
    "precio_venta": 170000,
    "existencia": 30
  },
  {
    "codigo": 1058,
    "marca": "Audi",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Audi_logo_detail.svg/1024px-Audi_logo_detail.svg.png",
    "tipo": "Crossover 🚙",
    "modelo": "Audi Q3",
    "caracteristicas": "Crossover compacto, estilo deportivo, funcionalidad premium",
    "imagen": "https://media.drive.com.au/obj/tx_q:70,rs:auto:1920:1080:1/driveau/upload/cms/uploads/irf6qowfxq7o6lbqb6ti",
    "numeroPuertas": 4,
    "motor": "2.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "Crossover",
    "precio_compra": 37000,
    "precio_venta": 42000,
    "existencia": 160
  },
  {
    "codigo": 1059,
    "marca": "Buick",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/6/62/Buick_2022_logo.png",
    "tipo": "SUV 🚙",
    "modelo": "Buick Enclave",
    "caracteristicas": "SUV de lujo, interior espacioso, tecnología premium",
    "imagen": "https://static.tcimg.net/vehicles/primary/e1f32698c52b045e/2015-Buick-Enclave-gold-full_color-driver_side_front_quarter.png",
    "numeroPuertas": 4,
    "motor": "3.6L V6",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 45000,
    "precio_venta": 50000,
    "existencia": 120
  },
  {
    "codigo": 1060,
    "marca": "Buick",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/6/62/Buick_2022_logo.png",
    "tipo": "Crossover 🚙",
    "modelo": "Buick Encore GX",
    "caracteristicas": "Crossover compacto, eficiente y moderno",
    "imagen": "https://static.tcimg.net/vehicles/primary/090e3492c1bf03f5/2022-Buick-Encore_GX-blue-full_color-driver_side_front_quarter.png",
    "numeroPuertas": 4,
    "motor": "1.3L Turbo",
    "combustible": "Gasolina",
    "categoria": "Crossover",
    "precio_compra": 27000,
    "precio_venta": 32000,
    "existencia": 150
  },
  {
    "codigo": 1061,
    "marca": "Buick",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/6/62/Buick_2022_logo.png",
    "tipo": "Sedán 🚗",
    "modelo": "Buick LaCrosse",
    "caracteristicas": "Sedán de lujo, diseño sofisticado y cómodo",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/12311/2019-Buick-LaCrosse-front_12311_032_1797x730_GPJ_cropped.png",
    "numeroPuertas": 4,
    "motor": "2.5L Híbrido",
    "combustible": "Híbrido",
    "categoria": "Sedán",
    "precio_compra": 37000,
    "precio_venta": 42000,
    "existencia": 100
  },
  {
    "codigo": 1062,
    "marca": "Buick",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/6/62/Buick_2022_logo.png",
    "tipo": "SUV 🚙",
    "modelo": "Buick Envision",
    "caracteristicas": "SUV compacto, manejo ágil, tecnología de seguridad avanzada",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/14905/2021-Buick-Envision-front_14905_032_1838x859_GR8_cropped.png",
    "numeroPuertas": 4,
    "motor": "2.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 36000,
    "precio_venta": 40000,
    "existencia": 140
  },
  {
    "codigo": 1063,
    "marca": "Dodge",
    "logo": "https://seeklogo.com/images/D/Dodge-logo-06B7E884FC-seeklogo.com.png",
    "tipo": "Deportivo 🏎️",
    "modelo": "Dodge Challenger",
    "caracteristicas": "Deportivo clásico, motor potente, diseño agresivo",
    "imagen": "https://images.dealer.com/ddc/vehicles/2023/Dodge/Challenger/Coupe/perspective/front-left/2023_76.png",
    "numeroPuertas": 2,
    "motor": "6.2L V8",
    "combustible": "Gasolina",
    "categoria": "Deportivo",
    "precio_compra": 55000,
    "precio_venta": 60000,
    "existencia": 80
  },
  {
    "codigo": 1064,
    "marca": "Dodge",
    "logo": "https://seeklogo.com/images/D/Dodge-logo-06B7E884FC-seeklogo.com.png",
    "tipo": "Pickup 🛻",
    "modelo": "Dodge RAM 1500",
    "caracteristicas": "Pickup resistente, alta capacidad de carga, interior cómodo",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/54487/2024-Ram-1500%20Classic%20Crew%20Cab-front_54487_032_1824x831_PR4_cropped.png",
    "numeroPuertas": 4,
    "motor": "5.7L V8",
    "combustible": "Gasolina",
    "categoria": "Pickup",
    "precio_compra": 47000,
    "precio_venta": 53000,
    "existencia": 100
  },
  {
    "codigo": 1065,
    "marca": "Dodge",
    "logo": "https://seeklogo.com/images/D/Dodge-logo-06B7E884FC-seeklogo.com.png",
    "tipo": "SUV 🚙",
    "modelo": "Dodge Durango",
    "caracteristicas": "SUV grande, capacidad para 7 pasajeros, motor potente",
    "imagen": "https://images.dealer.com/ddc/vehicles/2024/Dodge/Durango/SUV/perspective/front-left/2024_76.png",
    "numeroPuertas": 4,
    "motor": "3.6L V6",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 41000,
    "precio_venta": 46000,
    "existencia": 90
  },
  {
    "codigo": 1066,
    "marca": "Dodge",
    "logo": "https://seeklogo.com/images/D/Dodge-logo-06B7E884FC-seeklogo.com.png",
    "tipo": "Deportivo 🏎️",
    "modelo": "Dodge Charger",
    "caracteristicas": "Deportivo sedán, motor potente, estilo musculoso",
    "imagen": "https://images.dealer.com/ddc/vehicles/2019/Dodge/Charger/Sedan/trim_SXT_124ea6/perspective/front-left/2019_76.png",
    "numeroPuertas": 4,
    "motor": "5.7L V8",
    "combustible": "Gasolina",
    "categoria": "Deportivo",
    "precio_compra": 45000,
    "precio_venta": 50000,
    "existencia": 85
  },
 {
    "codigo": 1066,
    "marca": "Fiat",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Fiat_Automobiles_logo.svg/2048px-Fiat_Automobiles_logo.svg.png",
    "tipo": "Hatchback 🚗",
    "modelo": "Fiat 500",
    "caracteristicas": "Compacto, urbano, diseño clásico",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/10146/2016-FIAT-500-front_10146_032_1903x985_PBJ_cropped.png",
    "numeroPuertas": 2,
    "motor": "1.4L I4",
    "combustible": "Gasolina",
    "categoria": "Compacto",
    "precio_compra": 17000,
    "precio_venta": 20000,
    "existencia": 300
  },
  {
    "codigo": 1067,
    "marca": "Fiat",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Fiat_Automobiles_logo.svg/2048px-Fiat_Automobiles_logo.svg.png",
    "tipo": "SUV 🚙",
    "modelo": "Fiat Pulse",
    "caracteristicas": "SUV compacto, eficiente, diseño moderno",
    "imagen": "https://www.autocity.ar/wp-content/uploads/2024/10/pulse-autocity.webp",
    "numeroPuertas": 4,
    "motor": "1.0L Turbo",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 20000,
    "precio_venta": 24000,
    "existencia": 250
  },
  {
    "codigo": 1068,
    "marca": "Fiat",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Fiat_Automobiles_logo.svg/2048px-Fiat_Automobiles_logo.svg.png",
    "tipo": "Sedán 🚗",
    "modelo": "Fiat Cronos",
    "caracteristicas": "Sedán económico, espacioso, ideal para familias",
    "imagen": "https://cronos.fiat.com.ar/assets/images/img-version-cronos-precision-13-at.png",
    "numeroPuertas": 4,
    "motor": "1.3L I4",
    "combustible": "Gasolina",
    "categoria": "Sedán",
    "precio_compra": 18000,
    "precio_venta": 21000,
    "existencia": 300
  },
  {
    "codigo": 1069,
    "marca": "Fiat",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Fiat_Automobiles_logo.svg/2048px-Fiat_Automobiles_logo.svg.png",
    "tipo": "Convertible 🌟",
    "modelo": "Fiat 124 Spider",
    "caracteristicas": "Deportivo, diseño clásico, techo retráctil",
    "imagen": "https://images.dealer.com/ddc/vehicles/2018/FIAT/124%20Spider/Convertible/perspective/front-left/1018_24.png",
    "numeroPuertas": 2,
    "motor": "1.4L Turbo",
    "combustible": "Gasolina",
    "categoria": "Convertible",
    "precio_compra": 27000,
    "precio_venta": 32000,
    "existencia": 100
  },
  {
    "codigo": 1070,
    "marca": "Jeep",
    "logo": "https://www.pngplay.com/wp-content/uploads/13/Jeep-Logo-Background-PNG-Image.png",
    "tipo": "SUV 🚙",
    "modelo": "Jeep Wrangler",
    "caracteristicas": "Todo terreno, diseño clásico, gran desempeño",
    "imagen": "https://images.dealer.com/ddc/vehicles/2025/Jeep/Wrangler%204xe/SUV/perspective/front-left/2025_76.png",
    "numeroPuertas": 4,
    "motor": "3.6L V6",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 40000,
    "precio_venta": 47000,
    "existencia": 150
  },
  {
    "codigo": 1071,
    "marca": "Jeep",
    "logo": "https://www.pngplay.com/wp-content/uploads/13/Jeep-Logo-Background-PNG-Image.png",
    "tipo": "SUV 🚙",
    "modelo": "Jeep Grand Cherokee",
    "caracteristicas": "SUV de lujo, tecnología avanzada, cómodo",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/8584/2013-Jeep-Grand%20Cherokee-front_8584_032_1848x890_PRP_cropped.png",
    "numeroPuertas": 4,
    "motor": "3.6L V6",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 50000,
    "precio_venta": 58000,
    "existencia": 120
  },
  {
    "codigo": 1072,
    "marca": "Jeep",
    "logo": "https://www.pngplay.com/wp-content/uploads/13/Jeep-Logo-Background-PNG-Image.png",
    "tipo": "SUV 🚙",
    "modelo": "Jeep Compass",
    "caracteristicas": "SUV compacto, diseño moderno, eficiente",
    "imagen": "https://cdn.dlron.us/static/dealer-15533/Jeep_Compass_2021_in_Redline_Pearl.png",
    "numeroPuertas": 4,
    "motor": "2.4L I4",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 30000,
    "precio_venta": 35000,
    "existencia": 200
  },
  {
    "codigo": 1073,
    "marca": "Jeep",
    "logo": "https://www.pngplay.com/wp-content/uploads/13/Jeep-Logo-Background-PNG-Image.png",
    "tipo": "SUV 🚙",
    "modelo": "Jeep Gladiator",
    "caracteristicas": "Camioneta todo terreno, diseño único",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/55495/2025-Jeep-Gladiator-front_55495_032_1851x840_PW7_cropped.png",
    "numeroPuertas": 4,
    "motor": "3.6L V6",
    "combustible": "Gasolina",
    "categoria": "Camioneta",
    "precio_compra": 45000,
    "precio_venta": 52000,
    "existencia": 100
  },
  {
    "codigo": 1074,
    "marca": "Acura",
    "logo": "https://seeklogo.com/images/A/Acura-logo-6A7CD0D53A-seeklogo.com.png",
    "tipo": "SUV 🚙",
    "modelo": "Acura MDX",
    "caracteristicas": "SUV de lujo, tracción integral, tecnología avanzada",
    "imagen": "https://images.dealer.com/ddc/vehicles/2025/Acura/MDX/SUV/perspective/front-left/2025_76.png",
    "numeroPuertas": 4,
    "motor": "3.5L V6",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 47000,
    "precio_venta": 52000,
    "existencia": 150
  },
    {
    "codigo": 1075,
    "marca": "Kia",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/KIA_logo2.svg/2560px-KIA_logo2.svg.png",
    "tipo": "Sedán 🚗",
    "modelo": "Kia K5",
    "caracteristicas": "Sedán deportivo, tecnología avanzada, diseño moderno",
    "imagen": "https://images.dealer.com/ddc/vehicles/2021/Kia/K5/Sedan/perspective/front-left/2021_24.png",
    "numeroPuertas": 4,
    "motor": "1.6L Turbo",
    "combustible": "Gasolina",
    "categoria": "Sedán",
    "precio_compra": 24000,
    "precio_venta": 28000,
    "existencia": 220
  },
  {
    "codigo": 1076,
    "marca": "Kia",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/KIA_logo2.svg/2560px-KIA_logo2.svg.png",
    "tipo": "SUV 🚙",
    "modelo": "Kia Sportage",
    "caracteristicas": "SUV compacto, diseño atractivo, versátil",
    "imagen": "https://file.kelleybluebookimages.com/kbb/base/evox/CP/53393/2025-Kia-Sportage-front_53393_032_1815x859_DWR_cropped.png",
    "numeroPuertas": 4,
    "motor": "2.5L I4",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 27000,
    "precio_venta": 31000,
    "existencia": 250
  },
  {
    "codigo": 1077,
    "marca": "Kia",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/KIA_logo2.svg/2560px-KIA_logo2.svg.png",
    "tipo": "Hatchback 🚗",
    "modelo": "Kia Rio",
    "caracteristicas": "Compacto, eficiente, diseño funcional",
    "imagen": "https://images.dealer.com/ddc/vehicles/2021/Kia/Rio/Hatchback/perspective/front-left/2021_24.png",
    "numeroPuertas": 4,
    "motor": "1.6L I4",
    "combustible": "Gasolina",
    "categoria": "Compacto",
    "precio_compra": 17000,
    "precio_venta": 20000,
    "existencia": 300
  },
  {
    "codigo": 1078,
    "marca": "Kia",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/KIA_logo2.svg/2560px-KIA_logo2.svg.png",
    "tipo": "SUV 🚙",
    "modelo": "Kia Telluride",
    "caracteristicas": "SUV de lujo, espacioso, ideal para familias",
    "imagen": "https://di-uploads-pod19.dealerinspire.com/rontonkinkia/uploads/2022/11/mlp-img-top-2023-telluride-temp.png",
    "numeroPuertas": 4,
    "motor": "3.8L V6",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 32000,
    "precio_venta": 38000,
    "existencia": 180
  },
  {
    "codigo": 1079,
    "marca": "Lexus",
    "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d1/Lexus_division_emblem.svg/1200px-Lexus_division_emblem.svg.png",
    "tipo": "Sedán 🚗",
    "modelo": "Lexus ES",
    "caracteristicas": "Sedán de lujo, tecnología avanzada, silencioso",
    "imagen": "https://dealerimages.dealereprocess.com/image/upload/v1687205358/1/lexus/2024_ES/LEX-ESG-MY23-0021.07.png",
    "numeroPuertas": 4,
    "motor": "2.5L I4 Hybrid",
    "combustible": "Híbrido",
    "categoria": "Sedán",
    "precio_compra": 42000,
    "precio_venta": 49000,
    "existencia": 150
  },
  {
    "codigo": 1080,
    "marca": "Lexus",
    "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d1/Lexus_division_emblem.svg/1200px-Lexus_division_emblem.svg.png",
    "tipo": "SUV 🚙",
    "modelo": "Lexus RX",
    "caracteristicas": "SUV de lujo, diseño elegante, interior premium",
    "imagen": "https://lacddam.lexusasia.com/Peru/Cars/navegacion-home/lexus-rx-350h-nav.png",
    "numeroPuertas": 4,
    "motor": "3.5L V6",
    "combustible": "Gasolina",
    "categoria": "SUV",
    "precio_compra": 48000,
    "precio_venta": 56000,
    "existencia": 120
  },
  {
    "codigo": 1081,
    "marca": "Lexus",
    "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d1/Lexus_division_emblem.svg/1200px-Lexus_division_emblem.svg.png",
    "tipo": "Deportivo 🏎️",
    "modelo": "Lexus LC",
    "caracteristicas": "Deportivo, diseño audaz, tecnología avanzada",
    "imagen": "https://images.dealer.com/ddc/vehicles/2023/Lexus/LC%20500/Convertible/perspective/front-left/2020_24.png",
    "numeroPuertas": 2,
    "motor": "5.0L V8",
    "combustible": "Gasolina",
    "categoria": "Deportivo",
    "precio_compra": 90000,
    "precio_venta": 110000,
    "existencia": 80
  },
  {
    "codigo": 1082,
    "marca": "Lexus",
    "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d1/Lexus_division_emblem.svg/1200px-Lexus_division_emblem.svg.png",
    "tipo": "Convertible 🌟",
    "modelo": "Lexus IS C",
    "caracteristicas": "Convertible, elegante, diseño premium",
    "imagen": "https://65e81151f52e248c552b-fe74cd567ea2f1228f846834bd67571e.ssl.cf1.rackcdn.com/Lexus/Comparisons/2021-Lexus-IS-350-F-Sport-comp.png",
    "numeroPuertas": 2,
    "motor": "2.5L V6",
    "combustible": "Gasolina",
    "categoria": "Convertible",
    "precio_compra": 50000,
    "precio_venta": 58000,
    "existencia": 90
  },

  
  {
    "codigo": 1083,
    "marca": "Bugatti",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Bugatti_logo.svg/2560px-Bugatti_logo.svg.png",
    "tipo": "Híperdeportivo 🏎️",
    "modelo": "Bugatti Divo",
    "caracteristicas": "Diseño aerodinámico, motor W16, producción limitada",
    "imagen": "https://www.driva.com.au/static/25481a08d4cf0165bedaf7424ddf99e3/9e8a7/66cebc73-a717-4603-96b8-32ad88d05e1a_5a3aa8b9764983.18250154151379372148459565.png",
    "numeroPuertas": 2,
    "motor": "8.0L W16 Quad-Turbo",
    "combustible": "Gasolina",
    "categoria": "Híperdeportivo",
    "precio_compra": 5000000,
    "precio_venta": 5800000,
    "existencia": 2
  },
  {
    "codigo": 1084,
    "marca": "Bugatti",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Bugatti_logo.svg/2560px-Bugatti_logo.svg.png",
    "tipo": "Híperdeportivo 🏎️",
    "modelo": "Bugatti Centodieci",
    "caracteristicas": "Homenaje al EB110, motor W16, edición limitada a 10 unidades",
    "imagen": "https://cdn.carprices.ae/assets/api_uploads_img_trim_1686164624483_16fe430f9e.png",
    "numeroPuertas": 2,
    "motor": "8.0L W16 Quad-Turbo",
    "combustible": "Gasolina",
    "categoria": "Híperdeportivo",
    "precio_compra": 8000000,
    "precio_venta": 9000000,
    "existencia": 1
  },
  {
    "codigo": 1085,
    "marca": "Bugatti",
    "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Bugatti_logo.svg/2560px-Bugatti_logo.svg.png",
    "tipo": "Híperdeportivo 🏎️",
    "modelo": "Bugatti La Voiture Noire",
    "caracteristicas": "Diseño único, motor W16, el coche más caro del mundo",
    "imagen": "https://imagenes.20minutos.es/files/image_1920_1080/uploads/imagenes/2019/05/01/941493.jpg",
    "numeroPuertas": 2,
    "motor": "8.0L W16 Quad-Turbo",
    "combustible": "Gasolina",
    "categoria": "Híperdeportivo",
    "precio_compra": 11000000,
    "precio_venta": 12000000,
    "existencia": 1
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
# Función para generar factura con tipo de pago
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

        if 'logo' not in producto or 'imagen' not in producto:
            print(f"Advertencia: Producto faltante de clave 'logo' o 'imagen': {producto}")
        
        productos.append({
            "producto": producto['modelo'],
            "cantidad": cantidad,
            "total_producto": total_producto,
            "costo": costo,
            "margen": margen,
            "porcentaje_margen": porcentaje_margen,
            "imagen": producto.get('imagen', 'N/A'),
            "logo": producto.get('logo', 'N/A')  # Agregar el logo del producto
        })

    # Definir el tipo de pago con probabilidades específicas
    tipo_pago_choices = [
        ("Efectivo", 0.40),  # 40% Efectivo
        ("Tarjeta de Crédito", 0.28),  # 28% Tarjeta de Crédito
        ("Crédito", 0.20),  # 20% Crédito
        ("Transferencias", 0.12)  # 12% Transferencias
    ]
    
    random_number = random.random()
    tipo_pago = ""
    cumulative_probability = 0

    for tipo, probabilidad in tipo_pago_choices:
        cumulative_probability += probabilidad
        if random_number < cumulative_probability:
            tipo_pago = tipo
            break

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
        "tipo_pago": tipo_pago  # Agregar el campo tipo_pago
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
