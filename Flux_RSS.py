import pandas as pd
import feedparser

# Définir l'URL du flux RSS
url_flux = "https://www.lemonde.fr/rss/une.xml"

# Récupérer les données du flux RSS
flux = feedparser.parse(url_flux)

# Extraire les titres, sources et contenus
titres = [item.get("title") for item in flux["entries"]]
sources = ["Cryptoast" for _ in range(len(flux["entries"]))]
contenus = [item.get("content") for item in flux["entries"]]

# Créer un DataFrame
df = pd.DataFrame({
    "Titre": titres,
    "Source": sources,
    "Contenu": contenus,
})

# Afficher les 10 premières lignes du DataFrame
print(df.head(10))
