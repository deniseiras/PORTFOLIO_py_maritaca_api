"""
Maritaca AI API

:author: Denis Eiras

Functions:
    - get_completion: get models response using MaritacaAI API
    - get_maritalk_instance: gets an model instance and sets the maritacaai key using environment variable MARITACAAI_API_KEY inside.env file
"""

import maritalk
import dotenv
import os
import tiktoken

model_instances = {}

def get_maritalk_instance(model_name):
    """
        gets an model instance and sets the maritacaai key using environment variable MARITACAAI_API_KEY inside.env file
    """
    if len(model_instances) == 0:
        del os.environ['MARITACAAI_API_KEY']
        # load the MARITACAAI_API_KEY in .env file
        dotenv.load_dotenv()
        
    if len(model_instances) == 0 or model_name not in model_instances.keys():
        print(f'Criando instância do modelo {model_name} ...')
        
        model = maritalk.MariTalk(
            key=os.getenv('MARITACAAI_API_KEY'),
            model=model_name  
        )
        maritalk.api_key = os.getenv('MARITACAAI_API_KEY')
        model_instances[model_name] = model
    return model_instances[model_name]
        

def get_completion(prompt_user, prompt_system=None, model_name="sabia-2-small", temperature=0):
    """
        get models response using MaritacaAI API

        :param prompt: prompt to send to Maritalk
        :param model: Maritalk model to use
        :param temperature: degree of randomness/creativity of the model's output (0= no randomness, 1=super-random)
        :return: message, finish_reason
            - message is the response message or the exception code
            - finish_reason is the reason why the message was returned
        
        Every response will include a finish_reason. The possible values for finish_reason are:
        - stop: API returned complete message, or a message terminated by one of the stop sequences provided via the stop parameter
        - 'maritacaai_exception' will be raised when there is an exception

        Whether your API call works at all, as total tokens must be below the model’s maximum limit:
        Sabiá-3        - In/Out Tokens = R$ 0,00001 por tokens  (R$10 / 1M tokens)
        Sabiá-2 Medium - Input Tokens  = R$ 0,000005 por token  (R$5  / 1M tokens)
                       - Output Tokens = R$ 0,000015 por tokens (R$15 / 1M tokens)
        Sabiá-2 Small  - Input Tokens  = R$ 0,000001 por token  (R$1  / 1M tokens)
                       - Output Tokens = R$ 0,000003 por token  (R$1  / 1M tokens)

    """
        
    
    mssgs = [{"role": "user", "content": prompt_user}]
    if prompt_system:
        mssgs.append({"role": "system", "content": prompt_system})
    try:

        model = get_maritalk_instance(model_name)
        response = model.generate(mssgs, temperature=temperature)
        ret_message = response["answer"]
        
        ret_fin_reason = 'stop'
        # ret_fin_reason = response.finish_reason ??
        prompt_tokens = response["usage"]['prompt_tokens']
        compl_tokens = response["usage"]['completion_tokens']
        
    except Exception as e:
        ret_message = e.message
        ret_fin_reason = 'maritacaai_exception'
        prompt_tokens = 0
        compl_tokens = 0

    
    print(f'\n\nUsing model {model_name}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(f'Prompt System  ===> {prompt_system}')
    print(f'Prompt User    ===> {prompt_user}')
    print(f'Temperature ===> {temperature}')
    print(f'Prompt tokens: {prompt_tokens}')
    print(f'Response tokens: {compl_tokens}')
    print(f'Total tokens: {prompt_tokens+compl_tokens}')
    print(f'Response: {ret_message}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(f'\nFinish reason: {ret_fin_reason}')
    
    return ret_message, ret_fin_reason

