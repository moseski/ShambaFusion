import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Union
import logging
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PricePredictor:
    """Class for predicting crop prices using machine learning models"""
    
    def __init__(self):
        self.model_dir = Path(__file__).resolve().parent / 'model' / 'trained_models'
        self.wholesale_model_path = self.model_dir / 'wholesale_model.joblib'
        self.retail_model_path = self.model_dir / 'retail_model.joblib'
        self.wholesale_model = None
        self.retail_model = None
        
        # Ensure model directory exists
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Load or train models
        self._load_or_train_models()
    
    def _load_or_train_models(self):
        """Load trained models or train new ones if they don't exist"""
        try:
            # Try to load existing models
            self.wholesale_model = joblib.load(self.wholesale_model_path)
            self.retail_model = joblib.load(self.retail_model_path)
            logger.info("Successfully loaded existing price prediction models")
        except (FileNotFoundError, Exception) as e:
            logger.warning(f"Could not load models: {e}")
            logger.info("Training new price prediction models...")
            self._train_and_save_models()
    
    def _train_and_save_models(self):
        """Train and save new models"""
        try:
            # Generate synthetic data
            data = self._generate_synthetic_data()
            
            # Prepare features and targets
            X = data.drop(['Wholesale', 'Retail', 'Date'], axis=1)
            y_wholesale = data['Wholesale']
            y_retail = data['Retail']
            
            # Define categorical and numerical features
            categorical_features = ['Market', 'County', 'Commodity', 'Season']
            numerical_features = [
                'SupplyVolume', 'Temperature', 'Rainfall', 'Inflation', 
                'DemandIndex', 'FuelPrice', 'Holiday', 'ProductionCost',
                'TransportCost', 'Month', 'DayOfWeek'
            ]
            
            # Create preprocessor
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(), numerical_features),
                    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
                ]
            )
            
            # Create and train wholesale model
            self.wholesale_model = Pipeline([
                ('preprocessor', preprocessor),
                ('regressor', GradientBoostingRegressor(
                    n_estimators=200, 
                    max_depth=5, 
                    learning_rate=0.1,
                    random_state=42
                ))
            ])
            self.wholesale_model.fit(X, y_wholesale)
            
            # Create and train retail model
            self.retail_model = Pipeline([
                ('preprocessor', preprocessor),
                ('regressor', GradientBoostingRegressor(
                    n_estimators=200, 
                    max_depth=5, 
                    learning_rate=0.1,
                    random_state=42
                ))
            ])
            self.retail_model.fit(X, y_retail)
            
            # Save models
            joblib.dump(self.wholesale_model, self.wholesale_model_path)
            joblib.dump(self.retail_model, self.retail_model_path)
            
            logger.info(f"Models trained and saved to {self.model_dir}")
        except Exception as e:
            logger.error(f"Error training models: {e}")
            raise RuntimeError(f"Failed to train price prediction models: {e}")
    
    def _generate_synthetic_data(self):
        """Generate synthetic data for model training"""
        # Define parameters
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2023, 12, 31)
        days = (end_date - start_date).days + 1
        
        # Create dates with daily frequency
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # Define markets, counties, and commodities
        markets = ["Wakulima Market", "Gikomba Market", "Kongowea Market", "City Market", "Marikiti Market"]
        counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Kiambu", "Machakos", "Uasin Gishu", 
                   "Kakamega", "Nyeri", "Kilifi", "Bungoma", "Trans Nzoia"]
        commodities = ["Tomatoes", "Potatoes", "Onions", "Maize", "Beans", "Cabbage", "Kale", 
                      "Carrots", "Spinach", "Green Peas"]
        
        # Base prices for different commodities (in KES)
        base_prices = {
            "Tomatoes": {"wholesale": 80, "retail": 120, "volatility": 0.3},
            "Potatoes": {"wholesale": 50, "retail": 80, "volatility": 0.2},
            "Onions": {"wholesale": 70, "retail": 100, "volatility": 0.25},
            "Maize": {"wholesale": 40, "retail": 60, "volatility": 0.15},
            "Beans": {"wholesale": 110, "retail": 150, "volatility": 0.2},
            "Cabbage": {"wholesale": 30, "retail": 50, "volatility": 0.25},
            "Kale": {"wholesale": 25, "retail": 40, "volatility": 0.2},
            "Carrots": {"wholesale": 60, "retail": 90, "volatility": 0.2},
            "Spinach": {"wholesale": 45, "retail": 70, "volatility": 0.25},
            "Green Peas": {"wholesale": 90, "retail": 130, "volatility": 0.3}
        }
        
        # County price factors
        county_factors = {
            "Nairobi": 1.2, "Mombasa": 1.15, "Kisumu": 1.1, "Nakuru": 1.05, "Kiambu": 1.1,
            "Machakos": 1.0, "Uasin Gishu": 0.95, "Kakamega": 0.9, "Nyeri": 1.0, "Kilifi": 1.05,
            "Bungoma": 0.9, "Trans Nzoia": 0.85
        }
        
        # Market factors
        market_factors = {
            "Wakulima Market": 1.0, "Gikomba Market": 1.05, "Kongowea Market": 0.95,
            "City Market": 1.1, "Marikiti Market": 0.9
        }
        
        # Generate samples - multiple entries per day for different market/commodity combinations
        num_samples = days * 20  # 20 entries per day on average
        
        # Create random indices for sampling
        random_indices = np.random.choice(len(dates), num_samples)
        sampled_dates = [dates[i] for i in random_indices]
        
        # Generate features with seasonal patterns and trends
        temperature = []
        rainfall = []
        inflation = []
        fuel_prices = []
        
        for date in sampled_dates:
            # Temperature (°C) - seasonal pattern
            month = date.month
            if 3 <= month <= 5:  # Spring
                temp = np.random.normal(25, 3)
            elif 6 <= month <= 8:  # Summer
                temp = np.random.normal(30, 2)
            elif 9 <= month <= 11:  # Fall
                temp = np.random.normal(23, 3)
            else:  # Winter
                temp = np.random.normal(20, 4)
            temperature.append(max(10, min(35, temp)))
            
            # Rainfall (mm) - seasonal pattern
            if month in [4, 5, 11]:  # Rainy seasons in Kenya
                rain = np.random.gamma(5, 20)
            elif month in [6, 7, 8, 9]:  # Dry season
                rain = np.random.gamma(0.5, 10)
            else:
                rain = np.random.gamma(2, 15)
            rainfall.append(min(300, rain))
            
            # Inflation - increasing trend with noise
            years_from_start = (date - start_date).days / 365
            infl = 5.0 + years_from_start * 1.5 + np.sin(month / 12 * 2 * np.pi) * 0.5
            infl += np.random.normal(0, 0.3)
            inflation.append(max(3, min(12, infl)))
            
            # Fuel prices (KES) - increasing trend with fluctuations
            fuel = 110.0 + years_from_start * 15 + np.sin(month / 6 * np.pi) * 5
            fuel += np.random.normal(0, 3)
            fuel_prices.append(max(100, min(180, fuel)))
        
        # Generate random commodities, markets, and counties
        sampled_commodities = np.random.choice(commodities, num_samples)
        sampled_markets = np.random.choice(markets, num_samples)
        sampled_counties = np.random.choice(counties, num_samples)
        
        # Supply volume - seasonal pattern based on commodity and rainfall
        supply_volume = []
        for i in range(num_samples):
            date = sampled_dates[i]
            commodity = sampled_commodities[i]
            rain = rainfall[i]
            
            # Base supply varies by commodity
            base_supply = {
                "Tomatoes": 5000, "Potatoes": 8000, "Onions": 4000, "Maize": 10000,
                "Beans": 6000, "Cabbage": 7000, "Kale": 6000, "Carrots": 4500,
                "Spinach": 3500, "Green Peas": 3000
            }.get(commodity, 5000)
            
            # Seasonal factor
            month = date.month
            if commodity in ["Tomatoes", "Onions", "Kale", "Spinach"]:
                seasonal_factor = 0.9 + 0.2 * np.sin((month - 3) / 12 * 2 * np.pi)
            elif commodity in ["Potatoes", "Cabbage", "Carrots"]:
                seasonal_factor = 1.0 + 0.3 * np.cos(month / 12 * 2 * np.pi)
            elif commodity in ["Maize", "Beans", "Green Peas"]:
                seasonal_factor = 1.2 if 3 <= month <= 8 else 0.8
            else:
                seasonal_factor = 1.0
            
            # Rainfall effect
            if rain < 50:
                rain_factor = 0.8 + rain / 50 * 0.4
            elif rain < 150:
                rain_factor = 1.2
            else:
                rain_factor = 1.2 - (rain - 150) / 150 * 0.4
            
            # Calculate supply
            supply = base_supply * seasonal_factor * rain_factor * np.random.normal(1, 0.15)
            supply_volume.append(max(1000, min(15000, supply)))
        
        # Demand index (0-100) - seasonal with holidays effect
        demand_index = []
        holiday_indicator = []
        
        for i in range(num_samples):
            date = sampled_dates[i]
            commodity = sampled_commodities[i]
            
            # Check if it's a holiday
            is_holiday = False
            if (date.month == 1 and date.day <= 2) or \
               (date.month == 12 and date.day >= 23) or \
               (date.month == 5 and date.day == 1) or \
               (date.month == 6 and date.day == 1) or \
               (date.month == 10 and date.day == 20) or \
               (date.month == 12 and date.day == 12):
                is_holiday = True
                
            holiday_indicator.append(1 if is_holiday else 0)
            
            # Base demand by commodity
            if commodity in ["Tomatoes", "Onions", "Kale"]:
                base_demand = 75
            elif commodity in ["Potatoes", "Maize", "Beans"]:
                base_demand = 80
            else:
                base_demand = 65
                
            # Seasonal factor
            month = date.month
            seasonal_factor = 1.0 + 0.1 * np.sin((month - 6) / 12 * 2 * np.pi)
            
            # Calculate demand
            demand = base_demand * seasonal_factor * (1.2 if is_holiday else 1.0) * \
                    (1.1 if date.weekday() >= 5 else 1.0) * np.random.normal(1, 0.05)
            demand_index.append(max(50, min(100, demand)))
        
        # Production cost
        production_cost = []
        for i in range(num_samples):
            commodity = sampled_commodities[i]
            infl = inflation[i]
            fuel = fuel_prices[i]
            
            # Base production cost varies by commodity
            base_cost = {
                "Tomatoes": 40, "Potatoes": 25, "Onions": 30, "Maize": 20, "Beans": 35,
                "Cabbage": 15, "Kale": 12, "Carrots": 20, "Spinach": 18, "Green Peas": 30
            }.get(commodity, 25)
            
            # Calculate production cost
            cost = base_cost * (1.0 + (infl - 5) / 100) * (1.0 + (fuel - 110) / 500) * np.random.normal(1, 0.1)
            production_cost.append(max(10, min(100, cost)))
        
        # Transport cost
        transport_cost = []
        for i in range(num_samples):
            county = sampled_counties[i]
            market = sampled_markets[i]
            fuel = fuel_prices[i]
            
            # Base transport cost by county
            base_transport = {
                "Nairobi": 10, "Mombasa": 15, "Kisumu": 12, "Nakuru": 8, "Kiambu": 5,
                "Machakos": 7, "Uasin Gishu": 6, "Kakamega": 10, "Nyeri": 7, "Kilifi": 14,
                "Bungoma": 12, "Trans Nzoia": 10
            }.get(county, 10)
            
            # Calculate transport cost
            cost = base_transport * market_factors.get(market, 1.0) * (1.0 + (fuel - 110) / 110) * np.random.normal(1, 0.1)
            transport_cost.append(max(3, min(30, cost)))
        
        # Calculate wholesale and retail prices
        wholesale_prices = []
        retail_prices = []
        
        for i in range(num_samples):
            commodity = sampled_commodities[i]
            county = sampled_counties[i]
            market = sampled_markets[i]
            
            # Get base prices
            base_wholesale = base_prices[commodity]["wholesale"]
            base_retail = base_prices[commodity]["retail"]
            price_volatility = base_prices[commodity]["volatility"]
            
            # Get factors
            county_factor = county_factors[county]
            market_factor = market_factors[market]
            
            # Supply-demand effect
            supply = supply_volume[i]
            demand = demand_index[i]
            supply_demand_ratio = (demand / 75) / (supply / 5000)
            supply_demand_factor = supply_demand_ratio ** 0.5
            
            # Cost factors
            prod_cost = production_cost[i]
            trans_cost = transport_cost[i]
            
            # Cost effect on wholesale price
            cost_factor = 1.0 + ((prod_cost + trans_cost) / base_wholesale - 0.5) * 0.5
            
            # Seasonal volatility
            date = sampled_dates[i]
            month = date.month
            seasonal_volatility = 1.0 + price_volatility * np.sin((month - 3) / 12 * 2 * np.pi)
            
            # Calculate wholesale price
            wholesale = base_wholesale * county_factor * market_factor * supply_demand_factor * \
                       cost_factor * seasonal_volatility * np.random.normal(1, price_volatility * 0.3)
            wholesale_prices.append(max(base_wholesale * 0.5, min(base_wholesale * 2.5, wholesale)))
            
            # Retail markup
            markup_factor = np.random.uniform(1.3, 1.6)
            retail = wholesale * markup_factor
            retail_prices.append(max(base_retail * 0.5, min(base_retail * 2.5, retail)))
        
        # Create DataFrame
        data = pd.DataFrame({
            "Date": sampled_dates,
            "Market": sampled_markets,
            "County": sampled_counties,
            "Commodity": sampled_commodities,
            "Wholesale": wholesale_prices,
            "Retail": retail_prices,
            "Temperature": temperature,
            "Inflation": inflation,
            "SupplyVolume": supply_volume,
            "DemandIndex": demand_index,
            "Rainfall": rainfall,
            "FuelPrice": fuel_prices,
            "Holiday": holiday_indicator,
            "ProductionCost": production_cost,
            "TransportCost": transport_cost
        })
        
        # Add derived features
        data["Month"] = data["Date"].dt.month
        data["DayOfWeek"] = data["Date"].dt.dayofweek
        data["Season"] = data["Month"].apply(lambda x: 
                                           "Spring" if 3 <= x <= 5 else
                                           "Summer" if 6 <= x <= 8 else
                                           "Fall" if 9 <= x <= 11 else
                                           "Winter")
        
        return data
    
    def predict_prices(
        self,
        crop_type: str,
        county: str,
        supply_volume: float
    ) -> List[Dict[str, Union[str, float]]]:
        """
        Predict prices for given parameters
        
        Parameters:
        -----------
        crop_type : str
            The type of crop (e.g., "tomatoes")
        county : str
            The county (e.g., "nairobi")
        supply_volume : float
            The supply volume in kg
            
        Returns:
        --------
        list
            Predicted prices for different markets
        """
        try:
            # List of markets
            markets = ["Wakulima Market", "Gikomba Market", "Kongowea Market"]
            
            # Current date
            current_date = datetime.now()
            
            predictions = []
            for market in markets:
                # Prepare input features for the model
                features = pd.DataFrame({
                    'Commodity': [crop_type.title()],
                    'County': [county.title()],
                    'Market': [market],
                    'SupplyVolume': [float(supply_volume)],
                    'Month': [current_date.month],
                    'DayOfWeek': [current_date.weekday()],
                    'Season': ["Summer" if 6 <= current_date.month <= 8 else
                              "Fall" if 9 <= current_date.month <= 11 else
                              "Winter" if current_date.month <= 2 else "Spring"],
                    'Temperature': [25],  # Default values for other features
                    'Rainfall': [50],
                    'Inflation': [7.5],
                    'DemandIndex': [75],
                    'FuelPrice': [130],
                    'Holiday': [0],
                    'ProductionCost': [30],
                    'TransportCost': [10]
                })
                
                # Make predictions
                wholesale_price = float(self.wholesale_model.predict(features)[0])
                retail_price = float(self.retail_model.predict(features)[0])
                
                predictions.append({
                    'market': market,
                    'wholesale': wholesale_price,
                    'retail': retail_price
                })
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error generating predictions: {e}")
            raise RuntimeError(f"Failed to generate price predictions: {e}")