class SimilitudCoseno:
    def __init__(self):
        pass

    def producto_punto(self, vector_a, vector_b):
        resultado = 0

        for palabra in vector_a:
            if palabra in vector_b:
                resultado += vector_a[palabra] * vector_b[palabra]

        return resultado

    def magnitud(self, vector):
        suma = 0

        for palabra in vector:
            suma += vector[palabra] ** 2

        return suma ** 0.5

    def calcular_similitud(self, vector_a, vector_b):
        producto = self.producto_punto(vector_a, vector_b)
        magnitud_a = self.magnitud(vector_a)
        magnitud_b = self.magnitud(vector_b)

        if magnitud_a == 0 or magnitud_b == 0:
            return 0

        similitud = producto / (magnitud_a * magnitud_b)

        return similitud


    #Estas funciones son para el word2vec, ya que los vectores son listas y no diccionarios, tiene otro enfoque
    def producto_punto_vectores(self, vector_a, vector_b):
        resultado = 0

        for i in range(len(vector_a)):
            resultado += vector_a[i] * vector_b[i]

        return resultado

    def magnitud_vector(self, vector):
        suma = 0

        for valor in vector:
            suma += valor ** 2

        return suma ** 0.5

    def calcular_similitud_vectores(self, vector_a, vector_b):
        if vector_a is None or vector_b is None:
            return 0

        producto = self.producto_punto_vectores(vector_a, vector_b)
        magnitud_a = self.magnitud_vector(vector_a)
        magnitud_b = self.magnitud_vector(vector_b)

        if magnitud_a == 0 or magnitud_b == 0:
            return 0

        similitud = producto / (magnitud_a * magnitud_b)

        return float(similitud)