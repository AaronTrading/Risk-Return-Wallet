import numpy as np
import pandas as pd
from cvxopt import matrix, solvers
from typing import Tuple, List, Optional

class PortfolioOptimizer:
    def __init__(self, mean_returns: pd.Series, cov_matrix: pd.DataFrame):
        """
        Initialise l'optimiseur de portefeuille.
        
        Args:
            mean_returns: Série des rendements moyens
            cov_matrix: Matrice de covariance des rendements
        """
        # Vérification des données
        if mean_returns.isnull().any():
            raise ValueError("Les rendements moyens contiennent des valeurs manquantes")
        if cov_matrix.isnull().any().any():
            raise ValueError("La matrice de covariance contient des valeurs manquantes")
            
        # Vérification de la semi-définie positivité de la matrice de covariance
        eigenvalues = np.linalg.eigvals(cov_matrix)
        if not np.all(eigenvalues >= -1e-10):  # Tolérance pour les erreurs numériques
            raise ValueError("La matrice de covariance n'est pas semi-définie positive")
            
        self.mean_returns = mean_returns
        self.cov_matrix = cov_matrix
        self.n_assets = len(mean_returns)
        
    def optimize_portfolio(self, target_return: Optional[float] = None, 
                         risk_free_rate: float = 0.0) -> Tuple[np.ndarray, float, float]:
        """
        Optimise le portefeuille selon le critère de Markowitz.
        
        Args:
            target_return: Rendement cible (si None, maximise le ratio de Sharpe)
            risk_free_rate: Taux sans risque
            
        Returns:
            Tuple contenant (poids optimaux, rendement espéré, risque)
        """
        try:
            # Conversion en matrices pour cvxopt
            P = matrix(self.cov_matrix.values)
            q = matrix(0.0, (self.n_assets, 1))
            
            # Contraintes
            G = matrix(0.0, (self.n_assets, self.n_assets))
            G[::self.n_assets+1] = -1.0
            h = matrix(0.0, (self.n_assets, 1))
            
            A = matrix(1.0, (1, self.n_assets))
            b = matrix(1.0)
            
            if target_return is not None:
                # Vérification du rendement cible
                if target_return < self.mean_returns.min() or target_return > self.mean_returns.max():
                    raise ValueError(f"Le rendement cible doit être entre {self.mean_returns.min():.2%} et {self.mean_returns.max():.2%}")
                    
                # Ajout de la contrainte de rendement cible
                A = matrix(np.vstack((A, self.mean_returns.values)))
                b = matrix([1.0, target_return])
            
            # Configuration des options de résolution
            solvers.options['show_progress'] = False
            solvers.options['abstol'] = 1e-8
            solvers.options['reltol'] = 1e-7
            solvers.options['feastol'] = 1e-8
            
            # Résolution du problème quadratique
            sol = solvers.qp(P, q, G, h, A, b)
            
            if sol['status'] != 'optimal':
                raise ValueError(f"L'optimisation n'a pas convergé: {sol['status']}")
                
            weights = np.array(sol['x']).flatten()
            
            # Vérification des poids
            if not np.all(np.isfinite(weights)):
                raise ValueError("Les poids calculés contiennent des valeurs infinies ou NaN")
                
            # Normalisation des poids
            weights = weights / np.sum(weights)
            
            portfolio_return = np.sum(weights * self.mean_returns)
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
            
            return weights, portfolio_return, portfolio_risk
            
        except Exception as e:
            raise ValueError(f"Erreur lors de l'optimisation: {str(e)}")
    
    def efficient_frontier(self, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calcule la frontière efficiente.
        
        Args:
            n_points: Nombre de points sur la frontière
            
        Returns:
            Tuple contenant (rendements, risques, poids)
        """
        min_ret = self.mean_returns.min()
        max_ret = self.mean_returns.max()
        target_returns = np.linspace(min_ret, max_ret, n_points)
        
        returns = []
        risks = []
        weights_list = []
        
        for target in target_returns:
            try:
                w, ret, risk = self.optimize_portfolio(target_return=target)
                if np.all(np.isfinite([ret, risk])):
                    returns.append(ret)
                    risks.append(risk)
                    weights_list.append(w)
            except ValueError:
                continue
                
        if not returns:
            raise ValueError("Impossible de calculer la frontière efficiente")
                
        return np.array(returns), np.array(risks), np.array(weights_list)
    
    def max_sharpe_ratio(self, risk_free_rate: float = 0.0) -> Tuple[np.ndarray, float, float]:
        """
        Trouve le portefeuille avec le ratio de Sharpe maximum.
        
        Args:
            risk_free_rate: Taux sans risque
            
        Returns:
            Tuple contenant (poids optimaux, rendement espéré, risque)
        """
        try:
            weights, ret, risk = self.optimize_portfolio(risk_free_rate=risk_free_rate)
            return weights, ret, risk
        except Exception as e:
            raise ValueError(f"Erreur lors du calcul du ratio de Sharpe maximum: {str(e)}") 