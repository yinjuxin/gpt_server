import json
from typing import List
from fastchat.constants import ErrorCode, SERVER_ERROR_MSG
import torch

from gpt_server.model_worker.base import ModelWorkerBase


class LlamaWorker(ModelWorkerBase):
    def __init__(
        self,
        controller_addr: str,
        worker_addr: str,
        worker_id: str,
        model_path: str,
        model_names: List[str],
        limit_worker_concurrency: int,
        conv_template: str = None,  # type: ignore
    ):
        super().__init__(
            controller_addr,
            worker_addr,
            worker_id,
            model_path,
            model_names,
            limit_worker_concurrency,
            conv_template,
            model_type="AutoModelForCausalLM",
        )

        self.stop_words_ids = [
            128000,  # bos  <|begin_of_text|>
            128001,  # eos  <|end_of_text|>
            128009,  #  <|eot_id|>
        ]

        self.stop = [
            self.tokenizer.decode(skip_word) for skip_word in self.stop_words_ids
        ]
        print("Llama停用词:", self.stop)

    async def generate_stream_gate(self, params):
        self.call_ct += 1
        print("params", params)
        print("worker_id:", self.worker_id)
        try:
            query = ""
            messages = params["messages"]
            # for msg in messages:
            #     if msg["role"] == "function":
            #         msg["role"] = "Observation:"

            text = self.tokenizer.apply_chat_template(
                conversation=messages, tokenize=False, add_generation_prompt=True
            )
            input_ids = self.tokenizer([text], return_tensors="pt").input_ids
            prompt = self.tokenizer.decode(input_ids.tolist()[0])
            print(prompt)
            # ---------------添加额外的参数------------------------
            params["prompt"] = prompt
            params["stop"].extend(self.stop)
            params["stop_words_ids"] = self.stop_words_ids
            params["input_ids"] = input_ids
            # ---------------添加额外的参数------------------------
            async for response, usage in self.backend.stream_chat(
                query=query, params=params
            ):
                ret = {"text": response, "error_code": 0, "usage": usage}

                yield json.dumps(ret).encode() + b"\0"

        except torch.cuda.OutOfMemoryError as e:
            ret = {
                "text": f"{SERVER_ERROR_MSG}\n\n({e})",
                "error_code": ErrorCode.CUDA_OUT_OF_MEMORY,
            }
            yield json.dumps(ret).encode() + b"\0"
        except (ValueError, RuntimeError) as e:
            print(e)
            ret = {
                "text": f"{SERVER_ERROR_MSG}\n\n({e})",
                "error_code": ErrorCode.INTERNAL_ERROR,
            }
            yield json.dumps(ret).encode() + b"\0"

    def get_embeddings(self, params):
        return super().get_embeddings(params)


if __name__ == "__main__":
    LlamaWorker.run()
