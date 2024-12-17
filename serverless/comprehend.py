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
bucket_name = "ceu-aziz-de2"
files = [
    {"file_key": "news_1_crunch.txt"},
    {"file_key": "news_2_crunch.txt"},
    {"file_key": "news_3_radar_translated.txt"},
    {"file_key": "news_4_radar_translated.txt"}
]

sentiment_results = []

# Sentiment Analysis for Each File
for file in files:
    file_key = file["file_key"]
    print(f"\n📥 Fetching file '{file_key}' from S3...")
    try:
        # Fetch file content
        response_s3 = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response_s3['Body'].read().decode('utf-8')

        # Perform sentiment analysis
        print("💬 Running sentiment analysis...")
        response = comprehend.detect_sentiment(Text=file_content, LanguageCode="en")

        # Display Results
        print("\n📝 Input text:")
        print("-" * 40)
        print(file_content[:500])  # Show first 500 characters
        print("-" * 40)

        print("\n💭 Sentiment analysis results:")
        scores = response["SentimentScore"]
        sentiment_results.append({
            "File": file_key,
            "Positive": scores["Positive"],
            "Negative": scores["Negative"],
            "Neutral": scores["Neutral"],
            "Mixed": scores["Mixed"]
        })

        print(f"✅ Sentiment analysis completed for '{file_key}'.")

    except Exception as e:
        print(f"❌ Error processing '{file_key}': {str(e)}")

print("\n✅ Sentiment analysis for all files completed!")

# %%
# Generating a plot out of sentiment scores
df = pd.DataFrame(sentiment_results)
print("\n📊 Sentiment Analysis Results:")
print(df)

print("\n📊 Generating sentiment score graph...")
plt.figure(figsize=(10, 6))
bar_width = 0.2
x = range(len(df))

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
plt.savefig("sentiment_summary.png")
plt.show()
