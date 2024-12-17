<a id="readme-top"></a>

<div align="center">
  
# Homework 3
## Comparing Delivery Tone of News from **TechCrunch** and **TechRadar**
<img src="https://github.com/user-attachments/assets/32bb48b6-5c82-48aa-9e7c-f5a427ec3e19" alt="Linkedin" width="500" height="220" align="center">

Source: [Rödl &amp; Partner](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.roedl.cz%2Fde%2Fmedien%2Fnewsletter%2Fnews%2F&psig=AOvVaw3cbNLj4bC8XJPM5E734P1G&ust=1734550175252000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCODNupTFr4oDFQAAAAAdAAAAABAE)

<details open>
  <summary>Table of Contents</summary>
  <div align="center">
    <p></p><a href="#about-the-project">About The Use Case</a></p>
    <p></p><a href="#web-scraping">Web Scraping</a></p>
    <p></p><a href="#aws-translate">AWS Translate</a></p>
    <p></p><a href="#aws-comprehend">AWS Comprehend</a></p>
    <p></p><a href="#cost-estimation">Cost Estimation</a></p>
    <p></p><a href="#summary">Summary</a></p>
  </div>
</details>
</div>

<hr> 

## About the Project

The goal of this use case is to compare the news delivery tone of [TechCrunch](https://techcrunch.com/) and [TechRadar](https://global.techradar.com/de-de) on the similar topic. The former website is one of the popular journal about the tech StartApp and all novelties in tech industry. The latter one is famous for being best advisor for providing news about the tech products like Macbook. 

This use case focuses on Apple devices for the tone comparison. The reason for this is that, despite being the top leader, Apple has been increasingly challenged by competitors who are launching cutting-edge tech products to outpace Apple. One can get up-to-date information about the Apple products from the official website but one may not find information being delivered with negative tone. So, all news will be positive from the official website. That is why the focus on third party news providers such as **TechCrunch** and **TechRadar** to reflect on true information on Apple products. So, running a sentiment analysis on the news on both sources related to Apple can show the differences in news delivery. Without any delays, let's get started 🔍!

```
import pprint
import boto3

print("📚 Setting up the environment...")
# %%
# Initialize pretty printer for better output formatting
pp = pprint.PrettyPrinter(indent=2)

# Create S3 client using default credentials from AWS CLI
# boto3 will automatically use credentials from ~/.aws/credentials
s3 = boto3.client(
    "s3",
    region_name="eu-west-1",  # Ireland region
)

print("✅ Environment setup complete!")
print(f"🌍 Using AWS region: {s3.meta.region_name}")
```

```
# Let's first check what buckets already exist in your AWS account
# This helps us understand what resources we're starting with
print("📋 Listing all S3 buckets in your account...")
response = s3.list_buckets()

print("\n📦 Raw response from AWS:")
pp.pprint(response)

print("\n📦 Your current S3 buckets:")
if response["Buckets"]:
    for bucket in response["Buckets"]:
        print(f"- {bucket['Name']}")
else:
    print("No buckets found in your account")

print(f"\n✅ Successfully retrieved {len(response['Buckets'])} buckets")
```
```
{ 'Buckets': [{ 'CreationDate': datetime.datetime(2024, 11, 27, 14, 49, 54, tzinfo=tzlocal()),
                 'Name': 'ceu-aziz-de2'}]
}

📦 Your current S3 buckets:
- ceu-aziz-de2
```

```
files = [
    "news_1_crunch.txt",
    "news_2_crunch.txt",
    "news_3_radar.txt",
    "news_4_radar.txt",
]

bucket_name = "ceu-aziz-de2"

print(f"⬆️  Uploading {len(files)} files to bucket: {bucket_name}")

try:
    for file in files:
        print(f"Uploading {file}...")
        s3.upload_file(file, bucket_name, file)
        print(f"✅ {file} uploaded successfully!")

    # Verify the upload by listing objects in the bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)
    print("\n📦 Current bucket contents:")
    for obj in objects.get("Contents", []):
        print(f"- {obj['Key']} ({obj['Size']} bytes)")

except Exception as e:
    print(f"❌ Error uploading files: {str(e)}")
```

```
files_translateed = [
    "news_3_radar_translated.txt",
    "news_4_radar_translated.txt",
]

bucket_name = "ceu-aziz-de2"

print(f"⬆️  Uploading {len(files)} files to bucket: {bucket_name}")

try:
    for file in files_translateed:
        print(f"Uploading {file}...")
        s3.upload_file(file, bucket_name, file)
        print(f"✅ {file} uploaded successfully!")

    # Verify the upload by listing objects in the bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)
    print("\n📦 Current bucket contents:")
    for obj in objects.get("Contents", []):
        print(f"- {obj['Key']} ({obj['Size']} bytes)")

except Exception as e:
    print(f"❌ Error uploading files: {str(e)}")

```

<hr>

```
# %%
pp = PrettyPrinter(indent=2)
translate = boto3.client("translate")

# %%
print("🔄 Translating longer text to English...")

bucket_name = "ceu-aziz-de2"
files = [
    {"file_key": "news_3_radar.txt", "output_file": "news_3_radar_translated.txt"},
    {"file_key": "news_4_radar.txt", "output_file": "news_4_radar_translated.txt"}
]

for file in files:
    file_key = file["file_key"]
    output_file = file["output_file"]

    try:
        print("\n📥 Fetching file from S3...")
        response_s3 = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response_s3['Body'].read().decode('utf-8')

        response = translate.translate_text(Text=file_content, SourceLanguageCode="de", TargetLanguageCode="en")

        print("\n📝 Translation details:")
        print("Original text (Deutsch):")
        print("-" * 40)
        print(file_content[:500])
        print("-" * 40)
        print("\nDetected language:", response["SourceLanguageCode"])
        print("\nTranslated text (English):")
        print("-" * 40)
        print(response["TranslatedText"])
        print("-" * 40)

        # Saving translated text to file
        print(f"💾 Saving translated text to '{output_file}'...")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(response["TranslatedText"])

        print(f"✅ Translation for '{file_key}' completed successfully!")

    except Exception as e:
        print(f"❌ Error during translation: {str(e)}")
```


```
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
```
![Architecture](https://github.com/user-attachments/assets/a072c4b9-10fd-47a6-8bf7-22cb25a18081)

![sentiment_summary](https://github.com/user-attachments/assets/e916a83f-912f-4d85-ad29-686bfbe325a1)

<img width="361" alt="image" src="https://github.com/user-attachments/assets/51744b1f-473a-411a-8ba4-2553f9a7241c" />

