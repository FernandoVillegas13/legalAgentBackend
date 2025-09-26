from langchain.tools import tool
import requests
from domain.entities.agente_response import Source
import json

# Global variable para almacenar las fuentes
_jurisprudencia_sources = []

@tool
def search_jurisprudencia(query: str) -> str:
    """Función para buscar jurisprudencia en la base de datos usando API externa"""
    print("---------"*20)
    print(f"Buscando jurisprudencia para la consulta: {query}")
    
    try:
        # Paso 1: Obtener token de autenticación
        token_url = "https://deepfeel-labs.site/token"
        auth_data = {
            "user": "user", ##Get our credentials - DM me
            "password": "password"
        }
        
        token_response = requests.post(token_url, json=auth_data, timeout=30)
        token_response.raise_for_status()
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            print("Error: No se pudo obtener el token de acceso")
            return "Error: No se pudo autenticar con el servicio de jurisprudencia"
        
        # Paso 2: Realizar búsqueda de jurisprudencia
        search_url = "https://deepfeel-labs.site/search"
        search_data = {
            "query": query,
            "plan_type": "basic",
            "algorithm": "hybrid",
            "limit": 4,
            "use_hyde": True,
            "date_from": "2016-01-01",
            "date_to": "2027-12-31"
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        search_response = requests.post(search_url, json=search_data, headers=headers, timeout=30)
        search_response.raise_for_status()
        
        respuesta = search_response.json()
        
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        respuesta = get_fallback_data()
    except Exception as e:
        print(f"Error inesperado: {e}")
        respuesta = get_fallback_data()
    
    # Procesar respuesta y guardar fuentes
    save_sources_from_api_response(respuesta)
    print("---------"*20)
    return format_jurisprudencia_response(respuesta, query)

def get_fallback_data():
    """Datos de fallback en caso de que la API no esté disponible"""
    return {
        "results": {
            "documents": [
                {
                    "document_id": "d0383e78-15e8-4323-9c6c-40eacbc0d8bc",
                    "relevance_score": 0.426,
                    "document_metadata": {
                        "documento_id": "d0383e78-15e8-4323-9c6c-40eacbc0d8bc",
                        "numero_expediente": "03006-2023-HC",
                        "distrito_judicial": "Distrito Judicial de Lima Norte",
                        "sentido_resolucion": "Improcedente",
                        "demandante": "Fray Luis Albites Gonzales",
                        "demandado": "Poder Judicial",
                        "fecha_emision": "2025-05-21",
                        "url": "https://jurisprudencia.sedetc.gob.pe/sentencia/03006-2023-hc-709-2025"
                    },
                    "chunk_fragments": [
                        {
                            "id": "3e65c2e0-685c-403e-ae76-1670d26868a1",
                            "score": 0.5881374,
                            "chunk_id": "a2a0907d-518f-4863-9072-ab17d60a5ff9",
                            "chunk_index": 17,
                            "text": "como autor del delito contra la libertad sexual - violación sexual de menor de\nedad, pretextando con tal propósito la presunta afectación de los derechos\nreclamados en la demanda. Asimismo, estimó que las resoluciones judiciales\ncuestionadas se encuentran debidamente motivadas, pues han dado respuesta a\ncada una de las alegaciones de las partes y se han merituado en conjunto todos\nlos medios probatorios, generando certeza en los magistrados, respecto a la\ncondena impuesta.\nLa Primera Sala Penal de Apelaciones de la Corte Superior de Justicia de\nLima Norte confirmó la apelada por similares fundamentos.\n"
                        },
                        {
                            "id": "0eaceff8-7124-4d43-8b8d-5419df3ef790",
                            "score": 0.5401771,
                            "chunk_id": "a4d64dcb-6ced-4122-a8c5-a4ddf4a03198",
                            "chunk_index": 20,
                            "text": "LIMA NORTE\nFRAY LUIS ALBITES GONZALES\nFUNDAMENTOS\nDelimitación del petitorio\n1. El objeto de la demanda es que se declare la nulidad de lo siguiente: (i) la\nsentencia, Resolución 5, de fecha 4 de setiembre de 2019, que condenó a\ndon Fray Luis Albites Gonzales a cadena perpetua como autor del delito\ncontra la libertad sexual de menor de edad; y (ii) la sentencia de vista,\nResolución 4, de fecha 23 de enero de 2020, que confirmó la condena.9\n2. Denunció la vulneración de los derechos a tutela procesal efectiva, a la\ndebida motivación de las resoluciones judiciales, a la libertad personal y\n"
                        },
                        {
                            "id": "1dd25a50-95e5-4277-bef7-eaf691a1ec8b",
                            "score": 0.5296265,
                            "chunk_id": "444339ea-e463-414e-bd70-aaac764fec68",
                            "chunk_index": 12,
                            "text": "LIMA NORTE\nFRAY LUIS ALBITES GONZALES\nmencionada tía ni con alguna otra prueba periférica. Agregó que el sentenciado\nseñaló coherente y uniformemente en su declaración y en su examen de juicio\noral, que la menor “le decía que tenía 16 años, luego se enteró que tenía 14\naños”.\nAlegó que la menor agraviada ha brindado declaraciones incoherentes\nrespecto del lugar y las veces que mantuvieron relaciones sexuales con el\nbeneficiario; pese a ello, en la sentencia de vista se concluyó que las\ndeclaraciones de la menor son verosímiles por tratarse de un relato coherente y\nuniforme.\nEl Octavo Juzgado de la Investigación Preparatoria de Independencia de\nla Corte Superior de Justicia de Lima Norte, por Resolución 1, de fecha 4 de\n"
                        },
                        {
                            "id": "544846fc-ceca-46be-87b4-4229571ead62",
                            "score": 0.5233433,
                            "chunk_id": "9ccc8377-3275-45fa-bbd9-fb1e137c2c5a",
                            "chunk_index": 29,
                            "text": "LIMA NORTE\nFRAY LUIS ALBITES GONZALES\n6. Así, para efectos de sustentar que las sentencias condenatorias son\nincoherentes y carecen de motivación, el recurrente alude a argumentos\ntales como que la menor declaró que el favorecido sabía que tenía “trece\naños de edad porque su tía le dijo”; sin embargo, “esta afirmación nunca\nfue corroborada de alguna forma con la declaración de la tía de la menor\nagraviada, ni mucho menos existe una prueba periférica (…)”; y que la\nmenor brindó declaraciones incoherentes respecto del lugar y las veces\nque mantuvieron relaciones sexuales.\n7. De lo expuesto, en este caso se cuestionan elementos tales como la\nvaloración de las pruebas y su suficiencia, así como el criterio de los\njuzgadores aplicados al caso concreto y la subsunción del delito penal.\nEstos cuestionamientos resultan incompatibles con la naturaleza del\n"
                        },
                        {
                            "id": "f7b088d4-b52d-43ce-9851-118e2f8947d8",
                            "score": 0.513869,
                            "chunk_id": "f7e9e789-1c49-4acd-b889-71ea0dadbdc0",
                            "chunk_index": 2,
                            "text": "resolución, de fecha 20 de junio de 20231, expedida por la Primera Sala Penal\nde Apelaciones de la Corte Superior de Justicia de Lima Norte, que declaró\ninfundada la demanda de habeas corpus de autos.\nANTECEDENTES\nCon fecha 25 de setiembre de 2022, doña Charito Beatriz Albites\nGonzales interpuso demanda de habeas corpus a favor de don Fray Luis\nAlbites Gonzales y la dirigió contra el procurador público del Poder Judicial.2\nMediante la cual solicitó que se declare la nulidad de lo siguiente: (i) la\nsentencia, Resolución 5, de fecha 4 de setiembre de 20193, emitida por el\nJuzgado Penal Colegiado Permanente de la Corte Superior de Justicia de Lima\nNorte, que condenó al favorecido como autor del delito contra la libertad sexual\nde menor de edad a cadena perpetua; y (ii) la sentencia de vista, Resolución 4,\nde fecha 23 de enero de 20204, emitida por la Primera Sala Penal de\nApelaciones de la citada corte superior de justicia, que confirmó la condena.5\nDenunció la afectación de los derechos a la debida motivación de las\n"
                        }
                    ]
                },
                {
                    "document_id": "fc4b9151-6c77-4843-8b68-83d96121e538",
                    "relevance_score": 0.4176,
                    "document_metadata": {
                        "documento_id": "fc4b9151-6c77-4843-8b68-83d96121e538",
                        "numero_expediente": "01973-2024-HC",
                        "distrito_judicial": "Distrito Judicial de Cañete",
                        "sentido_resolucion": "Improcedente",
                        "demandante": "Carlos Manuel Ríos Grández",
                        "demandado": "Segunda Sala Penal Transitoria de la Corte Suprema de Justicia de la República",
                        "fecha_emision": "2025-05-29",
                        "url": "https://jurisprudencia.sedetc.gob.pe/sentencia/01973-2024-hc-528-2025"
                    },
                    "chunk_fragments": [
                        {
                            "id": "105207cb-b1e0-4d5e-8bc8-547680e7c72e",
                            "score": 0.58459044,
                            "chunk_id": "5fccb68c-ec98-49ae-ab81-cca951c45f1f",
                            "chunk_index": 30,
                            "text": "determinar al responsable de la desfloración producida antiguamente, y ha\nllegado a establecer su culpabilidad con base en la sindicación de la menor, y a\npartir de los demás medios de prueba que fueron actuados en juicio. Por lo tanto,\nsu condena ha sido impuesta luego de haber procedido conforme a una valoración\nindividual y conjunta de los elementos que se llevaron a juicio. Es así que con\nuna debida valoración y, por ende, motivación, se lo encontró responsable de\nviolación de la indemnidad sexual de la agraviada en el año 2001.\nLa Sala Penal de Apelaciones de la Corte Superior de Justicia de Cañete\nconfirma la apelada, por considerar que de las resoluciones cuestionadas,\nexpedidas en el proceso penal, se observa que no contienen un mandato que\nrestrinja o afecte la libertad personal del favorecido, ni se ha precisado de qué\nmodo lo resuelto en tales resoluciones afectó, en forma concreta, su derecho de\ndefensa en conexidad con su libertad personal, de manera que la reclamación del\nrecurrente no está vinculada al contenido constitucionalmente protegido del\nderecho tutelado por el habeas corpus. En todo caso, de acuerdo con el recurso\nde apelación, la libertad del recurrente se encuentra limitada por una resolución\n"
                        },
                        {
                            "id": "6216da8c-a091-4683-b7fc-c8474dc5fb02",
                            "score": 0.56926703,
                            "chunk_id": "8a8a6905-e051-406e-b512-d5591d0557f5",
                            "chunk_index": 32,
                            "text": "FUNDAMENTOS\nDelimitación del petitorio\n1. El objeto de la demanda es que se declaren nulas (i) la sentencia de fecha 8\nde enero de 2016, que condenó a don Carlos Manuel Ríos Grández a\nveinticinco años de pena privativa de la libertad por el delito de violación de\nla libertad sexual de menor de menor de edad10; y (ii) la ejecutoria suprema\nde fecha 8 de mayo de 2017, que declaró no haber nulidad en la precitada\nsentencia condenatoria11; y (iii) que se ordene la emisión de una nueva\nresolución y la inmediata liberación del favorecido.\n10 Expediente 17-2010 (53-2008-MALA).\n"
                        },
                        {
                            "id": "c21cad35-7af3-4669-9da5-63408f07ce43",
                            "score": 0.5378876,
                            "chunk_id": "b0bd6b2d-402f-4ab6-b32f-115deb68d9e9",
                            "chunk_index": 17,
                            "text": "menor de menor de edad4; y (ii) la ejecutoria suprema de fecha 8 de mayo de\n20175, que declaró no haber nulidad en la precitada sentencia condenatoria6; y\n(iii) que se ordene la emisión de una nueva resolución y la inmediata liberación\ndel favorecido.\nRefiere que la Sala Penal de Apelaciones en Adición Sala Penal\nLiquidadora de la Corte Superior de Justicia de Cañete, integrada por los señores\nSanz Quiroz, Ruiz Cochachín y Berger Vigueras, y los magistrados de la Segunda\nSala Penal Transitoria de la Corte Suprema de Justicia de la República, señores\nHinostroza Pariachi, Ventura Cueva, Pacheco Huancas, Cevallos Vegas y Chávez\nMella, expidieron las cuestionadas sentencias.\nEl recurrente manifiesta que la condena impuesta al favorecido se basa\núnicamente en la declaración de la supuesta agraviada y en un certificado médico\nlegal que hace referencia a la existencia de una “desfloración antigua”, sin que\nello constituya una prueba plena de un acto de violación sexual, pues se considera\ndesfloración al hecho de que haya ocurrido con una antigüedad de ocho días en\nadelante. Asimismo, señala que no se valoró el contexto de los hechos,\nespecíficamente que la menor en cuestión había fugado de su domicilio junto con\nsu entonces enamorado José Edulio Silva Silva, con quien en plena investigación\ncontrajo matrimonio y tuvo una hija, por lo que estos hechos desvirtúan la\n"
                        },
                        {
                            "id": "2398a436-dc77-4004-bb55-97b41ce0fa93",
                            "score": 0.53787637,
                            "chunk_id": "59e6fb92-dfcd-4e79-bc40-85f4424d17dc",
                            "chunk_index": 40,
                            "text": "reclamo que alegue a priori la afectación del derecho a la libertad personal o\nderechos conexos puede reputarse efectivamente como tal y merecer tutela,\npues para ello es necesario analizar previamente si los actos denunciados\nvulneran el contenido constitucionalmente protegido de los derechos\ninvocados.\n4. Este Tribunal Constitucional, en reiterada jurisprudencia, ha establecido que\nno es función del juez constitucional proceder a la subsunción de la conducta\nde un determinado tipo penal; a la calificación específica del tipo penal\nimputado; a la resolución de diligencias o actos de investigación; a efectuar\nel reexamen o revaloración de los medios probatorios, así como el\nestablecimiento de la inocencia o responsabilidad penal del procesado, pues,\ncomo es evidente, ello es tarea exclusiva del juez ordinario, por lo que escapa\na la competencia del juez constitucional.\n5. En el caso concreto, este Tribunal aprecia de lo descrito en los antecedentes\nque, en puridad, se pretende el reexamen de lo resuelto en vía judicial. En\nefecto, el recurrente cuestiona básicamente (i) que la sentencia condenatoria\nha sido dictada sin prueba plena, sustentándose exclusivamente en la\ndeclaración de la supuesta agraviada y en un certificado médico legal en el\n"
                        },
                        {
                            "id": "0021bd5e-b54b-4f27-96d2-26d8df9032a7",
                            "score": 0.51917326,
                            "chunk_id": "fa5fab00-37a3-41cc-b88b-f31cfc8ddeac",
                            "chunk_index": 25,
                            "text": "Por esta razón, la demanda\nconstitucional deberá declararse improcedente de conformidad con lo dispuesto\npor el artículo 7.1 del Nuevo Código Procesal Constitucional.\nEl Segundo Juzgado de Investigación Preparatoria de Cañete de la Corte\nSuperior de Justicia de Cañete, mediante sentencia, Resolución 6, de fecha 4 de\nabril de 20249, declara improcedente la demanda de habeas corpus, por\nconsiderar que la condena impuesta al favorecido se debió a la comisión del delito\ntipificado en el artículo 173, último párrafo, del Código Penal, pues, conforme a\nlas declaraciones de la agraviada, si bien pudo haber tenido una relación\n"
                        }
                    ]
                }
            ]
        }
    }


def format_jurisprudencia_response(api_response: dict, query: str):
    documents = api_response.get("results", {}).get("documents", [])

    if not documents:
        return "No se encontraron resultados para la consulta."
    
    formatted_text = f"JURISPRUDENCIA ENCONTRADA SOBRE: {query}\n\n"

    for i, doc in enumerate(documents, 1):
        metadata = doc.get("document_metadata", {})
        fragments = doc.get("chunk_fragments", [])

        formatted_text += f"CASO {i}:\n"
        formatted_text += f"Expediente: {metadata.get('numero_expediente', 'N/A')}\n"
        formatted_text += f"Distrito Judicial: {metadata.get('distrito_judicial', 'N/A')}\n"
        formatted_text += f"Fecha de Emisión: {metadata.get('fecha_emision', 'N/A')}\n"

        formatted_text += f"FRAGMENTOS:\n"
        for j, fragment in enumerate(fragments[:2], 1):
            text = fragment.get("text", "").strip()
            if text:
                formatted_text += f"• {text}\n\n"
        
        formatted_text += "---\n\n"

    return formatted_text

def save_sources_from_api_response(api_response: dict):
    global _jurisprudencia_sources

    documents = api_response.get("results", {}).get("documents", [])

    for doc in documents[:4]:
        metadata = doc.get("document_metadata", {})
        fragments = doc.get("chunk_fragments", [])

        excerpt = ""
        if fragments:
            text = fragments[0].get("text", "").strip()
            if text:
                excerpt = text.replace('\n', ' ').strip()
                if len(excerpt) > 200:
                    excerpt = excerpt[:200] + "..."
        
        if not excerpt:
            excerpt = "Jurisprudencia no disponible."

        expediente = metadata.get('numero_expediente', 'N/A')
        distrito = metadata.get('distrito_judicial', 'Tribunal').replace('Distrito Judicial de ', '')
        title = f"{expediente} - {distrito}"

        source = {
                "id": metadata.get('documento_id', doc.get('document_id', '')),
                "title": title,
                "excerpt": excerpt,
                "type": "document",  # Tipo que espera el frontend
                "url": metadata.get('url')
        }

        _jurisprudencia_sources.append(source)

def get_jurisprudencia_sources():
    global _jurisprudencia_sources
    return _jurisprudencia_sources.copy()

def clear_jurisprudencia_sources():
    global _jurisprudencia_sources
    _jurisprudencia_sources = []