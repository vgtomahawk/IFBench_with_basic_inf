#!/usr/bin/env python3
import argparse
import json
import os
import time
import re
import litellm
from tqdm import tqdm

def load_jsonl(filepath):
    """Load JSONL file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def save_jsonl(data, filepath):
    """Save data to JSONL file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def extract_answer(response):
    """
    Extract content within <answer> tags.
    If no tags found, return the full response.
    """
    import re
    
    # Try to find content within <answer> tags
    match = re.search(r'<answer>(.*?)</answer>', response, re.DOTALL)
    
    # Return matched content or full response
    return match.group(1).strip() if match else response.strip()


def run_ifbench_eval(input_data, model, output_dir, max_retries=3):
    """
    Run IFBench evaluation using specified model.
    
    Args:
        input_data (list): List of input data from IFBench_test.jsonl
        model (str): Model identifier for LiteLLM
        output_dir (str): Directory to save output
        max_retries (int): Maximum number of retries for each prompt
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare output filepath
    output_filepath = os.path.join(output_dir, f'ifbench_output_{model.replace("/", "_")}.jsonl')
    
    # Stores successful responses
    output_data = []
    
    # Progress bar
    for item in tqdm(input_data, desc=f"Evaluating with {model}"):
        prompt = item['prompt']
        prompt_wformat = item['prompt'] + "\n\nFormat: Enclose the answer part of your response in <answer> </answer>"

        # Retry mechanism
        for attempt in range(max_retries):
            try:
                # Call LiteLLM to get response
                response = litellm.completion(
                    model=model,
                    messages=[{"role": "user", "content": prompt_wformat}],
                    temperature=0 # You can adjust this
                )
                
                # Extract the actual text response
                model_response = response.choices[0].message.content
                model_response = extract_answer(model_response)

                #print(model_response)
                #exit()


                # Create output item
                output_item = {
                    "prompt": prompt,
                    "response": model_response
                }
                
                output_data.append(output_item)
                break  # Success, exit retry loop
            
            except Exception as e:
                # Last retry failed
                if attempt == max_retries - 1:
                    print(f"Failed to get response for prompt after {max_retries} attempts:")
                    print(f"Error: {e}")
                    print(f"Prompt: {prompt}")
                    
                    # Optionally append a placeholder or error response
                    output_item = {
                        "prompt": prompt,
                        "response": f"ERROR: {str(e)}",
                        "failed_attempts": max_retries
                    }
                    output_data.append(output_item)
                
                # Wait before retrying
                time.sleep(2 ** attempt)  # Exponential backoff
    
    # Save output
    save_jsonl(output_data, output_filepath)
    print(f"Evaluation complete. Output saved to {output_filepath}")
    
    return output_filepath

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="IFBench Evaluation Script")
    parser.add_argument(
        "--input_data", 
        type=str, 
        default="data/IFBench_test.jsonl", 
        help="Path to input JSONL file"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        required=True, 
        help="LiteLLM model identifier (e.g., 'openai/gpt-3.5-turbo', 'anthropic/claude-3-sonnet-20240229')"
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        default="inferred_outputs", 
        help="Directory to save output files"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load input data
    input_data = load_jsonl(args.input_data)
    
    # Run evaluation
    run_ifbench_eval(
        input_data, 
        model=args.model, 
        output_dir=args.output_dir
    )

if __name__ == "__main__":
    main()
