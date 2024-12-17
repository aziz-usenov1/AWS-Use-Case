# %%
# Import required libraries and set up our environment
from pprint import PrettyPrinter

import boto3

print("📚 Setting up the environment...")
pp = PrettyPrinter(indent=2)
translate = boto3.client("translate")
print("✅ Environment setup complete!")
print(f"🌍 Using AWS region: {translate.meta.region_name}")

# %%
print("🔄 Translating longer text to English...")

bucket_name = "ceu-aziz-de2"
files = [
    {"file_key": "news_3_radar.txt", "output_file": "news_3_radar_translated.txt"},
    {"file_key": "news_4_radar.txt", "output_file": "news_4_radar_translated.txt"}
]

# Translation process
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
