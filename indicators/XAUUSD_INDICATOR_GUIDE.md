# XAUUSD Gold Confluence Signals — User Guide

A TradingView indicator (Pine Script v5) that prints **BUY / SELL** signals on gold
with an entry price, ATR-based stop loss, and two take-profit targets, plus
real-time alerts. Signals are evaluated on confirmed bar closes only, so they
**never repaint** — what you see in history is what you would have gotten live.

## How it works (v2)

**Bias** — all three must agree before any signal can fire:

| Filter | What it checks |
|--------|----------------|
| Chart trend | Fast EMA (21) above/below Slow EMA (55) |
| HTF bias | 1H close above/below the 1H EMA(50), confirmed bars only. This reacts within a few bars of a real trend turn — v1 used a 4H EMA cross, which lagged a full session and blocked entire intraday trends. |
| Chop guard | EMAs separated by at least 0.1 × ATR — no signals in flat chop |

**Entries** — two triggers per direction, so a sustained trend keeps producing
signals instead of relying on a one-time RSI crossover:

- **A. Pullback resumption** — price touched the fast EMA within the last 8
  bars and now closes back through it in the trend direction with RSI on side.
- **B. Continuation breakout** — close beyond the highest high / lowest low of
  the prior 10 bars with RSI momentum confirming.

**Guards** — both entry types are vetoed when the move is already exhausted:
no sells when RSI < 25 or price is stretched more than 3 × ATR below the slow
EMA (mirrored for buys), no signals outside London (07:00–16:00 UTC) / New York
(12:00–21:00 UTC), and a 6-bar cooldown between signals. These guards are what
stop the indicator from shorting V-bottoms after a capitulation drop.

Every signal prints a label with the entry type and **Entry / SL / TP1 / TP2**.
The stop is 1.5 × ATR(14); TP1 is 1R and TP2 is 2R by default. The dashboard
shows chart trend, HTF bias, which side signals are currently allowed on
(BUYS ONLY / SELLS ONLY / STAND ASIDE), RSI, and session status.

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

- **Timeframes:** 15m or 1H for signals, with the HTF bias on 1H (default) —
  use 4H bias only for 1H+ charts. On 15m expect several signals per week;
  on 5m more signals but more noise.
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
| Higher timeframe / HTF EMA | 60 (1H) / 50 | Higher TF or longer EMA = fewer, stronger signals but slower to flip after reversals |
| Breakout lookback | 10 bars | Larger = only stronger breakouts qualify as continuation entries |
| Max distance from slow EMA | 3.0 × ATR | Lower = stricter exhaustion guard, skips more late entries |
| Stop loss (× ATR) | 1.5 | Wider = fewer stop-outs, larger risk per trade |
| Pullback lookback | 8 bars | Larger = more signals allowed after a pullback |
| Min bars between signals | 6 | Lower = more frequent signals |
| Session filter | On | Turn off to also trade the Asian session (thinner, choppier for gold) |
