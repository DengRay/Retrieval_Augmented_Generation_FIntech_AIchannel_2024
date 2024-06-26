import re
from loguru import logger
#mport logger
from .llm_client import ChatClient

def is_truth(llm: ChatClient, prompt:str, throttle: int, default: int):
    """Generate a score based on the prompt, and then compares it to
    threshold.

    Args:
        prompt (str): The prompt for the language model.
        throttle (int): Threshold value to compare the score against.
        default (int): Default score to be assigned in case of failure in score calculation.  # noqa E501

    Returns:
        bool: True if the score surpasses the throttle, otherwise False.
        dict: Debugging logs.
    """
    logs = {}
    logs['input'] = prompt
    if prompt is None or len(prompt) == 0:
        return False, logs

    score = default
    logs['default'] = default
    relation = llm.generate_response(prompt=prompt, backend='local')
    logs['relation'] = relation
    filtered_relation = ''.join([c for c in relation if c.isdigit()])
    #score = -3
    try:
        score_str = re.sub(r'[^\d]', ' ', filtered_relation).strip()
        score = int(score_str.split(' ')[0])
    except Exception as e:
        logger.error(str(e))
    logs['throttle'] = throttle
    logs['output'] = score
    
    if score >= throttle:
        return True, logs
    return False, logs
