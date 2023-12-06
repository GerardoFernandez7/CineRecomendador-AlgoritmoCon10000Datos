# Gerardo Andre Fernandez Cruz 23763
# Con este programa de preguntas y respuestas seras capaz de saber mas sobre el archivo csv movies2023-1 y preprocesar el mismo

# Importar modulos
import pandas as pd

        # Parte 1
    # 1-
movies = pd.read_csv("movies2023-1.csv")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

    # 2-      
# a
print("")
print("a. ¿Cuántas filas y cuántas columnas tiene el conjunto de datos?")
print(f'El conjunto de datos tiene {movies.shape[0]} filas y {movies.shape[1]} columnas.\n')

# b
print("b. Cuántas variables numéricas tiene el conjunto de datos? ")
num_vars = (movies.dtypes == 'int64').sum() + (movies.dtypes == 'float64').sum()
print(f'Hay {num_vars} variables numericas en el conjunto de datos.\n')

# c
print("c. ¿Cuáles son los diferentes géneros principales que tiene el conjunto de datos? ")
genres = movies['genres'].unique()
print(f'Los diferentes generos en el conjunto de datos son: {genres} \n')

# d
print("d. ¿Cuántas películas hay en cada uno de los años? ¿cuántos años diferentes tiene el conjunto de datos?")
movies_per_year = movies['startYear'].value_counts()
print(f'Hay {len(movies_per_year)} años diferentes en el conjunto de datos.')
print('Numero de peliculas por año:')
print(f"{movies_per_year}\n")

# e
print("e. ¿Cuántas películas hay de cada género principal?")
movies_genre = movies['principalGenre'].value_counts()
print(f"{movies_genre}\n")

# f
print("f. ¿Cuáles son las diferentes regiones a las que pertenecen las películas?")
regiones = movies['region'].unique()
print(f'Las diferentes regiones a las que pertenecen las peliculas son: {regiones}\n')

# g
print("g. ¿Cuál es la película más larga y la más corta?")
corta = movies['runtimeMinutes'].idxmin()
larga = movies['runtimeMinutes'].idxmax()
corta_nombre = movies.loc[corta, 'primaryTitle']
larga_nombre = movies.loc[larga, 'primaryTitle']
print(f'La pelicula mas corta es {corta_nombre}.')
print(f'La pelicula mas larga es {larga_nombre}.\n')

# h
print("h. ¿Cuál es el promedio de la duración de las películas?")
promedio = movies['runtimeMinutes'].mean()
print(f'Las peliculas en promedio duran {promedio:.2f} minutos.\n')

        # Parte 2
# 1- 
# Encontrar columnas con solo un valor unico
cols_borrar = [col for col in movies.columns if movies[col].nunique() == 1]

# Borrar esas columnas del conjunto de datos
for col in cols_borrar:
    movies.pop(col)

# 2- 
# Remplazar '\\N' con 'unknown'
movies = movies.replace('\\N', 'unknown')

# 3-
# Guardar nuevamente el archivo con los cambios realizados
movies.to_csv('preprocesado_movies.csv', index=False)