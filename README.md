# cf-automation-airline-api

## Descripción
Este proyecto es una API de demostración construida con **FastAPI** que simula la gestión de una aerolínea. Permite registrar usuarios, administrar vuelos, manejar aeronaves, realizar reservas y pagos. La información se almacena en memoria, por lo que es ideal para fines educativos o pruebas locales.

Se incluye un usuario administrador predefinido:

- **Correo**: `admin@demo.com`
- **Contraseña**: `admin123`

## Instalación
1. Asegúrate de tener **Python 3.11** o superior instalado.
2. Clona este repositorio y entra en la carpeta del proyecto.
3. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de la API
Inicia el servidor con **uvicorn**:
```bash
uvicorn main:app --reload
```
Al ejecutarse, la API estará disponible en [http://localhost:8000](http://localhost:8000). Puedes explorar y probar los endpoints desde la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

## Uso básico de los endpoints
A continuación se muestra un flujo de ejemplo utilizando `curl`. Primero registramos un usuario, luego obtenemos un token de acceso y finalmente realizamos operaciones autenticadas.

### 1. Registro de usuario
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@demo.com", "password": "clave123", "full_name": "Usuario Demo"}'
```

### 2. Inicio de sesión
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=usuario@demo.com&password=clave123'
```
La respuesta contiene `access_token`. Guarda este valor para las siguientes llamadas.

### 3. Llamadas autenticadas
Para acceder a la mayoría de los endpoints necesitas incluir el token en la cabecera `Authorization`:
```bash
-H "Authorization: Bearer <access_token>"
```
Por ejemplo, para listar tus reservas:
```bash
curl http://localhost:8000/bookings \
  -H "Authorization: Bearer <access_token>"
```

Consulta `/docs` para ver todos los endpoints disponibles, incluyendo la creación de vuelos, aeropuertos, aeronaves, reservas y pagos.
Los vuelos ahora requieren asociar una aeronave mediante el campo `aircraft_id` y cuentan con el campo `available_seats` para indicar los asientos libres. Al crear una reserva se asigna un `seat` a cada pasajero registrado.

## Generación de datos de ejemplo
Para poblar la base de datos en memoria con datos ficticios puedes ejecutar el script `seed.py`:

```bash
python seed.py
```
Este script utiliza la biblioteca **Faker** para generar un conjunto reducido de datos por defecto:
- 20 aeropuertos
- 10 aeronaves
- 200 vuelos
- 50 usuarios
- 300 reservas
- 200 pagos
Puedes aumentar estas cantidades definiendo la variable de entorno `FAST_SEED=false` antes de ejecutarlo.

Cada tipo de entidad incluye la siguiente información principal:
- **Aeropuertos**: código IATA, ciudad y país.
- **Aeronaves**: matrícula (`tail_number`), modelo y capacidad de pasajeros.
- **Vuelos**: aeropuertos de origen y destino, horarios, precio base, aeronave asignada y asientos disponibles.
- **Usuarios**: correo electrónico, contraseña encriptada y nombre completo.
- **Reservas**: vuelo, usuario, estado y lista de pasajeros con nombre, pasaporte y asiento.
- **Pagos**: reserva asociada y estado del pago.

## Contribuciones
Este proyecto es solo para demostración. Cualquier mejora o corrección es bienvenida mediante pull requests.
