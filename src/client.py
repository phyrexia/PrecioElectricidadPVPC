"""
Cliente para la API de ESIOS (Red Eléctrica de España).
"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime, date


class ESIOSClient:
    """Cliente para interactuar con la API de ESIOS."""
    
    BASE_URL = "https://api.esios.ree.es"
    
    def __init__(self, api_key: str, timeout: int = 30):
        """
        Inicializa el cliente ESIOS.
        
        Args:
            api_key: Token de autenticación de ESIOS
            timeout: Timeout para las peticiones en segundos
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json; application/vnd.esios-api-v2+json',
            'Content-Type': 'application/json',
            'Host': 'api.esios.ree.es',
            'x-api-key': self.api_key
        })
    
    def get_indicator(
        self, 
        indicator_id: int, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        time_trunc: str = 'hour'
    ) -> Dict[str, Any]:
        """
        Obtiene datos de un indicador específico.
        
        Args:
            indicator_id: ID del indicador en ESIOS
            start_date: Fecha de inicio (opcional, por defecto hoy)
            end_date: Fecha de fin (opcional, por defecto hoy)
            time_trunc: Granularidad temporal ('hour', 'day', etc.)
            
        Returns:
            Respuesta JSON de la API
            
        Raises:
            requests.exceptions.RequestException: Si hay error en la petición
        """
        # Si no se especifican fechas, usar hoy
        if start_date is None:
            start_date = datetime.now().date()
        if end_date is None:
            end_date = start_date
        
        # Formatear fechas para la API (formato: YYYY-MM-DDTHH:MM)
        # Para obtener el día completo, añadir horas
        params = {
            'start_date': f"{start_date.strftime('%Y-%m-%d')}T00:00",
            'end_date': f"{end_date.strftime('%Y-%m-%d')}T23:59",
            'time_trunc': time_trunc
        }
        
        url = f"{self.BASE_URL}/indicators/{indicator_id}"
        
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP {response.status_code}: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {e}")
            raise
    
    def close(self):
        """Cierra la sesión."""
        self.session.close()
    
    def __enter__(self):
        """Soporte para context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra la sesión al salir del context manager."""
        self.close()
