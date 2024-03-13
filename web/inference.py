import transformers
import datetime
import logging
import ctranslate2

tokenizers = {}
models = {}


class Inference:
    def _discard_recommendations(self, original, proposal):
        proposal = proposal.lower()
        original = original.lower()
        if proposal == original:
            return True

        chars = [".", "!", " ", "?", ","]
        for char in chars:
            proposal = proposal.replace(char, "")
            original = original.replace(char, "")

        if proposal == original:
            return True

        return False

    def get_paraphrases(
        self,
        model_name,
        sentence,
        temperature,
    ):
        prefix = "paraphrase: "
        n_predictions = 2
        top_k = 120
        max_length = 256
        device = "cpu"

        model = models.get(model_name)
        print(f"model_name: {model_name}")
        if not model:
            model = ctranslate2.Translator(model_name)
            models[model_name] = model
            print(f"Loaded model: {model_name}")

        tokenizer = tokenizers.get(model_name)
        if not tokenizer:
            tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
            tokenizers[model_name] = tokenizer
            print(f"Loaded tokenizer: {model_name}")

        outputs = []
        discarded = 0
        input_text = prefix + sentence
        input_tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(input_text))

        if temperature > 0:
            sampling_topk = 10
        else:
            sampling_topk = 1

        # https://opennmt.net/CTranslate2/python/ctranslate2.Translator.html?highlight=translate_batch#ctranslate2.Translator.translate_batch
        results = model.translate_batch(
            [input_tokens],
            beam_size=n_predictions,
            num_hypotheses=n_predictions,
            sampling_temperature=temperature,
            sampling_topk=sampling_topk,
        )

        for output_tokens in results[0].hypotheses:
            # print(output_tokens)
            generated_sent = tokenizer.decode(
                tokenizer.convert_tokens_to_ids(output_tokens)
            )

            if (
                self._discard_recommendations(sentence, generated_sent) is False
                and generated_sent not in outputs
            ):
                generated_sent = generated_sent.replace("’", "'")
                outputs.append(generated_sent)
            else:
                logging.debug(f"Discarded: {generated_sent} - source:{sentence}")
                discarded = +1

            if len(outputs) == n_predictions:
                break

        return outputs, discarded
