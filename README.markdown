# Multi-Agent Text Processing System

This project is a Streamlit application that leverages the OpenAI API to perform various text processing tasks through a multi-agent system. Each agent specializes in a different aspect of text analysis and enhancement, such as summarization, tone adjustment, sentiment analysis, translation, style enhancement, and readability scoring.

## Setup Instructions

1. **Uncompress the Zip File**
   - Extract the contents of the zip file to a directory of your choice.

2. **Navigate to the Project Directory**
   - Open a terminal and change to the project's root directory:
     ```
     cd path/to/multi_agent_text_processing
     ```

3. **Install Required Packages**
   - Run the following command to install the necessary dependencies:
     ```
     pip install -r requirements.txt
     ```

4. **Set Up Your API Key**
   - Obtain an OpenAI API key from [OpenAI](https://beta.openai.com/signup/).
   - Set the API key as an environment variable:
     - On macOS/Linux:
       ```
       export OPENAI_API_KEY='your_api_key_here'
       ```
     - On Windows:
       ```
       set OPENAI_API_KEY=your_api_key_here
       ```

5. **Start the Streamlit App**
   - Launch the application with:
     ```
     streamlit run streamlit_app.py
     ```
   - Open your web browser and go to `http://localhost:8501` to interact with the app.

## Sample Input Data

To get started, you can copy and paste the following sample text inputs into the application’s input forms. Note that processing times may vary depending on the task and API response.

- **For Summarization:**
  ```
  Artificial intelligence is transforming industries by automating tasks and providing insights from data. From healthcare to finance, AI is enhancing efficiency and decision-making.
  ```

- **For Tone Adjustment:**
  ```
  The report was not good. It missed key points and lacked clarity.
  ```

- **For Sentiment Analysis:**
  ```
  I love the new features in this app! They make my work so much easier.
  ```

- **For Translation (to Spanish):**
  ```
  Hello, how are you today?
  ```

- **For Style Enhancement:**
  ```
  The data shows a increase in sales. This is good for the company.
  ```

- **For Readability Scoring:**
  ```
  Utilizing obfuscatory lexemes in textual compositions can obfuscate the intended message, thereby diminishing the communicative efficacy.
  ```

Feel free to experiment with your own text inputs to explore the full range of features offered by the multi-agent system.

## Troubleshooting

- **API Key Issues:** Ensure your OpenAI API key is correctly set and has the necessary permissions.
- **Dependency Errors:** Verify that all packages listed in `requirements.txt` are installed. You can check with `pip list`.
- **Streamlit Not Running:** Make sure you are in the correct directory and that `streamlit_app.py` exists.

For further assistance, refer to the [Streamlit documentation](https://docs.streamlit.io/) or the [OpenAI API documentation](https://beta.openai.com/docs/).