import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Tuple, Union

class DataLoader:
    def __init__(self):
        """Initialise le chargeur de données."""
        pass

    def get_market_data(self, tickers: List[str], period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Récupère les données boursières via yfinance.
        
        Args:
            tickers: Liste des symboles boursiers
            period: Période d'analyse (ex: "1mo", "2mo", "3mo", "6mo", "1y", "2y", "5y")
            interval: Fréquence des données (ex: "1d", "1wk", "1mo")
            
        Returns:
            DataFrame contenant les prix de clôture ajustés
        """
        try:
            data = yf.download(tickers, period=period, interval=interval, auto_adjust=True)
            # On prend 'Close' si auto_adjust=True, sinon 'Adj Close'
            if isinstance(data, pd.DataFrame) and 'Close' in data:
                prices = data['Close']
            elif isinstance(data, pd.DataFrame) and 'Adj Close' in data:
                prices = data['Adj Close']
            else:
                raise ValueError("Aucune colonne de prix ('Close' ou 'Adj Close') trouvée dans les données téléchargées.")
            if prices.empty:
                raise ValueError("Aucune donnée n'a été récupérée")
            if prices.isnull().any().any():
                prices = prices.dropna()
                if prices.empty:
                    raise ValueError("Toutes les données ont été supprimées après le nettoyage des valeurs manquantes")
            return prices
        except Exception as e:
            raise ValueError(f"Erreur lors de la récupération des données: {str(e)}")

    def calculate_returns(self, prices: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
        """
        Calcule les rendements, rendements moyens et matrice de covariance.
        
        Args:
            prices: DataFrame des prix
            
        Returns:
            Tuple contenant (rendements, rendements moyens, matrice de covariance)
        """
        try:
            # Calcul des rendements
            returns = prices.pct_change().dropna()
            
            if returns.empty:
                raise ValueError("Aucun rendement n'a pu être calculé")
                
            # Vérification des valeurs infinies
            if np.isinf(returns.values).any():
                raise ValueError("Des valeurs infinies ont été détectées dans les rendements")
                
            # Calcul des statistiques
            mean_returns = returns.mean()
            cov_matrix = returns.cov()
            
            # Vérification de la matrice de covariance
            if not np.all(np.linalg.eigvals(cov_matrix) >= -1e-10):
                raise ValueError("La matrice de covariance n'est pas semi-définie positive")
                
            return returns, mean_returns, cov_matrix
            
        except Exception as e:
            raise ValueError(f"Erreur lors du calcul des rendements: {str(e)}")

    def generate_random_data(self, n_assets: int, n_days: int, seed: int = 42) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
        """
        Génère des données simulées pour les tests.
        
        Args:
            n_assets: Nombre d'actifs
            n_days: Nombre de jours
            seed: Seed pour la reproductibilité
            
        Returns:
            Tuple contenant (prix, rendements moyens, matrice de covariance)
        """
        try:
            np.random.seed(seed)
            
            # Génération de rendements aléatoires
            returns = np.random.normal(0.0005, 0.02, (n_days, n_assets))
            prices = (1 + returns).cumprod(axis=0)
            
            # Création des noms d'actifs
            asset_names = [f'ASSET_{i+1}' for i in range(n_assets)]
            dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days)
            
            # Conversion en DataFrame
            prices_df = pd.DataFrame(prices, index=dates, columns=asset_names)
            
            # Calcul des statistiques
            mean_returns = pd.Series(np.mean(returns, axis=0), index=asset_names)
            cov_matrix = pd.DataFrame(np.cov(returns.T), index=asset_names, columns=asset_names)
            
            return prices_df, mean_returns, cov_matrix
            
        except Exception as e:
            raise ValueError(f"Erreur lors de la génération des données aléatoires: {str(e)}") 