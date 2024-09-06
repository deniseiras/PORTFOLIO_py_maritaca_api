import unittest

from src.maritacaai_api import get_completion


class TestGetCompletion(unittest.TestCase):
    
    def test_get_completion_with_default_model(self):
        prompt = "Qual é a capital da França?"
        response, finish_reason = get_completion(prompt)
        self.assertIn("Paris", response)
        self.assertEqual(finish_reason, "stop")

    def test_get_completion_with_sabia2_medium(self):
        prompt = "Gere um plano para resolver o problema: Como criar uma ideia de negócio em 30 palavras?"
        response, finish_reason = get_completion(prompt, model_name="sabia-2-medium")
        self.assertNotEqual(response, "")
        self.assertEqual(finish_reason, "stop")
        
    def test_get_completion_with_sabia_3(self):
        prompt = "Gere um plano para resolver o problema: Como criar uma ideia de negócio em 30 palavras?"
        response, finish_reason = get_completion(prompt, model_name="sabia-3")
        self.assertNotEqual(response, "")
        self.assertEqual(finish_reason, "stop")

    def test_get_completion_with_temperature_with_default_model(self):
        prompt = "Escreva uma estória com 20 palavras"
        response1, _ = get_completion(prompt, temperature=0)
        response2, _ = get_completion(prompt, temperature=1)
        self.assertNotEqual(response1, response2)

    def test_get_completion_with_invalid_model(self):
        prompt = "Qual é a velocidade da luz?"
        response, err = get_completion(prompt, model_name="invalid-model")
        self.assertEqual(response[:48], 'Sorry, we do not support the model you requested')
        self.assertEqual(err, 'maritacaai_exception')

    def test_get_completion_with_more_than_max_tokens(self):
        prompt = "Escreva uma estória com 20 palavras."
        # Max tokens sabia-2 = 8192, so it passes the limit
        response, err = get_completion(prompt, max_tokens=8192)
        self.assertEqual(response, 'The messages submitted occupy 78 tokens. You asked to generate a maximum of 8192, with 8270 in total. ' + \
            'The maximum supported is 8192 tokens. If you want to generate as many tokens as possible, please do not specify the max_tokens parameter')
        self.assertEqual(err, 'maritacaai_exception')


if __name__ == '__main__':
    unittest.main()