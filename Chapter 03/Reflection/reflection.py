
# Example: Code Generation Agent

#Task: Write a Python function to sort a list of dictionaries by a key



#Task: Write a Python function to sort a list of dictionaries by a key

#Generation:

def sort_dicts(data):
    return sorted(data)


#Reflection: Notices it doesn't specify the key.

#Refinement:

def sort_dicts(data):
    return sorted(data, key=lambda x: x['key'])

  
if __name__ == "__main__":
    # Example usage
    data = [{'key': 2}, {'key': 1}, {'key': 3}]
    sorted_data = sort_dicts(data)
    print(sorted_data)
    
# Output: [{'key': 1}, {'key': 2}, {'key': 3}]