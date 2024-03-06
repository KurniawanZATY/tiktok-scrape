import json
from apify_client import ApifyClient

def scrape_tiktok_hashtags(hashtags, results_per_page):
    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_Sd42jiNxLabuE6fHCdQb1ki5OJfBxN3hRf56")

    # Prepare the Actor input
    run_input = {
        "hashtags": hashtags,
        "resultsPerPage": results_per_page,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

    # Fetch and return Actor results from the run's dataset (if there are any)
    scraped_data = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        scraped_data.append(item)

    return scraped_data

def scrape_trending_videos(region, limit, use_apify_proxy=True):
    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_vD3uDFCNjC8BBalQZs7Dpyw3l40iKr4oYuI2")

    # Prepare the Actor input for trending videos
    run_input = {
        "region": region,
        "limit": limit,
        "proxyConfiguration": {"useApifyProxy": use_apify_proxy},
    }

    # Run the Actor and wait for it to finish (replace with the correct actor ID)
    run = client.actor("4pk0g8nqBJorlmlx9").call(run_input=run_input)

    # Fetch and return Actor results from the run's dataset (if there are any)
    scraped_data = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        scraped_data.append(item)

    return scraped_data

def save_video_urls_to_file(file_name, video_urls):
    with open(file_name, 'w') as file:
        for url in video_urls:
            file.write(url + '\n')

def main():
    print("Choose an option:")
    print("1. Scrape TikTok data using hashtags")
    print("2. Scrape trending TikTok videos")

    option = input("Enter your choice (1 or 2): ")

    if option == "1":
        hashtags = input("Enter TikTok Hashtags (comma-separated): ")
        results_per_page = int(input("Results Per Page (1-100): "))

        if hashtags:
            print("Scraping...")
            hashtag_list = [hashtag.strip() for hashtag in hashtags.split(",")]
            scraped_data = scrape_tiktok_hashtags(hashtag_list, results_per_page)

            # Extracting the video URLs without additional parameters
            video_urls = [item.get('webVideoUrl').split('?')[0] for item in scraped_data]
            save_video_urls_to_file("hashtag.txt", video_urls)

            print(f"Video URLs saved to 'hashtag.txt'")
        else:
            print("Please enter TikTok hashtags.")

    elif option == "2":
        region = input("Enter region code (e.g., 'ID' for Indonesia): ")
        limit = int(input("Enter the limit for results: "))
        use_apify_proxy = input("Use proxy? (y/n): ").lower() == 'y'

        print("Scraping...")
        trending_data = scrape_trending_videos(region, limit, use_apify_proxy)

        # Extracting the share URLs from the trending data without additional parameters
        trending_video_urls = [item.get('share_url').split('?')[0] for item in trending_data if 'share_url' in item]
        save_video_urls_to_file("trending.txt", trending_video_urls)

        print(f"Trending Video URLs saved to 'trending.txt'")
    else:
        print("Invalid option. Please enter either '1' or '2'.")

if __name__ == "__main__":
    main()
