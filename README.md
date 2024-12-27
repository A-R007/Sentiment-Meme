# Sentiment Analysis and Meme Generator Flask Application

This Flask application performs sentiment analysis on a given text input and generates a corresponding meme based on the sentiment. It integrates with Groq's AI API for sentiment analysis and Imgflip's API for meme generation. The app is designed to analyze emotions like **Happy**, **Sad**, **Angry**, **Disgusted**, **Surprised**, **Fearful**, or **Neutral** and generate a related meme dynamically.

## Features

- **Sentiment Analysis**: Analyze the sentiment of a given text using Groq's AI API, which classifies the text into different emotional categories.
- **Meme Generation**: Based on the analyzed sentiment, generate a meme with a relevant template from Imgflip's API.
- **Environment Configurations**: The application loads environment variables from a `.env` file for sensitive information like API keys.
- **Error Handling**: The application handles exceptions gracefully and falls back to default values when necessary.
  
## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone <repo-link>
cd <your-folder>
```

### 2. Set Up a Virtual Environment

It is recommended to use a virtual environment for managing dependencies.

For **Linux/macOS**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For **Windows**:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages using `pip`.

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

Create a `.env` file in the root directory and add the following configuration:

```env
GROQ_API_KEY=your_groq_api_key
IMGFLIP_USERNAME=your_imgflip_username
IMGFLIP_PASSWORD=your_imgflip_password
```

Replace the placeholders with your actual API keys.

### 5. Run the Flask Application

You can run the Flask application locally by executing the following command:

```bash
python app.py
```

The application will run on port `10000` by default. You can visit it by navigating to `http://127.0.0.1:10000` in your browser.

### 6. Deploy to a Cloud Provider (Optional)

For production, deploy the application to a cloud service like **Heroku**, **Render**, or **AWS**.

---

## How It Works

### 1. **Sentiment Analysis**
The `analyze_sentiment` function sends a prompt to Groq's AI API. It asks Groq to analyze the sentiment of the input text and classify it into one of the following emotions:

- **Happy**
- **Sad**
- **Angry**
- **Disgusted**
- **Surprised**
- **Fearful**
- **Neutral**

The result is returned to the Flask app.

### 2. **Post-Processing Sentiment**
The sentiment received from the Groq API is further refined by the `post_process_sentiment` function. This function checks the presence of specific keywords in the text to adjust the sentiment if needed. For example:

- If the text contains words like "gross", "ew", or "disgusting", the sentiment will be classified as **Disgusted**.
- If words like "amazing", "happy", or "joy" are found, it will classify as **Happy**.

### 3. **Meme Generation**
After determining the sentiment, the app generates a meme using the Imgflip API. It selects a relevant meme template based on the sentiment and uses captions that reflect the emotional tone.

- **Happy**: Uses cheerful meme templates like "Success Kid" and "Doge".
- **Sad**: Selects sad memes like "Crying Jordan".
- **Angry**: Uses memes like "Drake" or "Gru".
- **Disgusted**: Chooses disgusted face templates.
- **Surprised**: Uses memes like "Pikachu Surprise".
- **Fearful**: Selects scared memes.
- **Neutral**: Uses neutral memes like "Meh".

### 4. **API Endpoints**

#### **POST /analyze**
- **Description**: Analyzes the sentiment of the provided text and generates a corresponding meme.
- **Request Body**:
  ```json
  {
    "text": "I am so happy today!"
  }
  ```
- **Response**:
  ```json
  {
    "sentiment": "Happy",
    "meme_url": "https://i.imgflip.com/your_meme.jpg"
  }
  ```

---

## Environment Variables

The application requires the following environment variables:

- `GROQ_API_KEY`: Your API key from Groq to perform sentiment analysis.
- `IMGFLIP_USERNAME`: Your Imgflip username for meme generation.
- `IMGFLIP_PASSWORD`: Your Imgflip password for meme generation.

---

## Dependencies

This project requires the following Python libraries:

- **Flask**: Web framework for building the app.
- **requests**: HTTP library to make requests to the Imgflip API.
- **python-dotenv**: For loading environment variables from `.env` file.
- **groq**: Groq client to interact with Groq's AI API.

These dependencies are listed in the `requirements.txt` file.

---

## Logging

The application uses Python's `logging` library to log errors, especially for API calls to Groq and Imgflip. You can adjust the log level as needed during development.

---

## Error Handling

The application ensures that if there's an error with the Groq or Imgflip APIs, a fallback default behavior is applied:

- If sentiment analysis fails, the default sentiment is **Neutral**.
- If meme generation fails, a default meme is returned.

---

### Contributions

Feel free to contribute to this project by submitting a pull request or opening an issue if you encounter any bugs or have suggestions for improvements.
