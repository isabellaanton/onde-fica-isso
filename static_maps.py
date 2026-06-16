import requests
from PIL import Image
import io

def get_satellite_image(lat: float, lon: float, zoom: int = 18):
    """Busca imagem de satélite sem API Key"""
    try:
        # ArcGIS World Imagery (funciona bem)
        n = 2 ** zoom
        x = int((lon + 180.0) / 360.0 * n)
        y = int((1.0 - (lat * 3.141592653589793 / 180.0 + 1.0) / 3.141592653589793 * 0.5) * n)
        
        url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        pass
    
    # Fallback
    img = Image.new('RGB', (640, 480), color=(10, 25, 40))
    return img