# SearchQuery2FuncCall
Convert search query to API function executable calls

## Project Name: 
Smart Search Queries Application

## Project Decription:
System tack  user quires to generate intent-based executable call, covering unit conversion, calculations, and general searches. 
Instruction: Given a search query, then route to different backend components based on the search intent.
1. If the search is about unit conversion, return API function UnitConvert(SourceUnit, TargetUnit, SourceValue).
2. If the search is about calculation, return API function Calculate(Equation).
3. If the search is about other search intent, return API function Search().

#### For unit conversion:
common unit conversion in length, mass, time, area,speed, temperature, volume should be covered. And it should be consistent for the same unit throughout. E.g. it should always be “foot”, it cannot be “feet” or “ft” in API calls.

#### For calculation:
Common operation such as +, -, *, /, pow, log, ln, exp, tan(h), sin(h), cos(h), factorial should be covered. And it should be consistent for the same operation throughout. E.g. it should always be “ * ”, it cannot be “x” or “X” in API calls.

Handle input queries in different language styles. Cover common unit conversion and calculation operations.

## Pair Examples
1. **Input**:“ft to cm”, **Output**:“UnitConvert(SourceUnit:foot, TargetUnit:centimeter,SourceValue:1)”
2. **Input**:“how many ounces in 5.8 kilograms”, **Output**:“UnitConvert(SourceUnit:kilogram,TargetUnit:ounce,SourceValue:5.8)”
3. **Input**:“two to the power of 10”, **Output**:“Calculate(2^10)”
4. **Input**:“2001-1989” , **Output**:“Calculate(2001-1989)”
5. **Input**:“what is chatgpt”, **Output**:“Search()”
6. **Input**:“primary year 1 maths calculation checklist”, **Output**:“Search()”
7. **Input**:“what are different length units”, **Output**:“Search()”
8. **Input**:“Natural logarithm of -3/18”, **Output**:“Calculate(ln(-3/18))”
9. **Input**:“what is tan of 3/4”, **Output**:“Calculate(tan(3/4))”


## Development and Technology
* Utilized ChatGPT 3.5 to generate datasets, total of 240 examples.
* Enhanced search intent recognition and decision-making through prompt engineering, using proprietary model APIs (Cohere, Google Palm) and open-source local models via Hugging Face.
* Fine-tuned open-source causal (quantized Llama 2) and seq2seq (flan-t5-large) model using Peft and Lora, where __flan-t5-large__ give significant faster inference, due to smaller model size.
* Evaluated model performance with ROUGH and BLEU scores, with __Peft fine-tuned quantized Llama 2__ achieving comparable results to proprietary models.

## Eveluation and Metric Scores
The results use random 80 examples in test dataset for each model evaluation below, it would be better for proper comparison using same testing dataset. (Keep the current results due to compute limit, it could be updated in future)

| Model                                  | Rouge-1     | Rouge-2     | Rouge-L     | Rouge-Lsum  | Bleu       | Precision (P1) | Precision (P2) | Precision (P3) | Precision (P4) | Brevity Penalty | Length Ratio | Translation Length | Reference Length |
|----------------------------------------|------------|------------|------------|------------|-----------|----------------|----------------|----------------|----------------|-----------------|--------------|-------------------|------------------|
| quantized LLama 2 fine-tuned with peft | 0.9828     | 0.7005     | 0.9833     | 0.9833     | 0.9334    | 0.9898         | 0.9752         | 0.9580         | 0.9392         | 0.9669          | 0.9675       | 684               | 707              |
| Palm API with prompt engineering       | 0.9792     | 0.6571     | 0.9787     | 0.9797     | 0.9031    | 0.9669         | 0.9402         | 0.9049         | 0.8588         | 0.9851          | 0.9852       | 665               | 675              |
| flan-t5-large fine-tuned with peft     | 0.9415     | 0.5829     | 0.9341     | 0.9337     | 0.8543    | 0.9289         | 0.8770         | 0.8288         | 0.7888         | 1.0             | 1.0161       | 633               | 623              |
| quantized LLama 2 with prompt engineering | 0.8859  | 0.5330     | 0.8777     | 0.8810     | 0.8039    | 0.9368         | 0.8771         | 0.8297         | 0.7942         | 0.9372          | 0.9391       | 617               | 657              |


### Evaluation Results with flan-t5-large

**Merged model loaded in 8 bits use less than half the inference time compare to loaded in 32 bit float**

| Metric                 | Model loaded in 8 bits | Model loaded in 32 bits float |
|------------------------|------------------------|-------------------------------|
| Rouge-1 Score          | 0.9376                 | 0.9415                        |
| Rouge-2 Score          | 0.5733                 | 0.5829                        |
| Rouge-L Score          | 0.9299                 | 0.9341                        |
| Rouge-Lsum Score       | 0.9297                 | 0.9337                        |

| Metric                 | Model loaded in 8 bits | Model loaded in 32 bits float |
|------------------------|------------------------|-------------------------------|
| BLEU Score             | 0.8429                 | 0.8543                        |
| BLEU Precisions        | [0.9266, 0.8702, 0.8158, 0.7674] | [0.9289, 0.8770, 0.8288, 0.7888] |
| Brevity Penalty        | 1.0                    | 1.0                           |
| Length Ratio           | 1.0064                 | 1.0161                        |
| Translation Length     | 627                    | 633                           |
| Reference Length       | 623                    | 623                           |
