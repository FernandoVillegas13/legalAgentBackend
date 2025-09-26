from langchain.tools import tool
from ddgs import DDGS
from typing import List, Dict


@tool
def buscar_web_duckduckgo(query: str, max_results: int = 5) -> str:
    """
    Herramienta para buscar información en la web usando DuckDuckGo.
    
    Args:
        query: Términos de búsqueda
        max_results: Número máximo de resultados (por defecto 5)
    
    Returns:
        str: Resultados de búsqueda formateados
    """
    print(f"DUCKDUCKGO: Buscando '{query}' con máximo {max_results} resultados")
    
    try:
        # Inicializar DuckDuckGo
        ddgs = DDGS()
        
        # Realizar búsqueda
        results = ddgs.text(
            query,  # El primer parámetro es query ahora
            max_results=max_results,
            region='es-pe',  # Región Perú para resultados relevantes
            safesearch='moderate'
        )
        
        if not results:
            return f"No se encontraron resultados para: {query}"
        
        # Formatear resultados
        formatted_results = f"Resultados de búsqueda para: '{query}'\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'Sin título')
            snippet = result.get('body', 'Sin descripción')
            url = result.get('href', '')
            
            formatted_results += f"{i}. **{title}**\n"
            formatted_results += f"   {snippet}\n"
            formatted_results += f"   🔗 {url}\n\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error al realizar la búsqueda: {str(e)}"


@tool
def buscar_noticias_duckduckgo(query: str, max_results: int = 3) -> str:
    """
    Herramienta para buscar noticias específicamente usando DuckDuckGo.
    
    Args:
        query: Términos de búsqueda para noticias
        max_results: Número máximo de noticias (por defecto 3)
    
    Returns:
        str: Noticias encontradas formateadas
    """
    
    try:
        # Inicializar DuckDuckGo
        ddgs = DDGS()
        
        # Realizar búsqueda de noticias
        news_results = ddgs.news(
            query,  # El primer parámetro es query ahora
            max_results=max_results,
            region='es-pe',
            safesearch='moderate'
        )
        
        if not news_results:
            return f"No se encontraron noticias para: {query}"
        
        # Formatear noticias
        formatted_news = f"Noticias sobre: '{query}'\n\n"
        
        for i, news in enumerate(news_results, 1):
            title = news.get('title', 'Sin título')
            snippet = news.get('body', 'Sin descripción')
            url = news.get('url', '')
            date = news.get('date', 'Fecha no disponible')
            source = news.get('source', 'Fuente no disponible')
            
            formatted_news += f"{i}. **{title}**\n"
            formatted_news += f"   📅 {date} | 📰 {source}\n"
            formatted_news += f"   {snippet}\n"
            formatted_news += f"   🔗 {url}\n\n"
        
        print(f"DUCKDUCKGO NEWS: Encontradas {len(news_results)} noticias")
        return formatted_news
        
    except Exception as e:
        print(f"DUCKDUCKGO NEWS: Error en búsqueda: {str(e)}")
        return f"Error al buscar noticias: {str(e)}"
