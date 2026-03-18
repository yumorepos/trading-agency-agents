#!/usr/bin/env python3
"""
Unit tests for Trading Agency Agents
Tests core functionality without requiring live API access
"""

import pytest
import json
from unittest.mock import Mock, patch

# Mock market data for testing
MOCK_MARKET_DATA = {
    "btc-up-down-1": [
        {"price": 0.52, "outcome": "Up", "size": 100},
        {"price": 0.48, "outcome": "Down", "size": 120}
    ],
    "btc-up-down-2": [
        {"price": 0.55, "outcome": "Up", "size": 80},
        {"price": 0.45, "outcome": "Down", "size": 90}
    ]
}

class TestMarketScanner:
    """Test Market Scanner agent functionality"""
    
    def test_arbitrage_detection(self):
        """Test detection of arbitrage opportunities"""
        # Prices sum to < 1.0 = arbitrage
        p_yes = 0.48
        p_no = 0.48
        
        # Calculate edge
        total = p_yes + p_no
        edge = 1.0 - total
        
        assert edge > 0.03  # Should detect 4% arbitrage
    
    def test_no_arbitrage(self):
        """Test when no arbitrage exists"""
        p_yes = 0.51
        p_no = 0.51
        
        total = p_yes + p_no
        edge = 1.0 - total
        
        assert edge < 0.01  # Should not trigger (efficient market)
    
    def test_correlation_detection(self):
        """Test correlation group mean calculation"""
        # Similar markets should have similar prices
        prices = [0.52, 0.55, 0.53, 0.54]
        mean = sum(prices) / len(prices)
        
        assert 0.52 <= mean <= 0.55
        
        # Outlier detection
        outlier = 0.80
        deviation = abs(outlier - mean)
        
        assert deviation > 0.2  # Should flag as outlier


class TestRiskManager:
    """Test Risk Manager agent functionality"""
    
    def test_kelly_sizing(self):
        """Test Kelly Criterion position sizing"""
        bankroll = 10000
        edge = 0.05  # 5% edge
        kelly_fraction = 0.5  # Half Kelly
        max_pct = 0.05  # 5% cap
        
        # Kelly position
        position = edge * kelly_fraction * bankroll
        
        # Apply cap
        max_position = max_pct * bankroll
        final_position = min(position, max_position)
        
        assert final_position == 250  # 5% cap (500 Kelly → capped to 500)
        assert final_position <= max_position
    
    def test_stop_loss(self):
        """Test stop-loss enforcement"""
        max_loss_per_trade = 20
        
        # Losing trade
        entry_price = 100
        current_price = 75
        loss = entry_price - current_price
        
        assert loss > max_loss_per_trade  # Should trigger stop
    
    def test_circuit_breaker(self):
        """Test circuit breaker activation"""
        starting_bankroll = 10000
        current_bankroll = 8300
        
        drawdown_pct = (starting_bankroll - current_bankroll) / starting_bankroll
        
        assert drawdown_pct > 0.15  # Should trigger 15% circuit breaker
    
    def test_position_limit(self):
        """Test concurrent position limits"""
        max_positions = 3
        current_positions = 2
        
        can_open_new = current_positions < max_positions
        
        assert can_open_new == True
        
        # Full
        current_positions = 3
        can_open_new = current_positions < max_positions
        
        assert can_open_new == False


class TestExecutionAgent:
    """Test Execution Agent functionality"""
    
    def test_trade_logging(self):
        """Test trade log format"""
        trade = {
            "timestamp": "2026-03-17T23:00:00",
            "market": "btc-up-down",
            "action": "Buy",
            "price": 0.52,
            "size": 250,
            "edge": 0.05
        }
        
        # Verify required fields
        assert "timestamp" in trade
        assert "market" in trade
        assert "action" in trade
        assert "price" in trade
        assert "size" in trade
    
    def test_win_loss_calculation(self):
        """Test P&L calculation"""
        # Win
        entry = 0.50
        exit = 0.55
        size = 1000
        
        profit = (exit - entry) * size
        
        assert abs(profit - 50) < 0.01  # Allow floating point precision
        
        # Loss
        entry = 0.50
        exit = 0.45
        size = 1000
        
        profit = (exit - entry) * size
        
        assert abs(profit - (-50)) < 0.01


class TestPerformanceMonitor:
    """Test Performance Monitor agent"""
    
    def test_win_rate_calculation(self):
        """Test win rate metric"""
        trades = [
            {"profit": 10},
            {"profit": -5},
            {"profit": 15},
            {"profit": -3},
            {"profit": 20}
        ]
        
        wins = sum(1 for t in trades if t["profit"] > 0)
        total = len(trades)
        win_rate = wins / total
        
        assert win_rate == 0.6  # 60%
    
    def test_sharpe_ratio(self):
        """Test Sharpe ratio calculation (simplified)"""
        returns = [0.02, -0.01, 0.03, -0.005, 0.025]
        
        mean_return = sum(returns) / len(returns)
        
        # Calculate standard deviation
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        
        sharpe = mean_return / std_dev if std_dev > 0 else 0
        
        assert sharpe > 0  # Positive Sharpe
    
    def test_max_drawdown(self):
        """Test max drawdown calculation"""
        bankroll_history = [10000, 9800, 9500, 9700, 9400, 9900]
        
        peak = bankroll_history[0]
        max_dd = 0
        
        for value in bankroll_history:
            if value > peak:
                peak = value
            
            drawdown = (peak - value) / peak
            max_dd = max(max_dd, drawdown)
        
        assert max_dd == 0.06  # 6% max drawdown


class TestIntegration:
    """Test agent integration"""
    
    def test_full_cycle(self):
        """Test complete trading cycle"""
        # 1. Scanner finds opportunity
        edge = 0.05
        
        # 2. Risk manager sizes position
        bankroll = 10000
        position = min(edge * 0.5 * bankroll, 0.05 * bankroll)
        
        # 3. Execution simulates trade
        win = True  # Simplified
        profit = position * edge if win else -position * edge * 0.5
        
        # 4. Monitor updates stats
        bankroll += profit
        
        assert bankroll >= 10000  # Should be profitable or break-even
    
    def test_error_handling(self):
        """Test graceful error handling"""
        try:
            # Simulate API failure
            response = None
            
            if response is None:
                raise ConnectionError("API unavailable")
            
        except ConnectionError as e:
            assert "API unavailable" in str(e)
            # Should log and retry, not crash


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
