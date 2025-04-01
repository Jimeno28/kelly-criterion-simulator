import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Function to compute Kelly Criterion
def kelly_binary(p, b):
    return (p * b - (1 - p)) / b

# Simulation function
def simulate_growth(capital, fraction, win_prob, odds, trials, stop_loss):
    capital_history = [capital]
    for _ in range(trials):
        bet_size = fraction * capital
        if np.random.rand() < win_prob:
            capital += bet_size * (odds - 1)
        else:
            capital -= bet_size * stop_loss
        capital_history.append(capital)
    return capital_history, capital

# Streamlit UI
st.title("📈 Kelly Criterion Growth Simulation")

# Sidebar inputs
st.sidebar.header("Simulation Parameters")
p_win = st.sidebar.slider("Winning Probability (%)", 0, 100, 68, 1) / 100
odds = st.sidebar.slider("Odds (Payout Ratio)", 1.1, 3.0, 1.3, 0.1)
trials = st.sidebar.slider("Number of Bets", 50, 500, 180, 10)
initial_capital = st.sidebar.number_input("Starting Capital ($)", 1000, 100000, 5000, 100)
stop_loss = st.sidebar.slider("Stop Loss (% of Bet)", 0.1, 1.0, 0.2, 0.05)

# Compute Kelly fraction
kelly_fraction = kelly_binary(p_win, odds)
fractions = [0.5 * kelly_fraction]

# Plot results
fig, ax = plt.subplots(figsize=(10, 6))
legend_labels = []

for f in fractions:
    history, final_capital = simulate_growth(initial_capital, f, p_win, odds, trials, stop_loss)
    ax.plot(history, label=f"{f:.2f}x Kelly")
    
    # Calculate return metrics
    total_return = final_capital - initial_capital
    percent_return = (total_return / initial_capital) * 100
    legend_labels.append(f"{(f*100):.2f}% Bet Size | Start: ${initial_capital:,.0f} | End: ${final_capital:,.0f} ({percent_return:.2f}%)")

# Format plot
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
ax.set_xlabel("Number of Bets")
ax.set_ylabel("Capital Growth")
ax.set_title("Kelly Criterion Growth Simulation")
ax.legend(legend_labels)
ax.grid()

# Display plot in Streamlit
st.pyplot(fig)

# Show final results
st.write(f"**Optimal Kelly Fraction:** {(kelly_fraction * 0.5) * 100:.2f}%")
st.write(f"**Final Capital:** ${final_capital:,.2f}")
st.write(f"**Total Return:** ${total_return:,.2f} ({percent_return:.2f}%)")
