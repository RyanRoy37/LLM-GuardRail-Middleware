
import torch


def predict(prompt):
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    model=AutoModelForSequenceClassification.from_pretrained("bert_tiny_jailbreak")
    tokenizer=AutoTokenizer.from_pretrained("bert_tiny_jailbreak")
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def preprocess_and_predict(prompt):
        encoding = tokenizer(
        prompt,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt"
    )

        input_ids = encoding["input_ids"].to(device)
        attention_mask = encoding["attention_mask"].to(device)

    # Step 2: Feed into model
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]  # shape: (num_classes,)

    # Step 3: Apply threshold for Class 0
        if probs[0] > 0.6:   # if prob for class 0 > 60%
         predicted_class = 0
        else:
         predicted_class = 1  # fallback

        return predicted_class, probs
    pred,prob=preprocess_and_predict(prompt)
    return pred
  

