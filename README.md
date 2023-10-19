# SearchQuery2FuncCall
Convert search query to API function executable calls

## Project Name: 
Smart Search Queries Application

## Project Decription:
* System tack  user quires to generate intent-based executable call, covering unit conversion, calculations, and general searches. 
>Instruction: Given a search query, then route to different backend components based on the search intent.
1. If the search is about unit conversion, return API function UnitConvert(SourceUnit, TargetUnit, SourceValue).
2. If the search is about calculation, return API function Calculate(Equation).
3. If the search is about other search intent, return API function Search().
* For unit conversion: common unit conversion in length, mass, time, area, speed, temperature, volume should be covered. And it should be consistent for the same unit throughout. E.g. it should always be “foot”, it cannot be “feet” or “ft” in API calls.
* For calculation: common operation such as +, -, *, /, pow, log, ln, exp, tan(h), sin(h), cos(h), factorial should be covered. And it should be consistent for the same operation throughout. E.g. it should always be “ * ”, it cannot be “x” or “X” in API calls.
Handle input queries in different language styles. Cover common unit conversion and calculation operations.

## Pair Examples
1. ##Input##:“ft to cm”, ##Output##:“UnitConvert(SourceUnit:foot, TargetUnit:centimeter,SourceValue:1)”
2. ##Input##:“how many ounces in 5.8 kilograms”, ##Output##:“UnitConvert(SourceUnit:kilogram,TargetUnit:ounce,SourceValue:5.8)”
3. ##Input##:“:“two to the power of 10”, ##Output##:“Calculate(2^10)”
4. ##Input##:“:“2001-1989” , ##Output##:“Calculate(2001-1989)”
5. ##Input##:“:“what is chatgpt”, ##Output##:“Search()”
6. ##Input##:“:“primary year 1 maths calculation checklist”, ##Output##:“Search()”
7. ##Input##:“:“what are different length units”, ##Output##:“Search()”
8. ##Input##:“:“Natural logarithm of -3/18”, ##Output##:“Calculate(ln(-3/18))”
9. ##Input##:“:“what is tan of 3/4”, ##Output##:“Calculate(tan(3/4))”


## Development and Technology
* Utilized ChatGPT 3.5 to generate datasets, total of 240 examples.
* Enhanced search intent recognition and decision-making through prompt engineering, using proprietary model APIs (Cohere, Google Palm) and open-source local models via Hugging Face.
* Fine-tuned open-source causal (quantized Llama 2) and seq2seq (flan-t5-large) model using Peft and Lora
* Evaluated model performance with ROUGH and BULE scores, with Peft fine-tuned quantized Llama 2 achieving comparable results to proprietary models.
