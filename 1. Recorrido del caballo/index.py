import tkinter as tk
from tkinter import messagebox

# Función para verificar si una posición es válida en el tablero
def es_valido(x, y, n, m, tablero):
    return 0 <= x < n and 0 <= y < m and tablero[x][y] == -1

# Movimientos posibles del caballo
movimientos = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

# Función recursiva para realizar la búsqueda en profundidad
def recorrido_caballo(x, y, paso, tablero, n, m, lista_movimientos, lista_backtracking):
    # Si hemos cubierto todas las casillas, retornamos verdadero
    if paso == n * m:
        return True
    
    # Intentar todos los posibles movimientos del caballo
    for dx, dy in movimientos:
        nuevo_x, nuevo_y = x + dx, y + dy
        if es_valido(nuevo_x, nuevo_y, n, m, tablero):
            tablero[nuevo_x][nuevo_y] = paso  # Marcar la casilla con el paso actual
            lista_movimientos.append((nuevo_x, nuevo_y, paso))  # Agregar movimiento a la lista
            if recorrido_caballo(nuevo_x, nuevo_y, paso + 1, tablero, n, m, lista_movimientos, lista_backtracking):
                return True
            tablero[nuevo_x][nuevo_y] = -1  # Desmarcar la casilla si no funciona
            lista_backtracking.append((nuevo_x, nuevo_y, paso))  # Agregar retroceso a la lista
            lista_movimientos.pop()  # Eliminar el movimiento si no funciona
    
    return False

# Función principal para iniciar el recorrido del caballo
def iniciar_recorrido(n, m):
    # Crear un tablero de tamaño n x m lleno de -1 (sin visitar)
    tablero = [[-1 for _ in range(m)] for _ in range(n)]
    
    # Iniciar desde la esquina superior izquierda (0, 0)
    tablero[0][0] = 0
    lista_movimientos = [(0, 0, 0)]  # Lista de movimientos, comenzando en (0, 0)
    lista_backtracking = []  # Lista de retrocesos
    
    # Comenzar el recorrido del caballo
    if recorrido_caballo(0, 0, 1, tablero, n, m, lista_movimientos, lista_backtracking):
        return lista_movimientos, lista_backtracking, tablero
    else:
        return lista_movimientos, lista_backtracking, tablero

# Clase para la interfaz gráfica
class RecorridoCaballoApp:
    def __init__(self, root, n, m):
        self.root = root
        self.n = n
        self.m = m
        self.movimientos, self.backtracking, _ = iniciar_recorrido(n, m)
        self.index = 0
        
        # Crear el tablero de botones
        self.botones = [[None for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                b = tk.Button(root, text='', width=4, height=2, font=('Arial', 24))
                b.grid(row=i, column=j)
                self.botones[i][j] = b
        
        # Botón para avanzar
        self.siguiente_btn = tk.Button(root, text="Siguiente", command=self.mostrar_siguiente)
        self.siguiente_btn.grid(row=n, column=0, columnspan=m)

    def mostrar_siguiente(self):
        if self.index < len(self.movimientos):
            x, y, paso = self.movimientos[self.index]
            self.botones[x][y].config(text=str(paso + 1), bg="lightgreen")
            self.index += 1
        elif self.index < len(self.movimientos) + len(self.backtracking):
            idx_backtracking = self.index - len(self.movimientos)
            x, y, paso = self.backtracking[idx_backtracking]
            self.botones[x][y].config(text='', bg="red")
            self.index += 1
        else:
            messagebox.showinfo("Fin", "Recorrido completo")
            self.siguiente_btn.config(state=tk.DISABLED)

# Configuración de la interfaz gráfica
def main():
    root = tk.Tk()
    root.title("Recorrido del Caballo")
    
    n = 6  # Número de filas
    m = 6  # Número de columnas
    
    app = RecorridoCaballoApp(root, n, m)
    
    root.mainloop()

if __name__ == "__main__":
    main()
