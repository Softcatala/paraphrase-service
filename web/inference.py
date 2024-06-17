import transformers
import datetime
import logging
import ctranslate2
import os
from similarity import Similarity

tokenizers = {}
models = {}


class Inference:
    INTER_THREADS = 'CTRANSLATE_INTER_THREADS'
    INTRA_THREADS = 'CTRANSLATE_INTRA_THREADS'
    DEVICE = 'DEVICE'

    def __init__(self):
        if self.INTER_THREADS in os.environ:
            self.inter_threads = int(os.environ[self.INTER_THREADS])
        else:
            self.inter_threads = 1

        if self.INTRA_THREADS in os.environ:
            self.intra_threads = int(os.environ[self.INTRA_THREADS])
        else:
            self.intra_threads = 4

        self.device = os.environ.get(self.DEVICE, "cpu")

    def get_paraphrases(
        self,
        model_name,
        sentence,
        temperature,
    ):
        prefix = "paraphrase: "
        n_predictions = 5
        top_k = 120
        max_length = 256
        device = "cpu"

        model = models.get(model_name)
        if not model:
            model = ctranslate2.Translator(model_name, device = self.device, inter_threads = self.inter_threads, intra_threads = self.intra_threads)
            models[model_name] = model
            logging.debug(f"device: {self.device}, inter_threads: {self.inter_threads}, intra_threads: {self.intra_threads}, model_name: {model_name}")

        tokenizer = tokenizers.get(model_name)
        if not tokenizer:
            tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
            tokenizers[model_name] = tokenizer
            logging.debug(f"Loaded tokenizer: {model_name}")

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
                Similarity().are_sentences_almost_identical(sentence, generated_sent) is False and
               any(Similarity().are_sentences_almost_identical(generated_sent, o) for o in outputs) is False and
                generated_sent not in outputs
            ):
                generated_sent = generated_sent.replace("’", "'")
                outputs.append(generated_sent)
            else:
                logging.debug(f"Discarded: {generated_sent} - source:{sentence}")
                discarded = +1

            if len(outputs) == n_predictions:
                break

        get_first_two = outputs[0:2] if len(outputs) >= 2 else outputs
        return get_first_two, discarded
