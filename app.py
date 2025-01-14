import gradio as gr
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("./")
tokenizer = AutoTokenizer.from_pretrained("./")

def predict_clickbait(headline):
    # Tokenize and process the headline
    inputs = tokenizer(headline, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits

    # Calculate probabilities using softmax
    probabilities = F.softmax(logits, dim=-1)
    confidence_score, prediction = torch.max(probabilities, dim=-1)

    # Return prediction and confidence score
    label = "Clickbait" if prediction.item() == 1 else "Not Clickbait"
    confidence = confidence_score.item()
    return f"{label} (Confidence: {confidence:.6f})"  # Display six decimal points

# Create the Gradio interface
interface = gr.Interface(
    fn=predict_clickbait,
    inputs="text",
    outputs="text",
    title="Clickbait Detector",
    description="Enter a headline to check if it's clickbait or not."
)

if __name__ == "__main__":
    interface.launch()
