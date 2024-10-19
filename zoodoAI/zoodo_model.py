from langchain.schema.runnable import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import TextSplitter
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
import os 

load_dotenv()


class CustomTextSplitter(TextSplitter):
    def split_text(self, text):
        return text.split("\n\n")

# Define system and human messages
system_message = (
"You are an IT expert tasked with recommending the best computers from a provided list. Only recommend computers that exist within this list. Do not add computers that are not on the provided list. Here are the criteria to follow:"
"1. General Use: The computers you recommend must be suitable for common tasks such as word processing, audio and video playback, reading PDFs, and web browsing."
"2. Job Knowledge: You are familiar with the software and tasks specific to each profession. Recommend computers that meet the exact needs of the profession, and provide specific reasons based on the software and tasks."
"3. Technical Characteristics: The recommended computers must be shock-resistant, have a long lifespan, strong battery performance, and should not be slow."
"4. Selection of Computers: You must strictly recommend only the computers from the list provided by the user. Do not recommend any computer that is not in this list. This is a strict rule: if a computer is not in the list, do not suggest it."
"5. Results Format: Provide only a list of Python dictionaries with two fields: 'id' and 'reason' for each recommendation. Each reason should be convincing and clear."
"6. Clear Justification: The reason for each recommendation must explain how the computer meets the user’s criteria, focusing on performance, durability, lifespan, and suitability for the tasks. Mention specific tools and software, if necessary, to justify the recommendation."
"7. Alternative Suggestions: If none of the computers from the list match the requirements of the profession, suggest the most suitable computers for general use tasks such as word processing, reading PDFs, and web browsing. Even in this case, do not suggest computers that are not on the provided list."
"8. Response Format: Respond without using code blocks or adding extra text before or after the list. Do not use symbols like backticks, and avoid returning a Python code block."
"9. Strict Adherence to List: Do not add or recommend computers that are not on the provided list. If a suitable computer from the list cannot be found, suggest general-purpose computers from the list only."
"10. The descritpion sholud be done in frensh"
)


human_messages = (
    "Here is the Provided list"
    "{provided_list} \n\n"
    "Here is more description about the usage of required computer In frensh: "
    "{activity_description}"
)

model = ChatOpenAI(model="gpt-4o-mini")

# Branch function
def branch(system_message, human_messages, provided_list, max_num, activity_description):
    template = ChatPromptTemplate.from_messages([("system", system_message), ("human", human_messages)])
    return template.format_prompt(max_num=max_num, provided_list=provided_list, activity_description=activity_description)

# Combine results from the branches
def combine_result(results):
    import json 
    import ast
    final_result = []
    global_total_tokens = 0

    try:
        # results come as json data
        result_list = [json.loads(result.content) for result in results.values()]
        total_tokens_of_query = [r.response_metadata for r in results.values()]
        global_total_tokens = sum(item['token_usage']['total_tokens'] for item in total_tokens_of_query)
        final_result = []
        for r in result_list :
            final_result += r
            
    except Exception :
        # Result come as string data
        if isinstance(results, dict):
            for _,v in results.items():
                if hasattr(v, 'content') and "total_tokens" in v.usage_metadata:
                    content =  ast.literal_eval(v.content)
                    for value in content:
                        final_result.append(value)
                    global_total_tokens +=  v.usage_metadata["total_tokens"]
        else:
            # Another type: not meet yet
            print(results)
            print(type(results))

    return  final_result,global_total_tokens


# Run the chain
def zoodoAI(data_file_name,activity_description, max_num=15):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path   = os.path.join(current_dir, data_file_name)

        # Load your documents
    loader = TextLoader(file_path)
    try:
        documents = loader.load()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

    # Split documents into chunks
    custom_splitter = CustomTextSplitter(chunk_size=1, chunk_overlap=0)
    custom_docs     = custom_splitter.split_documents(documents)

    # Create RunnableParallel for parallel processing
    branches = {}
    for i, doc in enumerate(custom_docs):
        branches[f'branch_{i+1}'] = RunnableLambda(lambda x, idx=i: branch(system_message, human_messages, x[f'provided_list_{idx+1}'], max_num, activity_description)) | model
    parallel_branches = RunnableParallel(**branches)

    # Create the final chain
    final_chain = parallel_branches | RunnableLambda(combine_result)

    # Invocation du model 
    dynamic_input = {f'provided_list_{i+1}': doc.page_content for i, doc in enumerate(custom_docs)}
    final_result, global_total_tokens = final_chain.invoke(dynamic_input)
    # print(final_result)
    return final_result, global_total_tokens , file_path