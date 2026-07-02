# XAUUSD Gold Confluence Signals — User Guide

A TradingView indicator (Pine Script v5) that prints **BUY / SELL** signals on gold
with an entry price, ATR-based stop loss, and two take-profit targets, plus
real-time alerts. Signals are evaluated on confirmed bar closes only, so they
**never repaint** — what you see in history is what you would have gotten live.

## How it works

A signal only fires when all of these line up:

| # | Filter | What it checks |
|---|--------|----------------|
| 1 | Chart trend | Fast EMA (21) above/below Slow EMA (55) |
| 2 | Higher-timeframe trend | Same EMA trend on the 4H (configurable), using confirmed bars only |
| 3 | Pullback | Price touched the fast EMA within the last 8 bars — you enter on retracements, not chases |
| 4 | Momentum | RSI (14) crossing back through 50 in the trend direction |
| 5 | Candle confirmation | The signal bar closes in the trade direction |
| 6 | Session | Inside London (07:00–16:00 UTC) or New York (12:00–21:00 UTC) — gold's high-liquidity hours |
| 7 | Cooldown | At least 10 bars since the last signal, to avoid clusters |

Every signal prints a label with **Entry / SL / TP1 / TP2**. The stop is
1.5 × ATR(14); TP1 is 1R and TP2 is 2R by default. A dashboard in the top-right
shows current trend, HTF trend, RSI, and session status at a glance.

## Installation

1. Open TradingView and load an **XAUUSD** chart (OANDA:XAUUSD, FOREXCOM:XAUUSD, etc.).
2. Open the **Pine Editor** (bottom panel) → delete the boilerplate.
3. Paste the full contents of `xauusd_gold_confluence.pine`.
4. Click **Add to chart**, then **Save**.

## Setting up real-time alerts

1. Click the **⏰ Alert** button on the chart.
2. Condition: **XAUUSD Gold Confluence Signals** → **Any alert() function call**.
3. Expiration: open-ended; delivery: push notification / email / webhook as you prefer.

This single alert covers both buys and sells, and the message includes the
entry, stop, and both targets. Because signals confirm on bar close, the alert
arrives the moment the signal bar closes — that close price is your entry zone.

## Recommended usage

- **Timeframes:** 15m or 1H for signals, with the HTF filter on 4H (default).
  On 15m charts you'll get a few signals per week; on 5m more signals but more noise.
- **Risk per trade:** 1% of account or less. Position size = (account × 1%) ÷ (entry − stop distance in $).
- **Trade management:** take half off at TP1 and move the stop to breakeven; let the rest run to TP2.
- **Skip signals** right before major USD news (NFP, CPI, FOMC) — gold spikes through stops during releases.

## Honest expectations — read this

No indicator has a 90%+ win rate, and none catches every move. Anyone claiming
that is selling something. This system is built the way profitable systems
actually work:

- **Expect roughly a 40–60% win rate** depending on market regime. The edge
  comes from the reward:risk — winners at 1R–2R vs. losers at 1R means you can
  be profitable well below a 90% hit rate.
- **It will miss moves by design.** The session filter, HTF filter, and pullback
  requirement deliberately skip low-quality setups. Missing a trade costs
  nothing; taking a bad one costs money.
- **It will underperform in choppy, range-bound markets** — that's true of
  every trend-following system. The HTF filter and cooldown reduce, but don't
  eliminate, whipsaws.
- **Backtest and demo-trade it first.** Run it on at least 6–12 months of
  history and a few weeks on a demo account before risking real money. Tune the
  EMA lengths and ATR multiplier to your timeframe if needed.
- Nothing here is financial advice; you are responsible for your own risk.

## Key settings to experiment with

| Setting | Default | Effect of changing it |
|---------|---------|----------------------|
| Fast/Slow EMA | 21 / 55 | Shorter = more signals, more noise |
| Higher timeframe | 240 (4H) | Higher = fewer, stronger signals |
| Stop loss (× ATR) | 1.5 | Wider = fewer stop-outs, larger risk per trade |
| Pullback lookback | 8 bars | Larger = more signals allowed after a pullback |
| Min bars between signals | 10 | Lower = more frequent signals |
| Session filter | On | Turn off to also trade the Asian session (thinner, choppier for gold) |
