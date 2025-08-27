"""Monte Carlo simulations for yes-no market dynamics."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from typing import List, Tuple

class MarketSimulator:
    """Simulate yes-no prediction market dynamics."""
    
    def __init__(self, true_prob: float, n_traders: int, n_steps: int):
        self.true_prob = true_prob
        self.n_traders = n_traders
        self.n_steps = n_steps
        
    def simulate(self) -> Tuple[np.ndarray, np.ndarray]:
        """Run market simulation."""
        prices = np.zeros(self.n_steps)
        volumes = np.zeros(self.n_steps)
        
        # Initialize market
        market_prob = 0.5
        
        for t in range(self.n_steps):
            # Traders arrive with noisy signals
            signals = self.true_prob + np.random.normal(0, 0.1, self.n_traders)
            signals = np.clip(signals, 0, 1)
            
            # Update market based on trading
            for signal in signals:
                if signal > market_prob:
                    # Buy YES shares
                    trade_size = abs(signal - market_prob) * 100
                    market_prob += 0.001 * trade_size
                else:
                    # Buy NO shares
                    trade_size = abs(market_prob - signal) * 100
                    market_prob -= 0.001 * trade_size
                    
                volumes[t] += trade_size
            
            market_prob = np.clip(market_prob, 0.01, 0.99)
            prices[t] = market_prob
            
        return prices, volumes
    
    def analyze_convergence(self, prices: np.ndarray) -> dict:
        """Analyze price convergence to true probability."""
        errors = np.abs(prices - self.true_prob)
        
        return {
            'mean_error': np.mean(errors),
            'final_error': errors[-1],
            'convergence_time': np.argmax(errors < 0.05) if np.any(errors < 0.05) else -1,
            'volatility': np.std(np.diff(prices))
        }

# Run simulations
if __name__ == "__main__":
    simulator = MarketSimulator(true_prob=0.7, n_traders=100, n_steps=1000)
    prices, volumes = simulator.simulate()
    results = simulator.analyze_convergence(prices)
    
    print(f"Convergence Analysis:")
    print(f"  Mean Error: {results['mean_error']:.4f}")
    print(f"  Final Error: {results['final_error']:.4f}")
    print(f"  Convergence Time: {results['convergence_time']} steps")
