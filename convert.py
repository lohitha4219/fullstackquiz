import json

with open("py_easy_200.json") as f:
    data = json.load(f)

new_data = []

for q in data:

    answer_index = q["options"].index(q["answer"]) + 1

    new_data.append({
        "question_text": q["question"].replace("\n"," "),
        "option1": q["options"][0],
        "option2": q["options"][1],
        "option3": q["options"][2],
        "option4": q["options"][3],
        "correct_answer": answer_index,
        "domain": "python",
        "level": q["level"]
    })

with open("python_easy_200.json","w") as f:
    json.dump(new_data,f,indent=4)

print("Converted Successfully")