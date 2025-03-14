from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

def chatbot_response(text):
    inputs = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
    response_ids = model.generate(inputs, max_length=100)
    return tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)

print(chatbot_response("Hi! How are you?"))
print(chatbot_response("Turn on the lights"))  # Can be combined with rule-based processing

