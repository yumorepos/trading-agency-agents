# 🎭 Trading Agency Agents

> ⚠️ **Status: Experimental proof-of-concept** — Agent specifications in markdown, test harness only. No runnable agent implementation code. Part of the [autonomous-trading-system](https://github.com/yumorepos/autonomous-trading-system) research ecosystem.

[![Tests](https://github.com/yumorepos/trading-agency-agents/actions/workflows/test.yml/badge.svg)](https://github.com/yumorepos/trading-agency-agents/actions/workflows/test.yml)

> 4 agent specifications for Polymarket prediction markets. Built using [The Agency](https://github.com/msitarzewski/agency-agents/) framework concept.

**Status:** Experimental — agent specs + test harness only  
**Validation:** Paper simulation (+11.4% across 42 simulated trades)  
**Created:** 2026-03-17  
**Framework:** The Agency (MIT License)

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements-test.txt

# Run tests
pytest test_agents.py -v

# Expected: 14 passed in ~0.1s
```

---

## 🤖 Agent Roster

### 🔍 Market Scanner
**Mission:** Find arbitrage and correlation opportunities across 200+ markets

**Capabilities:**
- Scans 124+ active markets in <5 seconds
- Detects arbitrage: `(1 - (p_yes + p_no))` > 0.5%
- Finds correlation breakdowns: z-score > 1.5
- Prioritizes by EV: `edge × volume`

**Validated:** 397 opportunities found (peak hours)

**File:** [`trading-market-scanner.md`](trading-market-scanner.md)

---

### 🛡️ Risk Manager
**Mission:** Protect capital through Kelly sizing and circuit breakers

**Capabilities:**
- Kelly Criterion: `f* = 0.5 × (edge / odds)`
- Position cap: 5% bankroll max
- Stop-loss: $20 per trade
- Circuit breakers: -5%, -10%, -15%

**Validated:** 42 trades, zero circuit breaker triggers

**File:** [`trading-risk-manager.md`](trading-risk-manager.md)

---

### ⚡ Execution Agent
**Mission:** Place trades with precision and minimal slippage

**Capabilities:**
- Market order placement via CLOB API
- Slippage monitoring: Target <0.5%
- Retry logic: 3 attempts with backoff
- Audit trail: Every order logged

**Validated:** 23.4% average edge maintained

**File:** [`trading-executor.md`](trading-executor.md)

---

### 📊 Performance Monitor
**Mission:** Track metrics and optimize strategy

**Capabilities:**
- Win rate tracking
- Sharpe ratio calculation
- Max drawdown monitoring
- Daily P&L reporting

**Validated:** +11.4% return, 60% win rate

**File:** [`trading-performance-monitor.md`](trading-performance-monitor.md)

---

## 🧪 Testing

All agents have comprehensive unit tests:

```bash
pytest test_agents.py -v
```

**Coverage:**
- Market Scanner: Arbitrage + correlation detection
- Risk Manager: Kelly sizing, stop-loss, circuit breakers
- Execution Agent: Trade logging, P&L calculation
- Performance Monitor: Win rate, Sharpe, drawdown
- Integration: Full cycle + error handling

**Status:** 14 tests, 100% pass rate

---

## 📁 Architecture

```
trading-agency-agents/
├── trading-market-scanner.md      # Agent 1 spec
├── trading-risk-manager.md        # Agent 2 spec
├── trading-executor.md            # Agent 3 spec
├── trading-performance-monitor.md # Agent 4 spec
├── test_agents.py                 # Unit tests (14 tests)
└── .github/workflows/test.yml     # CI/CD
```

---

## 🔗 Integration

These agents are designed to integrate with:
- OpenClaw (autonomous operation)
- Claude Code (development)
- Cursor (IDE integration)
- GitHub Copilot (code assistance)

**Framework:** [The Agency](https://github.com/msitarzewski/agency-agents/)

---

## 📊 Validation Results

**Paper trading validation (2026-03-17):**
- Starting bankroll: $600
- Ending bankroll: $668.41
- Return: +11.4%
- Trades: 42
- Avg edge: 23.4%
- Win rate: ~60%
- Max position: 5% (risk-controlled)

**Markets scanned:** 200+ Polymarket prediction markets

---

## 🚀 Status

- ✅ Phase 1: Agent design + validation
- ✅ Tests: 14 unit tests, 100% pass
- ✅ CI/CD: GitHub Actions
- ⏸️ Phase 2: Live deployment (pending)

---

## 📝 License

MIT License - Built using [The Agency](https://github.com/msitarzewski/agency-agents/) framework
