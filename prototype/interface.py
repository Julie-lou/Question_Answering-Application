import pandas as pd
import gradio as gr
from src.components.helper import answer_questions, apply_answer_questions


def question_answering_interface(context, question):
    # Call answer_questions function with both context and question
    answer = answer_questions(context, question)  
    return answer

def df_interface(df_input, context):
    try:
        # Read the CSV file from the Gradio file input
        dataframe = pd.read_csv(df_input.name, encoding='utf-8')

        # Print the columns for debugging
        print("DataFrame columns:", dataframe.columns.tolist())

        # Check if the necessary columns are present
        if 'Question' not in dataframe.columns or 'Detected_answer' not in dataframe.columns:
            return "CSV must contain 'Question' and 'Detected_Answer' columns."

        # Create a new DataFrame for output using the original data
        df_output = pd.DataFrame()
        df_output['Question'] = dataframe['Question']
        df_output['Detected_answer'] = dataframe['Detected_answer']  # Directly use the original answers

        # Return the DataFrame for display in Gradio
        return df_output
    except Exception as e:
        return f"Error processing the file: {str(e)}"

def specific_question_interface(df_input, user_question):
    try:
        # Read the CSV file to access questions
        dataframe = pd.read_csv(df_input.name, encoding='utf-8')

        # Check if the 'Question' and 'Detected_Answer' columns are present
        if 'Question' not in dataframe.columns or 'Detected_answer' not in dataframe.columns:
            return "CSV must contain 'Question' and 'Detected_Answer' columns."

        # Check if the user question is in the DataFrame
        if user_question not in dataframe['Question'].values:
            return "Question not found in the uploaded CSV."

        # Get the corresponding detected answer for the user question
        detected_answer = dataframe.loc[dataframe['Question'] == user_question, 'Detected_answer'].values[0]

        return detected_answer
    except Exception as e:
        return f"Error processing the file: {str(e)}"

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("Question Answering System")

    # Tab for single question answering
    with gr.Tab("Single QAs"):
        context_input = gr.Textbox(label="Context", type="text", placeholder="Enter context here...", lines=10)
        question_input = gr.Textbox(label="Question", type="text", placeholder="Enter question here...")
        qa_button = gr.Button("Get Answer")
        qa_output = gr.Textbox(label="Answer", type="text", placeholder="Answer will be displayed here...")

        # Define action when button is clicked
        qa_button.click(question_answering_interface, inputs=[context_input, question_input], outputs=qa_output)

    # Tab for CSV file upload 
    with gr.Tab("Upload CSV File"):
        df_input = gr.File(label="Upload CSV File")
        df_button = gr.Button("Process")
        df_output = gr.Dataframe(label="Questions and Detected Answers")
        
        # Textbox for asking a specific question
        user_question_input = gr.Textbox(label="Ask a Specific Question", type="text", placeholder="Type your question here...")
        specific_qa_button = gr.Button("Get Specific Answer")
        specific_answer_output = gr.Textbox(label="Detected Answer", type="text", placeholder="Answer will be displayed here...")

        # Define actions when buttons are clicked
        df_button.click(df_interface, inputs=df_input, outputs=df_output)
        specific_qa_button.click(specific_question_interface, inputs=[df_input, user_question_input], outputs=specific_answer_output)

# Launch the Gradio interface
demo.launch()