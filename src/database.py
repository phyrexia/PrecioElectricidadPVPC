"""
Gestión de la base de datos SQLite para almacenar precios PVPC.
"""

import sqlite3
from datetime import date
from typing import List, Optional, Tuple
from pathlib import Path


class Database:
    """Gestiona la base de datos SQLite de precios PVPC."""
    
    def __init__(self, db_path: str = "pvpc.db"):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_path: Ruta del archivo de base de datos
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establece conexión con la base de datos."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    
    def _create_tables(self):
        """Crea las tablas necesarias si no existen."""
        cursor = self.conn.cursor()
        
        # Tabla de precios PVPC
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS precios_pvpc (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora INTEGER NOT NULL,
                precio REAL NOT NULL,
                tramo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(fecha, hora)
            )
        """)
        
        # Índice para búsquedas rápidas por fecha
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_fecha 
            ON precios_pvpc(fecha)
        """)
        
        self.conn.commit()
    
    def insert_price(
        self, 
        fecha: date, 
        hora: int, 
        precio: float, 
        tramo: Optional[str] = None
    ) -> bool:
        """
        Inserta o actualiza un precio en la base de datos.
        
        Args:
            fecha: Fecha del precio
            hora: Hora (0-23)
            precio: Precio en €/MWh
            tramo: Tramo de color ('verde', 'amarillo', 'rojo')
            
        Returns:
            True si se insertó/actualizó correctamente
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO precios_pvpc (fecha, hora, precio, tramo)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(fecha, hora) 
                DO UPDATE SET precio=excluded.precio, tramo=excluded.tramo
            """, (fecha.isoformat(), hora, precio, tramo))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar precio: {e}")
            return False
    
    def insert_prices_batch(
        self, 
        prices: List[Tuple[date, int, float, Optional[str]]]
    ) -> int:
        """
        Inserta múltiples precios en una transacción.
        
        Args:
            prices: Lista de tuplas (fecha, hora, precio, tramo)
            
        Returns:
            Número de registros insertados/actualizados
        """
        cursor = self.conn.cursor()
        count = 0
        
        try:
            for fecha, hora, precio, tramo in prices:
                cursor.execute("""
                    INSERT INTO precios_pvpc (fecha, hora, precio, tramo)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(fecha, hora) 
                    DO UPDATE SET precio=excluded.precio, tramo=excluded.tramo
                """, (fecha.isoformat(), hora, precio, tramo))
                count += 1
            
            self.conn.commit()
            return count
        except sqlite3.Error as e:
            print(f"Error al insertar batch: {e}")
            self.conn.rollback()
            return 0
    
    def get_prices_by_date(self, fecha: date) -> List[sqlite3.Row]:
        """
        Obtiene todos los precios de una fecha específica.
        
        Args:
            fecha: Fecha a consultar
            
        Returns:
            Lista de registros (Row objects)
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM precios_pvpc 
            WHERE fecha = ?
            ORDER BY hora
        """, (fecha.isoformat(),))
        
        return cursor.fetchall()
    
    def get_date_range(self) -> Tuple[Optional[date], Optional[date]]:
        """
        Obtiene el rango de fechas disponible en la base de datos.
        
        Returns:
            Tupla (fecha_minima, fecha_maxima) o (None, None) si está vacía
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT MIN(fecha), MAX(fecha) 
            FROM precios_pvpc
        """)
        
        result = cursor.fetchone()
        if result[0] is None:
            return None, None
        
        return (
            date.fromisoformat(result[0]),
            date.fromisoformat(result[1])
        )
    
    def has_date(self, fecha: date) -> bool:
        """
        Verifica si ya existen datos para una fecha.
        
        Args:
            fecha: Fecha a verificar
            
        Returns:
            True si existen datos para esa fecha
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM precios_pvpc 
            WHERE fecha = ?
        """, (fecha.isoformat(),))
        
        count = cursor.fetchone()[0]
        return count > 0
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Soporte para context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la conexión al salir del context manager."""
        self.close()
