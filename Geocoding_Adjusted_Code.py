
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# Carregar o DataFrame
df = pd.read_csv('seu_arquivo.csv')  # Substitua 'seu_arquivo.csv' pelo caminho correto do seu arquivo

# Instanciando o geocodificador com um timeout maior
geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)

# Função para obter endereço e coordenadas com retry
def get_location(name, cache):
    retries = 3
    for _ in range(retries):
        if name in cache:
            return cache[name]
        try:
            location = geolocator.geocode(name)
            if location:
                result = (location.address, location.latitude, location.longitude)
            else:
                result = (None, None, None)
            cache[name] = result
            return result
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Retry for {name} due to error: {str(e)}")
            time.sleep(5)  # Espera antes de tentar novamente
    return None, None, None

# Função para processar os nomes únicos e preencher as informações de localização
def process_names(names, delay=1):
    location_cache = {}
    results = {'address': [], 'latitude': [], 'longitude': []}
    for name in names:
        address, lat, lon = get_location(name, location_cache)
        results['address'].append(address)
        results['latitude'].append(lat)
        results['longitude'].append(lon)
        time.sleep(delay)  # Delay para respeitar os limites da API
    return results, location_cache

# Extrair nomes únicos de agentes
nomes_unicos = df['NomAgente'].unique()

# Processar os nomes para obter as informações de localização
location_results, cache = process_names(nomes_unicos)

# Adicionando os resultados ao DataFrame
df['Address'] = df['NomAgente'].map({name: addr for name, (addr, _, _) in cache.items()})
df['Latitude'] = df['NomAgente'].map({name: lat for name, (_, lat, _) in cache.items()})
df['Longitude'] = df['NomAgente'].map({name: lon for name, (_, _, lon) in cache.items()})

# Salvando o DataFrame atualizado
df.to_csv('seu_arquivo_atualizado.csv', index=False)  # Substitua 'seu_arquivo_atualizado.csv' pelo nome desejado para o arquivo de saída
