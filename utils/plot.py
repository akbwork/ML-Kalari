import matplotlib.pyplot as plt

users = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
latency = [0.31, 0.30, 0.45, 0.77, 1.44, 2.74, 4.66, 7.79, 13.57, 24.77, 50.41]

fig, ax = plt.subplots(figsize=(10, 6.5))

x = range(len(users))
ax.plot(x, latency, marker="o", markersize=8, linewidth=2.5, color="#1a73e8")

# Value labels above each point
for xi, yi in zip(x, latency):
    ax.annotate(f"{yi:.2f}s", (xi, yi), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=9)

ax.set_xticks(list(x))
ax.set_xticklabels(users)
ax.set_ylim(-2, max(latency) * 1.1)      # auto-scales to the data
ax.set_xlim(-0.5, len(users) - 0.5)

ax.set_title("Average Latency vs Concurrent Users", fontsize=16, pad=15)
ax.set_xlabel("Concurrent Users", fontsize=13, labelpad=10)
ax.set_ylabel("Average Latency (seconds)", fontsize=13, labelpad=10)

ax.grid(True, color="#e3e8f0", linewidth=0.8)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("latency_vs_users.png", dpi=150)
plt.show()