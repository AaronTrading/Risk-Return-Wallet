import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple

class PortfolioVisualizer:
    def __init__(self):
        """Initialise le visualiseur de portefeuille."""
        plt.style.use('default')
        
    def plot_efficient_frontier(self, returns: np.ndarray, risks: np.ndarray, 
                              optimal_point: Tuple[float, float] = None,
                              title: str = "Frontière Efficiente") -> None:
        """
        Trace la frontière efficiente.
        
        Args:
            returns: Tableau des rendements
            risks: Tableau des risques
            optimal_point: Point optimal (rendement, risque)
            title: Titre du graphique
        """
        plt.figure(figsize=(10, 6))
        plt.plot(risks, returns, 'b-', label='Frontière Efficiente')
        
        if optimal_point is not None:
            plt.plot(optimal_point[1], optimal_point[0], 'ro', 
                    label='Portefeuille Optimal')
            
        plt.xlabel('Risque (Écart-type)')
        plt.ylabel('Rendement Espéré')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def plot_weights(self, weights: np.ndarray, asset_names: list, title: str = "Répartition du Portefeuille", name_map: dict = None) -> None:
        """
        Trace la répartition des poids du portefeuille.
        Args:
            weights: Tableau des poids
            asset_names: Liste des noms d'actifs (tickers)
            title: Titre du graphique
            name_map: Dictionnaire ticker -> nom complet
        """
        if name_map:
            labels = [f"{t} ({name_map.get(t, t)})" for t in asset_names]
        else:
            labels = asset_names
        plt.figure(figsize=(10, 6))
        plt.pie(weights, labels=labels, autopct='%1.1f%%')
        plt.title(title)
        plt.axis('equal')
        plt.show()
        plt.figure(figsize=(12, 6))
        plt.bar(labels, weights)
        plt.xticks(rotation=45)
        plt.title(title)
        plt.ylabel('Poids')
        plt.tight_layout()
        plt.show()
        
    def plot_returns_distribution(self, returns: pd.DataFrame,
                                title: str = "Distribution des Rendements") -> None:
        """
        Trace la distribution des rendements pour chaque actif.
        
        Args:
            returns: DataFrame des rendements
            title: Titre du graphique
        """
        plt.figure(figsize=(12, 6))
        returns.hist(bins=50, figsize=(12, 6))
        plt.title(title)
        plt.tight_layout()
        plt.show()
        
    def plot_correlation_matrix(self, corr_matrix: pd.DataFrame,
                              title: str = "Matrice de Corrélation") -> None:
        """
        Trace la matrice de corrélation.
        
        Args:
            corr_matrix: DataFrame de la matrice de corrélation
            title: Titre du graphique
        """
        plt.figure(figsize=(10, 8))
        plt.imshow(corr_matrix, cmap='RdYlBu')
        plt.colorbar()
        plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
        plt.yticks(range(len(corr_matrix.index)), corr_matrix.index)
        plt.title(title)
        plt.tight_layout()
        plt.show() 