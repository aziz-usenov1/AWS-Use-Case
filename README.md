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

The goal of this use case is to compare the news delivery tone of [TechCrunch](https://techcrunch.com/) and [TechRadar](https://global.techradar.com/de-de) on the similar topic. The former website is one of the popular journal about the tech StartApp and all novelties in tech industry. The latter one is famous for being best advisor for providing news about the tech products like Macbook and it provides news in Deutsch. 

This use case focuses on Apple devices for the tone comparison. The reason for this is that, despite being the top leader, Apple has been increasingly challenged by competitors who are launching cutting-edge tech products to outpace Apple. One can get up-to-date information about the Apple products from the official website but one may not find information being delivered with negative tone. So, all news will be positive from the official website. That is why the focus on third party news providers such as **TechCrunch** and **TechRadar** to reflect on true information on Apple products. So, running a sentiment analysis on the news on both sources related to Apple can show the differences in news delivery. Without any delays, let's get started 🔍!

Since the focus is on the implementation of _AWS_ services in analyzing the news content of two sources, I decided to concentrate on 2 news per source. This ensures that no huge cost is charged for processing large content. I believe the logic underlined in this use-case can be applied to any similar use-cases or projects with the similar agenda. So, the procedures include:

- **Web Scrape**: to extract relevant news
- **Translate**: from Deutsch to English using _AWS Translate_
- Run a **sentiment** analysis using _AWS Comprehend_
- Estimate **cost** for used service

<hr>

## Web Scraping

This is not an usual practice but I decided to scrape each piece of news separately to get individual **.txt** files. This way I can use Amazon S3 as my main storage instead of using the VS code environment. I could also process the data directly from the website and apply necessary manipulations but this time the focus on practicing cloud storage and manage data easily. Overall, In total, I scraped _4 news_ and generated 4 .txt files with the news content. These files contain text in the original language, i.e. Enlgish and Deutsch and ready for further analysis.

**Extracting news content**

The following code snippet is used for scraping both website adjusted for the url and selector:

1. Connecting to a website: 
```
print("🌐 Attempting to access webpage without headers...")

url = "https://techcrunch.com/2024/12/15/apple-reportedly-developing-foldable-iphone-and-ipad/"

try:
    response = requests.get(url)
    print(f"📡 Response status code: {response.status_code}")

    if response.status_code == 403:
        print("❌ Access forbidden! This demonstrates why we need proper headers.")
        print("ℹ️  Websites often block requests without proper User-Agent headers")
        print("   to prevent automated scraping.")
except Exception as e:
    print(f"❌ Error: {str(e)}")

```

2. Extracting news content:

```
try:
    # Parse the HTML
    webpage = BeautifulSoup(response.content, "html.parser")

    # Extract title
    title = webpage.title.string.strip()
    print("\n📑 Page Title:")
    print("-" * 40)
    print(title)
    print("-" * 40)

    # Extract paragraphs
    print("\n📝 Article Content:")
    print("-" * 40)
    description_html = webpage.select(".wp-block-post-content-is-layout-constrained")  # <----------------- !!! Our selector: subject to adjustment !!!
    texts = [
    re.sub(r'\s+', ' ', text.get_text().strip())  # Collapse multiple spaces/newlines into one
    for text in description_html
    if text.get_text().strip()  # Ignore empty strings
    ]
    text = "\n".join(texts)
    print(text)
    print("-" * 40)

    print("\n✅ Content extracted successfully")
except Exception as e:
    print(f"❌ Error parsing content: {str(e)}")
```

**AWS configuration in codespace**

As I mentioned earlier Amazon S3 will be my main storage, so I need to configure with AWS to able to use its services programmatically. The configuration can be done with the following code:

```
aws configure
```

and checking for actual configuration:
```
code ~/.aws/config
code ~/.aws/credentials
```

✅ Configuration is done and ready to use AWS services programmatically. 

As a next step, I imported boto3 library, which is main library used to get access for AWS services programmatically. Since I always use VS code environment for coding, I really wanted to ensure that I have the similar setup with AWS and the solution is AWS S3. It is really nice to store all your files securely on the cloud for easy access. This was really a nice practice for uploading and calling documents directly from my bucket programmatically rather than doing on the website itself playing with UI. So, the following was used to set up boto3 client for S3 and uploading documents:

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

Here lets check for the available buckets:

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

I know that I have created one bucket several days ago and I ensured that it is still there and active:

```
{ 'Buckets': [{ 'CreationDate': datetime.datetime(2024, 11, 27, 14, 49, 54, tzinfo=tzlocal()),
                 'Name': 'ceu-aziz-de2'}]
}

📦 Your current S3 buckets:
- ceu-aziz-de2
```

Now, it is time upload files to my bucket in S3:

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

✅ Files were successfully uploaded to S3 bucket and ready to go for the next step.

<hr>

## AWS Translate

The TechRadar provides information in Deutsch and it needs to be translated into common language, in my case it is English because TechCrunch is English based website. So, 2 **.txt** files from TechRadar need to be translated to English and it is done by the following:

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

Once again, the translated **.txt** file also needs to be uploaded to S3 bucket to able to call them afterwards for sentiment analysis. It is done as follows:

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

✅ Everything is done and processed for sentiment analysis. Let's start the analyzing the tone 🔎.

## Amazon Comprehend

At this step, it is neeeded to call another AWS service 'AWS Comprehend' which is used for many purposes like keyword detection, lanugage detection, sentiment analysis, and more. I needed sentiment analysis to check for tone. I used the following code to run the sentiment analysis for all English based **.txt** files:

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
✅ The sentiment analysis is done. The result is demonstrated in the following bar chart:
![sentiment_summary](https://github.com/user-attachments/assets/e916a83f-912f-4d85-ad29-686bfbe325a1)

In general, the news have a neutral tone coupled with a bit positive one. The first three news are, in fact, about the neutral discussing about Apple products. However, it turned out to be that TechRadar delivered the last news with negative tone. It is actually true because the content is about abolishing 12 inch Macbook from the sale which is negative content. AWS Comprehend did well in providing insights into tones of the news. 

The overall analysis was simple but efficient and reliable in identifying the correct tones of the news. The product architecture for this use case can be found here:

![Architecture](https://github.com/user-attachments/assets/a072c4b9-10fd-47a6-8bf7-22cb25a18081)

## Cost Estimation

<img width="361" alt="image" src="https://github.com/user-attachments/assets/51744b1f-473a-411a-8ba4-2553f9a7241c" />

