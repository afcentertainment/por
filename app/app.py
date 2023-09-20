from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

# Define the path to your CSV file
csv_file_path = "videos.csv" # Update with the actual path to your CSV file
 # Update with the actual path to your CSV file

# Number of items to display per page
items_per_page = 30

@app.route('/')
def index():
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to a list of dictionaries (one for each row)
    videos = df.to_dict(orient='records')

    # Get the current page number from the query parameter
    page = request.args.get('page', default=1, type=int)

    # Calculate the start and end indices for the current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Get the videos for the current page
    videos_on_page = videos[start_index:end_index]
    videos_len=len(videos)
    return render_template('index.html',videos_len=videos_len, videos=videos_on_page, page=page,items_per_page=items_per_page)

@app.route('/play/<int:video_id>')
def play(video_id):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Get the selected video by video_id
    selected_video = df.iloc[video_id]
    url=selected_video["vdo"]
    r = requests.get(url)
    html = r.content
    print(url)
    soup = BeautifulSoup(html, 'html.parser')
    arr = []
    src_value="https://chiggywiggy.com/media/videos/mp4/14239_720p.mp4"
    source_tag240 = soup.find('source', type="video/mp4", title="240p")
    source_tag360 = soup.find('source', type="video/mp4", title="360p")
    source_tag480 = soup.find('source', type="video/mp4", title="480p")
    source_tag720 = soup.find('source', type="video/mp4", title="720p")
    source_tag1080 = soup.find('source', type="video/mp4", title="1080p")
    source_tag1440 = soup.find('source', type="video/mp4", title="1440p")
    source_tag2160 = soup.find('source', type="video/mp4", title="2160p")
    source_tag4320 = soup.find('source', type="video/mp4", title="4320p")

    # Assign src_value based on the best available resolution
    if source_tag4320:
        src_value = source_tag4320['src']
        print("Best Available Resolution: 4320p")
    elif source_tag2160:
        src_value = source_tag2160['src']
        print("Best Available Resolution: 2160p")
    elif source_tag1440:
        src_value = source_tag1440['src']
        print("Best Available Resolution: 1440p")
    elif source_tag1080:
        src_value = source_tag1080['src']
        print("Best Available Resolution: 1080p")
    elif source_tag720:
        src_value = source_tag720['src']
        print("Best Available Resolution: 720p")
    elif source_tag480:
        src_value = source_tag480['src']
        print("Best Available Resolution: 480p")
    elif source_tag360:
        src_value = source_tag360['src']
        print("Best Available Resolution: 360p")
    elif source_tag240:
        src_value = source_tag240['src']
        print("Best Available Resolution: 240p")
    else:
        print("No video source element found for any resolution.")

    selected_video["dwn"]=src_value
    return render_template('play.html', selected_video=selected_video)

if __name__ == '__main__':
    app.run(debug=True)
