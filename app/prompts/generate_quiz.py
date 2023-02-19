prompt = """
Generate quiz questions based on text content that you will be given to test a learner's understanding of the content. Your response must follow these requirements:
1. The questions should be in the following format:

[{'ques': 'what is 1+1?','ans': 1,'opt': ['3','2','1','0']},{'ques': 'what is 1+1?','ans': 1,'opt': ['3','2','1','0']}]

2. The value of the 'answer' property is the correct index of the options array
3. The correct option index must be fairly randomized. However, it must remain correct. Do not sacrifice correctness for randomness in any situation
4. The questions should aim to cover all parts of the text content provided
5. Your response should only contain valid JSON response. No extra numbers or characters
Here is the content from which you will generate the quiz from:
"""