# Gerardo Andre Fernandez Cruz 23763
# Con este programa el usuario podra disfrutar de peliculas que se adecuen a sus gustos basado en un algoritmo de filtrado colaborativo

# Importar modulos
import pandas as pd
import matplotlib.pyplot as plt
import string
import random

# Declarar variables
df = pd.read_csv('preprocesado_movies.csv')
seguir_en_programa = True

# Crear un conjunto de datos para almacenar los datos del usuario
data = {
    'Identificador único': [],
    'Usuario': [],
    'Favoritas': [],
    'Géneros preferidos': [],
    'Historial de visualización': [],
    'Calificaciones': []
}

# Cargar el DataFrame desde un archivo CSV existente o crear uno vacío
try:
    cd = pd.read_csv('algoritmo.csv')
except FileNotFoundError:
    cd = pd.DataFrame(data)

        # Funciones
# 1. Mostrar información de las películas disponibles en un año específico
def por_año():
    año = int(input("Ingrese el año para ver las películas disponibles: "))
    peliculas_año = df[df['startYear'] == año][['primaryTitle', 'principalGenre', 'directorName']]
    print(peliculas_año)

# 2. Mostrar las primeras n películas de un género ordenadas por rating
def por_genero():
    genero = input("Ingrese el género de la película: ")
    n = int(input("Ingrese el número de películas a mostrar: "))
    peliculas_genero = df[df['principalGenre'] == genero].sort_values('averageRating', ascending=False).head(n)
    print(peliculas_genero)

# 3. Mostrar películas de documentales, dramas, ciencia ficción, animación y comedia de un año
def por_generos_año():
    year = int(input("Ingrese el año para ver las películas: "))
    generos = ['Documentary', 'Drama', 'Sci-Fi', 'Animation', 'Comedy']
    peliculas_generos_año = df[(df['startYear'] == year) & (df['principalGenre'].isin(generos))]
    print(peliculas_generos_año)

# 4. Mostrar el promedio de duración en minutos de películas de un género principal específico
def promedio_duracion_por_genero():
    genero = input("Ingrese el género principal de películas: ")
    promedio = df[df['principalGenre'] == genero]['runtimeMinutes'].mean()
    print(f"El promedio de duracion de las peliculas de ese genero es {promedio} minutos")

# 5. Mostrar la cantidad de películas por año de lanzamiento
def cantidad_peliculas_por_año():
    peliculas_por_año = df['startYear'].value_counts().sort_index()
    print(peliculas_por_año)

# 6. Mostrar un gráfico de barras con la cantidad de películas por año de lanzamiento
def grafico_peliculas_por_año():
    peliculas_por_año = df['startYear'].value_counts().sort_index()
    años = peliculas_por_año.index
    cantidad_peliculas = peliculas_por_año.values

    plt.bar(años, cantidad_peliculas)
    plt.xlabel('Año de Lanzamiento')
    plt.ylabel('Cantidad de Películas')
    plt.title('Cantidad de Películas por Año de Lanzamiento')
    plt.xticks(rotation=45)
    plt.show()

# 7. Mostrar las n películas con más votos
def peliculas_mas_votadas():
    n = int(input("Ingrese el número de películas a mostrar: "))
    peliculas = df.nlargest(n, 'numVotes')
    print(peliculas)

# 8. Mostrar las películas de un director específico
def peliculas_por_director():
    director = input("Ingrese el nombre del director: ")
    peliculas = df[df['directorName'] == director][['primaryTitle']]
    print(peliculas)


# 9. Mostrar los directores con mayor cantidad de películas
def directores_con_mas_peliculas():
    directores_con_peliculas = df['directorName'].value_counts().head()
    print(directores_con_peliculas)

# 10. Mostrar los directores cuya primera profesión no es director
def directores_primera_profesion():
    directores_profesion = df[df['director1stProfession'] != 'director'][['directorName', 'director1stProfession']].drop_duplicates(subset='directorName').head()
    print(directores_profesion)

# Genera un identificador único aleatorio y único para cada usuario
def generar_identificador():
    identificador = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    if identificador in cd['Identificador único']:
        return generar_identificador()
    else:
        return identificador

# Solicita al usuario la información para registrar un nuevo usuario
def registrar_usuario():
    print("")
    print("### REGISTRO ###")
    usuario = input("Ingrese su nombre de usuario: ")
    favoritas = input("Ingrese sus películas favoritas (separadas por comas): ")
    generos = input("Ingrese sus géneros preferidos (separados por comas y en ingles): ")
    historial = input("Ingrese su historial de visualización (separado por comas): ")
    calificaciones = input("Ingrese sus calificaciones de películas (separadas por comas): ")
    identificador = generar_identificador()
    
    print(f"Se ha registrado exitosamente! su identificador para iniciar sesion es {identificador} guardelo.")
    
    # Agregar los datos del usuario al DataFrame
    cd.loc[len(cd)] = [identificador, usuario, favoritas, generos, historial, calificaciones]
    
    # Guardar el DataFrame en un archivo CSV
    cd.to_csv('algoritmo.csv', index=False)
    
# Solicita al usuario su identificador único para iniciar sesión.
def mis_datos():
    identificador = input("Ingrese su identificador único: ")
    
    if identificador in cd['Identificador único'].values:
        # Obtener los datos del usuario
        usuario = cd[cd['Identificador único'] == identificador]
        print("Estos son tus datos")
        print(usuario)
    else:
        print("Identificador único no válido. Por favor, inténtelo nuevamente.")

# Recomendar películas al usuario
def recomendar_peliculas():
    identificador = input("Ingrese su identificador único: ")

    if identificador in cd['Identificador único'].values:
        # Obtener los datos del usuario
        usuario = cd[cd['Identificador único'] == identificador].iloc[0]

        # Obtener las preferencias del usuario
        generos_preferidos = usuario['Géneros preferidos'].split(',')
        historial_visualizacion = usuario['Historial de visualización'].split(',')
        calificaciones = usuario['Calificaciones'].split(',')

        # Filtrar películas basadas en las preferencias del usuario
        peliculas_recomendadas = df[df['principalGenre'].isin(generos_preferidos) & ~df['tconst'].isin(historial_visualizacion)]

        # Ordenar las películas por calificación promedio y votos
        peliculas_recomendadas = peliculas_recomendadas.sort_values(['averageRating', 'numVotes'], ascending=False)

        # Mostrar las primeras n películas recomendadas al usuario
        n = int(input("Cuantas peliculas deseas que te recomiende: "))
        peliculas_recomendadas = peliculas_recomendadas.head(n)

        if not peliculas_recomendadas.empty:
            print("¡Recomendación de películas para ti!")
            print(peliculas_recomendadas[['primaryTitle', 'principalGenre', 'averageRating', 'numVotes']])
        else:
            print("No hay películas recomendadas en este momento.")
    else:
        print("Identificador único no válido. Por favor, inténtelo nuevamente.")


# Menú principal
while seguir_en_programa == True:
    print("")
    print("### BIENVENIDO ###")
    print("Que desea hacer?")
    print("1. Registrar nuevo usuario")
    print("2. Ver mis datos")
    print("3. Recomiendame peliculas")
    print("4. Saber informacion sobre el conjunto de datos de cinepolis")
    print("5. Salir")
    
    opcion = input("Seleccione una opción válida ")
    
    # Hacer que la opción elegida sea un dígito, y si no lo es, volver a ejecutar el menú
    if opcion.isdigit() == False:
        print("Seleccione un tipo de valor válido")
    else:
        opcion = int(opcion)

    if opcion == 1:
        registrar_usuario()

    elif opcion == 2:
        mis_datos()
    
    elif opcion == 3:
        recomendar_peliculas()

    elif opcion == 4:
        print("")
        print("¿Qué desea saber ?")
        print("1. Mostrar información de las películas disponibles en un año específico")
        print("2. Mostrar las primeras n películas de un género ordenadas por rating")
        print("3. Mostrar películas de documentales, dramas, ciencia ficción, animación y comedia de un año")
        print("4. Mostrar el promedio de duración en minutos de películas de un género principal específico")
        print("5. Mostrar la cantidad de películas por año de lanzamiento")
        print("6. Mostrar un gráfico de barras con la cantidad de películas por año de lanzamiento")
        print("7. Mostrar las n películas con más votos")
        print("8. Mostrar las películas de un director específico")
        print("9. Mostrar los directores con mayor cantidad de películas")
        print("10. Mostrar los directores cuya primera profesión no es director")
        print("11. Volver")
        print("")

        sub_opcion = input("Seleccione una opción válida: ")
        if sub_opcion.isdigit() == False:
            print("Seleccione un tipo de valor válido")
        else:
            sub_opcion = int(sub_opcion)

        if sub_opcion == 1:
            por_año()

        elif sub_opcion == 2:
            por_genero()
        
        elif sub_opcion == 3:
            por_generos_año()

        elif sub_opcion == 4:
            promedio_duracion_por_genero()

        elif sub_opcion == 5:
            cantidad_peliculas_por_año()

        elif sub_opcion == 6:
            grafico_peliculas_por_año()

        elif sub_opcion == 7:
            peliculas_mas_votadas()
        
        elif sub_opcion == 8:
            peliculas_por_director()

        elif sub_opcion == 9:
            directores_con_mas_peliculas()

        elif sub_opcion == 10:
            directores_primera_profesion()

        elif sub_opcion == 11:
            print("Volviendo al menu principal...")   
        else:
            print("Seleccione una opción válida.")

    elif opcion == 5:
        seguir_en_programa = False
        print("Eso ha sido todo, vuelva pronto!")        
    else:
        print("Seleccione una opción válida.")