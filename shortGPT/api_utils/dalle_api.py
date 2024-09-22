def generate_simple_prompts(input_data, style=None):
    prompts = []
    
    for segment in input_data:
        time_range, keywords = segment
        keywords_str = ", ".join(keywords)
        
        if style:
            prompt = f"{keywords_str} in {style} style"
        else:
            prompt = keywords_str
        
        prompts.append([time_range, prompt])
    
    return prompts