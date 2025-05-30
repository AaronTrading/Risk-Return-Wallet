import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import yfinance as yf
from data_loader import DataLoader
from optimizer import PortfolioOptimizer
from plots import PortfolioVisualizer
from typing import List
import numpy as np
import requests
from io import StringIO

# Liste de tickers populaires (S&P500 + tech US)
POPULAR_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'UNH',
    'HD', 'PG', 'MA', 'DIS', 'BAC', 'XOM', 'PFE', 'KO', 'PEP', 'CSCO',
    'ORCL', 'T', 'INTC', 'CMCSA', 'NFLX', 'ADBE', 'CRM', 'ABT', 'MCD', 'NKE',
    'WMT', 'CVX', 'MRK', 'TMO', 'COST', 'DHR', 'LLY', 'AVGO', 'TXN', 'QCOM',
    'LIN', 'HON', 'NEE', 'PM', 'IBM', 'SBUX', 'MDT', 'AMGN', 'LOW', 'AMAT',
    'GE', 'CAT', 'GS', 'AXP', 'BLK', 'SPY', 'QQQ', 'EEM', 'IWM', 'DIA',
    'AIR.PA', 'MC.PA', 'OR.PA', 'BNP.PA', 'SAN.PA', 'SU.PA', 'DG.PA', 'VIE.PA',
]

# --- Fonctions utilitaires pour récupérer les tickers dynamiquement ---
def get_sp500_tickers_with_names():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(StringIO(requests.get(url).text))[0]
    tickers = table['Symbol'].tolist()
    names = table['Security'].tolist()
    return [(t, n) for t, n in zip(tickers, names)]

def get_cac40_tickers_with_names():
    url = 'https://en.wikipedia.org/wiki/CAC_40'
    table = pd.read_html(StringIO(requests.get(url).text))[3]
    tickers = table['Ticker'].tolist()
    names = table['Company'].tolist()
    tickers = [t + '.PA' if not t.endswith('.PA') else t for t in tickers]
    return [(t, n) for t, n in zip(tickers, names)]

def get_nasdaq100_tickers_with_names():
    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    table = pd.read_html(StringIO(requests.get(url).text))[4]
    tickers = table['Ticker'].tolist()
    names = table['Company'].tolist()
    return [(t, n) for t, n in zip(tickers, names)]

def get_dax40_tickers_with_names():
    url = 'https://en.wikipedia.org/wiki/DAX'
    table = pd.read_html(StringIO(requests.get(url).text))[3]
    tickers = table['Ticker symbol'].tolist()
    names = table['Company'].tolist()
    tickers = [t + '.DE' if not t.endswith('.DE') else t for t in tickers]
    return [(t, n) for t, n in zip(tickers, names)]

def get_ftse100_tickers_with_names():
    url = 'https://en.wikipedia.org/wiki/FTSE_100_Index'
    table = pd.read_html(StringIO(requests.get(url).text))[3]
    tickers = table['EPIC'].tolist()
    names = table['Company'].tolist()
    tickers = [t + '.L' if not t.endswith('.L') else t for t in tickers]
    return [(t, n) for t, n in zip(tickers, names)]

class PortfolioOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimiseur de Portefeuille")
        self.root.geometry("900x700")
        
        # Initialisation des composants
        self.data_loader = DataLoader()
        self.visualizer = PortfolioVisualizer()
        self.selected_tickers = []
        self.ticker_name_map = {}  # Pour afficher le nom complet
        
        # Chargement dynamique des tickers
        self.all_tickers = self.load_all_tickers()
        
        self.create_widgets()
        
    def load_all_tickers(self):
        tickers = []
        try:
            sp500 = get_sp500_tickers_with_names()
            cac40 = get_cac40_tickers_with_names()
            nasdaq100 = get_nasdaq100_tickers_with_names()
            dax40 = get_dax40_tickers_with_names()
            ftse100 = get_ftse100_tickers_with_names()
            tickers = sp500 + cac40 + nasdaq100 + dax40 + ftse100
        except Exception as e:
            # Fallback sur une liste statique très enrichie
            tickers = [
                ('AAPL', 'Apple'), ('MSFT', 'Microsoft'), ('GOOGL', 'Alphabet'),
                ('AMZN', 'Amazon'), ('TSLA', 'Tesla'), ('META', 'Meta Platforms'),
                ('NVDA', 'Nvidia'), ('JPM', 'JPMorgan Chase'), ('V', 'Visa'),
                ('UNH', 'UnitedHealth'), ('HD', 'Home Depot'), ('PG', 'Procter & Gamble'),
                ('MA', 'Mastercard'), ('DIS', 'Disney'), ('BAC', 'Bank of America'),
                ('XOM', 'Exxon Mobil'), ('PFE', 'Pfizer'), ('KO', 'Coca-Cola'),
                ('PEP', 'PepsiCo'), ('CSCO', 'Cisco'), ('ORCL', 'Oracle'),
                ('T', 'AT&T'), ('INTC', 'Intel'), ('CMCSA', 'Comcast'),
                ('NFLX', 'Netflix'), ('ADBE', 'Adobe'), ('CRM', 'Salesforce'),
                ('ABT', 'Abbott'), ('MCD', "McDonald's"), ('NKE', 'Nike'),
                ('WMT', 'Walmart'), ('CVX', 'Chevron'), ('MRK', 'Merck'),
                ('TMO', 'Thermo Fisher'), ('COST', 'Costco'), ('DHR', 'Danaher'),
                ('LLY', 'Eli Lilly'), ('AVGO', 'Broadcom'), ('TXN', 'Texas Instruments'),
                ('QCOM', 'Qualcomm'), ('LIN', 'Linde'), ('HON', 'Honeywell'),
                ('NEE', 'NextEra Energy'), ('PM', 'Philip Morris'), ('IBM', 'IBM'),
                ('SBUX', 'Starbucks'), ('MDT', 'Medtronic'), ('AMGN', 'Amgen'),
                ('LOW', "Lowe's"), ('AMAT', 'Applied Materials'), ('GE', 'General Electric'),
                ('CAT', 'Caterpillar'), ('GS', 'Goldman Sachs'), ('AXP', 'American Express'),
                ('BLK', 'BlackRock'), ('SPY', 'S&P500 ETF'), ('QQQ', 'Nasdaq100 ETF'),
                ('EEM', 'Emerging Markets ETF'), ('IWM', 'Russell 2000 ETF'),
                ('DIA', 'Dow Jones ETF'), ('AIR.PA', 'Airbus'), ('MC.PA', 'LVMH'),
                ("OR.PA", "L'Oréal"), ('BNP.PA', 'BNP Paribas'), ('SAN.PA', 'Sanofi'),
                ('SU.PA', 'Schneider Electric'), ('DG.PA', 'Vinci'), ('VIE.PA', 'Veolia'),
                ('ADS.DE', 'Adidas'), ('ALV.DE', 'Allianz'), ('BAS.DE', 'BASF'),
                ('BAYN.DE', 'Bayer'), ('BMW.DE', 'BMW'), ('DAI.DE', 'Mercedes-Benz'),
                ('DBK.DE', 'Deutsche Bank'), ('DPW.DE', 'Deutsche Post'),
                ('DTE.DE', 'Deutsche Telekom'), ('FME.DE', 'Fresenius'),
                ('FRE.DE', 'Fresenius SE'), ('HEI.DE', 'HeidelbergCement'),
                ('HEN3.DE', 'Henkel'), ('IFX.DE', 'Infineon'), ('LHA.DE', 'Lufthansa'),
                ('LIN.DE', 'Linde'), ('MRK.DE', 'Merck KGaA'), ('MUV2.DE', 'Munich Re'),
                ('RWE.DE', 'RWE'), ('SAP.DE', 'SAP'), ('SIE.DE', 'Siemens'),
                ('VOW3.DE', 'Volkswagen'), ('BARC.L', 'Barclays'), ('BP.L', 'BP'),
                ('GSK.L', 'GSK'), ('HSBA.L', 'HSBC'), ('RIO.L', 'Rio Tinto'),
                ('SHEL.L', 'Shell'), ('ULVR.L', 'Unilever'), ('VOD.L', 'Vodafone'),
                ('AZN.L', 'AstraZeneca'), ('LLOY.L', 'Lloyds')
            ]
        self.ticker_name_map = {t: n for t, n in tickers}
        return [f"{t} ({n})" for t, n in tickers]

    def create_widgets(self):
        """Crée les widgets de l'interface."""
        param_frame = ttk.LabelFrame(self.root, text="Paramètres", padding="10")
        param_frame.pack(fill="x", padx=10, pady=5)
        
        # Combobox pour sélectionner un ticker
        ttk.Label(param_frame, text="Sélectionnez un ticker :").pack(anchor="w")
        self.ticker_var = tk.StringVar()
        self.ticker_combo = ttk.Combobox(param_frame, textvariable=self.ticker_var)
        self.ticker_combo['values'] = self.all_tickers
        self.ticker_combo.pack(fill="x", pady=5)
        
        # Bouton Ajouter depuis la combobox
        add_btn = ttk.Button(param_frame, text="Ajouter", command=self.add_ticker)
        add_btn.pack(pady=2)
        
        # Liste des tickers sélectionnés
        ttk.Label(param_frame, text="Tickers sélectionnés :").pack(anchor="w")
        self.selected_listbox = tk.Listbox(param_frame, height=8, exportselection=0)
        self.selected_listbox.pack(fill="x", pady=5)
        
        # Bouton Retirer
        remove_btn = ttk.Button(param_frame, text="Retirer", command=self.remove_ticker)
        remove_btn.pack(pady=2)
        
        # Période
        ttk.Label(param_frame, text="Période:").pack(anchor="w")
        self.period_var = tk.StringVar(value="1y")
        period_combo = ttk.Combobox(param_frame, textvariable=self.period_var)
        period_combo['values'] = ('1mo', '2mo', '3mo', '6mo', '1y', '2y', '5y')
        period_combo.pack(fill="x", pady=5)
        
        # Intervalle
        ttk.Label(param_frame, text="Intervalle:").pack(anchor="w")
        self.interval_var = tk.StringVar(value="1d")
        interval_combo = ttk.Combobox(param_frame, textvariable=self.interval_var)
        interval_combo['values'] = ('1d', '1wk', '1mo')
        interval_combo.pack(fill="x", pady=5)
        
        # Type d'optimisation
        ttk.Label(param_frame, text="Type d'optimisation:").pack(anchor="w")
        self.optim_type_var = tk.StringVar(value="sharpe")
        ttk.Radiobutton(param_frame, text="Max Sharpe Ratio", 
                       variable=self.optim_type_var, value="sharpe").pack(anchor="w")
        ttk.Radiobutton(param_frame, text="Rendement cible", 
                       variable=self.optim_type_var, value="target").pack(anchor="w")
        
        # Rendement cible
        self.target_frame = ttk.Frame(param_frame)
        self.target_frame.pack(fill="x", pady=5)
        ttk.Label(self.target_frame, text="Rendement cible (%):").pack(side="left")
        self.target_return_var = tk.StringVar(value="10")
        self.target_return_entry = ttk.Entry(self.target_frame, 
                                           textvariable=self.target_return_var, width=10)
        self.target_return_entry.pack(side="left", padx=5)
        
        # Bouton d'optimisation
        ttk.Button(self.root, text="Optimiser", command=self.optimize).pack(pady=10)
        
    def add_ticker(self):
        combo_value = self.ticker_var.get().strip()
        if not combo_value:
            messagebox.showerror("Erreur", "Veuillez sélectionner un ticker.")
            return
        # Extraire le ticker (avant l'espace)
        ticker = combo_value.split(' ')[0]
        display_name = self.ticker_name_map.get(ticker, ticker)
        display_str = f"{ticker} ({display_name})"
        if ticker and ticker not in self.selected_tickers:
            self.selected_tickers.append(ticker)
            self.selected_listbox.insert(tk.END, display_str)
        elif ticker in self.selected_tickers:
            messagebox.showinfo("Info", f"{ticker} est déjà sélectionné.")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un ticker.")

    def remove_ticker(self):
        selected_indices = self.selected_listbox.curselection()
        for i in reversed(selected_indices):
            display_str = self.selected_listbox.get(i)
            ticker = display_str.split(' ')[0]
            self.selected_listbox.delete(i)
            self.selected_tickers.remove(ticker)

    def optimize(self):
        """Lance l'optimisation du portefeuille."""
        try:
            tickers = self.selected_tickers
            if not tickers:
                messagebox.showerror("Erreur", "Veuillez sélectionner au moins un ticker.")
                return
            period = self.period_var.get()
            interval = self.interval_var.get()
            
            # Récupération des données
            prices = self.data_loader.get_market_data(tickers, period, interval)
            returns, mean_returns, cov_matrix = self.data_loader.calculate_returns(prices)
            
            # Création de l'optimiseur
            optimizer = PortfolioOptimizer(mean_returns, cov_matrix)
            
            # Optimisation selon le type choisi
            if self.optim_type_var.get() == "sharpe":
                weights, ret, risk = optimizer.max_sharpe_ratio()
            else:
                target_return_annual = float(self.target_return_var.get()) / 100
                freq = interval
                if freq == "1 jour":
                    periods = 252
                elif freq == "1 semaine":
                    periods = 52
                elif freq == "1 mois":
                    periods = 12
                else:
                    periods = 252  # fallback
                # Conversion du rendement annualisé en rendement par période
                target_return_period = (1 + target_return_annual) ** (1 / periods) - 1
                weights, ret, risk = optimizer.optimize_portfolio(target_return=target_return_period)
            
            # Calcul de la frontière efficiente
            ef_returns, ef_risks, _ = optimizer.efficient_frontier()
            
            # Affichage des résultats
            self.visualizer.plot_efficient_frontier(ef_returns, ef_risks, 
                                                  optimal_point=(ret, risk))
            self.visualizer.plot_weights(weights, tickers, name_map=self.ticker_name_map)
            self.visualizer.plot_correlation_matrix(returns.corr())
            
            # Affichage des statistiques
            stats = f"Rendement espéré: {ret*100:.2f}%\nRisque: {risk*100:.2f}%"
            messagebox.showinfo("Résultats", stats)
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioOptimizerApp(root)
    root.mainloop() 