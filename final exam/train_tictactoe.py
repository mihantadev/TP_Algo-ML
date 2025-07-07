import pandas as pd  # Importation de la bibliothèque pandas pour la manipulation des données
from sklearn.model_selection import train_test_split  # Pour diviser les données en ensembles d'entraînement et de test
from sklearn.tree import DecisionTreeClassifier  # Importation du modèle Arbre de Décision
from sklearn.metrics import classification_report, accuracy_score  # Pour évaluer les performances du modèle

# 1. Chargement du dataset à partir du fichier CSV
# Le fichier doit être dans le même dossier que ce script
file_path = 'Tic tac initial results.csv'
data = pd.read_csv(file_path)

# 2. Affichage des premières lignes pour vérifier le chargement
data.head()

# 3. Préparation des données
# Les colonnes MOVE1 à MOVE7 sont les features (entrées), CLASS est la cible (sortie)
X = data[[f'MOVE{i}' for i in range(1, 8)]]  # Sélection des colonnes de coups
# Remplacement des valeurs manquantes ("?") par -1 pour indiquer une case non jouée
X = X.replace('?', -1).astype(int)
y = data['CLASS']  # La colonne à prédire

# 4. Séparation des données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Création et entraînement du modèle Arbre de Décision
clf = DecisionTreeClassifier(random_state=42)  # Création du classifieur
clf.fit(X_train, y_train)  # Entraînement du modèle

# 6. Prédiction sur l'ensemble de test
y_pred = clf.predict(X_test)

# 7. Évaluation du modèle
print('Rapport de classification :')
print(classification_report(y_test, y_pred))  # Affiche la précision, le rappel, le f1-score
print('Exactitude globale :', accuracy_score(y_test, y_pred))  # Affiche l'exactitude globale

# 8. Exemple de prédiction
# Exemple : prédire le résultat d'une partie avec les coups [0, 4, 8, -1, -1, -1, -1]
# (-1 signifie que les coups suivants n'ont pas été joués)
example = [[0, 4, 8, -1, -1, -1, -1]]
prediction = clf.predict(example)
print('Prédiction pour la partie [0, 4, 8, -1, -1, -1, -1] :', prediction[0]) 