# %%
# Import required libraries and set up our environment
import pprint
import boto3
import pandas as pd
import matplotlib.pyplot as plt

print("📚 Setting up the environment...")

# Initialize pretty printer for better output formatting
pp = pprint.PrettyPrinter(indent=2)

# Create Comprehend client
comprehend = boto3.client(service_name="comprehend", region_name="eu-west-1")

print("✅ Environment setup complete!")
print(f"🌍 Using AWS region: {comprehend.meta.region_name}")


# %%
# Generating a plot out of sentiment scores
df = pd.DataFrame(sentiment_results)
print("\n📊 Sentiment Analysis Results:")
print(df)

print("\n📊 Generating sentiment score graph...")
plt.figure(figsize=(10, 6))
bar_width = 0.2
x = range(len(df))

# Plot bars for each sentiment category
plt.bar(x, df["Positive"], width=bar_width, label="Positive")
plt.bar([p + bar_width for p in x], df["Negative"], width=bar_width, label="Negative")
plt.bar([p + 2 * bar_width for p in x], df["Neutral"], width=bar_width, label="Neutral")
plt.bar([p + 3 * bar_width for p in x], df["Mixed"], width=bar_width, label="Mixed")

plt.xticks([p + 1.5 * bar_width for p in x], df["File"], rotation=45, ha="right")
plt.xlabel("Files")
plt.ylabel("Sentiment Scores")
plt.title("Sentiment Analysis Scores for Each File")
plt.legend()

plt.tight_layout()
plt.show()
