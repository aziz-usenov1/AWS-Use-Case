# %%
# Import required libraries and set up our environment
# We'll use these throughout the tutorial to interact with AWS S3
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

# %%
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

# %%
print(f"⬆️  Uploading file to bucket: ceu-aziz-de2")

try:
    s3.upload_file("news_1_crunch.txt", "ceu-aziz-de2", "news_1_crunch.txt")
    print("✅ Upload successful!")

    # Verify the upload by listing objects in the bucket
    objects = s3.list_objects_v2(Bucket="ceu-aziz-de2")
    print("\n📦 Current bucket contents:")
    for obj in objects.get("Contents", []):
        print(f"- {obj['Key']} ({obj['Size']} bytes)")
except Exception as e:
    print(f"❌ Error uploading file: {str(e)}")

# %% 
# Uploading origial files to S3

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

# %%
# Uploading translated files

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
