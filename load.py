import pandas as pd 
from pathlib import Path
import os
import geopandas as gpd



def load_cut_data(path) -> (list, list, list, list):
    """Carga los datos del archivo cut.xls y retorna los nombres de las regiones,
    
    Args:
        path (Path): Ruta del archivo cut.xls
    Returns:
        list: Lista de nombres de regiones
        list: Lista de códigos de regiones
        list: Lista de códigos de comunas
        list: Lista de nombres de comunas
    """
    data = pd.read_excel(path)
    # Obtener los códigos por region
    nombre_region = data.iloc[:, 1].unique().tolist()
    codigo_region = data.iloc[:, 0].unique().tolist()
    nombre_comuna = data.iloc[:, -1].unique().tolist()
    codigo_comuna = data.iloc[:, -2].unique().tolist()
    
    


    return nombre_region, codigo_region, codigo_comuna, nombre_comuna

def cargar_comunas(geoPath):
    # Reordenar en el orden visual 
    # XV- Arica y Parinacota
    # I - Tarapacá
    # II - Antofagasta
    # III - Atacama
    # IV - Coquimbo
    # V - Valparaíso
    # XIII - Metropolitana
    # VI - O'Higgins
    # VII - Maule
    # VIII - Biobío
    # IX - Araucanía
    # XIV - Los Ríos
    # X - Los Lagos
    # XI - Aysén
    # XII - Magallanes
    # XVI - Ñuble
    # Cargar los archivos geojson
    comunas = {
        1: gpd.read_file(f"{geoPath}/1.geojson"),
        2: gpd.read_file(f"{geoPath}/2.geojson"),
        3: gpd.read_file(f"{geoPath}/3.geojson"),
        4: gpd.read_file(f"{geoPath}/4.geojson"),
        5: gpd.read_file(f"{geoPath}/5.geojson"),
        6: gpd.read_file(f"{geoPath}/6.geojson"),
        7: gpd.read_file(f"{geoPath}/7.geojson"),
        8: gpd.read_file(f"{geoPath}/8.geojson"),
        9: gpd.read_file(f"{geoPath}/9.geojson"),
        10: gpd.read_file(f"{geoPath}/10.geojson"),
        11: gpd.read_file(f"{geoPath}/11.geojson"),
        12: gpd.read_file(f"{geoPath}/12.geojson"),
        13: gpd.read_file(f"{geoPath}/13.geojson"),
        14: gpd.read_file(f"{geoPath}/14.geojson"),
        15: gpd.read_file(f"{geoPath}/15.geojson"),
        16: gpd.read_file(f"{geoPath}/16.geojson"),

    }        
    return comunas

class Score:
    def __init__(self, path, identificador, code_column, score_column, regional=False,
                 aditional_columns=[]):
        """
        Args:
            path: Ruta del archivo que contiene los datos
            identificador: Nombre del archivo
            code_column: Nombre de la columna que contiene los códigos
            score_column: Nombre de la columna que contiene los scores
            regional: True si el archivo contiene datos regionales, False si contiene datos comunales

        Ejemplos:
            score = Score(path="./data/indice_riesgo.xlsx", identificador="Indice de Riesgo", code_column="Codigo", score_column="Indice de Riesgo", regional=True)
            score = Score(path="./data/indice_riesgo.xlsx", identificador="Indice de Riesgo", code_column="Codigo", score_column="Indice de Riesgo", regional=False)
        """
        # El identificador es un nombre interno para identificar el score 
        self.identificador = identificador

        # Cargamos los datos
        if 'xlsx' in path or 'xls' in path:
            self.data = pd.read_excel(path)
        if 'csv' in path:
            self.data = pd.read_csv(path)
        if regional:
            self.nombre_region, self.codigo_region, _, _ = load_cut_data("./data/cut.xls")
        else:
            _, _, self.codigo_comuna, self.nombre_comuna = load_cut_data("./data/cut.xls")

        # Guardamos los nombres de las columnas
        self.regional = regional
        self.code_column = code_column
        self.score_column = score_column
        self.aditional_data = aditional_columns
        
    def get_single_score_by_name(self, name):
        """Obtiene el score de una region o comuna usando el nombre de la region o comuna
        
        Args:
            name: Nombre de la region o comuna
        
        Ejemplos:
            score.get_single_score_by_name("Metropolitana")
            score.get_single_score_by_name("Santiago")
        
        La idea de esta función es que se use con el hover de un mapa para obtener el score de una region o comuna
        y mostrar su score en los controles de la interfaz

        Returns:
            float: Score de la region o comuna
        """
        # obtener el codigo de la region o comuna
        if self.regional:
            codigo = self.codigo_region[self.nombre_region.index(name)]
        else:
            codigo = self.codigo_comuna[self.nombre_comuna.index(name)]
    
        # obtener el score
        self.get_single_score_by_code(codigo)
    
    def get_single_score_by_code(self, code):
        """Obtiene el score de una region o comuna usando el codigo cut de la region o comuna

        Args:
            code: Codigo cut de la region o comuna

        Ejemplos:
            score.get_single_score_by_code(13110) # La cisterna
            score.get_single_score_by_code(13113) # La pintana
        
        La idea de esta función es que se use con el hover de un mapa para obtener el score de una region o comuna
        y mostrar su score en los controles de la interfaz

        Returns:
            float: Score de la region o comuna
        """
        # obtener el score
        score = self.data[self.data[self.code_column] == code][self.score_column]
        if score.empty:
            return -1
        return score.values[0]

    def get_all_scores(self):
        """Obtiene todos los scores de las regiones o comunas y sus respectivos codigos
        
        args:
            No recibe argumentos

        La idea de esta función es obtener los scores para poder hacer una función de color
        en el mapa, dependiendo de los valores son los colores que se van a mostrar en el mapa

        Returns:
            list: Lista de scores
            list: Lista de codigos

        Ejemplos:
            ```py
                scores, codes = score.get_all_scores()
            ```
            * Donde codes es una lista de codigos cut de regiones o comunas
            * Donde scores es una lista de scores de regiones o comunas
        """
        # obtener todos los scores y los codigos
        if self.regional:
            scores = self.data[self.score_column].values.tolist()
            codes = self.data[self.code_column].values.tolist()
            return scores, codes
        else:
            scores = []
            codes = []
            for codigo in self.codigo_comuna:

                scores.append(self.get_single_score_by_code(codigo))
                codes.append(codigo)
            return scores, codes
    
    def get_scores_and_locations(self):
        """Obtiene todos los scores de las regiones o comunas y sus respectivos nombres
        
        args:
            No recibe argumentos
        
        La idea de esta función es obtener los scores para poder hacer una función de color
        en el mapa, dependiendo de los valores son los colores que se van a mostrar en el mapa
        
        Returns:
            list: Lista de scores
            list: Lista de nombres

        Ejemplos:
            ```py
                scores, locations = score.get_all_scores()
            ```
            * Donde locations es una lista de nombres de regiones o comunas
            * Donde scores es una lista de scores de regiones o comunas
        """
        # obtener todos los scores y los nombres de las comunas
        if self.regional:
            scores = self.data[self.score_column].values.tolist()
            locations = self.data[self.code_column].values.tolist()
            return scores, locations
        else:
            scores = []
            locations = []
            for codigo in self.codigo_comuna:
                scores.append(self.get_single_score_by_code(codigo))
                locations.append(self.nombre_comuna[self.codigo_comuna.index(codigo)])
            return scores, locations
        
    def get_scores_from_geojson(self, df, column, target):
        """Obtiene los scores de un GeoDataFrame usando un GeoDataFrame y una columna
        
        Args:
            df: GeoDataFrame que contiene los datos
            column: Nombre de la columna que contiene los codigos
            target: Nombre de la columna que contiene los scores

        Ejemplos:
            score.get_scores_from_geojson(df, column="codregion", target="score")
            score.get_scores_from_geojson(df, column="codcomuna", target="score")
        
        La idea de esta función es que se use con el hover de un mapa para obtener el score de una region o comuna
        y mostrar su score en los controles de la interfaz

        Returns:
            GeoDataFrame: GeoDataFrame con los scores agregados
        """
        # obtener los scores
        scores = []
        for codigo in df[column]:
            scores.append(self.get_single_score_by_code(codigo))
        # agregar los scores al GeoDataFrame
        df[target] = scores
        return df

    def get_data_row(self, codigo):
        """Devuelve la fila de un codigo
        
        Args:
            codigo: Codigo de la region o comuna
        
        Ejemplos:
            score.get_data_row(13110)

        """
        return self.data[self.data[self.code_column] == codigo]
    
    def get_min_max(self, column):
        """Devuelve el minimo y el maximo de una columna

        Args:
            column: Nombre de la columna
        
        Ejemplos:
            score.get_min_max("Ranking1")
        
        """
        return self.data[column].min(), self.data[column].max()
if __name__ == "__main__":
    score = Score(
        path='./data/score.xlsx',
        identificador="Siniestros",
        code_column="Cod_comuna",
        score_column="Ranking1",
        regional=False
    )

    scores, codes = score.get_scores_and_locations()
    print(scores, codes)